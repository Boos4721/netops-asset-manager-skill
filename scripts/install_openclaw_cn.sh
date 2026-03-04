#!/bin/bash

# OpenClaw 国内一键安装脚本 (CN Optimized)
# 基于官方 install.sh 适配，解决国内网络环境下安装缓慢、超时等问题。
# 支持系统: Ubuntu / Debian / CentOS / Alpine / macOS

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}${BOLD}🦞 OpenClaw 国内加速安装程序${NC}"
echo -e "${YELLOW}正在优化网络配置以加速安装...${NC}"

# 1. 基础依赖检查与安装
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

install_deps() {
    echo -e "${YELLOW}正在安装必要依赖...${NC}"
    case "$OS" in
        "macos")
            if ! command -v brew &> /dev/null; then
                echo -e "${RED}未检测到 Homebrew，请先安装 Homebrew: https://brew.sh${NC}"
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
        *)
            echo -e "${RED}不支持的系统类型，请手动安装 Node.js 22+ 和 Git。${NC}"
            exit 1
            ;;
    esac
}

# 2. 配置国内镜像源
setup_mirrors() {
    echo -e "${YELLOW}正在配置国内镜像源 (npmmirror & tsinghua)...${NC}"
    
    # 配置 npm 镜像 (阿里镜像)
    if command -v npm &> /dev/null; then
        npm config set registry https://registry.npmmirror.com
    fi
    
    # 配置 pip 镜像 (清华镜像)
    if command -v pip3 &> /dev/null; then
        pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    elif command -v pip &> /dev/null; then
        pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    fi
}

# 3. 安装 OpenClaw
install_openclaw() {
    echo -e "${YELLOW}正在通过 npm 安装 OpenClaw (来自 npmmirror)...${NC}"
    # 使用 --unsafe-perm 防止某些环境下的权限问题
    npm install -g openclaw --unsafe-perm
}

# 4. 初始化
init_openclaw() {
    echo -e "${GREEN}正在初始化工作目录...${NC}"
    mkdir -p /root/clawd
    cd /root/clawd
    
    # 检查是否已有配置，没有则提示 init
    if [ ! -f "openclaw.json" ]; then
        echo -e "${YELLOW}安装完成！请运行 'openclaw init' 开始配置你的第一个 Agent。${NC}"
    fi
}

# 执行安装流
install_deps
setup_mirrors
install_openclaw
init_openclaw

echo -e "\n${GREEN}${BOLD}✅ OpenClaw 安装成功！${NC}"
echo -e "------------------------------------------------"
echo -e "常用命令:"
echo -e "  ${BOLD}openclaw init${NC}         - 初始化配置"
echo -e "  ${BOLD}openclaw gateway start${NC} - 启动后台服务"
echo -e "  ${BOLD}openclaw status${NC}        - 查看运行状态"
echo -e "------------------------------------------------"
