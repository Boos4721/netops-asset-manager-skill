#!/bin/bash

# OpenClaw 国内一键安装脚本 (Optimized for CN Region)
# 支持 Ubuntu/Debian/CentOS/Alpine

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 开始安装 OpenClaw (国内加速版)...${NC}"

# 1. 检查基础依赖
echo -e "${YELLOW}正在检查基础依赖...${NC}"
if [ -f /etc/alpine-release ]; then
    apk add --no-cache nodejs npm git curl python3 py3-pip bash
elif [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y nodejs npm git curl python3 python3-pip bash
elif [ -f /etc/redhat-release ]; then
    yum install -y nodejs npm git curl python3 python3-pip bash
fi

# 2. 配置 NPM / Pip 国内镜像
echo -e "${YELLOW}配置国内镜像加速...${NC}"
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 安装 OpenClaw 核心
echo -e "${YELLOW}正在安装 OpenClaw 核心...${NC}"
npm install -g openclaw --unsafe-perm

# 4. 初始化工作目录
echo -e "${YELLOW}初始化工作目录 /root/clawd ...${NC}"
mkdir -p /root/clawd
cd /root/clawd

# 5. 自动配置建议
echo -e "${GREEN}✅ OpenClaw 基础环境安装完成！${NC}"
echo -e "接下来你可以运行: ${YELLOW}openclaw init${NC} 来初始化你的第一个 Agent。"
echo -e "或者使用: ${YELLOW}openclaw gateway start${NC} 启动后台服务。"
