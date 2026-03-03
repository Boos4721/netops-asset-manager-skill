import pandas as pd
import json
import os
import sys

# Resolve paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_FILE = os.path.join(SKILL_DIR, 'assets/inventory.json')

# Map vendor names to Netmiko device types
VENDOR_DRIVERS = {
    "H3C": "hp_comware",
    "HUAWEI": "huawei",
    "CISCO": "cisco_ios",
    "MIKROTIK": "mikrotik_routeros",
    "RUIJIE": "ruijie_os",
    "DCN": "dcn_os",
    "TP-LINK": "tplink_jetstream",
    "NETGEAR": "netgear_prosafe",
    "LINUX": "linux"
}

def get_driver(vendor):
    return VENDOR_DRIVERS.get(str(vendor).upper(), "autodetect")

def bulk_import(file_path):
    """
    Import assets from Excel (.xlsx) or CSV.
    Expected columns: name, ip, vendor, model, location
    """
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            return {"error": "Unsupported file format. Use .xlsx or .csv"}

        # Normalize column names to lowercase
        df.columns = [c.lower() for d in df.columns]
        
        # Required columns check
        required = ['name', 'ip', 'vendor']
        for req in required:
            if req not in df.columns:
                return {"error": f"Missing required column: {req}"}

        new_devices = df.to_dict(orient='records')
        
        # Load existing
        existing = []
        if os.path.exists(INVENTORY_FILE):
            with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        
        # Merge by IP (overwrite if exists)
        inventory_dict = {d['ip']: d for d in existing}
        for dev in new_devices:
            # Basic validation
            if pd.isna(dev['ip']) or not isinstance(dev['ip'], str):
                continue
            
            # Clean data
            sn = str(dev.get('sn', '')).strip() if not pd.isna(dev.get('sn')) else ''
            server = str(dev.get('server', '')).strip() if not pd.isna(dev.get('server')) else ''
            
            clean_dev = {
                "name": str(dev.get('name', 'Unknown')),
                "ip": str(dev.get('ip')).strip(),
                "vendor": str(dev.get('vendor', 'UNKNOWN')).upper(),
                "model": str(dev.get('model', '')) if not pd.isna(dev.get('model')) else '',
                "location": str(dev.get('location', '')) if not pd.isna(dev.get('location')) else '',
                "sn": sn,
                "server": server,
                "driver": get_driver(dev.get('vendor', 'UNKNOWN')),
                "tags": []
            }
            inventory_dict[clean_dev['ip']] = clean_dev
            
        # Save back
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(inventory_dict.values()), f, indent=2, ensure_ascii=False)
            
        return {"status": "success", "count": len(new_devices)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(bulk_import(sys.argv[1]), indent=2))
    else:
        print("Usage: python3 bulk_importer.py <path_to_file>")
