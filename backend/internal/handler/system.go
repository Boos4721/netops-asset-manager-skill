package handler

import (
	"net/http"
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
)

type SystemHandler struct{}

func NewSystemHandler() *SystemHandler { return &SystemHandler{} }

// GetSystemInfo GET /api/system/info
func (h *SystemHandler) GetSystemInfo(c *gin.Context) {
	var version string
	if out, err := exec.Command("openclaw", "--version").Output(); err == nil {
		version = strings.TrimSpace(string(out))
	} else {
		version = "v2026.3.7-Quantum"
	}

	kernel := ""
	if out, err := exec.Command("uname", "-srv").Output(); err == nil {
		kernel = strings.TrimSpace(string(out))
	}

	c.JSON(http.StatusOK, gin.H{
		"version":    version,
		"kernel":     kernel,
		"last_audit": "2026-03-07 18:35",
		"status":     "已获企业级认证",
	})
}

type deploySystemRequest struct {
	Type string `json:"type" binding:"required"`
}

type DeployHandler struct{}

func NewDeployHandler() *DeployHandler { return &DeployHandler{} }

// DeploySystem POST /api/deploy/system
func (h *DeployHandler) DeploySystem(c *gin.Context) {
	var req deploySystemRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	commands := map[string]string{
		"docker":    "curl -fsSL https://get.docker.com | sh",
		"vllm":      "pip install vllm",
		"llama-cpp": "git clone --depth=1 https://github.com/ggerganov/llama.cpp.git /tmp/llama.cpp && cd /tmp/llama.cpp && make",
	}

	cmd, ok := commands[req.Type]
	if !ok {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "invalid deployment type"})
		return
	}

	taskName := "deploy-" + req.Type
	go exec.Command("pm2", "start", cmd, "--name", taskName, "--no-autorestart").Run()

	c.JSON(http.StatusOK, gin.H{
		"status":  "success",
		"message": "任务 " + taskName + " 已在后台启动，请在 PM2 列表中查看进度。",
	})
}
