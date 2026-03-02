# NetOps Asset Manager Skill 🚀

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

Automated IT infrastructure inventory and maintenance skill for OpenClaw. This skill empowers your AI agent to manage network devices (H3C, Huawei, Cisco, MikroTik, Ruijie, DCN, TP-LINK, NETGEAR) and Linux systems through natural language.

### ✨ Key Features
- **Intelligent Parsing**: Automatically extract IP, Vendor, Model, and Location from unstructured text or tables.
- **Bilingual Reporting**: Support for automated daily reports and alerts in both English and Chinese.
- **Bulk Import**: Native support for **Excel (.xlsx)** and **CSV** asset lists for rapid onboarding.
- **Enterprise Server OOB**: Full support for **DELL iDRAC**, **Inspur ISBMC**, and **Supermicro IPMI**.
- **Network Performance**: Integrated tools for **Speedtest**, **Route Tracing (MTR)**, and **Subnet Scanning (Nmap)**.
- **HPC/GPU Clusters**: Monitoring for **Infiniband (IB)**, **RDMA**, and **NCCL** bandwidth tests for high-performance AI clusters.
- **Monitoring Integration**: Support for pushing metrics to **Zabbix** and exporting data for **Prometheus**.
- **Service Security**: Automated **SSL/TLS Certificate expiry tracking**.
- **DevOps Capabilities**: Streamlined maintenance for **Docker**, **Kubernetes (K8s)**, and **Nginx**.
- **Virtualization Support**: Advanced management for **VMware ESXi**, **OpenStack**, **QEMU/KVM**, and **LXC**.
- **Storage Maintenance**: Management of **RAID (mdadm)**, **iSCSI**, **NFS/SMB** mounts, and common filesystems.
- **GPU Maintenance**: Support for **NVIDIA** and **AMD** driver installation and health monitoring.
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
2. **System Setup**: Install system-level dependencies. See [dependencies.md](references/dependencies.md).
3. **Python Setup**: Install Python requirements: `pip install -r requirements.txt`.
4. **Install Skill**: Clone this repository into your OpenClaw skills directory.
5. **Safety First**: All core configuration changes require **Human-in-the-loop** confirmation.
6. **Usage**: Tell your agent: *"Add a Huawei switch at 192.168.1.1 in the Data Center."*

### ⚖️ License
This project is licensed under the **CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)**.  
**Commercial use is strictly prohibited.**

---

<a name="chinese"></a>
## 中文

为 OpenClaw 打造的自动化 IT 基础设施资产管理与运维技能包。该技能赋予 AI Agent 通过自然语言管理内网网络设备（华三、华为、思科、锐捷、神州数码、TP-LINK、网件等）及 Linux 系统。

### ✨ 核心功能
- **智能解析**：自动从凌乱的文本或表格中提取 IP、厂商、型号和位置信息。
- **双语巡检**：支持自动化巡检日报及告警信息的“中英双语”展示与推送。
- **批量导入**：原生支持 **Excel (.xlsx)** 与 **CSV** 资产清单批量入库。
- **企业服务器带外管理 (OOB)**：深度支持 **DELL iDRAC**、**浪潮 ISBMC** 及 **超微 IPMI**。
- **网络性能监测**：集成 **Speedtest**、**路由追踪 (MTR)** 及 **网段扫描 (Nmap)**，用于资产发现与冲突检测。
- **HPC/显卡集群**：支持 **Infiniband (IB)**、**RDMA** 状态监控及 **NCCL** 多卡带宽测试，适配 AI 算力集群。
- **监控集成**：支持将巡检指标推送到 **Zabbix** 或导出为 **Prometheus** 指标格式。
- **业务安全保障**：支持 **SSL/TLS 证书到期自动监测**。
- **DevOps 运维**：集成 **Docker**、**Kubernetes** 及 **Nginx** 的自动化维护能力。
- **虚拟化管理**：支持 **VMware ESXi**、**OpenStack**、**QEMU/KVM** 及 **LXC**。
- **存储维护**：支持 **RAID**、**iSCSI**、**NFS/SMB** 及常见文件系统维护。
- **显卡维护 (GPU)**：支持 **NVIDIA** 与 **AMD** 显卡驱动安装及状态监控。
- **多渠道告警**：集成 **Bark**、**钉钉**及**飞书**机器人告警推送。
- **Web 可视化**：内置轻量级看板，可直观查看设备清单及资产状态。
- **安全加固**：核心网络变更引入 **人工审查 (Human-in-the-loop)** 机制，确保安全。
- **内网部署**：支持在内网单主机部署，安全可控。
- **审计日志**：记录所有基础设施变更操作，确保过程可追溯。

### 🛠️ 目录结构
- `SKILL.md`: 核心流程定义与 Agent 执行指令。
- `scripts/`: 用于资产管理、硬件巡检、GPU、带外、DevOps 及 Web 看板的 Python 工具集。
- `references/`: 厂商命令库与自动化执行参考文档。

### 🚀 快速开始
1. **内网部署**：在您的内网（管理网段）接入一台 OpenClaw 主机。
2. **系统环境**：安装必要的系统依赖。参见 [dependencies.md](references/dependencies.md)。
3. **Python 环境**：执行 `pip install -r requirements.txt` 安装依赖库。
4. **安装技能**：将此仓库克隆至 OpenClaw 的技能目录。
5. **安全确认**：针对所有核心配置修改，Agent 会先列出命令清单，等待您输入“确认”后才会下发。
6. **开始使用**：对 Agent 说：*"记录一台华为交换机，IP 是 192.168.1.1，在 A 座机房。"*

### ⚖️ 开源协议
本项目采用 **CC BY-NC 4.0 (知识共享署名-非商业性使用 4.0 国际许可协议)**。  
**严禁用于任何商业用途。**
