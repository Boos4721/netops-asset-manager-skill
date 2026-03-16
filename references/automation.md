# Network Automation Guide (Go SSH)

This project uses **Go native SSH** (`golang.org/x/crypto/ssh`) instead of Python/Netmiko.
All SSH operations are implemented in `backend/internal/service/ssh/`.

---

## Vendor → Driver Mapping

| Vendor (uppercase) | Driver (Netmiko compat) | SSH Reboot Command | Config Backup Command |
|---|---|---|---|
| `H3C` | `hp_comware` | `reboot force` | `display current-configuration` |
| `HUAWEI` | `huawei` | `reboot` | `display current-configuration` |
| `CISCO` | `cisco_ios` | `reload` | `show running-config` |
| `MIKROTIK` | `mikrotik_routeros` | `/system reboot` | `/export` |
| `RUIJIE` | `ruijie_os` | `reload` | `show running-config` |
| `DCN` | `digital_china_os` | `reboot` | `show running-config` |
| `LINUX` | `linux` | `reboot` | `cat /etc/os-release && ip addr && df -h` |

---

## Go SSH Client Usage

The SSH client is in `backend/internal/service/ssh/client.go`:

```go
// Connect to a device
client, err := ssh.NewClient(ip, user, password, timeout)
if err != nil { ... }
defer client.Close()

// Run a command
output, err := client.RunCommand("display current-configuration")
```

Key implementation details:
- Uses `gossh.InsecureIgnoreHostKey()` — acceptable for internal network ops
- Password authentication only (no key-based auth currently)
- `SSH_CONNECT_TIMEOUT` configurable in `config.yaml` (default: 10s)
- Reboot uses `sess.Start()` (non-blocking) since connection drops on reboot

---

## Maintenance Workflows

1. **Config Backup** (`POST /api/inventory/backup/:ip`): Fetches vendor-specific command output and stores in `backup` table in PostgreSQL.
2. **Remote Reboot** (`POST /api/inventory/reboot/:ip`): Sends reboot command via SSH; connection drop is expected and treated as success.
3. **Health Probe**: ICMP ping + TCP:22 check every 5 minutes (not SSH-based). See `backend/internal/service/health/`.

---

## Adding a New Vendor

1. Add vendor→command mapping in `backend/internal/service/ssh/backup.go`:
   ```go
   var vendorCommand = map[string]string{
       "NEWVENDOR": "show startup-config",
       ...
   }
   ```
2. Add vendor→driver in `backend/internal/handler/inventory.go`:
   ```go
   func vendorToDriver(v string) string {
       m := map[string]string{
           "NEWVENDOR": "newvendor_os",
           ...
       }
       ...
   }
   ```
3. Update this table above.

---

## References

- `references/vendors.md` — Full vendor CLI command reference
- `references/snmp.md` — SNMP OID reference for polling fallback
