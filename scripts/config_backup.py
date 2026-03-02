import os
import json
from datetime import datetime
try:
    from netmiko import ConnectHandler
except ImportError:
    ConnectHandler = None

# Resolve paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(SKILL_DIR, 'assets/backups')
INVENTORY_FILE = os.path.join(SKILL_DIR, 'assets/inventory.json')

# Device type mapping for Netmiko
VENDOR_MAPPING = {
    "H3C": "hp_comware",
    "HUAWEI": "huawei",
    "CISCO": "cisco_ios",
    "RUIJIE": "ruijie_os",
    "DCN": "digital_china_os",
    "TP-LINK": "tplink_jetstream",
    "NETGEAR": "netgear_prosafe",
    "MIKROTIK": "mikrotik_routeros"
}

def backup_device_config(ip, vendor, username, password):
    if not ConnectHandler:
        return {"status": "error", "message": "netmiko not installed"}
    
    device_type = VENDOR_MAPPING.get(vendor.upper())
    if not device_type:
        return {"status": "error", "message": f"Unsupported vendor for backup: {vendor}"}

    device = {
        'device_type': device_type,
        'host': ip,
        'username': username,
        'password': password,
    }

    try:
        with ConnectHandler(**device) as net_connect:
            if vendor.upper() == "MIKROTIK":
                config = net_connect.send_command("/export")
            else:
                config = net_connect.send_command("display current-configuration" if vendor.upper() in ["HUAWEI", "H3C"] else "show running-config")
            
            # Save to file
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{ip}_{timestamp}.cfg"
            filepath = os.path.join(BACKUP_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(config)
                
            return {"status": "success", "file": filepath, "size": len(config)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Usage: python3 config_backup.py <ip> <vendor> <user> <pass>
    import sys
    if len(sys.argv) == 5:
        print(json.dumps(backup_device_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]), indent=2))
    else:
        print("Usage: python3 config_backup.py <ip> <vendor> <user> <pass>")
