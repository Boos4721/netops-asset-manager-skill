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

### Storage & Filesystem Maintenance

#### Software RAID (mdadm)
- **Check Status**: `cat /proc/mdstat` or `mdadm --detail /dev/md0`
- **Examine Disk**: `mdadm --examine /dev/sdX`
- **Monitor Errors**: `journalctl -u mdmonitor`

#### iSCSI
- **Discovery**: `iscsiadm -m discovery -t st -p <Target_IP>`
- **Login**: `iscsiadm -m node --login`
- **Session Check**: `iscsiadm -m session -P 3`

#### NFS / SMB (CIFS)
- **Show Mounts**: `showmount -e <NFS_IP>` or `smbstatus`
- **Mount NFS**: `mount -t nfs <IP>:/path /mnt/nfs`
- **Mount SMB**: `mount -t cifs -o username=<user> //<IP>/share /mnt/smb`
- **Test Connectivity**: `rpcinfo -p <IP>` (NFS) or `smbclient -L <IP>` (SMB)

#### Filesystem Operations (vfat, ext4, xfs)
- **Format VFAT**: `mkfs.vfat -F 32 /dev/sdX` (Good for UEFI/Boot)
- **Disk Usage**: `df -Th` (Shows FS types)
- **Repair**: `fsck.vfat -a /dev/sdX` or `xfs_repair /dev/sdX`
- **Inodes Check**: `df -i`

### Enterprise Server Out-of-Band (OOB) Management

#### DELL iDRAC (Redfish/IPMI)
- **Power Control**: `ipmitool -I lanplus -H <IP> -U <User> -P <Pass> chassis power on/off/cycle`
- **System Health**: `ipmitool -I lanplus -H <IP> sdr list`
- **LCD Display Set**: `ipmitool -I lanplus -H <IP> delloem lcd set str <Text>`
- **Event Log**: `ipmitool -I lanplus -H <IP> sel list`

#### Inspur (ISBMC)
- **Health Check**: `ipmitool -I lanplus -H <IP> sensor list`
- **Boot Device Set**: `ipmitool -I lanplus -H <IP> chassis bootdev pxe/cdrom/disk`
- **Fan Speed Check**: `ipmitool -I lanplus -H <IP> sdr type Fan`

#### Supermicro (IPMI)
- **Reset BMC**: `ipmitool -I lanplus -H <IP> bmc reset cold`
- **Inventory Info**: `ipmitool -I lanplus -H <IP> fru print`
- **Chassis Status**: `ipmitool -I lanplus -H <IP> chassis status`

### DevOps & Cloud Native Maintenance

#### Docker
- **Container Status**: `docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"`
- **Resource Usage**: `docker stats --no-stream`
- **Cleanup**: `docker system prune -f`
- **Logs**: `docker logs --tail 50 <container_name>`

#### Kubernetes (K8s)
- **Node Status**: `kubectl get nodes -o wide`
- **Pod Health**: `kubectl get pods -A | grep -v Running`
- **Events**: `kubectl get events --sort-by='.lastTimestamp'`
- **Resource Check**: `kubectl top nodes` / `kubectl top pods`

#### Nginx
- **Config Syntax Check**: `nginx -t`
- **Hot Reload**: `nginx -s reload`
- **Active Connections**: `stub_status` module parsing
- **Error Analysis**: `tail -n 50 /var/log/nginx/error.log | grep -i error`

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
