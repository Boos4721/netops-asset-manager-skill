package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/backend/ent"
	enttopologylink "github.com/netops/asset-manager/backend/ent/topologylink"
)

type TopologyHandler struct {
	db *ent.Client
}

func NewTopologyHandler(db *ent.Client) *TopologyHandler {
	return &TopologyHandler{db: db}
}

// ListLinks GET /api/topology/links
func (h *TopologyHandler) ListLinks(c *gin.Context) {
	links, err := h.db.TopologyLink.Query().All(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	result := make([]gin.H, 0, len(links))
	for _, l := range links {
		result = append(result, gin.H{
			"id":         l.ID,
			"source_ip":  l.SourceIP,
			"target_ip":  l.TargetIP,
			"link_type":  l.LinkType,
			"label":      l.Label,
			"created_at": l.CreatedAt,
		})
	}
	c.JSON(http.StatusOK, result)
}

type linkRequest struct {
	SourceIP string `json:"source_ip" binding:"required"`
	TargetIP string `json:"target_ip" binding:"required"`
	LinkType string `json:"link_type"`
	Label    string `json:"label"`
}

// CreateLink POST /api/topology/links
func (h *TopologyHandler) CreateLink(c *gin.Context) {
	var req linkRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if req.LinkType == "" {
		req.LinkType = "logical"
	}
	l, err := h.db.TopologyLink.Create().
		SetSourceIP(req.SourceIP).
		SetTargetIP(req.TargetIP).
		SetLinkType(req.LinkType).
		SetLabel(req.Label).
		Save(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "id": l.ID})
}

// DeleteLink DELETE /api/topology/links/:id
func (h *TopologyHandler) DeleteLink(c *gin.Context) {
	var idParam struct {
		ID int `uri:"id" binding:"required"`
	}
	if err := c.ShouldBindUri(&idParam); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}
	n, err := h.db.TopologyLink.Delete().Where(enttopologylink.IDEQ(idParam.ID)).Exec(c)
	if err != nil || n == 0 {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "link not found"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}
