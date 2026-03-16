package ssh

import (
	"fmt"
	"time"
)

// Reboot connects to the device via SSH and sends a reboot command.
// The connection error after reboot is expected and ignored.
func Reboot(ip, user, password string, timeout time.Duration) error {
	client, err := NewClient(ip, user, password, timeout)
	if err != nil {
		return fmt.Errorf("connect: %w", err)
	}
	defer client.Close()

	sess, err := client.NewSession()
	if err != nil {
		return fmt.Errorf("session: %w", err)
	}
	// Don't wait for command to return – the device will drop the connection
	_ = sess.Start("reboot")
	sess.Close()
	return nil
}
