# NetOps Skill - System Dependencies / 系统依赖指南

To ensure all scripts function correctly, the following system packages are required. / 为确保所有脚本正常运行，需安装以下系统软件包。

---

## 📦 OS-Specific Installation / 各发行版安装命令

### Debian / Ubuntu / Proxmox
```bash
sudo apt update
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    gcc \
    libpq-dev \
    ipmitool \
    mtr-tiny \
    traceroute \
    snmp \
    snmp-mibs-downloader \
    smartmontools \
    lm-sensors \
    ethtool \
    nmap \
    iproute2 \
    openssl \
    curl \
    npm
```

### RedHat / CentOS / Rocky / Alma
```bash
sudo dnf install -y \
    python3-pip \
    python3-devel \
    gcc \
    postgresql-devel \
    ipmitool \
    mtr \
    traceroute \
    net-snmp-utils \
    smartmontools \
    lm_sensors \
    ethtool \
    nmap \
    iproute \
    openssl \
    curl \
    npm
```

### Alpine Linux
```bash
sudo apk add \
    py3-pip \
    python3-dev \
    gcc \
    musl-dev \
    postgresql-dev \
    ipmitool \
    mtr \
    traceroute \
    net-snmp-tools \
    smartmontools \
    lm-sensors \
    ethtool \
    nmap \
    iproute2 \
    openssl \
    curl \
    nodejs \
    npm
```

---

## 📦 PM2 Installation / PM2 安装

After system packages are installed, install PM2 for process management:

```bash
# For China region, configure npm mirror first
npm config set registry https://registry.npmmirror.com

# Install PM2 globally
sudo npm install -g pm2

# Setup PM2 to start on boot
sudo pm2 startup
pm2 save
```

Or simply run the auto-setup script:
```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

---

## 📝 Post-Installation Notes / 安装后注意事项

1. **Netmiko**: Requires Python headers for some SSH optimizations (optional but recommended: `apt install python3-dev libssl-dev`). / **Netmiko**: 某些 SSH 优化可能需要 Python 头文件（可选建议：`apt install python3-dev libssl-dev`）。
2. **Speedtest**: The `speedtest-cli` is included in `requirements.txt`. / **Speedtest**: 测速工具已包含在 `requirements.txt` 中。
3. **Sensors**: Run `sudo sensors-detect` once to configure hardware monitoring. / **Sensors**: 首次安装后运行 `sudo sensors-detect` 以配置硬件监控传感器。
4. **SNMP**: Ensure SNMP service is allowed in your network firewall. / **SNMP**: 确保您的网络防火墙已允许 SNMP 协议流量。
5. **Nmap**: Used for the asset discovery feature. Ensure the user running the script has appropriate permissions. / **Nmap**: 用于资产发现功能，请确保运行脚本的用户拥有相应权限。
