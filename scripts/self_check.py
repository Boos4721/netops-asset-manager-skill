import os
import json
import re
import sys

# Resolve paths
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)
VENDORS_FILE = os.path.join(PROJECT_ROOT, 'references/vendors.md')

def check_vendors_doc():
    """
    Scans vendors.md to ensure all expected vendors have command patterns defined.
    """
    expected_vendors = [
        "H3C", "Huawei", "Cisco", "MikroTik", "Ruijie", 
        "Digital China", "TP-LINK", "NETGEAR", "Fortinet", "Palo Alto",
        "ESXi", "OpenStack", "QEMU/KVM", "LXC", "NVIDIA", "AMD", "RAID"
    ]
    
    if not os.path.exists(VENDORS_FILE):
        return {"error": "vendors.md missing"}
        
    with open(VENDORS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    status = {}
    for v in expected_vendors:
        status[v] = "Found" if v.lower() in content.lower() else "MISSING"
        
    return status

if __name__ == "__main__":
    print(json.dumps(check_vendors_doc(), indent=2))
