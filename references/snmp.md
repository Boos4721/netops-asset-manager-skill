# SNMP Reference Guide

Use these OIDs for basic device polling when SSH is unavailable.

## Standard MIB-II (RFC 1213)
- **System Description**: `.1.3.6.1.2.1.1.1.0`
- **System Uptime**: `.1.3.6.1.2.1.1.3.0`
- **System Name**: `.1.3.6.1.2.1.1.5.0`
- **Interface Table**: `.1.3.6.1.2.1.2.2`
  - Index: `.1.3.6.1.2.1.2.2.1.1`
  - Description: `.1.3.6.1.2.1.2.2.1.2`
  - Admin Status: `.1.3.6.1.2.1.2.2.1.7` (1: up, 2: down)
  - Oper Status: `.1.3.6.1.2.1.2.2.1.8` (1: up, 2: down)

## Vendor Specific OIDs

### H3C / Huawei (Entity MIB)
- **CPU Usage**: `.1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5`
- **Memory Usage**: `.1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7`
- **Device Temperature**: `.1.3.6.1.4.1.2011.5.25.31.1.1.1.1.11`

### Cisco
- **CPU Usage (5min)**: `.1.3.6.1.4.1.9.9.109.1.1.1.1.5.1`
- **Memory Free**: `.1.3.6.1.4.1.9.9.48.1.1.1.6.1`

### MikroTik
- **System CPU Load**: `.1.3.6.1.2.1.25.3.3.1.2.1`
- **System Memory Total**: `.1.3.6.1.2.1.25.2.3.1.5.65536`
- **System Memory Used**: `.1.3.6.1.2.1.25.2.3.1.6.65536`

## Tools
- **snmpwalk**: `snmpwalk -v 2c -c public <IP> <OID>`
- **snmpget**: `snmpget -v 2c -c public <IP> <OID>`
