#!/bin/bash

# NetOps Skill - Auto Environment Setup Script
# Supports: Debian/Ubuntu, RedHat/CentOS/Rocky, Alpine Linux

echo "🚀 Starting NetOps Environment Setup..."

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
fi

install_debian() {
    echo "📦 Detected Debian-based system. Updating apt..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv ipmitool mtr-tiny traceroute snmp smartmontools lm-sensors ethtool nmap iproute2 openssl curl
}

install_redhat() {
    echo "📦 Detected RedHat-based system. Updating dnf/yum..."
    if command -v dnf > /dev/null; then
        sudo dnf install -y python3 python3-pip ipmitool mtr traceroute net-snmp-utils smartmontools lm_sensors ethtool nmap iproute openssl curl
    else
        sudo yum install -y python3 python3-pip ipmitool mtr traceroute net-snmp-utils smartmontools lm_sensors ethtool nmap iproute openssl curl
    fi
}

install_alpine() {
    echo "📦 Detected Alpine Linux. Updating apk..."
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
        echo "❌ Unsupported OS: $OS. Please install python3, pip, and dependencies manually."
        exit 1
        ;;
esac

# 2. Verify Python & Pip
if ! command -v python3 > /dev/null; then
    echo "❌ Python3 installation failed!"
    exit 1
fi

if ! command -v pip3 > /dev/null && ! python3 -m pip --version > /dev/null; then
    echo "⚠️ Pip not found. Attempting to install pip for Python 3..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# 3. Install Python Requirements
echo "🐍 Installing Python library requirements..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found in current directory!"
fi

echo "✅ Environment Setup Complete!"
echo "Next step: Run 'python3 scripts/dashboard.py' to start the asset dashboard."
