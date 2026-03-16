package handler

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/backend/ent"
	entuser "github.com/netops/asset-manager/backend/ent/user"
	"github.com/netops/asset-manager/backend/internal/auth"
)

type UsersHandler struct {
	db *ent.Client
}

func NewUsersHandler(db *ent.Client) *UsersHandler {
	return &UsersHandler{db: db}
}

// ListUsers GET /api/users [root]
func (h *UsersHandler) ListUsers(c *gin.Context) {
	users, err := h.db.User.Query().All(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	result := make([]gin.H, 0, len(users))
	for _, u := range users {
		result = append(result, gin.H{
			"id":         u.ID,
			"username":   u.Username,
			"role":       u.Role.String(),
			"active":     u.Active,
			"created_at": u.CreatedAt,
		})
	}
	c.JSON(http.StatusOK, result)
}

type createUserRequest struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
	Role     string `json:"role"`
}

// CreateUser POST /api/users [root]
func (h *UsersHandler) CreateUser(c *gin.Context) {
	var req createUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	role := entuser.Role(req.Role)
	if req.Role == "" {
		role = entuser.RoleOperator
	}

	hash, err := auth.HashPassword(req.Password)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": "failed to hash password"})
		return
	}

	_, err = h.db.User.Create().
		SetUsername(req.Username).
		SetPasswordHash(hash).
		SetRole(role).
		Save(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

// DeleteUser DELETE /api/users/:id [root]
func (h *UsersHandler) DeleteUser(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "invalid id"})
		return
	}
	if err := h.db.User.DeleteOneID(id).Exec(c); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}
