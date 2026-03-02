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

## Router & Enterprise Gateway Support

### H3C / Huawei (Enterprise Routers)
- **Routing Table**: `display ip routing-table`
- **BGP Status**: `display bgp peer`
- **OSPF Neighbors**: `display ospf peer brief`
- **Interface Status**: `display ip interface brief`
- **CPU/Memory**: `display cpu-usage`, `display memory-usage`

### Cisco (ISR/ASR Routers)
- **Routing Table**: `show ip route`
- **BGP Summary**: `show ip bgp summary`
- **Interface Stats**: `show ip interface brief`
- **EIGRP Neighbors**: `show ip eigrp neighbors`

### MikroTik (RouterOS - Core Routing)
- **Routes**: `/ip route print`
- **BGP Peers**: `/routing bgp peer print`
- **OSPF Neighbors**: `/routing ospf neighbor print`
- **NAT Rules**: `/ip firewall nat print`
- **Queue/QoS**: `/queue simple print`

### Ruijie (RGOS & EG Gateway)
- **Routing Table**: `show ip route`
- **EG Gateway Status**: `show gateway status`
- **EG NAT Sessions**: `show ip nat translations count`
- **EG Auth Users**: `show dot1x summary`
- **BGP Status**: `show ip bgp summary`

### TP-LINK / NETGEAR (Business Routers)
- **Static Routes**: `show ip route`
- **WAN Status**: `show interface wan`
- **NAT Table**: `show ip nat statistics`

## Ruijie (RGOS Switch & EG Gateway)
- Enter view: `configure terminal`
- View VLAN: `show vlan`
- Create VLAN: `vlan 10`
- Assign port: `interface gigabitEthernet 0/1`, `switchport mode access`, `switchport access vlan 10`
- **Check MAC Table**: `show mac-address-table`
- **Check Routing**: `show ip route`
- **EG Gateway Status**: `show gateway status`
- **EG NAT Sessions**: `show ip nat translations count`
- **EG Auth Users**: `show dot1x summary`
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

### Virtualization & Hypervisor Management

#### VMware ESXi (esxcli/vim-cmd)
- **VM List**: `vim-cmd vmsvc/getallvms`
- **Power Operations**: `vim-cmd vmsvc/power.on <vmid>` / `power.off` / `reboot`
- **Host Info**: `esxcli system version get`
- **Resource Check**: `esxcli system visstats display`

#### OpenStack (CLI)
- **Server List**: `openstack server list --all-projects`
- **Hypervisor Status**: `openstack hypervisor list`
- **Service Health**: `openstack compute service list`
- **Flavor Check**: `openstack flavor list`

#### QEMU/KVM & Proxmox (virsh/pct)
- **KVM List**: `virsh list --all`
- **KVM Resource**: `virsh domstats <name>`
- **LXC List**: `pct list`
- **LXC Enter**: `pct enter <vmid>`
- **Backup**: `vzdump <vmid> --storage local --compress lzo`

### Deep OSI-Layer Diagnostics

#### Physical Layer (L1 - SFP/Cable)
- **H3C/Huawei**: `display transceiver interface <Int> verbose` (Check Optical Power/Voltage)
- **Cisco**: `show interfaces <Int> transceiver`
- **Linux**: `ethtool <ethX>` (Speed/Duplex), `ethtool -m <ethX>` (Optical diagnostics)

#### Data Link & Network Layer (L2/L3 - VLAN/ARP/Routing)
- **MAC Table**: `display mac-address` (H3C/Huawei), `show mac address-table` (Cisco)
- **LACP/Bonding**: `display link-aggregation summary`, `cat /proc/net/bonding/bond0`
- **BGP/OSPF**: `display bgp peer`, `display ospf peer brief`
- **STP**: `display stp brief`

#### Session & Transport Layer (L4/L5 - Ports/Sessions)
- **Linux Netstat**: `ss -antp` (Detailed TCP sessions), `ss -s` (Summary)
- **Conntrack**: `conntrack -S` (Firewall session table stats)
- **Load Balancer**: `haproxy -c -f /etc/haproxy/haproxy.cfg` (Check config)

#### Presentation & Application Layer (L6/L7 - TLS/APIs)
- **TLS Handshake**: `openssl s_client -connect <IP>:443 -tls1_2` (Test protocol support)
- **HTTP/API**: `curl -o /dev/null -s -w "%{http_code}\n" <URL>` (Status code check)
- **Log Pattern**: `awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c` (HTTP code distribution)

