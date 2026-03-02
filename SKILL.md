---
name: netops-asset-manager
description: Manage IT infrastructure assets (routers, switches, servers) by parsing text/tables, storing structured inventory, and preparing automation tasks for H3C, Huawei, Cisco, Mikrotik, and Linux systems. Use when a user provides device lists (Excel, CSV, or text) or requests inventory-based network/system maintenance.
---

# NetOps Asset Manager

This skill transforms unstructured infrastructure information into a structured inventory and prepares it for automated operations.

## Capabilities

1. **Intelligent Parsing**: Extract fields like Management IP, Vendor (H3C/Huawei/Cisco/Mikrotik), Model, SN, and Location from messy text or tables.
2. **Inventory Management**: Store and query device information.
3. **Automation Readiness**: Map devices to specific command sets based on their vendor profile.

## Workflow

### 1. Asset Ingestion
When a user provides asset information:
- **Bulk Import**: Use `scripts/bulk_importer.py` to process Excel (.xlsx) or CSV files.
- **Discovery**: Use `scripts/ip_discover.py` to scan subnets for new or unauthorized devices.
- **External Integration**: Support importing assets from **NetBox** via `scripts/netbox_importer.py`. Requires NetBox API URL and Token.
- For unstructured text, use LLM extraction to identify key fields.
- **Auto-Verification**: After adding assets, use `scripts/health_prober.py` to check if the devices are reachable (Ping/SSH).

### 4. Reporting & Integration
- **Daily Summaries**: Use `scripts/daily_report.py` to aggregate hardware, storage, and GPU status into a single Markdown report.
- **External Monitoring**: Use `scripts/monitoring_bridge.py` to push critical metrics to enterprise systems like Zabbix or Prometheus.
- **Notifications**: Send reports via Bark, DingTalk, or Feishu using `scripts/notifier.py`.
- Categorize vendors accurately:
  - **H3C**: Comware-based commands.
  - **Huawei**: VRP-based commands.
  - **Cisco**: IOS/NX-OS commands.
  - **Mikrotik**: RouterOS commands.
  - **Linux**: Systemd/SSH-based maintenance.

### 2. Inventory Storage
Store data in `assets/inventory.json` using the provided manager.
- **Mandatory Fields**: `ip`, `vendor`, `name`.
- **Validation**: Ensure IPs are valid before saving.
- **Search**: Support fuzzy search by IP, name, or location.

### 3. Automation Execution (Advanced)
When execution is requested:
- Map vendor types to automation drivers (e.g., `hp_comware` for H3C).
- **Safe-Guard Backup**: Before applying any configuration changes, use `scripts/config_backup.py` to save the current configuration to `assets/backups/`.
- **Pre-flight Check**: Always run `scripts/health_prober.py` before attempting configuration to ensure targets are online.
- **Human-in-the-loop (CRITICAL)**: For core network changes (VLAN, Routing, ACL), the agent MUST present the planned command list to the user and wait for explicit confirmation before connecting to the device.
- Reference [automation.md](references/automation.md) for Netmiko implementation details.
- Log all configuration changes to `assets/audit_log.txt`.

## Deployment Guide
This skill is designed for **On-Premise Deployment**.
1. Simply install an OpenClaw instance on a host within your internal network (management VLAN).
2. Clone/Install this skill.
3. The agent will then have direct SSH access to your H3C, Huawei, Cisco, and other assets without exposing them to the public internet.

### GPU Maintenance
- **Driver Updates**: Always prioritize official downloads for driver updates.
  - **NVIDIA**: Use official `.run` installers from NVIDIA CN/HK sites.
  - **AMD**: Use official `amdgpu-install` packages from AMD CN site.
  - **Fallback**: Only use system package managers (apt/yum) if official installers fail or are explicitly requested.
- **Monitoring**: Continuous tracking of temperature and VRAM.
