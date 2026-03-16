package main

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"path/filepath"

	"github.com/netops/asset-manager/config"
	"github.com/netops/asset-manager/ent"
	"github.com/netops/asset-manager/internal/auth"

	_ "github.com/lib/pq"
)

type inventoryDevice struct {
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

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("config: %v", err)
	}

	db, err := ent.Open("postgres", cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("db connect: %v", err)
	}
	defer db.Close()

	ctx := context.Background()
	if err := db.Schema.Create(ctx); err != nil {
		log.Fatalf("schema create: %v", err)
	}

	// Migrate inventory.json
	migrateInventory(db, ctx)

	// Ensure default admin user
	count, _ := db.User.Query().Count(ctx)
	if count == 0 {
		hash, _ := auth.HashPassword("admin")
		_, err := db.User.Create().
			SetUsername("admin").
			SetPasswordHash(hash).
			SetRole("root").
			Save(ctx)
		if err != nil {
			log.Printf("create admin: %v", err)
		} else {
			log.Println("Created default admin user (password: admin)")
		}
	}

	log.Println("Migration complete.")
}

func migrateInventory(db *ent.Client, ctx context.Context) {
	// Try to find inventory.json in assets/
	paths := []string{
		"assets/inventory.json",
		"../../assets/inventory.json",
	}
	var data []byte
	for _, p := range paths {
		abs, _ := filepath.Abs(p)
		d, err := os.ReadFile(abs)
		if err == nil {
			data = d
			log.Printf("Reading inventory from: %s", abs)
			break
		}
	}
	if data == nil {
		log.Println("No inventory.json found, skipping device migration.")
		return
	}

	var devices []inventoryDevice
	if err := json.Unmarshal(data, &devices); err != nil {
		log.Printf("parse inventory.json: %v", err)
		return
	}

	imported := 0
	for _, d := range devices {
		if d.IP == "" {
			continue
		}
		tags := d.Tags
		if tags == nil {
			tags = []string{}
		}
		sshUser := d.SSHUser
		if sshUser == "" {
			sshUser = "root"
		}
		_, err := db.Device.Create().
			SetIP(d.IP).
			SetName(d.Name).
			SetVendor(d.Vendor).
			SetModel(d.Model).
			SetLocation(d.Location).
			SetSn(d.SN).
			SetServer(d.Server).
			SetDriver(d.Driver).
			SetTags(tags).
			SetSSHUser(sshUser).
			SetSSHPass(d.SSHPass).
			SetGpu(d.GPU).
			Save(ctx)
		if err != nil {
			log.Printf("  skip %s: %v", d.IP, err)
			continue
		}
		imported++
	}
	log.Printf("Imported %d/%d devices from inventory.json", imported, len(devices))
}
