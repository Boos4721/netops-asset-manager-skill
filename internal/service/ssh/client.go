package ssh

import (
	"fmt"
	"net"
	"time"

	gossh "golang.org/x/crypto/ssh"
)

// NewClient creates an SSH client connection with password auth.
func NewClient(ip, user, password string, timeout time.Duration) (*gossh.Client, error) {
	cfg := &gossh.ClientConfig{
		User: user,
		Auth: []gossh.AuthMethod{
			gossh.Password(password),
		},
		HostKeyCallback: gossh.InsecureIgnoreHostKey(), // for internal network use
		Timeout:         timeout,
	}

	addr := net.JoinHostPort(ip, "22")
	client, err := gossh.Dial("tcp", addr, cfg)
	if err != nil {
		return nil, fmt.Errorf("ssh dial %s: %w", addr, err)
	}
	return client, nil
}

// RunCommand opens a session on the client and executes a command, returning combined output.
func RunCommand(client *gossh.Client, cmd string) (string, error) {
	sess, err := client.NewSession()
	if err != nil {
		return "", fmt.Errorf("new session: %w", err)
	}
	defer sess.Close()

	out, err := sess.CombinedOutput(cmd)
	return string(out), err
}
