# NetOps Dashboard 使用文档

本文档介绍 NetOps Asset Manager 项目中 **Web Dashboard** 的功能、架构与使用说明。该 Dashboard 为用户提供了一个现代化的、响应式的控制台，用于管理资产、下发任务、管理权限以及使用 AI 助手。

## 1. 架构概述

Dashboard 采用前后端分离的架构：
*   **前端 (UI)**：基于 **Vue 3**（组合式 API）构建的单页应用（SPA），使用 **Tailwind CSS** 进行样式设计，图标采用 **Lucide**，拓扑图使用 **Vis.js** 渲染。界面具有“毛玻璃”质感和流畅的动画过渡。
*   **后端 (API)**：基于 **FastAPI** 与 **Uvicorn** 构建的现代化异步 API (`scripts/api_server.py`)，负责处理前端请求并与系统底层交互。
*   **数据库**：使用 **PostgreSQL** (`netops` 数据库) 进行用户权限管理（RBAC）。
*   **进程管理**：集成 **PM2** 进行后台脚本/任务的管理与监控。

## 2. 功能模块指南

### 2.1 登录与鉴权
*   **入口**：访问 Dashboard 时，首先进入登录页面。
*   **默认账号**：提供默认的超级管理员账户（用户名：`admin`，密码：`boos`）。
*   **安全**：账号信息由底层的 PostgreSQL 数据库验证。

### 2.2 资产总览 (Dashboard)
*   **数据大屏**：页面顶部展示系统的实时核心指标（总资产数、在线设备数、PM2 进程数、数据库用户数），并带有响应式动态更新（Vue Ref）。
*   **实时探测逻辑**：资产状态不再仅依赖静态记录。每次加载资产列表时，后端会通过 `asyncio` 并行对所有 IP 进行实时 Ping 探测，确保“在线/离线”状态的绝对准确。
*   **资产列表 (支持 CRUD)**：
    *   **展示与检索**：以表格形式列出所有已录入的设备（来源于 `assets/inventory.json`），并支持在顶部搜索框根据关键字（IP、设备名、品牌）进行即时过滤。
    *   **增删改查**：提供“添加资产”按钮用于手工录入；每行操作列支持“编辑”与“删除”设备数据。
    *   **详情视图**：点击表格中的任意设备行，可唤出设备详情面板，直观展示该设备的机柜、U位、功耗、备注等深度台账信息。

### 2.3 物理拓扑 (Topology) - *Beta*
*   使用 Vis.js 引擎自动将录入的网络设备与服务器渲染成带有层级（核心、汇聚、接入）的动态拓扑关系图，使网络结构可视化。

### 2.4 PM2 进程管理
*   **状态监控**：实时从后端拉取并显示本机的 PM2 任务状态，包括任务名称、运行状态（Online/Stopped）、内存占用、CPU 使用率和重启次数。
*   **业务机前置条件**：批量部署任务到业务机时，业务机需要**预装 PM2**（通过包管理器安装，如 `apt install pm2` 或 `yum install pm2`），无需安装 Node.js。
*   **自定义部署**：
    *   点击“部署新任务”可唤出部署面板。
    *   支持填写：任务名称、本地二进制文件路径（如 `/usr/local/bin/script`）、运行参数。
    *   支持批量部署：可填写多个目标设备的 IP（逗号分隔），系统会自动通过 SSH 下发执行 `pm2 start` 的指令。

### 2.5 用户权限管理 (RBAC)
*   **管理后台**：通过调用 PostgreSQL，直观展示当前系统中的账号列表（ID、用户名、角色）。
*   **账号操作**：
    *   **创建账号**：可以新建用户，并分配角色（Root 管理员、Operator 运维、Viewer 只读）。
    *   **删除账号**：支持快速删除账号（内置保护，防止误删 `admin`）。

