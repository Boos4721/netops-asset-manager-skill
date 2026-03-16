package ssh

import (
	"fmt"
	"strings"
	"time"
)

// vendorCommand maps normalized vendor names to the config-display command.
var vendorCommand = map[string]string{
	"H3C":      "display current-configuration",
	"HUAWEI":   "display current-configuration",
	"CISCO":    "show running-config",
	"MIKROTIK": "/export",
	"LINUX":    "cat /etc/os-release && ip addr",
}

// BackupConfig SSHes into the device and retrieves its running configuration.
func BackupConfig(ip, user, password, vendor string, timeout time.Duration) (string, error) {
	cmd, ok := vendorCommand[strings.ToUpper(vendor)]
	if !ok {
		cmd = "show running-config" // generic fallback
	}

	client, err := NewClient(ip, user, password, timeout)
	if err != nil {
		return "", fmt.Errorf("connect: %w", err)
	}
	defer client.Close()

	output, err := RunCommand(client, cmd)
	if err != nil {
		// Some devices return non-zero but still produce output
		if output == "" {
			return "", fmt.Errorf("run command: %w", err)
		}
	}
	return output, nil
}
