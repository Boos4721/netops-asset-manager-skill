# NetOps 安装部署指南 (CN Region)

本文档提供 NetOps Asset Manager 的完整安装部署步骤，针对中国大陆网络环境进行优化。

---

## 系统要求

| 组件 | 版本要求 | 说明 |
|---|---|---|
| **Go** | 1.26+ | 编译后端 |
| **Node.js** | 22+ | 构建前端 |
| **PostgreSQL** | 15+ | 数据存储 |
| **nmap** | 可选 | 子网设备发现 |
| **PM2** | 可选 | 进程管理功能 |

---

## 方式一：源码编译部署（推荐）

### 1. 安装依赖

**macOS:**
```bash
brew install go node postgresql nmap
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
# Go (官方安装)
wget https://go.dev/dl/go1.26.1.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.26.1.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql

# 工具
sudo apt install -y nmap
sudo npm install -g pm2
```

**中国大陆加速配置：**
```bash
# Go 代理
go env -w GOPROXY=https://goproxy.cn,direct

# NPM 镜像
npm config set registry https://registry.npmmirror.com
```

### 2. 初始化数据库

```bash
sudo -u postgres psql -c "CREATE DATABASE netops;"
# 如需自定义密码：
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'your_password';"
```

### 3. 配置

```bash
cd netops-asset-manager-skill
cp config.yaml config.local.yaml
```

编辑 `config.yaml`：
```yaml
PORT: 8081
DATABASE_URL: "postgres://postgres:your_password@127.0.0.1:5432/netops?sslmode=disable"
JWT_SECRET: "your-strong-secret-key"
JWT_EXPIRY: "24h"
PROBE_INTERVAL: "5m"
```

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

## 方式二：Docker 部署

```bash
# 构建镜像
make docker-build

# 运行（指定数据库和密钥）
docker run -d --name netops \
  -p 8081:8081 \
  -e DATABASE_URL="postgres://postgres:password@host.docker.internal:5432/netops?sslmode=disable" \
  -e JWT_SECRET="your-strong-secret" \
  netops-asset-manager:latest
```

---

## 方式三：开发模式

适用于二次开发和调试：

```bash
# 终端 1 — Go 后端热重载（端口 8081）
make dev-backend

# 终端 2 — Vite 前端开发服务器（端口 5173，/api 自动代理到 8081）
make dev-frontend
```

---

## 常用 Make 命令

| 命令 | 说明 |
|---|---|
| `make build` | 构建前端 + 后端，输出 `./netops` 单二进制 |
| `make dev-frontend` | 启动 Vite 开发服务器 |
| `make dev-backend` | 启动 Go 后端（支持 air 热重载） |
| `make migrate` | 执行数据迁移（inventory.json → PostgreSQL） |
| `make generate` | 重新生成 Ent ORM 代码 |
| `make clean` | 清理构建产物 |
| `make docker-build` | 构建 Docker 镜像 |

---

## 常见问题

### `go build` 下载超时
配置 Go 代理：
```bash
go env -w GOPROXY=https://goproxy.cn,direct
```

### `npm install` 下载超时
配置 NPM 镜像：
```bash
npm config set registry https://registry.npmmirror.com
```

### PostgreSQL 连接失败
1. 确认 PostgreSQL 服务正在运行：`systemctl status postgresql`
2. 确认 `config.yaml` 中的 `DATABASE_URL` 正确
3. 确认数据库 `netops` 已创建

### 端口被占用
修改 `config.yaml` 中的 `PORT` 或通过环境变量覆盖：
```bash
PORT=9090 ./netops
```

---

## 开发者支持

由 **NetOps Asset Manager** 维护。如有问题请前往 [GitHub Issues](https://github.com/Boos4721/netops-asset-manager-skill/issues) 反馈。
