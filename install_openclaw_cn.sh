#!/bin/bash
# OpenClaw CN Optimized Installer (Official adaptation)
# Usage: curl -fsSL https://cdn.jsdelivr.net/gh/Boos4721/netops-asset-manager-skill/scripts/install_openclaw_cn.sh | bash

set -euo pipefail

# Colors
BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}${BOLD}🦞 OpenClaw 国内加速安装程序${NC}"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [ -f /etc/alpine-release ]; then
        echo "alpine"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/redhat-release ]; then
        echo "redhat"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Install Dependencies
install_deps() {
    echo -e "${YELLOW}正在安装必要依赖...${NC}"
    case "$OS" in
        "macos")
            if ! command -v brew &> /dev/null; then
                echo -e "${RED}未检测到 Homebrew，请先安装: https://brew.sh${NC}"
                exit 1
            fi
            brew install node@22 git curl
            brew link node@22 --overwrite --force
            ;;
        "alpine")
            apk add --no-cache nodejs npm git curl python3 build-base bash
            ;;
        "debian")
            apt-get update
            apt-get install -y nodejs npm git curl python3 python3-pip build-essential bash
            ;;
        "redhat")
            yum install -y nodejs npm git curl python3 python3-pip gcc-c++ make bash
            ;;
    esac
}

# Setup CN Mirrors
setup_mirrors() {
    echo -e "${YELLOW}正在配置国内镜像源...${NC}"
    npm config set registry https://registry.npmmirror.com
    # Silence pip if it's not present
    if command -v pip3 &> /dev/null; then
        pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    elif command -v pip &> /dev/null; then
        pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    fi
}

# Install OpenClaw
install_openclaw() {
    echo -e "${YELLOW}正在安装 OpenClaw...${NC}"
    # Check if npm version is 7 or higher to avoid --unsafe-perm warning
    NPM_MAJOR=$(npm -v | cut -d. -f1)
    if [ "$NPM_MAJOR" -ge 7 ]; then
        npm install -g openclaw
    else
        npm install -g openclaw --unsafe-perm
    fi
}

# Main
install_deps
setup_mirrors
install_openclaw

echo -e "\n${GREEN}${BOLD}✅ OpenClaw 安装成功！${NC}"
echo -e "请运行 ${BOLD}openclaw init${NC} 开始配置。"