### High-Performance Networking (HPC/GPU Clusters)

#### NVIDIA Mellanox Infiniband (IB)
- **Adapter Status**: `ibstat` or `ibstatus`
- **HCA Health**: `ibv_devinfo`
- **Port Performance**: `perfquery`
- **Fabric Discovery**: `ibnetdiscover`
- **Subnet Manager Status**: `sminfo`

#### RDMA & NCCL (GPU-to-GPU)
- **RDMA Stats**: `rdma statistics show link`
- **NCCL Bandwidth Test**: `NCCL_DEBUG=INFO ./nccl-tests/build/all_reduce_perf -b 8 -e 256M -f 2 -g <gpu_count>`
- **RoCE Configuration**: `show_gids`

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

## Wireless & Security Device Commands (AC/AP/Firewall)

### H3C / Huawei (Wireless AC & Security)
- **AC Status**: `display wlan ap all`, `display wlan client`
- **AP Management**: `wlan ap <name>`, `serial-id <sn>`
- **Firewall Policy**: `display security-policy ip`
- **Firewall Session**: `display firewall session table`
- **Gateway/NAT**: `display nat session all`

### Cisco (Wireless & Firepower/ASA)
- **AC Client List**: `show client summary`
- **AP Status**: `show ap summary`
- **ASA Firewall**: `show conn`, `show access-list`
- **ASA NAT**: `show nat`

### Ruijie (Wireless & Firewall)
- **AC Status**: `show ap-config summary`
- **Client List**: `show sta-cap summary`
- **Firewall Policy**: `show security-policy`

### Fortinet (FortiGate)
- **System Status**: `get system status`
- **Policy Check**: `show firewall policy`
- **Session List**: `get system session list`
- **Interface Bandwidth**: `diagnose netlink interface list <int>`

### Palo Alto (PAN-OS)
- **Policy Check**: `show config running`
- **Session Stats**: `show session info`
- **System Resource**: `show system resources`

### MikroTik (Wireless/CAPsMAN)
- **CAPsMAN Status**: `/caps-man remote-cap print`
- **Registration Table**: `/interface wireless registration-table print`
- **Firewall Rules**: `/ip firewall filter print`
- **NAT Rules**: `/ip firewall nat print`

### TP-LINK / NETGEAR (WLAN)
- **AP Status**: `show wireless ap`
- **Clients**: `show wireless client`

## Enterprise Server Out-of-Band (OOB) Management

#### DELL iDRAC (Redfish/IPMI/racadm)
- **Power Control**: `ipmitool -I lanplus -H <IP> -U <User> -P <Pass> chassis power on/off/cycle`
- **System Health**: `ipmitool -I lanplus -H <IP> sdr list`
- **Event Log**: `ipmitool -I lanplus -H <IP> sel list`
- **Racadm (Remote)**: `racadm -r <IP> -u <User> -p <Pass> getsysinfo`
- **Racadm BIOS Set**: `racadm -r <IP> -u <User> -p <Pass> set BIOS.SysProfileSettings.SysProfile Performance`
- **Racadm Job Queue**: `racadm -r <IP> -u <User> -p <Pass> jobqueue view`

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
- **Driver Update (Primary - Official CN/HK)**:
  - Download from: `https://www.nvidia.cn/Download/index.aspx?lang=cn` or `https://www.nvidia.com/zh-hk/geforce/drivers/`
  - Install: `chmod +x NVIDIA-Linux-x86_64-xxx.run && ./NVIDIA-Linux-x86_64-xxx.run -s --no-questions --accept-license`
- **Driver Install (Fallback - Package Manager)**: `apt install -y nvidia-driver` (Debian)
- **Memory/Load Check**: `nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv`
- **Temperature**: `nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader`
- **PCI Errors**: `dmesg | grep -i nvidia`

#### AMD (A-Card)
- **Status Check**: `rocm-smi` or `radeontop`
- **Driver Update (Primary - Official CN)**:
  - Download from: `https://www.amd.com/zh-hans/support`
  - Install: `./amdgpu-install --usecase=dkms,graphics`
- **Driver Install (Fallback - Ubuntu)**: `apt install -y amdgpu-pro`
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
