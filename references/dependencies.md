# NetOps Skill - System Dependencies

To ensure all scripts function correctly, the following system packages are required.

## Debian / Ubuntu / Proxmox
```bash
sudo apt update
sudo apt install -y \
    python3-pip \
    ipmitool \
    mtr-tiny \
    traceroute \
    snmp \
    smartmontools \
    lm-sensors
```

## RedHat / CentOS / Rocky
```bash
sudo dnf install -y \
    python3-pip \
    ipmitool \
    mtr \
    traceroute \
    net-snmp-utils \
    smartmontools \
    lm_sensors
```

## Alpine Linux
```bash
sudo apk add \
    py3-pip \
    ipmitool \
    mtr \
    traceroute \
    net-snmp-tools \
    smartmontools \
    lm-sensors
```

---

## Post-Installation Notes
1. **Netmiko**: Requires Python headers for some SSH optimizations (optional but recommended: `apt install python3-dev libssl-dev`).
2. **Speedtest**: The `speedtest-cli` is included in `requirements.txt`.
3. **Sensors**: Run `sudo sensors-detect` once to configure hardware monitoring.
