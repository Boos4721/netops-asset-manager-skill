package handler

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/ent"
	entdevice "github.com/netops/asset-manager/ent/device"
)

type InventoryHandler struct {
	db *ent.Client
}

func NewInventoryHandler(db *ent.Client) *InventoryHandler {
	return &InventoryHandler{db: db}
}

// ListInventory GET /api/inventory
func (h *InventoryHandler) ListInventory(c *gin.Context) {
	devices, err := h.db.Device.Query().Order(ent.Asc(entdevice.FieldIP)).All(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, devicesToJSON(devices))
}

// AddDevice POST /api/inventory/add
func (h *InventoryHandler) AddDevice(c *gin.Context) {
	var req deviceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	vendor := strings.ToUpper(req.Vendor)
	driver := vendorToDriver(vendor)
	if req.Driver != "" {
		driver = req.Driver
	}

	d, err := h.db.Device.Create().
		SetIP(req.IP).
		SetName(req.Name).
		SetVendor(vendor).
		SetModel(req.Model).
		SetLocation(req.Location).
		SetSn(req.SN).
		SetServer(req.Server).
		SetDriver(driver).
		SetTags(req.Tags).
		SetSSHUser(req.SSHUser).
		SetSSHPass(req.SSHPass).
		SetGpu(req.GPU).
		Save(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "device": deviceToJSON(d)})
}

// UpdateDevice PUT /api/inventory/:ip
func (h *InventoryHandler) UpdateDevice(c *gin.Context) {
	ip := c.Param("ip")
	var req deviceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
		return
	}

	d, err := h.db.Device.Query().Where(entdevice.IPEQ(ip)).Only(c)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "device not found"})
		return
	}

	vendor := strings.ToUpper(req.Vendor)
	if vendor == "" {
		vendor = d.Vendor
	}
	driver := vendorToDriver(vendor)
	if req.Driver != "" {
		driver = req.Driver
	}

	upd := h.db.Device.UpdateOne(d)
	if req.Name != "" {
		upd = upd.SetName(req.Name)
	}
	if vendor != "" {
		upd = upd.SetVendor(vendor).SetDriver(driver)
	}
	if req.Model != "" {
		upd = upd.SetModel(req.Model)
	}
	if req.Location != "" {
		upd = upd.SetLocation(req.Location)
	}
	if req.SN != "" {
		upd = upd.SetSn(req.SN)
	}
	if req.Server != "" {
		upd = upd.SetServer(req.Server)
	}
	if req.SSHUser != "" {
		upd = upd.SetSSHUser(req.SSHUser)
	}
	if req.SSHPass != "" {
		upd = upd.SetSSHPass(req.SSHPass)
	}
	if len(req.Tags) > 0 {
		upd = upd.SetTags(req.Tags)
	}
	upd = upd.SetGpu(req.GPU)

	updated, err := upd.Save(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "device": deviceToJSON(updated)})
}

// DeleteDevice DELETE /api/inventory/:ip
func (h *InventoryHandler) DeleteDevice(c *gin.Context) {
	ip := c.Param("ip")
	n, err := h.db.Device.Delete().Where(entdevice.IPEQ(ip)).Exec(c)
	if err != nil || n == 0 {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "device not found"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success"})
}

// GetStats GET /api/stats
func (h *InventoryHandler) GetStats(c *gin.Context) {
	total, _ := h.db.Device.Query().Count(c)
	online, _ := h.db.Device.Query().Where(entdevice.StatusEQ(entdevice.StatusOnline)).Count(c)
	gpuCount, _ := h.db.Device.Query().Where(entdevice.GpuEQ(true)).Count(c)
	c.JSON(http.StatusOK, gin.H{
		"total":     total,
		"online":    online,
		"offline":   total - online,
		"alerts":    0,
		"gpu_count": gpuCount,
	})
}

// ---- helpers ----

type deviceRequest struct {
	IP       string   `json:"ip"`
	Name     string   `json:"name"`
	Vendor   string   `json:"vendor"`
	Model    string   `json:"model"`
	Location string   `json:"location"`
	SN       string   `json:"sn"`
	Server   string   `json:"server"`
	Driver   string   `json:"driver"`
	Tags     []string `json:"tags"`
	SSHUser  string   `json:"ssh_user"`
	SSHPass  string   `json:"ssh_pass"`
	GPU      bool     `json:"gpu"`
}

func vendorToDriver(vendor string) string {
	m := map[string]string{
		"H3C":      "hp_comware",
		"HUAWEI":   "huawei",
		"CISCO":    "cisco_ios",
		"MIKROTIK": "mikrotik_routeros",
		"LINUX":    "linux",
	}
	if d, ok := m[strings.ToUpper(vendor)]; ok {
		return d
	}
	return "generic"
}

func deviceToJSON(d *ent.Device) gin.H {
	return gin.H{
		"id":         d.ID,
		"ip":         d.IP,
		"name":       d.Name,
		"vendor":     d.Vendor,
		"model":      d.Model,
		"location":   d.Location,
		"sn":         d.Sn,
		"server":     d.Server,
		"driver":     d.Driver,
		"tags":       d.Tags,
		"ssh_user":   d.SSHUser,
		"status":     d.Status.String(),
		"last_seen":  d.LastSeen,
		"gpu":        d.Gpu,
		"created_at": d.CreatedAt,
		"updated_at": d.UpdatedAt,
	}
}

func devicesToJSON(devices []*ent.Device) []gin.H {
	result := make([]gin.H, 0, len(devices))
	for _, d := range devices {
		result = append(result, deviceToJSON(d))
	}
	return result
}
