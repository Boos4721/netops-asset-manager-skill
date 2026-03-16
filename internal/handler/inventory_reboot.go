package handler

import (
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/config"
	"github.com/netops/asset-manager/ent"
	entbackup "github.com/netops/asset-manager/ent/backup"
	entdevice "github.com/netops/asset-manager/ent/device"
	sshsvc "github.com/netops/asset-manager/internal/service/ssh"
)

type RebootHandler struct {
	db  *ent.Client
	cfg *config.Config
}

func NewRebootHandler(db *ent.Client, cfg *config.Config) *RebootHandler {
	return &RebootHandler{db: db, cfg: cfg}
}

type rebootRequest struct {
	User     string `json:"user"`
	Password string `json:"password"`
}

// RebootDevice POST /api/inventory/reboot/:ip
func (h *RebootHandler) RebootDevice(c *gin.Context) {
	ip := c.Param("ip")
	var req rebootRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		// try to get from device record
	}
	if req.User == "" {
		req.User = "root"
	}

	// If no creds provided, try from DB
	if req.Password == "" {
		d, err := h.db.Device.Query().Where(entdevice.IPEQ(ip)).Only(c)
		if err == nil {
			if req.User == "root" && d.SSHUser != "" {
				req.User = d.SSHUser
			}
			req.Password = d.SSHPass
		}
	}

	if err := sshsvc.Reboot(ip, req.User, req.Password, h.cfg.SSHConnectTimeout); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "message": fmt.Sprintf("已向 %s 发送重启指令", ip)})
}

type BackupHandler struct {
	db  *ent.Client
	cfg *config.Config
}

func NewBackupHandler(db *ent.Client, cfg *config.Config) *BackupHandler {
	return &BackupHandler{db: db, cfg: cfg}
}

// BackupDevice POST /api/inventory/backup/:ip
func (h *BackupHandler) BackupDevice(c *gin.Context) {
	ip := c.Param("ip")

	d, err := h.db.Device.Query().Where(entdevice.IPEQ(ip)).Only(c)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "device not found"})
		return
	}

	content, err := sshsvc.BackupConfig(ip, d.SSHUser, d.SSHPass, d.Vendor, h.cfg.SSHConnectTimeout)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": "error", "message": err.Error()})
		return
	}

	filename := fmt.Sprintf("%s_%s.txt", ip, time.Now().Format("20060102_150405"))
	b, err := h.db.Backup.Create().
		SetDeviceIP(ip).
		SetFilename(filename).
		SetContent(content).
		SetSizeBytes(int64(len(content))).
		SetVendor(d.Vendor).
		Save(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":   "success",
		"filename": b.Filename,
		"size":     b.SizeBytes,
	})
}

// ListBackups GET /api/inventory/backups/:ip
func (h *BackupHandler) ListBackups(c *gin.Context) {
	ip := c.Param("ip")
	backups, err := h.db.Backup.Query().
		Where(entbackup.DeviceIPEQ(ip)).
		Order(ent.Desc(entbackup.FieldCreatedAt)).
		All(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	result := make([]gin.H, 0, len(backups))
	for _, b := range backups {
		result = append(result, gin.H{
			"id":         b.ID,
			"device_ip":  b.DeviceIP,
			"filename":   b.Filename,
			"size_bytes": b.SizeBytes,
			"vendor":     b.Vendor,
			"created_at": b.CreatedAt,
		})
	}
	c.JSON(http.StatusOK, result)
}
