#!/bin/bash

# NetOps Skill - Auto Environment Setup Script
# Supports: Debian/Ubuntu (Standard & DEB822), RedHat/CentOS/Rocky, Alpine Linux
# Bilingual Support: Detects system locale to display EN or ZH
# Network Smart: Detects IP location to use domestic mirrors (CN) for OS and PIP packages

# Language Detection
LANG_PREF="en"
if [[ "$LANG" == *"zh"* ]] || [[ "$LANGUAGE" == *"zh"* ]]; then
    LANG_PREF="zh"
fi

# Translation Helper
t() {
    local zh="$1"
    local en="$2"
    if [ "$LANG_PREF" = "zh" ]; then
        echo -e "$zh"
    else
        echo -e "$en"
    fi
}

# Location Detection (CN or Global)
IS_CN=false
echo "🔍 $(t '正在检测网络区域...' 'Detecting network location...')"
IF_CONFIG_CO=$(curl -s --connect-timeout 5 https://ifconfig.co/country-iso || echo "UNKNOWN")
if [ "$IF_CONFIG_CO" = "CN" ]; then
    IS_CN=true
    echo "🇨🇳 $(t '检测到您位于中国大陆，将自动开启系统源与 PIP 镜像加速。' 'Detected Mainland China. Enabling OS and PIP mirror acceleration.')"
else
    echo "🌍 $(t '检测到非中国大陆区域，使用全球默认源。' 'Global location detected. Using default sources.')"
fi

echo "🚀 $(t '正在启动 NetOps 环境安装程序...' 'Starting NetOps Environment Setup...')"

# Check if running as root
if [ "$EUID" -eq 0 ] || [ "$(id -u)" -eq 0 ]; then
    SUDO=""
    echo "👤 $(t '检测到 root 用户，将自动跳过 sudo' 'Running as root, sudo not needed')"
else
    SUDO="$SUDO"
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION_ID=$VERSION_ID
else
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
fi

# OS-Specific Mirror & Installation
install_debian() {
    echo "📦 $(t '正在切换系统源至镜像站...' 'Switching system sources to mirror...')"
    
    # ... (skipping some lines for context matching)
    echo "📦 $(t '正在更新系统软件包...' 'Updating system packages...')"
    $SUDO apt update
    $SUDO apt install -y python3 python3-pip python3-venv python3-dev gcc libpq-dev ipmitool mtr-tiny traceroute snmp snmp-mibs-downloader smartmontools lm-sensors ethtool nmap iproute2 openssl curl npm
    
    # Install racadm if on Debian/Ubuntu (Dell repo might be needed, but adding basic message)
    echo "💡 $(t '如需使用 racadm，请安装 Dell iDRAC Tools。' 'For racadm, please install Dell iDRAC Tools.')"
}

install_redhat() {
    echo "📦 $(t '正在安装系统依赖...' 'Installing system dependencies...')"
    if command -v dnf > /dev/null; then
        $SUDO dnf install -y python3 python3-pip python3-devel gcc postgresql-devel ipmitool mtr traceroute net-snmp-utils smartmontools lm_sensors ethtool nmap iproute openssl curl npm
    else
        $SUDO yum install -y python3 python3-pip python3-devel gcc postgresql-devel ipmitool mtr traceroute net-snmp-utils smartmontools lm_sensors ethtool nmap iproute openssl curl npm
    fi
}

install_alpine() {
    if [ "$IS_CN" = true ]; then
        echo "⚡ $(t '正在切换 Alpine 源至中科大镜像 (USTC)...' 'Switching Alpine sources to USTC mirror...')"
        $SUDO sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
    fi
    echo "📦 $(t '正在更新系统软件包...' 'Updating system packages...')"
    $SUDO apk update
    $SUDO apk add python3 py3-pip python3-dev gcc musl-dev postgresql-dev ipmitool mtr traceroute net-snmp-tools smartmontools lm-sensors ethtool nmap iproute2 openssl curl nodejs npm
}

# Execute Installation
case "$OS" in
    ubuntu|debian|proxmox|kali|raspbian)
        install_debian
        ;;
    centos|rhel|rocky|alma|fedora)
        install_redhat
        ;;
    alpine)
        install_alpine
        ;;
    *)
        echo "❌ $(t '不支持的操作系统' 'Unsupported OS'): $OS."
        exit 1
        ;;
esac

# 2. Verify Python & Pip
if ! command -v python3 > /dev/null; then
    echo "❌ $(t 'Python3 安装失败！' 'Python3 installation failed!')"
    exit 1
fi

