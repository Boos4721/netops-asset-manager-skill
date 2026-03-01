import os
import json
import socket
import struct
import platform
import subprocess

def ping_check(ip):
    """
    Quick ICMP ping check using system command.
    Returns True if reachable, False otherwise.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '1', ip]
    try:
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except:
        return False

def port_check(ip, port=22, timeout=2):
    """
    Check if a specific port (default SSH: 22) is open.
    """
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def batch_verify(inventory_path):
    """
    Reads inventory.json and checks reachability for all devices.
    """
    results = []
    if not os.path.exists(inventory_path):
        return {"error": "Inventory file not found"}
    
    with open(inventory_path, 'r', encoding='utf-8') as f:
        devices = json.load(f)
    
    for dev in devices:
        ip = dev.get('ip')
        if ip:
            online = ping_check(ip)
            ssh_open = port_check(ip, 22) if online else False
            results.append({
                "name": dev.get('name'),
                "ip": ip,
                "status": "Online" if online else "Offline",
                "ssh": "Open" if ssh_open else "Closed"
            })
    
    return results

if __name__ == "__main__":
    import sys
    # Path relative to project root
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/inventory.json')
    if os.path.exists(path):
        print(json.dumps(batch_verify(path), indent=2, ensure_ascii=False))
    else:
        print("Inventory not found. Add devices first.")
