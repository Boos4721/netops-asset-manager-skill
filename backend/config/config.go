package config

import (
	"strings"
	"time"

	"github.com/spf13/viper"
)

type Config struct {
	Port               int           `mapstructure:"PORT"`
	DatabaseURL        string        `mapstructure:"DATABASE_URL"`
	JWTSecret          string        `mapstructure:"JWT_SECRET"`
	JWTExpiry          time.Duration `mapstructure:"JWT_EXPIRY"`
	ProbeInterval      time.Duration `mapstructure:"PROBE_INTERVAL"`
	OpenclawConfigPath string        `mapstructure:"OPENCLAW_CONFIG_PATH"`
	SSHConnectTimeout  time.Duration `mapstructure:"SSH_CONNECT_TIMEOUT"`
}

func Load() (*Config, error) {
	v := viper.New()

	v.SetDefault("PORT", 8081)
	v.SetDefault("DATABASE_URL", "postgres://postgres:boos@127.0.0.1:5432/netops?sslmode=disable")
	v.SetDefault("JWT_SECRET", "netops-change-me-in-production")
	v.SetDefault("JWT_EXPIRY", "24h")
	v.SetDefault("PROBE_INTERVAL", "5m")
	v.SetDefault("OPENCLAW_CONFIG_PATH", "~/.openclaw/openclaw.json")
	v.SetDefault("SSH_CONNECT_TIMEOUT", "10s")

	v.SetConfigName("config")
	v.SetConfigType("yaml")
	v.AddConfigPath(".")
	v.AddConfigPath("/etc/netops/")

	v.AutomaticEnv()
	v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

	_ = v.ReadInConfig() // ignore if config.yaml doesn't exist

	cfg := &Config{}
	if err := v.Unmarshal(cfg); err != nil {
		return nil, err
	}

	return cfg, nil
}
