import json
import os
import re

# Resolve paths relative to the skill directory
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_FILE = os.path.join(SKILL_DIR, 'assets/inventory.json')

def load_inventory():
    if not os.path.exists(os.path.dirname(INVENTORY_FILE)):
        os.makedirs(os.path.dirname(INVENTORY_FILE))
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_inventory(data):
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def validate_ip(ip):
    return re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ip)

def add_device(ip, vendor, name, model=None, location=None, tags=None):
    if not validate_ip(ip):
        return {"error": f"Invalid IP address: {ip}"}
    
    inventory = load_inventory()
    # Update if exists, otherwise add
    for device in inventory:
        if device['ip'] == ip:
            device.update({"vendor": vendor, "name": name, "model": model, "location": location, "tags": tags or []})
            save_inventory(inventory)
            return {"status": "updated", "device": device}
            
    new_device = {
        "ip": ip,
        "vendor": vendor.upper(),
        "name": name,
        "model": model,
        "location": location,
        "tags": tags or []
    }
    inventory.append(new_device)
    save_inventory(inventory)
    return {"status": "added", "device": new_device}

def search_devices(query):
    inventory = load_inventory()
    results = []
    q = query.lower()
    for d in inventory:
        if q in d['ip'] or q in d['name'].lower() or q in d.get('location', '').lower() or q in d['vendor'].lower():
            results.append(d)
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Simple CLI for adding via exec if needed
        # Usage: python3 inventory_manager.py add <ip> <vendor> <name>
        if sys.argv[1] == "add":
            print(add_device(sys.argv[2], sys.argv[3], sys.argv[4]))
