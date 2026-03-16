package handler

import (
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

type ModelsHandler struct {
	configPath string
}

func NewModelsHandler(configPath string) *ModelsHandler {
	return &ModelsHandler{configPath: configPath}
}

type openclawConfig struct {
	Models struct {
		Providers map[string]providerConfig `json:"providers"`
	} `json:"models"`
	Agents struct {
		Defaults struct {
			Model struct {
				Primary string `json:"primary"`
			} `json:"model"`
		} `json:"defaults"`
	} `json:"agents"`
}

type providerConfig struct {
	BaseURL string      `json:"baseUrl"`
	APIKey  string      `json:"apiKey"`
	API     string      `json:"api"`
	Models  []modelItem `json:"models"`
}

type modelItem struct {
	ID            string                 `json:"id"`
	Name          string                 `json:"name"`
	Reasoning     bool                   `json:"reasoning"`
	Input         []string               `json:"input"`
	ContextWindow int                    `json:"contextWindow"`
	MaxTokens     int                    `json:"maxTokens"`
	Cost          map[string]interface{} `json:"cost"`
}

func (h *ModelsHandler) readConfig() (*openclawConfig, error) {
	path := expandHome(h.configPath)
	data, err := os.ReadFile(path)
	if err != nil {
		return &openclawConfig{}, nil
	}
	var cfg openclawConfig
	if err := json.Unmarshal(data, &cfg); err != nil {
		return &openclawConfig{}, nil
	}
	if cfg.Models.Providers == nil {
		cfg.Models.Providers = make(map[string]providerConfig)
	}
	return &cfg, nil
}

func (h *ModelsHandler) writeConfig(cfg *openclawConfig) error {
	path := expandHome(h.configPath)
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return err
	}
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, data, 0644)
}

// GetModels GET /api/models
func (h *ModelsHandler) GetModels(c *gin.Context) {
	cfg, _ := h.readConfig()
	var result []gin.H
	for providerName, provider := range cfg.Models.Providers {
		for _, m := range provider.Models {
			result = append(result, gin.H{
				"id":            m.ID,
				"name":          m.Name,
				"provider":      providerName,
				"base_url":      provider.BaseURL,
				"api_key":       provider.APIKey,
				"reasoning":     m.Reasoning,
				"input":         m.Input,
				"contextWindow": m.ContextWindow,
				"maxTokens":     m.MaxTokens,
				"cost":          m.Cost,
				"enabled":       true,
				"source":        "openclaw",
			})
		}
	}
	if result == nil {
		result = []gin.H{}
	}
	c.JSON(http.StatusOK, result)
}

// GetProviders GET /api/providers
func (h *ModelsHandler) GetProviders(c *gin.Context) {
	cfg, _ := h.readConfig()
	providers := make([]string, 0, len(cfg.Models.Providers))
	for k := range cfg.Models.Providers {
		providers = append(providers, k)
	}
	c.JSON(http.StatusOK, providers)
}

type addModelRequest struct {
	ID            string                 `json:"id"`
	Name          string                 `json:"name"`
	Provider      string                 `json:"provider"`
	BaseURL       string                 `json:"base_url"`
	APIKey        string                 `json:"api_key"`
	Reasoning     bool                   `json:"reasoning"`
	Input         []string               `json:"input"`
	ContextWindow int                    `json:"contextWindow"`
	MaxTokens     int                    `json:"maxTokens"`
	Cost          map[string]interface{} `json:"cost"`
}

// AddModel POST /api/models/add
func (h *ModelsHandler) AddModel(c *gin.Context) {
	var req addModelRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if req.ContextWindow == 0 {
		req.ContextWindow = 4096
	}
	if req.MaxTokens == 0 {
		req.MaxTokens = 4096
	}
	if len(req.Input) == 0 {
		req.Input = []string{"text"}
	}

	cfg, _ := h.readConfig()
	providerName := req.Provider
	if providerName == "" {
		providerName = "custom"
	}
	p, ok := cfg.Models.Providers[providerName]
	if !ok {
		p = providerConfig{
			BaseURL: req.BaseURL,
			APIKey:  req.APIKey,
			API:     "openai-completions",
		}
	}
	modelID := req.ID
	if modelID == "" {
		modelID = req.Name
	}
	p.Models = append(p.Models, modelItem{
		ID:            modelID,
		Name:          req.Name,
		Reasoning:     req.Reasoning,
		Input:         req.Input,
		ContextWindow: req.ContextWindow,
		MaxTokens:     req.MaxTokens,
		Cost:          req.Cost,
	})
	cfg.Models.Providers[providerName] = p

	if err := h.writeConfig(cfg); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

// UpdateModel PUT /api/models/:id
func (h *ModelsHandler) UpdateModel(c *gin.Context) {
	modelID := c.Param("id")
	var req addModelRequest
	_ = c.ShouldBindJSON(&req)

	cfg, _ := h.readConfig()
	for provName, prov := range cfg.Models.Providers {
		for i, m := range prov.Models {
			if m.ID == modelID {
				if req.Name != "" {
					prov.Models[i].Name = req.Name
				}
				prov.Models[i].Reasoning = req.Reasoning
				if len(req.Input) > 0 {
					prov.Models[i].Input = req.Input
				}
				if req.ContextWindow > 0 {
					prov.Models[i].ContextWindow = req.ContextWindow
				}
				if req.MaxTokens > 0 {
					prov.Models[i].MaxTokens = req.MaxTokens
				}
				if req.Cost != nil {
					prov.Models[i].Cost = req.Cost
				}
				cfg.Models.Providers[provName] = prov
				if err := h.writeConfig(cfg); err != nil {
					c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
					return
				}
				c.JSON(http.StatusOK, gin.H{"status": "success"})
				return
			}
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "model not found"})
}

// DeleteModel DELETE /api/models/:id
func (h *ModelsHandler) DeleteModel(c *gin.Context) {
	modelID := c.Param("id")
	cfg, _ := h.readConfig()
	for provName, prov := range cfg.Models.Providers {
		newModels := prov.Models[:0]
		found := false
		for _, m := range prov.Models {
			if m.ID == modelID {
				found = true
				continue
			}
			newModels = append(newModels, m)
		}
		if found {
			prov.Models = newModels
			cfg.Models.Providers[provName] = prov
			if err := h.writeConfig(cfg); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
				return
			}
			c.JSON(http.StatusOK, gin.H{"status": "success"})
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "model not found"})
}

type setDefaultRequest struct {
	ModelID  string `json:"model_id"`
	Provider string `json:"provider"`
}

// SetDefaultModel POST /api/models/set-default
func (h *ModelsHandler) SetDefaultModel(c *gin.Context) {
	var req setDefaultRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	cfg, _ := h.readConfig()
	cfg.Agents.Defaults.Model.Primary = req.Provider + "/" + req.ModelID
	if err := h.writeConfig(cfg); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

func expandHome(path string) string {
	if len(path) >= 2 && path[:2] == "~/" {
		home, _ := os.UserHomeDir()
		return filepath.Join(home, path[2:])
	}
	return path
}