### 2.6 AI 智能助理 (在线 Session)
*   **形态**：已升级为左侧菜单中的全屏独立视图，提供沉浸式的自然语言对话体验。
*   **OpenClaw 深度集成**：底层通过代理连接至 **OpenClaw Gateway**，复用 OpenClaw 的强大推理与工具调用能力。
*   **Markdown 支持**：聊天界面原生支持 **Markdown 渲染**（基于 marked.js），能够美观地展示列表、代码块和加粗文本。
*   **自动化资产录入**：
    *   助理具备意图识别能力。例如，当你说：“录入一台 10.1.1.1 的 H3C 交换机”时，助理会返回结构化的指令标签。
    *   前端会自动解析 `ACTION: ADD_ASSET` 标签并静默执行录入操作，无需手动填写表单。
    *   对话过程中支持“清空历史”重置当前会话。

### 2.7 LLM 模型与 API 管理
*   **形态**：全新的独立管理面板，对标 OpenClaw 的 `models` 管理逻辑。
*   **同步机制**：模型列表**实时同步**自 OpenClaw 配置文件 (`~/.openclaw/openclaw.json`)。
*   **高级参数支持**：支持配置每个模型的 `contextWindow` (上下文窗口) 与 `maxTokens` (最大输出)，避免空值导致请求失败。
*   **设为默认模型**：支持一键将选定模型设为 OpenClaw 的 **Global Primary Model**，修改后 OpenClaw 的所有 Agent 将默认使用该模型。
*   **增删改功能**：在 Dashboard 中添加、编辑或删除模型配置，会**直接同步写回** OpenClaw 配置文件，修改立即生效。

## 3. 部署与启动

### 前置条件
1.  **PostgreSQL**：
    *   必须已安装并运行。
    *   初始化数据库（setup_env.sh 会自动执行）：
      ```bash
      sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'boos';"
      sudo -u postgres psql -c "CREATE DATABASE netops;"
      ```
    *   默认存在 `admin` 账号（密码：`boos`），首次登录后可在界面中管理用户。
2.  **Node.js / PM2**：通过包管理器安装（如 `apt install npm`，然后 `npm install -g pm2`），运行 `scripts/setup_env.sh` 时会自动检测并安装。
3.  **Python 依赖**：后端需安装 `psycopg2`, `fastapi`, `httpx`, `uvicorn` 等模块（由 `setup_env.sh` 自动安装）。

### 启动服务

**推荐方式（自动启动）：**
在运行 `scripts/setup_env.sh` 初始化环境的最后一步，脚本会询问您是否启动 Dashboard：
`❓ 是否启动 NetOps Dashboard (API与Web界面)? [Y/n]`
输入 `Y` 或直接回车，系统将通过 PM2 自动为您拉起前后端服务。

**手动启动方式：**
如果您跳过了自动启动，也可以进入项目根目录，手动通过 PM2 拉起这两个服务：

1.  **启动后端 API 服务** (默认端口 8081)：
    ```bash
    pm2 start python3 --name "netops-api" --interpreter python3 -- ./scripts/api_server.py
    ```
2.  **启动前端 Web 服务** (推荐使用内置 proxy，端口 8082)：
    ```bash
    pm2 start python3 --name "netops-ui" --interpreter python3 -- ./ui/serve_ui.py
    ```

> ℹ️ 启动完成后，终端会显示本机 IP 地址，直接访问 `http://<IP>:8082` 即可。

## 4. 常见问题排查

*   **页面白屏**：通常是由于 JS 变量冲突（已在 Commit `1b85d59` 修复）或 `v-cloak` 导致。请确保 `ui/index.html` 中的 Vue 挂载逻辑正确。
*   **无法加载数据**：检查 `serve_ui.py` 是否正常工作，且 8081 端口的 API 服务是否存活。
*   **AI 助手不回复**：检查 `openclaw gateway` 是否在运行，以及 `api_server.py` 是否能正确调用 `openclaw agent` 命令。
*   **资产显示离线**：系统会实时 Ping 目标 IP。如果设备确实在线但显示离线，请检查运行 `api_server.py` 的账号是否有执行 `ping` 命令的权限。