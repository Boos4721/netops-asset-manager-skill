# Network Vendor Command Patterns

## H3C (Comware)
- Enter view: `system-view`
- View VLAN: `display vlan`
- Create VLAN: `vlan 10`
- Assign port: `interface Bridge-Aggregation 1`, `port access vlan 10`
- Save config: `save force`

## Huawei (VRP)
- Enter view: `system-view`
- View VLAN: `display vlan`
- Create VLAN: `vlan 10`
- Assign port: `interface GigabitEthernet 0/0/1`, `port default vlan 10`
- Save config: `save`

## Cisco (IOS)
- Enter view: `configure terminal`
- View VLAN: `show vlan brief`
- Create VLAN: `vlan 10`
- Assign port: `interface GigabitEthernet 0/1`, `switchport access vlan 10`
- Save config: `write memory`

## MikroTik (RouterOS)
- Add VLAN: `/interface vlan add name=vlan10 vlan-id=10 interface=bridge`
- Check status: `/system resource print`
- Update: `/system package update check-for-updates`

## Ruijie (RGOS)
- Enter view: `configure terminal`
- View VLAN: `show vlan`
- Create VLAN: `vlan 10`
- Assign port: `interface gigabitEthernet 0/1`, `switchport mode access`, `switchport access vlan 10`
- Save config: `write`

## Digital China (DCN)
- Enter view: `config`
- View VLAN: `show vlan`
- Create VLAN: `vlan 10`
- Assign port: `interface ethernet 1/0/1`, `switchport access vlan 10`
- Save config: `write`

## TP-LINK (Enterprise/CLI)
- Enter view: `configure`
- View VLAN: `show vlan`
- Create VLAN: `vlan 10`
- Assign port: `interface gigabitEthernet 1/0/1`, `switchport general allowed vlan 10 untagged`
- Save config: `copy running-config startup-config`

## NETGEAR (ProSAFE CLI)
- Enter view: `configure`
- View VLAN: `show vlan`
- Create VLAN: `vlan database`, `vlan 10`
- Assign port: `interface 1/g1`, `vlan participation include 10`, `vlan untagged 10`
- Save config: `save`

### GPU Maintenance & Monitoring

#### NVIDIA (N-Card)
- **Status Check**: `nvidia-smi`
- **Driver Install (Debian)**: `apt install -y nvidia-driver`
- **Memory/Load Check**: `nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv`
- **Temperature**: `nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader`
- **PCI Errors**: `dmesg | grep -i nvidia`

#### AMD (A-Card)
- **Status Check**: `rocm-smi` or `radeontop`
- **Driver Install (Ubuntu)**: `amdgpu-install`
- **Hardware Info**: `clinfo`
- **PCI Errors**: `dmesg | grep -i amdgpu`

#### System Level (PCI/Bus)
- **List GPUs**: `lspci | grep -i vga` or `lspci | grep -i display`
- **Detailed PCI Info**: `lspci -vnn -s <slot_id>`
- **PCIe Link Errors**: `dmesg | grep -i "PCIe Bus Error"`

### Core Hardware Checks (All Distros)
- **CPU Load**: `top -bn1 | grep "load average" | awk '{print $NF}'`
- **Memory**: `free -h`
- **Disk Usage**: `df -h`
- **Disk Health (Smartmontools)**: `smartctl -H /dev/sda`
- **CPU Temp**: `sensors` (requires lm-sensors)

### Debian / Ubuntu / Proxmox (APT-based)
- **Update check**: `apt update && apt list --upgradable`
- **Service management**: `systemctl status <service>`
- **Package install**: `apt install -y <package>`
- **System Logs**: `tail -f /var/log/syslog`

### RedHat / CentOS / Rocky / Alma (YUM/DNF-based)
- **Update check**: `dnf check-update` or `yum check-update`
- **Service management**: `systemctl status <service>`
- **Package install**: `dnf install -y <package>`
- **System Logs**: `tail -f /var/log/messages`

### Alpine Linux (APK-based)
- **Update check**: `apk update && apk list --upgradable`
- **Service management**: `rc-service <service> status`
- **Package install**: `apk add <package>`
