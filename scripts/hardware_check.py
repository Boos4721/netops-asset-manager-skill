import json
import os
import subprocess

def get_hardware_status():
    """
    Local hardware status collector for Linux systems.
    Can be extended to run via SSH on remote nodes.
    """
    status = {}
    
    # CPU Load
    try:
        load = os.getloadavg()
        status['cpu_load'] = {"1m": load[0], "5m": load[1], "15m": load[2]}
    except:
        status['cpu_load'] = "N/A"

    # Memory Usage
    try:
        mem = subprocess.check_output(['free', '-m']).decode('utf-8').split('\n')[1].split()
        status['memory_mb'] = {"total": mem[1], "used": mem[2], "free": mem[3]}
    except:
        status['memory_mb'] = "N/A"

    # Disk Usage (Root)
    try:
        disk = subprocess.check_output(['df', '-h', '/']).decode('utf-8').split('\n')[1].split()
        status['disk_usage'] = {"size": disk[1], "used": disk[2], "avail": disk[3], "percent": disk[4]}
    except:
        status['disk_usage'] = "N/A"

    return status

if __name__ == "__main__":
    print(json.dumps(get_hardware_status(), indent=2))
