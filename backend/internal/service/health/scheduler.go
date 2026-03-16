package health

import (
	"context"
	"log"
	"time"

	"github.com/netops/asset-manager/backend/ent"
	entdevice "github.com/netops/asset-manager/backend/ent/device"
)

// StartScheduler runs a background goroutine that probes all devices every interval.
func StartScheduler(db *ent.Client, interval time.Duration) {
	go func() {
		log.Printf("[health] prober started, interval=%s", interval)
		for {
			probeAll(db)
			time.Sleep(interval)
		}
	}()
}

func probeAll(db *ent.Client) {
	ctx := context.Background()
	devices, err := db.Device.Query().All(ctx)
	if err != nil {
		log.Printf("[health] failed to query devices: %v", err)
		return
	}

	for _, d := range devices {
		online := IsOnline(d.IP)
		status := entdevice.StatusOffline
		if online {
			status = entdevice.StatusOnline
		}
		now := time.Now()
		upd := db.Device.UpdateOne(d).SetStatus(status)
		if online {
			upd = upd.SetLastSeen(now)
		}
		if err := upd.Exec(ctx); err != nil {
			log.Printf("[health] failed to update device %s: %v", d.IP, err)
		}
	}
	log.Printf("[health] probed %d devices", len(devices))
}
