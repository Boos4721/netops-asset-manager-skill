#!/bin/bash

# NetOps Skill - Auto Environment Setup Script
# Supports: Debian/Ubuntu, RedHat/CentOS/Rocky, Alpine Linux
# Bilingual Support: Detects system locale to display EN or ZH
# Network Smart: Detects IP location to use domestic mirrors (CN) for faster downloads

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
    echo "🇨🇳 $(t '检测到您位于中国大陆，将自动开启镜像加速。' 'Detected Mainland China location. Mirror acceleration enabled.')"
else
    echo "🌍 $(t '检测到非中国大陆区域，使用全球默认源。' 'Global location detected. Using default sources.')"
fi

echo "🚀 $(t '正在启动 NetOps 环境安装程序...' 'Starting NetOps Environment Setup...')"

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
fi

# OS-Specific Installers
install_debian() {
    echo "📦 $(t '正在更新系统源...' 'Updating system sources...')"
    if [ "$IS_CN" = true ]; then
        # Optional: Switch APT to TUNA mirror if needed, but keeping it safe for now
        echo "💡 $(t '建议手动切换 APT 到清华或阿里镜像源以获得最佳速度。' 'Suggested: Switch APT to TUNA or Alibaba mirrors for best speed.')"
    fi
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv ipmitool mtr-tiny traceroute snmp smartmontools lm-sensors ethtool nmap iproute2 openssl curl
}

install_redhat() {
    echo "📦 $(t '正在更新 YUM/DNF 源...' 'Updating YUM/DNF sources...')"
    if command -v dnf > /dev/null; then
        sudo dnf install -y python3 python3-pip ipmitool mtr traceroute net-snmp-utils smartmontools lm_sensors ethtool nmap iproute openssl curl
    else
        sudo yum install -y python3 python3-pip ipmitool mtr traceroute net-snmp-utils smartmontools lm_sensors ethtool nmap iproute openssl curl
    fi
}

install_alpine() {
    echo "📦 $(t '正在更新 APK 源...' 'Updating APK sources...')"
    if [ "$IS_CN" = true ]; then
        sudo sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
    fi
    sudo apk add python3 py3-pip ipmitool mtr traceroute net-snmp-tools smartmontools lm-sensors ethtool nmap iproute2 openssl curl
}

# 1. Install System Dependencies & Python/Pip
case "$OS" in
    ubuntu|debian|proxmox|kali)
        install_debian
        ;;
    centos|rhel|rocky|alma|fedora)
        install_redhat
        ;;
    alpine)
        install_alpine
        ;;
    *)
        echo "❌ $(t '不支持的操作系统' 'Unsupported OS'): $OS. $(t '请手动安装依赖。' 'Please install dependencies manually.')"
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
    echo "⚠️ $(t '未找到 Pip。尝试为 Python 3 安装 Pip...' 'Pip not found. Attempting to install pip for Python 3...')"
    GET_PIP_URL="https://bootstrap.pypa.io/get-pip.py"
    if [ "$IS_CN" = true ]; then
        GET_PIP_URL="https://mirrors.aliyun.com/pypi/get-pip.py"
    fi
    curl "$GET_PIP_URL" -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# Configure PIP Mirror for CN users
if [ "$IS_CN" = true ]; then
    echo "⚡ $(t '正在配置 PIP 国内加速源 (阿里云)...' 'Configuring PIP domestic mirror (Alibaba)...')"
    python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
fi

# 3. Install Python Requirements
echo "🐍 $(t '正在安装 Python 依赖库...' 'Installing Python library requirements...')"
if [ -f "requirements.txt" ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
else
    echo "⚠️ $(t '当前目录未找到 requirements.txt！' 'requirements.txt not found in current directory!')"
fi

echo "✅ $(t '环境安装完成！' 'Environment Setup Complete!')"
echo "$(t '下一步：运行 \"python3 scripts/dashboard.py\" 启动资产看板。' 'Next step: Run \"python3 scripts/dashboard.py\" to start the asset dashboard.')"
