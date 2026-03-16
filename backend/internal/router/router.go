package router

import (
	"io/fs"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/netops/asset-manager/backend/config"
	"github.com/netops/asset-manager/backend/ent"
	"github.com/netops/asset-manager/backend/internal/auth"
	"github.com/netops/asset-manager/backend/internal/handler"
)

func Setup(db *ent.Client, cfg *config.Config, distFS fs.FS) *gin.Engine {
	r := gin.Default()
	r.SetTrustedProxies(nil)

	// CORS
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	// Handlers
	authH := handler.NewAuthHandler(db, cfg)
	usersH := handler.NewUsersHandler(db)
	invH := handler.NewInventoryHandler(db)
	rebootH := handler.NewRebootHandler(db, cfg)
	backupH := handler.NewBackupHandler(db, cfg)
	importH := handler.NewImportHandler(db)
	topoH := handler.NewTopologyHandler(db)
	modelsH := handler.NewModelsHandler(cfg.OpenclawConfigPath)
	jobsH := handler.NewJobsHandler()
	systemH := handler.NewSystemHandler()
	deployH := handler.NewDeployHandler()
	chatH := handler.NewChatHandler()
	discoverH := handler.NewDiscoverHandler(db)

	api := r.Group("/api")

	// Public
	api.POST("/users/login", authH.Login)

	// Authenticated
	secured := api.Group("")
	secured.Use(auth.JWTAuth(cfg.JWTSecret))
	{
		// Inventory - read
		secured.GET("/inventory", invH.ListInventory)
		secured.GET("/stats", invH.GetStats)

		// Inventory - operator+
		op := secured.Group("")
		op.Use(auth.RoleRequired("operator"))
		{
			op.POST("/inventory/add", invH.AddDevice)
			op.PUT("/inventory/:ip", invH.UpdateDevice)
			op.DELETE("/inventory/:ip", invH.DeleteDevice)
			op.POST("/inventory/reboot/:ip", rebootH.RebootDevice)
			op.POST("/inventory/backup/:ip", backupH.BackupDevice)
			op.GET("/inventory/backups/:ip", backupH.ListBackups)
			op.POST("/inventory/import", importH.ImportDevices)
			op.POST("/discover", discoverH.Discover)

			op.POST("/pm2/restart/:name", jobsH.RestartPM2)
			op.POST("/pm2/stop/:name", jobsH.StopPM2)
			op.POST("/pm2/rename/:name", jobsH.RenamePM2)
			op.POST("/pm2/schedule/:name", jobsH.SchedulePM2)
			op.POST("/pm2/deploy", jobsH.DeployPM2)

			op.POST("/topology/links", topoH.CreateLink)
			op.DELETE("/topology/links/:id", topoH.DeleteLink)
		}

		// PM2/topology/models - read for all authenticated
		secured.GET("/pm2/status", jobsH.GetPM2Status)
		secured.GET("/pm2/logs/:name", jobsH.GetPM2Logs)
		secured.GET("/topology/links", topoH.ListLinks)
		secured.GET("/models", modelsH.GetModels)
		secured.GET("/providers", modelsH.GetProviders)
		secured.GET("/system/info", systemH.GetSystemInfo)
		secured.POST("/chat", chatH.Chat)

		// Root only
		root := secured.Group("")
		root.Use(auth.RoleRequired("root"))
		{
			root.GET("/users", usersH.ListUsers)
			root.POST("/users", usersH.CreateUser)
			root.DELETE("/users/:id", usersH.DeleteUser)
			root.DELETE("/pm2/delete/:name", jobsH.DeletePM2)
			root.POST("/models/add", modelsH.AddModel)
			root.PUT("/models/:id", modelsH.UpdateModel)
			root.DELETE("/models/:id", modelsH.DeleteModel)
			root.POST("/models/set-default", modelsH.SetDefaultModel)
			root.POST("/deploy/system", deployH.DeploySystem)
		}
	}

	// SPA fallback
	if distFS != nil {
		spaH := handler.NewSPAHandler(distFS)
		r.NoRoute(spaH)
	}

	return r
}
