package handler

import (
	"encoding/json"
	"net/http"
	"os/exec"

	"github.com/gin-gonic/gin"
)

type JobsHandler struct{}

func NewJobsHandler() *JobsHandler { return &JobsHandler{} }

type pm2Process struct {
	Name   string `json:"name"`
	Status string `json:"status"`
	Uptime int64  `json:"pm_uptime"`
}

// GetPM2Status GET /api/pm2/status
func (h *JobsHandler) GetPM2Status(c *gin.Context) {
	out, err := exec.Command("pm2", "jlist").Output()
	if err != nil {
		c.JSON(http.StatusOK, []gin.H{})
		return
	}
	var raw []map[string]interface{}
	if err := json.Unmarshal(out, &raw); err != nil {
		c.JSON(http.StatusOK, []gin.H{})
		return
	}
	tasks := make([]gin.H, 0, len(raw))
	for _, p := range raw {
		env, _ := p["pm2_env"].(map[string]interface{})
		monit, _ := p["monit"].(map[string]interface{})
		tasks = append(tasks, gin.H{
			"name":     p["name"],
			"status":   strGet(env, "status"),
			"restarts": env["restart_time"],
			"memory":   monit["memory"],
			"cpu":      monit["cpu"],
		})
	}
	c.JSON(http.StatusOK, tasks)
}

// GetPM2Logs GET /api/pm2/logs/:name
func (h *JobsHandler) GetPM2Logs(c *gin.Context) {
	name := c.Param("name")
	lines := c.DefaultQuery("lines", "100")
	out, err := exec.Command("pm2", "logs", name, "--lines", lines, "--nostream", "--raw").CombinedOutput()
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": string(out)})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "logs": string(out)})
}

// RestartPM2 POST /api/pm2/restart/:name
func (h *JobsHandler) RestartPM2(c *gin.Context) {
	name := c.Param("name")
	if out, err := exec.Command("pm2", "restart", name).CombinedOutput(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": string(out)})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

// StopPM2 POST /api/pm2/stop/:name
func (h *JobsHandler) StopPM2(c *gin.Context) {
	name := c.Param("name")
	if out, err := exec.Command("pm2", "stop", name).CombinedOutput(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": string(out)})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

// DeletePM2 DELETE /api/pm2/delete/:name
func (h *JobsHandler) DeletePM2(c *gin.Context) {
	name := c.Param("name")
	if out, err := exec.Command("pm2", "delete", name).CombinedOutput(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": string(out)})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

type renameRequest struct {
	NewName string `json:"new_name"`
}

// RenamePM2 POST /api/pm2/rename/:name
func (h *JobsHandler) RenamePM2(c *gin.Context) {
	name := c.Param("name")
	var req renameRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if out, err := exec.Command("pm2", "restart", name, "--name", req.NewName).CombinedOutput(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": string(out)})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

type scheduleRequest struct {
	Cron string `json:"cron"`
}

// SchedulePM2 POST /api/pm2/schedule/:name
func (h *JobsHandler) SchedulePM2(c *gin.Context) {
	name := c.Param("name")
	var req scheduleRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if out, err := exec.Command("pm2", "restart", name, "--cron", req.Cron).CombinedOutput(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": string(out)})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

type deployRequest struct {
	TaskName   string   `json:"task_name"`
	BinaryPath string   `json:"binary_path"`
	Args       string   `json:"args"`
	TargetIPs  []string `json:"target_ips"`
}

// DeployPM2 POST /api/pm2/deploy
func (h *JobsHandler) DeployPM2(c *gin.Context) {
	var req deployRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	results := make([]gin.H, 0)
	for _, ip := range req.TargetIPs {
		pm2Cmd := "pm2 start \"" + req.BinaryPath + "\""
		if req.Args != "" {
			pm2Cmd += " -- " + req.Args
		}
		pm2Cmd += " --name " + req.TaskName
		out, err := exec.Command("ssh", "-o", "StrictHostKeyChecking=no", "root@"+ip, pm2Cmd).CombinedOutput()
		if err != nil {
			results = append(results, gin.H{"ip": ip, "status": "failed", "error": string(out)})
		} else {
			results = append(results, gin.H{"ip": ip, "status": "deployed"})
		}
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "results": results})
}

func strGet(m map[string]interface{}, key string) interface{} {
	if v, ok := m[key]; ok {
		return v
	}
	return nil
}
