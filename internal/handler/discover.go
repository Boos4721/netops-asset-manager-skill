package handler

import (
	"net/http"
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/ent"
)

type DiscoverHandler struct {
	db *ent.Client
}

func NewDiscoverHandler(db *ent.Client) *DiscoverHandler {
	return &DiscoverHandler{db: db}
}

type discoverRequest struct {
	Subnet string `json:"subnet" binding:"required"`
}

// Discover POST /api/discover
func (h *DiscoverHandler) Discover(c *gin.Context) {
	var req discoverRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	out, err := exec.Command("nmap", "-sn", "-oG", "-", req.Subnet).Output()
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": "nmap not available or failed: " + err.Error()})
		return
	}

	var ips []string
	for _, line := range strings.Split(string(out), "\n") {
		if strings.HasPrefix(line, "Host:") {
			parts := strings.Fields(line)
			if len(parts) >= 2 {
				ips = append(ips, parts[1])
			}
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"subnet": req.Subnet,
		"found":  ips,
		"count":  len(ips),
	})
}
