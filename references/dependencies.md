# NetOps Asset Manager — System Dependencies

Runtime and build dependencies for the **Go + Vue 3** stack. No Python required.

---

## Required Components

| Component | Version | Purpose |
|---|---|---|
| **Go** | 1.26+ | Backend build & run |
| **Node.js** | 22+ | Frontend build (`make build`) |
| **PostgreSQL** | 15+ | Data storage |
| **nmap** | any | Subnet device discovery (`POST /api/discover`) |
| **PM2** | any | Process management feature |
| **openssh-client** | any | SSH operations (or use Go native SSH — built-in) |

---

## OS-Specific Installation

### macOS
```bash
brew install go node postgresql nmap
brew services start postgresql
```

### Debian / Ubuntu / Proxmox
```bash
# Go (official installer — apt version is usually outdated)
wget https://go.dev/dl/go1.26.1.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.26.1.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql

# Optional tools
sudo apt install -y nmap openssh-client
sudo npm install -g pm2
```

### RedHat / CentOS / Rocky / Alma
```bash
# Go (same official installer as above)

# Node.js 22
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo dnf install -y nodejs

# PostgreSQL
sudo dnf install -y postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql

# Optional tools
sudo dnf install -y nmap openssh
sudo npm install -g pm2
```

### Alpine Linux
```bash
apk add go nodejs npm postgresql postgresql-contrib nmap openssh
rc-service postgresql start
npm install -g pm2
```

---

## China Region Mirror Acceleration

```bash
# Go module proxy
go env -w GOPROXY=https://goproxy.cn,direct

# npm mirror
npm config set registry https://registry.npmmirror.com
```

---

## Database Setup

```bash
# Create database
sudo -u postgres psql -c "CREATE DATABASE netops;"

# Optional: set postgres user password
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'your_password';"
```

---

## PM2 Setup (Process Management Feature)

```bash
sudo npm install -g pm2

# Auto-start on boot
sudo pm2 startup
pm2 save
```

---

## OpenClaw (AI Assistant Feature)

Install via the provided script (CN-optimized):
```bash
bash install_openclaw_cn.sh
```

Or directly:
```bash
npm install -g openclaw
openclaw init
```

---

## Post-Installation Notes

1. **ICMP Ping permissions**: Health prober uses `ping -c 1`, which may require root or `cap_net_raw` on Linux. Run as root or: `sudo setcap cap_net_raw+ep $(which ping)`.
2. **Nmap permissions**: Subnet scan (`-sn`) typically requires root for ARP-based detection on local subnets.
3. **PostgreSQL authentication**: Default `config.yaml` assumes `trust` or `md5` auth for localhost. Adjust `pg_hba.conf` if needed.
4. **PM2 global install**: Use `sudo npm install -g pm2` or ensure `~/.npm-global/bin` is in PATH.
