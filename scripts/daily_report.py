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

def generate_report(lang="auto"):
    """Generate bilingual or localized report. lang: 'zh', 'en', or 'auto' (bilingual)"""
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Hardware
    hw = hardware_check.get_hardware_status()
    
    # 2. Storage
    st = storage_prober.get_storage_report()
    
    # 3. GPU
    gpu_alerts = gpu_manager.check_gpu_alerts()

    # Build Markdown Content
    title_zh = "🛠️ NetOps 自动化巡检日报"
    title_en = "🛠️ NetOps Automated Inspection Report"
    
    content = f"## {title_zh} / {title_en}\n"
    content += f"**Time / 时间**: {report_time}\n\n"
    
    # Section: System Stats
    content += "### 🖥️ System Stats / 系统核心指标\n"
    content += f"- **CPU Load / CPU 负载**: {hw.get('cpu_load', 'N/A / 未知')}\n"
    
    mem = hw.get('memory_mb', {})
    if isinstance(mem, dict):
        mem_str = f"{mem.get('used', 'N/A')}MB / {mem.get('total', 'N/A')}MB"
        content += f"- **Memory / 内存使用**: {mem_str}\n"
    else:
        content += f"- **Memory / 内存使用**: {mem}\n"
    
    disk = hw.get('disk_usage', {})
    if isinstance(disk, dict):
        content += f"- **Disk (/) / 根分区磁盘**: {disk.get('percent', 'N/A')} used / 已使用\n\n"
    else:
        content += f"- **Disk (/) / 根分区磁盘**: {disk}\n\n"
    
    # Section: Storage
    content += "### 💾 Storage & RAID / 存储与 RAID 状态\n"
    if st.get('raid_raw') and 'degraded' in str(st['raid_raw']).lower():
        content += "⚠️ **ALERT / 紧急告警**: RAID Array is Degraded / RAID 阵列已降级！\n"
    else:
        content += "✅ RAID Arrays are healthy / RAID 阵列运行正常。\n"
    
    net_mounts = st.get('network_mounts', [])
    content += f"- **Network Mounts / 网络挂载**: {len(net_mounts)} active / 个活跃连接\n\n"
    
    # Section: GPU
    content += "### 🎮 GPU Status / GPU 显卡状态\n"
    if gpu_alerts:
        for a in gpu_alerts:
            msg_en = str(a)
            msg_zh = msg_en.replace("ALERT:", "告警:").replace("High Temperature", "温度过高").replace("Out of Memory", "显存溢出")
            content += f"❌ {msg_zh} ({msg_en})\n"
    else:
        content += "✅ All GPUs are healthy / 所有 GPU 状态正常。\n"
    
    return content

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    bark_key = os.getenv("BARK_KEY")
    if bark_key:
        notifier.send_bark(bark_key, "NetOps Report / 巡检日报", "Check completed / 巡检完成")
