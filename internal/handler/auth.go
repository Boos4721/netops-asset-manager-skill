package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/config"
	"github.com/netops/asset-manager/ent"
	entuser "github.com/netops/asset-manager/ent/user"
	"github.com/netops/asset-manager/internal/auth"
)

type AuthHandler struct {
	db  *ent.Client
	cfg *config.Config
}

func NewAuthHandler(db *ent.Client, cfg *config.Config) *AuthHandler {
	return &AuthHandler{db: db, cfg: cfg}
}

type loginRequest struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}

// Login handles POST /api/users/login
func (h *AuthHandler) Login(c *gin.Context) {
	var req loginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	u, err := h.db.User.Query().
		Where(entuser.UsernameEQ(req.Username)).
		Only(c)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": "invalid credentials"})
		return
	}

	if !u.Active {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": "account disabled"})
		return
	}

	if !auth.CheckPassword(u.PasswordHash, req.Password) {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": "invalid credentials"})
		return
	}

	token, err := auth.GenerateToken(h.cfg.JWTSecret, h.cfg.JWTExpiry, u.ID, u.Username, u.Role.String())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": "token generation failed"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":   "success",
		"token":    token,
		"role":     u.Role.String(),
		"username": u.Username,
	})
}
