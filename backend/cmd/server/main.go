package main

import (
	"context"
	"fmt"
	"log"

	"github.com/netops/asset-manager/backend/config"
	"github.com/netops/asset-manager/backend/ent"
	"github.com/netops/asset-manager/backend/internal/auth"
	"github.com/netops/asset-manager/backend/internal/embedded"
	"github.com/netops/asset-manager/backend/internal/router"
	"github.com/netops/asset-manager/backend/internal/service/health"

	_ "github.com/lib/pq"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	// Connect to PostgreSQL via Ent
	db, err := ent.Open("postgres", cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("failed to connect to db: %v", err)
	}
	defer db.Close()

	// Auto-migrate schema
	if err := db.Schema.Create(context.Background()); err != nil {
		log.Fatalf("failed to create schema: %v", err)
	}

	// Ensure a default root user exists
	ensureDefaultUser(db, cfg)

	// Start health prober in background
	health.StartScheduler(db, cfg.ProbeInterval)

	// Embedded SPA dist/
	distFS := embedded.DistFS()

	r := router.Setup(db, cfg, distFS)

	addr := fmt.Sprintf(":%d", cfg.Port)
	log.Printf("NetOps server listening on %s", addr)
	if err := r.Run(addr); err != nil {
		log.Fatalf("server error: %v", err)
	}
}

func ensureDefaultUser(db *ent.Client, cfg *config.Config) {
	ctx := context.Background()
	count, _ := db.User.Query().Count(ctx)
	if count > 0 {
		return
	}
	hash, err := auth.HashPassword("admin")
	if err != nil {
		log.Printf("warn: failed to hash default password: %v", err)
		return
	}
	_, err = db.User.Create().
		SetUsername("admin").
		SetPasswordHash(hash).
		SetRole("root").
		Save(ctx)
	if err != nil {
		log.Printf("warn: failed to create default user: %v", err)
		return
	}
	log.Println("Created default user: admin / admin (please change password)")
}
