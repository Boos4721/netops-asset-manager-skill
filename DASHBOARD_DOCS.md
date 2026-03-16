# NetOps Dashboard 使用文档

本文档介绍 NetOps Asset Manager 的 **Web Dashboard** 功能、架构与使用说明。

## 1. 架构概述

Dashboard 采用前后端一体化的单二进制架构：

| 组件 | 技术 | 说明 |
|---|---|---|
| **后端** | Go 1.26 + Gin + Ent ORM | RESTful API，JWT 认证，后台健康探测 |
| **前端** | Vue 3.4 + Vite 5 + TailwindCSS | SPA，通过 Go `embed.FS` 内嵌到二进制 |
| **数据库** | PostgreSQL 15+ | 全量数据存储（设备、用户、备份、拓扑） |
| **SSH** | golang.org/x/crypto/ssh | Go 原生 SSH，替代 sshpass/Netmiko |

### 目录结构
```
backend/                      # Go 后端
├── cmd/server/main.go        # 入口：加载配置、连接DB、启动路由和健康探测
├── config/config.go          # Viper 配置加载
├── ent/schema/               # 数据库模型（device, user, backup, topology_link）
└── internal/
    ├── auth/                 # JWT 生成/验证、bcrypt、中间件
    ├── handler/              # 13 个 API Handler
    ├── router/router.go      # 路由注册 + 中间件链
    ├── service/              # 健康探测、SSH、Excel 导入
    └── embedded/             # embed.FS（内嵌前端 dist/）

frontend/                     # Vue 3 前端
├── src/
│   ├── api/client.ts         # Axios 实例（JWT 拦截器 + 401 自动登出）
│   ├── stores/               # Pinia 状态管理（auth, inventory, stats, theme）
│   ├── components/           # 布局组件（Sidebar, Header）+ UI 组件（Modal, StatusBadge）
│   └── views/                # 8 个视图页面
└── vite.config.ts            # Vite 配置（开发代理 + 构建输出）
```

## 2. 功能模块

### 2.1 登录与鉴权
- **JWT 认证**：登录后返回 JWT Token，所有 API 请求通过 `Authorization: Bearer` 头传递。
- **默认账号**：首次启动自动创建超级管理员 `admin`（密码：`admin`）。
- **角色体系**：`root`（全部权限） > `operator`（设备操作） > `viewer`（只读）。
- **401 自动处理**：Token 过期后前端自动跳转登录页。

### 2.2 控制台 (Dashboard)
- **实时统计卡片**：资产总数、在线设备、离线设备、GPU 节点数。
- **最近资产列表**：展示最近录入的 8 台设备及其状态。
- **数据来源**：后端 `/api/stats` + `/api/inventory` API。

### 2.3 资产清单 (Inventory)
- **搜索过滤**：按 IP、名称、厂商、位置实时搜索。
- **增删改查**：添加、编辑、删除设备，支持 SSH 凭据管理。
- **批量导入**：上传 Excel (.xlsx) 文件批量导入设备（支持中英文表头）。
- **远程操作**：
  - **SSH 重启**：Go 原生 SSH 发送 reboot 命令。
  - **配置备份**：按厂商自动发送对应命令（`display current-configuration` / `show running-config` 等），备份存入数据库。
- **设备详情**：点击查看设备全部字段信息。

### 2.4 网络拓扑 (Topology)
- **可视化引擎**：基于 vis-network 渲染交互式网络拓扑图。
- **连接管理**：添加/删除设备间连接，支持标签标注。
- **状态着色**：在线设备节点高亮显示为绿色。

### 2.5 任务管理 (Jobs / PM2)
- **状态监控**：实时展示 PM2 进程名称、状态、重启次数、CPU/内存占用。
- **操作控制**：重启、停止、删除进程。
- **日志查看**：查看进程运行日志。
- **远程部署**：批量部署二进制到目标设备。

### 2.6 系统部署 (Deploy)
- **一键部署**：支持 Docker Engine、vLLM、llama.cpp 的后台安装。
- **异步执行**：部署任务通过 PM2 在后台运行，可在任务管理页查看进度。

### 2.7 模型管理 (Models)
- **模型 CRUD**：添加、编辑、删除 AI 模型配置。
- **OpenClaw 同步**：直接读写 `~/.openclaw/openclaw.json`。
- **设为默认**：一键设置默认推理模型。
- **参数配置**：Context Window、Max Tokens、推理模式等。

