import os
import sys
import subprocess
import json

def check_l1_link(interface):
    """L1: Physical Link Check"""
    try:
        res = subprocess.check_output(["ethtool", interface], stderr=subprocess.STDOUT).decode()
        link_detected = "Link detected: yes" in res
        return {"status": "Up" if link_detected else "Down", "detail": res.split('\n')[0]}
    except Exception as e:
        return {"status": "Error", "error": str(e)}

def check_l3_connectivity(target):
    """L3: Network Connectivity (Ping)"""
    try:
        subprocess.check_call(["ping", "-c", "1", "-W", "2", target], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return {"status": "Reachable"}
    except Exception:
        return {"status": "Unreachable"}

def check_l7_http(url):
    """L7: Application Check (HTTP)"""
    try:
        res = subprocess.check_output(["curl", "-o", "/dev/null", "-s", "-w", "%{http_code}", url]).decode()
        return {"status": "Healthy" if res == "200" else "Alert", "code": res}
    except Exception as e:
        return {"status": "Error", "error": str(e)}

def run_full_diag(target_ip, web_url=None):
    report = {
        "L3_Connectivity": check_l3_connectivity(target_ip),
    }
    if web_url:
        report["L7_HTTP"] = check_l7_http(web_url)
    return report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(run_full_diag(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None), indent=2))
