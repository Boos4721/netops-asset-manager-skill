package handler

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/backend/ent"
	entdevice "github.com/netops/asset-manager/backend/ent/device"
	"github.com/netops/asset-manager/backend/internal/service/importer"
)

type ImportHandler struct {
	db *ent.Client
}

func NewImportHandler(db *ent.Client) *ImportHandler {
	return &ImportHandler{db: db}
}

// ImportDevices POST /api/inventory/import
func (h *ImportHandler) ImportDevices(c *gin.Context) {
	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "file required"})
		return
	}

	// Save to temp
	tmp, err := os.CreateTemp("", "import-*"+filepath.Ext(file.Filename))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	defer os.Remove(tmp.Name())
	tmp.Close()

	if err := c.SaveUploadedFile(file, tmp.Name()); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}

	rows, err := importer.ParseExcel(tmp.Name())
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	imported, skipped := 0, 0
	for _, row := range rows {
		vendor := strings.ToUpper(row.Vendor)
		driver := vendorToDriver(vendor)

		// Skip if IP already exists
		exists, _ := h.db.Device.Query().Where(entdevice.IPEQ(row.IP)).Exist(c)
		if exists {
			skipped++
			continue
		}

		tags := row.Tags
		if tags == nil {
			tags = []string{}
		}
		sshUser := row.SSHUser
		if sshUser == "" {
			sshUser = "root"
		}

		_, err := h.db.Device.Create().
			SetIP(row.IP).
			SetName(row.Name).
			SetVendor(vendor).
			SetModel(row.Model).
			SetLocation(row.Location).
			SetSn(row.SN).
			SetDriver(driver).
			SetTags(tags).
			SetSSHUser(sshUser).
			SetSSHPass(row.SSHPass).
			Save(c)
		if err != nil {
			skipped++
			continue
		}
		imported++
	}

	c.JSON(http.StatusOK, gin.H{
		"status":   "success",
		"imported": imported,
		"skipped":  skipped,
		"total":    len(rows),
	})
}
