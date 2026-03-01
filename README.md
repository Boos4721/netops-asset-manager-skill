# NetOps Asset Manager Skill 🚀

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

Automated IT infrastructure inventory and maintenance skill for OpenClaw. This skill empowers your AI agent to manage network devices (H3C, Huawei, Cisco, MikroTik, Ruijie, DCN, TP-LINK, NETGEAR) and Linux systems through natural language.

### ✨ Key Features
- **Intelligent Parsing**: Automatically extract IP, Vendor, Model, and Location from unstructured text or tables.
- **Bulk Import**: Native support for **Excel (.xlsx)** and **CSV** asset lists for rapid onboarding.
- **Enterprise Server OOB**: Full support for **DELL iDRAC**, **Inspur ISBMC**, and **Supermicro IPMI**.
- **DevOps Capabilities**: Streamlined maintenance for **Docker**, **Kubernetes (K8s)**, and **Nginx**.
- **Virtualization Support**: Advanced management for **VMware ESXi**, **OpenStack**, **QEMU/KVM**, and **LXC** (Proxmox compatible).
- **Storage Maintenance**: Management of **RAID (mdadm)**, **iSCSI**, **NFS/SMB** mounts, and common filesystems.
- **GPU Maintenance**: Support for **NVIDIA (N-Card)** and **AMD (A-Card)** driver installation and health monitoring.
- **Multi-Vendor Support**: Pre-defined command patterns for H3C, Huawei, Cisco, MikroTik, Ruijie, DCN, TP-LINK, and NETGEAR.
- **External Integration**: Import assets directly from **NetBox** via API.
- **Multi-Channel Notifications**: Integrated support for **Bark (iOS)**, **DingTalk**, and **Feishu** webhooks.
- **Web Dashboard**: Light-weight built-in web interface to visualize device inventory and status.
- **Safety First**: **Human-in-the-loop** confirmation required for all core network configuration changes.
- **On-Premise Deployment**: Secure management within internal networks.
- **Audit Logging**: Tracks all infrastructure changes for security and compliance.

### 🛠️ Structure
- `SKILL.md`: Core workflow definitions and agent instructions.
- `scripts/`: Python tools for inventory, health checks, GPU, OOB, DevOps, and Dashboards.
- `references/`: Vendor command libraries and automation implementation guides.

### 🚀 Quick Start
1. **Internal Deployment**: Install OpenClaw on a host within your internal management network.
2. **Install Skill**: Clone this repository into your OpenClaw skills directory.
3. **Safety First**: All core configuration changes require **Human-in-the-loop** confirmation.
4. **Usage**: Tell your agent: *"Add a Huawei switch at 192.168.1.1 in the Data Center."*

### ⚖️ License
This project is licensed under the **CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)**.  
**Commercial use is strictly prohibited.**

---

<a name="chinese"></a>
## 中文

为 OpenClaw 打造的自动化 IT 基础设施资产管理与运维技能包。该技能赋予 AI Agent 通过自然语言管理内网网络设备（华三、华为、思科、锐捷、神州数码、TP-LINK、网件等）及 Linux 系统。

### ✨ 核心功能
- **智能解析**：自动从凌乱的文本或表格中提取 IP、厂商、型号和位置信息。
- **批量导入**：原生支持 **Excel (.xlsx)** 与 **CSV** 资产清单，实现快速入库。
- **企业服务器带外管理 (OOB)**：深度支持 **DELL iDRAC**、**浪潮 ISBMC** 及 **超微 IPMI**。
- **DevOps 运维**：集成 **Docker**、**Kubernetes** 及 **Nginx** 的自动化维护能力。
- **虚拟化管理**：深度支持 **VMware ESXi**、**OpenStack**、**QEMU/KVM** 及 **LXC** (兼容 Proxmox) 的虚机状态监控与基础维护。
- **存储维护**：支持 **RAID (mdadm)**、**iSCSI** 挂载、**NFS/SMB** 共享及常见文件系统的健康检查与维护。
- **显卡维护 (GPU)**：支持 **NVIDIA (N卡)** 与 **AMD (A卡)** 的驱动安装、定期更新及状态监控。
- **多厂商兼容**：内置华三、华为、思科、锐捷、神州数码、TP-LINK、网件等主流厂商命令库。
- **外部集成**：支持通过 API 直接从 **NetBox** 导入设备资产。
- **多渠道告警**：集成 **Bark (iOS)**、**钉钉**及**飞书**机器人 Webhook，支持自动推送巡检报告。
- **Web 可视化**：内置轻量级看板，可直观查看设备清单、厂商分布及资产状态。
- **安全加固**：核心网络变更引入 **人工审查 (Human-in-the-loop)** 机制，必须经用户确认后方可执行。
- **内网部署**：支持在内网单主机部署，管理流量不经过公网，安全可控。
- **审计日志**：记录所有基础设施变更操作，确保运维过程可追溯。

### 🛠️ 目录结构
- `SKILL.md`: 核心流程定义与 Agent 执行指令。
- `scripts/`: 用于资产管理、硬件巡检、GPU、带外、DevOps 及 Web 看板的 Python 工具集。
- `references/`: 厂商命令库与自动化执行参考文档。

### ⚖️ 开源协议
本项目采用 **CC BY-NC 4.0 (知识共享署名-非商业性使用 4.0 国际许可协议)**。  
**严禁用于任何商业用途。**

### 🚀 快速开始
1. **内网部署**：在您的内网（管理网段）接入一台 OpenClaw 主机。
2. **安装技能**：将此仓库克隆至 OpenClaw 的技能目录。
3. **安全确认**：针对所有核心配置修改，Agent 会先列出命令清单，等待您输入“确认”后才会下发。
4. **开始使用**：对 Agent 说：*"记录一台华为交换机，IP 是 192.168.1.1，在 A 座机房。"*
