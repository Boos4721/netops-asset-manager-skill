# NetOps Asset Manager Skill 🚀

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

Automated IT infrastructure inventory and maintenance skill for OpenClaw. This skill empowers your AI agent to manage network devices (H3C, Huawei, Cisco, MikroTik, Ruijie, DCN, TP-LINK, NETGEAR) and Linux systems through natural language.

### ✨ Key Features
- **Intelligent Parsing**: Automatically extract IP, Vendor, Model, and Location from unstructured text or tables.
- **Bilingual Reporting**: Support for automated daily reports and alerts in both English and Chinese (Supports Bark, DingTalk, Feishu).
- **Bulk Import**: Native support for **Excel (.xlsx)** and **CSV** asset lists for rapid onboarding.
- **Full-Stack Diagnostics**: Deep inspection capabilities across OSI layers, from **Physical (SFP/Cable)** to **Application (HTTP/API)**.
- **Enterprise Server OOB**: Full support for **DELL iDRAC**, **Inspur ISBMC**, and **Supermicro IPMI**.
- **Wireless, Security & Routing**: Support for **AC/AP**, **Firewalls** (Fortinet, Palo Alto, etc.), **Gateways** (including Ruijie EG), and core routing protocols.
- **Cloud Native & DevOps**: Streamlined maintenance for **Docker**, **Kubernetes (K8s)**, and **Nginx**.
- **Virtualization Support**: Advanced management for **VMware ESXi**, **OpenStack**, **QEMU/KVM**, and **LXC** (Proxmox compatible).
- **GPU Maintenance**: Support for **NVIDIA** and **AMD** driver installation (official CN/HK sources) and health monitoring.
- **Network Performance**: Integrated tools for **Speedtest**, **Route Tracing (MTR)**, and **Subnet Scanning (Nmap)**.
- **Safety First**: **Human-in-the-loop** confirmation required for all core network configuration changes.
- **On-Premise Deployment**: Secure management within internal networks via one-click environment setup.

### 🛠️ Structure
- `SKILL.md`: Core workflow definitions and agent instructions.
- `scripts/`: Python tools for inventory, health checks, GPU, OOB, DevOps, and Dashboards. Includes `setup_env.sh` for auto-initialization.
- `references/`: Vendor command libraries, dependency guides, and automation implementation guides.

### 🚀 Quick Start
1. **Internal Deployment**: Install OpenClaw on a host within your internal management network.
2. **Auto Setup**: Run the integrated setup script to install Python, Pip, and all dependencies automatically (supports location-based mirror acceleration):
   ```bash
   chmod +x scripts/setup_env.sh
   ./scripts/setup_env.sh
   ```
3. **Usage**: Tell your agent: *"Add a Huawei switch at 192.168.1.1 in the Data Center."*

### ⚖️ License
This project is licensed under the **CC BY-NC 4.0**. **Commercial use is strictly prohibited.**

---

<a name="chinese"></a>
## 中文

为 OpenClaw 打造的自动化 IT 基础设施资产管理与运维技能包。该技能赋予 AI Agent 通过自然语言管理内网网络设备（华三、华为、思科、锐捷、神州数码、TP-LINK、网件等）、Linux 系统及算力集群。

### ✨ 核心功能
- **智能解析**：自动从凌乱的文本或表格中提取 IP、厂商、型号和位置信息。
- **双语巡检与告警**：支持自动化巡检日报及告警信息的“中英双语”推送（支持 Bark、钉钉、飞书）。
- **批量导入**：原生支持 **Excel (.xlsx)** 与 **CSV** 资产清单批量入库。
- **全栈链路诊断**：具备覆盖 OSI 七层模型的深层巡检能力，从物理层（SFP/线缆）到应用层（HTTP/API）。
- **企业服务器带外 (OOB)**：深度支持 **DELL iDRAC**、**浪潮 ISBMC** 及 **超微 IPMI**。
- **无线、安全与路由**：支持 **AC/AP**、**防火墙**（飞塔、Palo Alto 等）、**网关**（含锐捷 EG 系列）及核心路由协议。
- **DevOps 与云原生**：集成 **Docker**、**Kubernetes** 及 **Nginx** 的自动化维护。
- **虚拟化管理**：支持 **VMware ESXi**、**OpenStack**、**QEMU/KVM** 及 **LXC** (Proxmox 兼容)。
- **显卡运维 (GPU)**：支持 **NVIDIA (N卡)** 与 **AMD (A卡)** 官网驱动静默安装及高温/显存监控。
- **网络性能监测**：集成 **Speedtest**、**MTR 路由追踪**及 **Nmap 网段发现**。
- **安全加固**：核心网络变更引入 **人工审查 (Human-in-the-loop)** 机制，确保安全。
- **内网部署**：支持一键环境初始化，确保管理流量不经过公网，安全可控。

### 🛠️ 目录结构
- `SKILL.md`: 核心流程定义与 Agent 执行指令。
- `scripts/`: Python 工具集（资产管理、硬件巡检、Web 看板等）及 `setup_env.sh` 环境初始化脚本。
- `references/`: 厂商命令库、系统依赖指南及自动化执行参考文档。

### 🚀 快速开始
1. **内网部署**：在您的内网接入一台 OpenClaw 主机。
2. **自动环境搭建**：运行内置脚本自动安装环境（支持根据 IP 归属地自动切换国内镜像源）：
   ```bash
   chmod +x scripts/setup_env.sh
   ./scripts/setup_env.sh
   ```
3. **开始使用**：对 Agent 说：*"记录一台华为交换机，IP 是 192.168.1.1，在 A 座机房。"*

### ⚖️ 开源协议
本项目采用 **CC BY-NC 4.0** 协议。**严禁用于任何商业用途。**
