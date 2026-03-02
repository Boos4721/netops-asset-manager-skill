import json
import os
import sys
from datetime import datetime

# Ensure we can import other scripts in the same folder
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

import hardware_check
import storage_prober
import gpu_manager
import notifier

def generate_report():
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Hardware
    hw = hardware_check.get_hardware_status()
    
    # 2. Storage
    st = storage_prober.get_storage_report()
    
    # 3. GPU
    gpu_alerts = gpu_manager.check_gpu_alerts()

    # Build Markdown Content
    content = f"## 🛠️ NetOps Daily Report ({report_time})\n\n"
    
    content += "### 🖥️ System Stats\n"
    content += f"- **CPU Load**: {hw.get('cpu_load', 'N/A')}\n"
    mem = hw.get('memory_mb', {})
    if isinstance(mem, dict):
        content += f"- **Memory**: {mem.get('used', 'N/A')}MB / {mem.get('total', 'N/A')}MB\n"
    else:
        content += f"- **Memory**: {mem}\n"
    
    disk = hw.get('disk_usage', {})
    if isinstance(disk, dict):
        content += f"- **Disk (/)**: {disk.get('percent', 'N/A')} used\n\n"
    else:
        content += f"- **Disk (/)**: {disk}\n\n"
    
    content += "### 💾 Storage Health\n"
    if st.get('raid_raw') and 'degraded' in str(st['raid_raw']).lower():
        content += "⚠️ **ALERT**: RAID Array is Degraded!\n"
    else:
        content += "✅ RAID Arrays are healthy.\n"
    content += f"- Network Mounts: {len(st.get('network_mounts', []))} active\n\n"
    
    content += "### 🎮 GPU Status\n"
    if gpu_alerts:
        for a in gpu_alerts:
            content += f"❌ {a}\n"
    else:
        content += "✅ GPU Temperatures and Memory are within limits.\n"
    
    return content

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # Example: Send to Bark if key is set in env
    bark_key = os.getenv("BARK_KEY")
    if bark_key:
        notifier.send_bark(bark_key, "NetOps Daily", "System check completed.")