# PIP Setup with Mirror Support
if ! command -v pip3 > /dev/null && ! python3 -m pip --version > /dev/null; then
    echo "⚠️ $(t '未找到 Pip。尝试从国内源安装 Pip...' 'Pip not found. Attempting to install pip from mirror...')"
    GET_PIP_URL="https://bootstrap.pypa.io/get-pip.py"
    if [ "$IS_CN" = true ]; then
        GET_PIP_URL="https://mirrors.aliyun.com/pypi/get-pip.py"
    fi
    curl -s "$GET_PIP_URL" -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# Configure PIP Mirror for CN users
if [ "$IS_CN" = true ]; then
    echo "⚡ $(t '正在配置 PIP 国内加速源 (中科大)...' 'Configuring PIP domestic mirror (USTC)...')"
    python3 -m pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
fi

# 3. Install Python Requirements
# Resolve root directory for requirements.txt
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
REPO_ROOT=$(dirname "$SCRIPT_DIR")

echo "🐍 $(t '正在从根目录安装 Python 依赖库...' 'Installing Python library requirements from root...')"
if [ -f "$REPO_ROOT/requirements.txt" ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r "$REPO_ROOT/requirements.txt"
else
    echo "⚠️ $(t '根目录下未找到 requirements.txt。' 'requirements.txt not found in root directory.')"
    # Fallback to current dir
    if [ -f "requirements.txt" ]; then
        python3 -m pip install -r "requirements.txt"
    fi
fi

# 3.5. Setup PostgreSQL Database
echo "🗄️ $(t '正在初始化 PostgreSQL 数据库...' 'Initializing PostgreSQL database...')"

# Detect PostgreSQL and create database/user
setup_postgres() {
    if command -v psql >/dev/null 2>&1; then
        # Try to create database and user
        $SUDO -u postgres psql -c "ALTER USER postgres PASSWORD 'boos';" 2>/dev/null || true
        $SUDO -u postgres psql -c "CREATE DATABASE netops;" 2>/dev/null || true
        
        # Create tables for RBAC
        $SUDO -u postgres psql -d netops -c "
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'operator',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        " 2>/dev/null || true
        
        # Create default admin user if not exists
        $SUDO -u postgres psql -d netops -c "
        INSERT INTO users (username, password, role) 
        SELECT 'admin', 'boos', 'root' 
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE username='admin');
        " 2>/dev/null || true
        
        echo "✅ $(t 'PostgreSQL 初始化完成' 'PostgreSQL initialized')"
    else
        echo "⚠️ $(t '未检测到 PostgreSQL，跳过数据库初始化' 'PostgreSQL not detected, skipping database setup')"
    fi
}

# Check if PostgreSQL is installed (client or server)
if command -v psql >/dev/null 2>&1 || command -v postgres >/dev/null 2>&1; then
    setup_postgres
else
    echo "⚠️ $(t 'PostgreSQL 未安装，如需用户管理功能请先安装 PostgreSQL' 'PostgreSQL not installed, install it first for user management')"
fi

# 4. Configure NPM mirror and install PM2
if ! command -v pm2 > /dev/null; then
    # Step 1: Configure npm mirror based on location (after npm is installed via system packages)
    if [ "$IS_CN" = true ]; then
        echo "📦 $(t '配置 NPM 镜像为国内源...' 'Configuring NPM mirror to China mirror...')"
        npm config set registry https://registry.npmmirror.com 2>/dev/null || true
    fi
    
    # Step 2: Install PM2
    echo "📦 $(t '正在安装 PM2...' 'Installing PM2...')"
    $SUDO npm install -g pm2
    
    # Setup PM2 to start on boot
    $SUDO pm2 startup 2>/dev/null || true
    pm2 save 2>/dev/null || true
fi

# 5. Optional: Start Dashboard
echo ""
# Get local IP address
get_local_ip() {
    local ip
    ip=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$ip" ]; then
        ip=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K\S+' || echo "127.0.0.1")
    fi
    echo "$ip"
}

echo "❓ $(t '是否启动 NetOps Dashboard (API与Web界面)? [Y/n]' 'Do you want to start the NetOps Dashboard (API & UI)? [Y/n]')"
read -r -p " > " START_DASHBOARD
if [[ "$START_DASHBOARD" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
    echo "🚀 $(t '正在通过 PM2 启动后台服务...' 'Starting backend services via PM2...')"
    pm2 delete netops-api netops-ui 2>/dev/null || true
    pm2 start python3 --name "netops-api" -- "$REPO_ROOT/scripts/api_server.py"
    pm2 start python3 --name "netops-ui" -- "$REPO_ROOT/ui/serve_ui.py"
    
    LOCAL_IP=$(get_local_ip)
    echo "✅ $(t "Dashboard 启动成功！访问地址: http://$LOCAL_IP:8082" "Dashboard started! Access at: http://$LOCAL_IP:8082")"
else
    echo "⏭️ $(t '跳过 Dashboard 启动。' 'Skipped Dashboard startup.')"
fi

echo "✅ $(t '环境安装完成！' 'Environment Setup Complete!')"