### 2.8 AI 助手 (Chat)
- **对话界面**：全屏对话视图，支持历史消息上下文。
- **Markdown 渲染**：AI 回复支持代码块、列表、加粗等 Markdown 格式。
- **OpenClaw 集成**：底层通过 `openclaw agent` CLI 代理。
- **资产自动录入**：AI 识别录入意图后返回 `ACTION: ADD_ASSET` 标签。

### 2.9 系统设置 (Settings)
- **系统信息**：显示 OpenClaw 版本、内核信息、认证状态。
- **外观主题**：深色 / 浅色 / 自动（按时间切换）。
- **用户管理**（root 专属）：创建/删除用户，分配角色。

## 3. 部署与启动

### 前置条件
- **Go 1.26+**：编译后端。
- **Node.js 22+**：构建前端。
- **PostgreSQL 15+**：数据存储。

### 构建与运行

```bash
# 创建数据库
createdb netops

# 方式 A：源码直接运行（无需编译，适合快速启动）
cd frontend && npm install --legacy-peer-deps && cd ..
make run           # 终端 1：Go 后端 :8081
make dev-frontend  # 终端 2：Vite :5173 → 访问 http://localhost:5173

# 方式 B：构建单二进制（生产部署）
make build
./netops
# → http://localhost:8081
# → 默认账号：admin / admin
```

### 开发模式

```bash
# 安装热重载工具（仅需一次）
make install-tools

# 终端 1：后端热重载（端口 8081）
make dev-backend

# 终端 2：前端（端口 5173，自动代理 /api → 8081）
make dev-frontend

# 也可直接源码运行（不需要 air）
make run
```

### Docker 部署

```bash
# 构建镜像
make docker-build

# 运行
docker run -p 8081:8081 \
  -e DATABASE_URL="postgres://user:pass@host:5432/netops?sslmode=disable" \
  -e JWT_SECRET="your-secret" \
  netops-asset-manager:latest
```

### 数据迁移（从旧版）

```bash
# 将 assets/inventory.json 导入 PostgreSQL
make migrate
```

## 4. 配置说明

配置文件 `config.yaml`，所有选项支持环境变量覆盖：

| 键 | 默认值 | 说明 |
|---|---|---|
| `PORT` | 8081 | 监听端口 |
| `DATABASE_URL` | postgres://postgres:postgres@127.0.0.1:5432/netops?sslmode=disable | PostgreSQL 连接串 |
| `JWT_SECRET` | netops-change-me-in-production | JWT 签名密钥 |
| `JWT_EXPIRY` | 24h | Token 有效期 |
| `PROBE_INTERVAL` | 5m | 健康探测间隔 |
| `OPENCLAW_CONFIG_PATH` | ~/.openclaw/openclaw.json | OpenClaw 配置路径 |
| `SSH_CONNECT_TIMEOUT` | 10s | SSH 连接超时 |

## 5. API 路由一览

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/users/login` | 公开 | 登录，返回 JWT |
| GET | `/api/inventory` | 认证 | 设备列表 |
| POST | `/api/inventory/add` | operator+ | 添加设备 |
| PUT | `/api/inventory/:ip` | operator+ | 编辑设备 |
| DELETE | `/api/inventory/:ip` | operator+ | 删除设备 |
| POST | `/api/inventory/reboot/:ip` | operator+ | SSH 远程重启 |
| POST | `/api/inventory/backup/:ip` | operator+ | SSH 配置备份 |
| POST | `/api/inventory/import` | operator+ | Excel 批量导入 |
| GET | `/api/stats` | 认证 | 统计数据 |
| GET/POST/DELETE | `/api/users` | root | 用户管理 |
| POST | `/api/discover` | operator+ | Nmap 子网扫描 |
| GET/POST/DELETE | `/api/topology/links` | 认证/operator+ | 拓扑连接管理 |
| GET/POST/PUT/DELETE | `/api/models` | 认证/root | AI 模型管理 |
| GET | `/api/pm2/status` | 认证 | PM2 状态 |
| POST | `/api/chat` | 认证 | AI 对话 |
| GET | `/api/system/info` | 认证 | 系统信息 |

## 6. 常见问题

- **页面白屏**：确认 `make build` 已执行前端构建（`frontend/` → `backend/internal/embedded/dist/`）。
- **无法连接数据库**：检查 `config.yaml` 中的 `DATABASE_URL` 和 PostgreSQL 服务状态。
- **AI 助手不回复**：确认 `openclaw gateway` 正在运行。
- **设备显示离线**：健康探测依赖 ICMP ping 权限，确保运行用户有 ping 权限。
- **SSH 操作失败**：检查设备的 SSH 凭据是否已配置（资产编辑页）。
