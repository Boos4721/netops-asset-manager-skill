package health

import (
	"fmt"
	"net"
	"os/exec"
	"runtime"
	"time"
)

// PingCheck sends a single ICMP ping to the given IP.
func PingCheck(ip string) bool {
	var cmd *exec.Cmd
	if runtime.GOOS == "windows" {
		cmd = exec.Command("ping", "-n", "1", "-w", "1000", ip)
	} else {
		cmd = exec.Command("ping", "-c", "1", "-W", "1", ip)
	}
	return cmd.Run() == nil
}

// TCPCheck attempts a TCP connection to ip:22.
func TCPCheck(ip string) bool {
	conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:22", ip), 2*time.Second)
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

// IsOnline returns true if the device is reachable (ping OR tcp:22).
func IsOnline(ip string) bool {
	return PingCheck(ip) || TCPCheck(ip)
}
