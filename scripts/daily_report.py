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

    # Build Markdown Content in Chinese
    content = f"## 🛠️ NetOps 自动化巡检日报 ({report_time})\n\n"
    
    content += "### 🖥️ 系统核心指标\n"
    content += f"- **CPU 负载**: {hw.get('cpu_load', '未知')}\n"
    mem = hw.get('memory_mb', {})
    if isinstance(mem, dict):
        content += f"- **内存使用**: {mem.get('used', '未知')}MB / {mem.get('total', '未知')}MB\n"
    else:
        content += f"- **内存使用**: {mem}\n"
    
    disk = hw.get('disk_usage', {})
    if isinstance(disk, dict):
        content += f"- **根分区磁盘 (/)**: 已使用 {disk.get('percent', '未知')}\n\n"
    else:
        content += f"- **根分区磁盘 (/)**: {disk}\n\n"
    
    content += "### 💾 存储与 RAID 状态\n"
    if st.get('raid_raw') and 'degraded' in str(st['raid_raw']).lower():
        content += "⚠️ **紧急告警**: RAID 阵列已降级 (Degraded)！请检查硬盘健康。\n"
    else:
        content += "✅ RAID 阵列运行正常。\n"
    
    net_mounts = st.get('network_mounts', [])
    content += f"- **网络挂载 (NFS/SMB)**: 当前有 {len(net_mounts)} 个活跃连接\n\n"
    
    content += "### 🎮 GPU 显卡状态\n"
    if gpu_alerts:
        for a in gpu_alerts:
            # Simple translation for known alerts
            msg = str(a).replace("ALERT:", "告警:").replace("High Temperature", "温度过高").replace("Out of Memory", "显存溢出")
            content += f"❌ {msg}\n"
    else:
        content += "✅ 所有 GPU 温度与显存占用均在正常范围内。\n"
    
    return content

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # Example: Send to Bark if key is set in env
    bark_key = os.getenv("BARK_KEY")
    if bark_key:
        notifier.send_bark(bark_key, "NetOps巡检日报", "服务器健康检查已完成")
