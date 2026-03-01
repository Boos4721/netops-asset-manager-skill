import subprocess
import json
import os

def run_ipmi_cmd(host, user, password, sub_cmd):
    """Generic IPMI runner using ipmitool"""
    base_cmd = ["ipmitool", "-I", "lanplus", "-H", host, "-U", user, "-P", password]
    try:
        full_cmd = base_cmd + sub_cmd.split()
        output = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode('utf-8')
        return {"status": "success", "output": output}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_server_health_summary(host, user, password):
    """Fetch power status and critical sensors"""
    health = {}
    
    # Power Status
    power = run_ipmi_cmd(host, user, password, "chassis status")
    health['power'] = power.get('output', 'N/A')
    
    # Critical SDR (Sensors)
    sensors = run_ipmi_cmd(host, user, password, "sdr list critical")
    health['critical_sensors'] = sensors.get('output', 'No critical issues').strip()
    
    # SEL (System Event Log) - Last 5 entries
    events = run_ipmi_cmd(host, user, password, "sel list last 5")
    health['recent_events'] = events.get('output', 'N/A').strip()
    
    return health

if __name__ == "__main__":
    # Integration test placeholder
    print("OOB Manager ready. Use with IPMI credentials.")
