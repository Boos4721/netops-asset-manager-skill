# NetOps 安装部署指南 (CN Region)

本文档提供 NetOps Asset Manager 的完整安装部署步骤，针对中国大陆网络环境进行优化。

---

## 系统要求

| 组件 | 版本要求 | 说明 |
|---|---|---|
| **Go** | 1.26+ | 运行/编译后端 |
| **Node.js** | 22+ | 构建前端（编译部署必需） |
| **PostgreSQL** | 15+ | 数据存储 |
| **nmap** | 可选 | 子网设备发现 |
| **PM2** | 可选 | 进程管理功能 |

---

## 方式一：源码直接运行（快速体验）

无需编译二进制，适合快速启动和开发调试。需要两个终端并行运行。

### 1. 安装依赖 & 初始化数据库

```bash
# macOS
brew install go node postgresql nmap
brew services start postgresql

# Ubuntu/Debian
sudo apt install -y golang nodejs postgresql postgresql-contrib nmap
sudo systemctl enable --now postgresql
```

**中国大陆加速：**
```bash
go env -w GOPROXY=https://goproxy.cn,direct
npm config set registry https://registry.npmmirror.com
```

### 2. 初始化数据库

```bash
sudo -u postgres psql -c "CREATE DATABASE netops;"
```

### 3. 配置

编辑 `config.yaml`：
```yaml
PORT: 8081
DATABASE_URL: "postgres://postgres:postgres@127.0.0.1:5432/netops?sslmode=disable"
JWT_SECRET: "your-strong-secret-key"
```

### 4. 安装前端依赖

```bash
cd frontend && npm install --legacy-peer-deps && cd ..
```

### 5. 启动（两个终端）

```bash
# 终端 1 — Go 后端（源码直接运行，端口 8081）
make run
# 或: go run ./backend/cmd/server

# 终端 2 — Vite 前端开发服务器（端口 5173，/api 自动代理到 8081）
make dev-frontend
# 或: cd frontend && npm run dev
```

访问 `http://localhost:5173`，默认账号：`admin / admin`

> **说明**：`make run` 模式下前端通过 Vite dev server 独立服务，与后端 API 通过代理联通。无需构建前端或编译二进制。

---

## 方式二：编译单二进制部署（生产推荐）

### 1. 安装依赖（同方式一）

### 2. 初始化数据库（同方式一）

### 3. 配置（同方式一）

### 4. 构建

```bash
# 安装前端依赖
cd frontend && npm install --legacy-peer-deps && cd ..

# 一键构建（前端 + 后端 → 单二进制）
make build
```

### 5. 运行

```bash
./netops
# → 访问 http://localhost:8081
# → 默认账号：admin / admin（首次启动自动创建）
```

### 6. 迁移旧数据（可选）

如果之前使用 `assets/inventory.json` 存储设备数据：
```bash
make migrate
```

---

## 方式三：开发模式（热重载）

适用于二次开发，后端代码改动自动重载：

```bash
# 安装 air 热重载工具（仅需一次）
make install-tools

# 终端 1 — Go 后端热重载（端口 8081）
make dev-backend

# 终端 2 — Vite 前端开发服务器（端口 5173）
make dev-frontend
```

---

## 方式四：Docker 部署

```bash
# 构建镜像
make docker-build

# 运行（镜像已内置 PostgreSQL 数据库，开箱即用）
docker run -d --name netops \
  -p 8081:8081 \
  -e JWT_SECRET="your-strong-secret" \
  netops-asset-manager:latest
```

---

## OpenClaw 安装（AI 助手功能）

项目根目录提供国内加速安装脚本：

```bash
bash install_openclaw_cn.sh
```

或直接使用 curl：
```bash
curl -fsSL https://cdn.jsdelivr.net/gh/Boos4721/netops-asset-manager-skill/install_openclaw_cn.sh | bash
```

---

## 常用 Make 命令

| 命令 | 说明 |
|---|---|
| `make run` | 源码直接运行后端（无需编译，配合 dev-frontend 使用） |
| `make build` | 构建前端 + 后端，输出 `./netops` 单二进制 |
| `make dev-frontend` | 启动 Vite 开发服务器（端口 5173） |
| `make dev-backend` | 启动 Go 后端（支持 air 热重载） |
| `make migrate` | 执行数据迁移（inventory.json → PostgreSQL） |
| `make generate` | 重新生成 Ent ORM 代码 |
| `make clean` | 清理构建产物 |
| `make docker-build` | 构建 Docker 镜像 |
| `make install-tools` | 安装 air 热重载工具 |

---

## 常见问题

### `go build` 下载超时
```bash
go env -w GOPROXY=https://goproxy.cn,direct
```

### `npm install` 下载超时
```bash
npm config set registry https://registry.npmmirror.com
```

### PostgreSQL 连接失败
1. 确认 PostgreSQL 服务正在运行：`systemctl status postgresql`
2. 确认 `config.yaml` 中的 `DATABASE_URL` 正确
3. 确认数据库 `netops` 已创建

### 端口被占用
```bash
PORT=9090 ./netops
# 或源码模式：
PORT=9090 go run ./backend/cmd/server
```

### `make run` 前端显示空白
确认 `make dev-frontend` 已在另一个终端运行，访问 `:5173` 而非 `:8081`。

---

## 开发者支持

由 **NetOps Asset Manager** 维护。如有问题请前往 [GitHub Issues](https://github.com/Boos4721/netops-asset-manager-skill/issues) 反馈。
