package handler

import (
	"net/http"
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
)

type ChatHandler struct{}

func NewChatHandler() *ChatHandler { return &ChatHandler{} }

type chatRequest struct {
	Message string                   `json:"message"`
	History []map[string]interface{} `json:"history"`
}

// Chat POST /api/chat
func (h *ChatHandler) Chat(c *gin.Context) {
	var req chatRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	systemPrompt := `你是一个专业的 NetOps 网络运维助理。你能够帮助用户管理资产、监控任务、分析日志。

**核心能力：资产录入**
如果用户要求录入或添加资产（例如："录入一台 10.1.1.1 的 H3C 交换机"），请你在回复的最后添加一行特殊的标记：
` + "`ACTION: ADD_ASSET | IP: <IP地址> | VENDOR: <品牌> | NAME: <设备名>`" + `
例如：` + "`ACTION: ADD_ASSET | IP: 10.1.1.1 | VENDOR: H3C | NAME: H3C-Switch-01`" + `

请保持专业、简洁、高效的语气。`

	historyText := ""
	history := req.History
	if len(history) > 10 {
		history = history[len(history)-10:]
	}
	for _, msg := range history {
		from, _ := msg["from"].(string)
		text, _ := msg["text"].(string)
		role := "Assistant"
		if from == "user" {
			role = "User"
		}
		historyText += role + ": " + text + "\n"
	}

	fullPrompt := systemPrompt + "\n\n---\n历史对话:\n" + historyText + "\n---\nUser: " + req.Message + "\nAssistant:"

	proc := exec.Command("openclaw", "agent", "--session-id", "netops-chat", "--message", fullPrompt, "--timeout", "60", "--json")
	out, err := proc.Output()
	if err != nil {
		// fallback: try without --json
		out2, err2 := exec.Command("openclaw", "agent", "--session-id", "netops-chat", "--message", fullPrompt).Output()
		if err2 != nil {
			c.JSON(http.StatusOK, gin.H{"status": "error", "message": "OpenClaw unavailable: " + err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "success", "reply": strings.TrimSpace(string(out2))})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": "success", "reply": strings.TrimSpace(string(out))})
}
