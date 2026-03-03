# NetOps Dashboard 使用文档

本文档介绍 NetOps Asset Manager 项目中 **Web Dashboard** 的功能、架构与使用说明。该 Dashboard 为用户提供了一个现代化的、响应式的控制台，用于管理资产、下发任务、管理权限以及使用 AI 助手。

## 1. 架构概述

Dashboard 采用前后端分离的架构：
*   **前端 (UI)**：基于 **Vue 3**（组合式 API）构建的单页应用（SPA），使用 **Tailwind CSS** 进行样式设计，图标采用 **Lucide**，拓扑图使用 **Vis.js** 渲染。界面具有“毛玻璃”质感和流畅的动画过渡。
*   **后端 (API)**：使用 Python 编写的轻量级 HTTP API (`scripts/api_server.py`)，负责处理前端请求并与系统底层交互。
*   **数据库**：使用 **PostgreSQL** (`netops` 数据库) 进行用户权限管理（RBAC）。
*   **进程管理**：集成 **PM2** 进行后台脚本/任务的管理与监控。

## 2. 功能模块指南

### 2.1 登录与鉴权
*   **入口**：访问 Dashboard 时，首先进入登录页面。
*   **默认账号**：提供默认的超级管理员账户（用户名：`admin`，密码：`boos`）。
*   **安全**：账号信息由底层的 PostgreSQL 数据库验证。

### 2.2 资产总览 (Dashboard)
*   **数据大屏**：页面顶部展示系统的实时核心指标（总资产数、在线设备数、PM2 进程数、数据库用户数），并带有响应式动态更新（Vue Ref）。
*   **资产列表**：以表格形式列出所有已录入的设备（来源于 `assets/inventory.json`），显示设备名称、IP、品牌及当前在线状态。

### 2.3 物理拓扑 (Topology) - *Beta*
*   使用 Vis.js 引擎自动将录入的网络设备与服务器渲染成带有层级（核心、汇聚、接入）的动态拓扑关系图，使网络结构可视化。

### 2.4 PM2 进程管理
*   **状态监控**：实时从后端拉取并显示本机的 PM2 任务状态，包括任务名称、运行状态（Online/Stopped）、内存占用、CPU 使用率和重启次数。
*   **自定义部署**：
    *   点击“部署新任务”可唤出部署面板。
    *   支持填写：任务名称、本地二进制文件路径（如 `/usr/local/bin/script`）、运行参数。
    *   支持批量部署：可填写多个目标设备的 IP（逗号分隔），系统会自动通过 SSH 下发执行 `pm2 start` 的指令。

### 2.5 用户权限管理 (RBAC)
*   **管理后台**：通过调用 PostgreSQL，直观展示当前系统中的账号列表（ID、用户名、角色）。
*   **账号操作**：
    *   **创建账号**：可以新建用户，并分配角色（Root 管理员、Operator 运维、Viewer 只读）。
    *   **删除账号**：支持快速删除账号（内置保护，防止误删 `admin`）。

### 2.6 AI 智能助理对话框
*   **形态**：集成在页面右侧的悬浮对话框，支持与用户的 OpenClaw Agent 进行交互。
*   **智能缩放**：页面向下滚动时，对话框会自动最小化为右下角的“圆形浮窗”（带展开提示）；点击后可恢复为全尺寸面板。
*   **快捷录入**：
    *   用户可以直接在对话框中输入自然语言，例如：“录入一台 10.1.1.1 的 H3C 交换机”。
    *   前端会进行正则预解析，并通过 `/api/inventory/add` 接口将解析出的 IP、品牌等信息直接写入后端的资产清单。

## 3. 部署与启动

### 前置条件
1.  **PostgreSQL**：必须已安装并运行，包含数据库 `netops` 及表 `users`，默认存在 `admin` 账号。
2.  **PM2**：必须已通过 npm 全局安装（`npm install -g pm2`）。
3.  **Python 依赖**：后端需安装 `psycopg2` 等模块。

### 启动服务
启动 Dashboard 需要同时拉起两个服务：

1.  **启动后端 API 服务** (默认端口 8081)：
    ```bash
    nohup python3 /root/clawd/skills/netops-asset-manager/scripts/api_server.py > /dev/null 2>&1 &
    ```
2.  **启动前端 Web 服务** (例如指定端口 18793)：
    ```bash
    cd /root/clawd/skills/netops-asset-manager/ui
    nohup python3 -m http.server 18793 > /dev/null 2>&1 &
    ```

访问地址通常为：`http://<服务器IP>:18793/index.html`。

## 4. 常见问题排查

*   **页面白屏或显示 404**：检查启动 `http.server` 时的执行路径是否为 `ui/` 目录。
*   **登录无反应/报错**：检查后端 API（8081端口）是否正常运行；检查 `api_server.py` 内配置的 PostgreSQL 用户名密码是否与实际匹配。
*   **AI 助手无法添加设备**：确保服务器有写入 `assets/inventory.json` 的权限。前端与后端的跨域请求已通过动态获取 `window.location.hostname` 解决。