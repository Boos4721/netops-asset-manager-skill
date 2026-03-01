# NetOps Asset Manager Skill 🚀

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

Automated IT infrastructure inventory and maintenance skill for OpenClaw. This skill empowers your AI agent to manage network devices (H3C, Huawei, Cisco, MikroTik) and Linux systems through natural language.

### ✨ Key Features
- **Intelligent Parsing**: Automatically extract IP, Vendor, Model, and Location from unstructured text or tables.
- **DevOps Capabilities**: Streamlined maintenance for **Docker** (containers/resources), **Kubernetes** (node/pod health), and **Nginx** (config syntax/reload).
- **GPU Maintenance**: Support for **NVIDIA (N-Card)** and **AMD (A-Card)** driver installation, periodic updates, and health monitoring.
- **Inventory Management**: Built-in Python scripts to store and query device assets in a structured JSON format.
- **Multi-Vendor Support**: Pre-defined command patterns for H3C, Huawei, Cisco, MikroTik, Ruijie, DCN, TP-LINK, and NETGEAR.
- **Automation Ready**: Detailed integration guides for `Netmiko` to perform automated configuration backups and batch provisioning.
- **Multi-Channel Notifications**: Integrated support for **Bark (iOS)**, **DingTalk**, and **Feishu** webhooks for inspection reports.
- **Safety First**: **Human-in-the-loop** confirmation required for all core network configuration changes.
- **On-Premise Deployment**: Easily deployable on a single OpenClaw host within an internal network for secure management.
- **Audit Logging**: Tracks all infrastructure changes for security and compliance.

### 🛠️ Structure
- `SKILL.md`: Core workflow definitions and agent instructions.
- `scripts/`: Python tools for inventory CRUD operations.
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

为 OpenClaw 打造的自动化 IT 基础设施资产管理与运维技能包。该技能赋予 AI Agent 通过自然语言管理内网网络设备（华三、华为、思科、MikroTik）及 Linux 系统。

### ✨ 核心功能
- **智能解析**：自动从凌乱的文本或表格中提取 IP、厂商、型号和位置信息。
- **DevOps 运维**：集成 **Docker**（容器/资源监控）、**Kubernetes**（节点/Pod 健康检查）及 **Nginx**（配置校验/热重载）的自动化维护能力。
- **显卡维护 (GPU)**：支持 **NVIDIA (N卡)** 与 **AMD (A卡)** 的驱动安装、定期更新及状态监控。
- **资产管理**：内置 Python 脚本，支持对设备资产进行结构化存储（JSON）与快速查询。
- **多厂商兼容**：预置了华三、华为、思科、锐捷、神州数码、TP-LINK、网件等常用运维命令模板。
- **自动化就绪**：提供了 `Netmiko` 集成指南，支持自动化配置备份、健康检查及批量下发。
- **多渠道告警**：集成 **Bark (iOS)**、**钉钉**及**飞书**机器人 Webhook，支持自动推送巡检报告。
- **安全加固**：核心网络变更引入**人工审查（Human-in-the-loop）**机制，必须经用户确认后方可执行。
- **审计日志**：记录所有基础设施变更操作，确保运维过程可追溯、更安全。

### 🛠️ 目录结构
- `SKILL.md`: 核心流程定义与 Agent 执行指令。
- `scripts/`: 用于资产增删改查及硬件巡检的 Python 工具集。
- `references/`: 厂商命令库与自动化执行参考文档。

### ⚖️ 开源协议
本项目采用 **CC BY-NC 4.0 (知识共享署名-非商业性使用 4.0 国际许可协议)**。  
**严禁用于任何商业用途。**

### 🚀 快速开始
1. **内网部署**：在您的内网（管理网段）接入一台 OpenClaw 主机。
2. **安装技能**：将此仓库克隆至 OpenClaw 的技能目录。
3. **安全确认**：针对所有核心配置修改，Agent 会先列出命令清单，等待您输入“确认”后才会下发。
4. **开始使用**：对 Agent 说：*"记录一台华为交换机，IP 是 192.168.1.1，在 A 座机房。"*
