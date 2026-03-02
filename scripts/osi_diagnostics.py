import subprocess
import json
import socket
import os

def get_physical_layer(interface="eth0"):
    """Check L1: Interface speed and link"""
    try:
        output = subprocess.check_output(['ethtool', interface]).decode('utf-8')
        speed = "Unknown"
        link = "Unknown"
        for line in output.split('\n'):
            if "Speed:" in line: speed = line.split(':')[1].strip()
            if "Link detected:" in line: link = line.split(':')[1].strip()
        return {"interface": interface, "speed": speed, "link_detected": link}
    except:
        return {"error": "ethtool failed"}

def get_transport_session_stats():
    """Check L4/L5: Active TCP connections"""
    try:
        # Get TCP state counts
        output = subprocess.check_output(['ss', '-s']).decode('utf-8')
        return {"summary": output.strip()}
    except:
        return {"error": "ss command failed"}

def get_application_health(urls):
    """Check L7: HTTP Status codes"""
    import requests
    results = {}
    for url in urls:
        try:
            res = requests.get(url, timeout=5)
            results[url] = {"status": res.status_code, "latency_ms": res.elapsed.total_seconds() * 1000}
        except Exception as e:
            results[url] = {"error": str(e)}
    return results

if __name__ == "__main__":
    print(json.dumps({
        "L1_Physical": get_physical_layer(),
        "L4_L5_Session": get_transport_session_stats(),
        "L7_Application": get_application_health(["https://www.google.com", "https://api.github.com"])
    }, indent=2))
