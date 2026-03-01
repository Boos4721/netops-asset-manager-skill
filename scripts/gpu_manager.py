import subprocess
import json
import re

def get_nvidia_status():
    try:
        cmd = "nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=json"
        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode('utf-8')
        return json.loads(output)
    except Exception:
        # Fallback to CSV if JSON format not supported in older drivers
        try:
            cmd = "nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv,noheader,nounits"
            output = subprocess.check_output(cmd.split()).decode('utf-8').strip()
            gpus = []
            for line in output.split('\n'):
                v = line.split(', ')
                gpus.append({
                    "index": v[0], "name": v[1], "temp": v[2],
                    "load": v[3], "mem_util": v[4], "mem_total": v[5],
                    "mem_free": v[6], "mem_used": v[7]
                })
            return gpus
        except:
            return None

def get_amd_status():
    try:
        # Requires rocm-smi
        output = subprocess.check_output(['rocm-smi', '--showuse', '--showtemp', '--json']).decode('utf-8')
        return json.loads(output)
    except:
        return None

def check_gpu_alerts(temp_limit=85, mem_util_limit=95):
    alerts = []
    
    # NVIDIA Checks
    nv = get_nvidia_status()
    if nv:
        for g in (nv if isinstance(nv, list) else nv.get('gpus', [])):
            if float(g.get('temp', 0)) > temp_limit:
                alerts.append(f"ALERT: NVIDIA GPU {g.get('index')} High Temperature: {g.get('temp')}C")
            if float(g.get('mem_util', 0)) > mem_util_limit:
                alerts.append(f"ALERT: NVIDIA GPU {g.get('index')} Out of Memory (Util: {g.get('mem_util')}%)")

    # PCI/Dmesg Checks
    try:
        dmesg = subprocess.check_output(['dmesg', '-T']).decode('utf-8').lower()
        if "pcie bus error" in dmesg or "gpu fallen off the bus" in dmesg:
            alerts.append("CRITICAL: GPU PCI/Bus hardware error detected in dmesg!")
    except:
        pass
        
    return alerts

if __name__ == "__main__":
    print(json.dumps({
        "nvidia": get_nvidia_status(),
        "amd": get_amd_status(),
        "alerts": check_gpu_alerts()
    }, indent=2))
