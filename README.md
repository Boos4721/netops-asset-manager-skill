# NetOps Asset Manager

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

High-performance IT infrastructure asset management platform built with **Go + Vue 3**. A single binary serves both API and frontend, designed for internal network operations teams managing routers, switches, servers, and GPU clusters.

### Key Features
- **Device Lifecycle**: Full CRUD for network devices with SSH credential management, vendor auto-detection, and bulk Excel/CSV import.
- **Real-time Health Probing**: Background goroutine performs ICMP ping + TCP:22 checks every 5 minutes across all assets.
- **Native SSH Operations**: Go-native SSH client for remote reboot and configuration backup (H3C, Huawei, Cisco, MikroTik, Linux).
- **AI Assistant**: Integrated OpenClaw-powered chat with Markdown rendering and intent-based asset auto-registration.
- **LLM Model Management**: Full CRUD for OpenClaw AI model configurations, synced to `~/.openclaw/openclaw.json`.
- **Network Topology**: Interactive vis-network graph visualization of device connections.
- **PM2 Process Management**: Monitor, restart, stop, and deploy PM2 tasks across machines.
- **Role-Based Access**: JWT authentication with three roles — `root`, `operator`, `viewer`.
- **Theme Support**: Dark / Light / Auto (time-based) theme switching with glass morphism UI.
- **Single Binary Deployment**: Frontend embedded via Go `embed.FS` — one binary, no nginx required.

### Tech Stack
| Layer | Technology |
|---|---|
| Backend | Go 1.26 + Gin + Ent ORM |
| Frontend | Vue 3.4 + Vite 5 + TailwindCSS + Pinia |
| Database | PostgreSQL 15+ |
| SSH | golang.org/x/crypto/ssh (native) |
| Auth | JWT (golang-jwt/v5) + bcrypt |

### Project Structure
```
netops-asset-manager-skill/
├── backend/                  # Go backend
│   ├── cmd/
│   │   ├── server/main.go    # Entry point: config, DB, router, health prober
│   │   └── migrate/main.go   # One-shot: inventory.json → PostgreSQL
│   ├── config/config.go      # Viper config loader
│   ├── ent/schema/           # Ent ORM schemas (device, user, backup, topology_link)
│   └── internal/
│       ├── auth/             # JWT, bcrypt, middleware
│       ├── handler/          # 13 Gin handlers (inventory, auth, topology, models, chat, etc.)
│       ├── router/           # Route registration + middleware chain
│       ├── service/          # Health prober, SSH client, Excel importer
│       └── embedded/         # embed.FS for frontend dist/
├── frontend/                 # Vue 3 SPA
│   ├── src/
│   │   ├── api/client.ts     # Axios + JWT interceptor
│   │   ├── stores/           # Pinia: auth, inventory, stats, theme
│   │   ├── components/       # Layout (Sidebar, Header) + UI (Modal, StatusBadge)
│   │   └── views/            # 8 views: Dashboard, Inventory, Topology, Jobs, etc.
│   └── vite.config.ts
├── config.yaml               # Default configuration
├── Makefile                  # build / dev / migrate / generate
├── Dockerfile                # Multi-stage (node → go → alpine)
└── go.mod
```

### Quick Start

```bash
# Prerequisites: Go 1.26+, Node.js 22+, PostgreSQL 15+

# 1. Create database
createdb netops

# 2. Configure
cp config.yaml config.local.yaml
# Edit DATABASE_URL and JWT_SECRET

# 3. Build & run
make build
./netops
# → http://localhost:8081  (default: admin / admin)

# Development mode (two terminals)
make dev-backend    # Go server on :8081
make dev-frontend   # Vite dev server on :5173 (proxies /api → :8081)
```

### License
This project is licensed under **CC BY-NC 4.0**. Commercial use is prohibited.

---

<a name="chinese"></a>
## 中文

基于 **Go + Vue 3** 构建的高性能 IT 基础设施资产管理平台。单二进制部署，内嵌前端，专为内网运维团队设计，管理路由器、交换机、服务器及 GPU 集群。

### 核心功能
- **设备全生命周期**：设备增删改查，SSH 凭据管理，厂商自动识别，Excel/CSV 批量导入。
- **实时健康探测**：后台 goroutine 每 5 分钟对所有资产执行 ICMP ping + TCP:22 检测。
- **原生 SSH 操作**：Go 原生 SSH 客户端，支持远程重启和配置备份（华三、华为、思科、锐捷、MikroTik、Linux）。
- **AI 智能助手**：集成 OpenClaw 驱动的对话式 AI，支持 Markdown 渲染和自然语言资产录入。
- **LLM 模型管理**：OpenClaw 模型配置的增删改查，直接同步 `~/.openclaw/openclaw.json`。
- **网络拓扑**：基于 vis-network 的交互式拓扑图可视化。
- **PM2 进程管理**：监控、重启、停止、跨机器部署 PM2 任务。
- **RBAC 权限控制**：JWT 认证，三级角色 — `root`、`operator`、`viewer`。
- **主题切换**：深色 / 浅色 / 自动（按时间），玻璃拟态 UI 设计。
- **单二进制部署**：前端通过 Go `embed.FS` 内嵌，一个文件即可运行，无需 nginx。

### 技术栈
| 层级 | 技术 |
|---|---|
| 后端 | Go 1.26 + Gin + Ent ORM |
| 前端 | Vue 3.4 + Vite 5 + TailwindCSS + Pinia |
| 数据库 | PostgreSQL 15+ |
| SSH | golang.org/x/crypto/ssh（原生） |
| 认证 | JWT (golang-jwt/v5) + bcrypt |

### 快速开始

```bash
# 前置条件：Go 1.26+、Node.js 22+、PostgreSQL 15+

# 1. 创建数据库
createdb netops

# 2. 配置
cp config.yaml config.local.yaml
# 编辑 DATABASE_URL 和 JWT_SECRET

# 3. 构建并运行
make build
./netops
# → http://localhost:8081（默认账号：admin / admin）

# 开发模式（两个终端）
make dev-backend    # Go 服务 :8081
make dev-frontend   # Vite 开发服务器 :5173（自动代理 /api → :8081）
```

### 开源协议
本项目采用 **CC BY-NC 4.0** 协议。**严禁商用。**
