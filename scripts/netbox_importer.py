import requests
import json
import os

def import_from_netbox(url, token, device_role=None, tag=None):
    """
    Import devices from NetBox API.
    url: NetBox base URL (e.g., https://netbox.example.com)
    token: NetBox API Token
    device_role: Optional filter by role slug
    tag: Optional filter by tag slug
    """
    api_url = f"{url.rstrip('/')}/api/dcim/devices/"
    headers = {
        "Authorization": f"Token {token}",
        "Accept": "application/json"
    }
    
    params = {}
    if device_role:
        params['role'] = device_role
    if tag:
        params['tag'] = tag

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        imported_devices = []
        for item in data.get('results', []):
            # Extract primary IP (handling NetBox IP format 1.1.1.1/24)
            primary_ip = item.get('primary_ip', {})
            ip_str = "N/A"
            if primary_ip:
                ip_address = primary_ip.get('address', "")
                ip_str = ip_address.split('/')[0] if '/' in ip_address else ip_address

            device = {
                "name": item.get('name'),
                "ip": ip_str,
                "vendor": item.get('device_type', {}).get('manufacturer', {}).get('name', 'UNKNOWN').upper(),
                "model": item.get('device_type', {}).get('model', ''),
                "location": item.get('site', {}).get('name', ''),
                "status": item.get('status', {}).get('value', ''),
                "source": "NetBox"
            }
            if ip_str != "N/A":
                imported_devices.append(device)
        
        return imported_devices
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example for testing via direct execution
    # env vars: NETBOX_URL, NETBOX_TOKEN
    nb_url = os.getenv("NETBOX_URL")
    nb_token = os.getenv("NETBOX_TOKEN")
    if nb_url and nb_token:
        print(json.dumps(import_from_netbox(nb_url, nb_token), indent=2, ensure_ascii=False))
    else:
        print("Set NETBOX_URL and NETBOX_TOKEN to test NetBox import.")
