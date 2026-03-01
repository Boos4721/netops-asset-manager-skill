# Network Automation Guide (Netmiko)

## Installation
Ensure `netmiko` is installed in the environment:
`pip install netmiko`

## Device Type Mapping
When connecting, map the identified `vendor` to Netmiko's `device_type`:
- **H3C**: `hp_comware`
- **Huawei**: `huawei`
- **Cisco**: `cisco_ios`
- **MikroTik**: `mikrotik_routeros`
- **Ruijie**: `ruijie_os`
- **Digital China**: `digital_china_os`
- **TP-LINK**: `tplink_jetstream`
- **NETGEAR**: `netgear_prosafe`

## Usage Pattern (Python)
```python
from netmiko import ConnectHandler

def execute_commands(ip, vendor, username, password, commands):
    device = {
        'device_type': mapping[vendor],
        'host': ip,
        'username': username,
        'password': password,
    }
    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_config_set(commands)
        return output
```

## Maintenance Workflows
1. **Health Check**: Run `display diagnostic-information` (H3C/Huawei) or `show tech-support` (Cisco).
2. **Configuration Backup**: Fetch `display current-configuration` and save to `assets/backups/`.
3. **VLAN Provisioning**: Use the patterns in [VENDORS.md](vendors.md).
