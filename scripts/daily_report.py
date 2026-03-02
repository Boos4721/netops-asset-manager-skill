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

def generate_report(lang="bilingual"):
    """
    Generate report content based on language preference.
    lang: 'zh' (Chinese only), 'en' (English only), 'bilingual' (Both)
    """
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Hardware
    hw = hardware_check.get_hardware_status()
    # 2. Storage
    st = storage_prober.get_storage_report()
    # 3. GPU
    gpu_alerts = gpu_manager.check_gpu_alerts()

    # Helpers for conditional content
    def t(zh, en):
        if lang == "zh": return zh
        if lang == "en": return en
        return f"{zh} / {en}"

    # Build Markdown Content
    content = f"## {t('🛠️ NetOps 自动化巡检日报', '🛠️ NetOps Automated Inspection Report')}\n"
    content += f"**{t('Time', '时间')}**: {report_time}\n\n"
    
    # Section: System Stats
    content += f"### 🖥️ {t('System Stats', '系统核心指标')}\n"
    content += f"- **{t('CPU Load', 'CPU 负载')}**: {hw.get('cpu_load', t('N/A', '未知'))}\n"
    
    mem = hw.get('memory_mb', {})
    if isinstance(mem, dict):
        mem_str = f"{mem.get('used', 'N/A')}MB / {mem.get('total', 'N/A')}MB"
        content += f"- **{t('Memory', '内存使用')}**: {mem_str}\n"
    else:
        content += f"- **{t('Memory', '内存使用')}**: {mem}\n"
    
    disk = hw.get('disk_usage', {})
    if isinstance(disk, dict):
        content += f"- **{t('Disk (/)', '根分区磁盘')}**: {disk.get('percent', 'N/A')} {t('used', '已使用')}\n\n"
    else:
        content += f"- **{t('Disk (/)', '根分区磁盘')}**: {disk}\n\n"
    
    # Section: Storage
    content += f"### 💾 {t('Storage & RAID', '存储与 RAID 状态')}\n"
    if st.get('raid_raw') and 'degraded' in str(st['raid_raw']).lower():
        content += f"⚠️ **{t('ALERT', '紧急告警')}**: {t('RAID Array is Degraded', 'RAID 阵列已降级')}!\n"
    else:
        content += f"✅ {t('RAID Arrays are healthy', 'RAID 阵列运行正常')}。\n"
    
    net_mounts = st.get('network_mounts', [])
    content += f"- **{t('Network Mounts', '网络挂载')}**: {len(net_mounts)} {t('active', '个活跃连接')}\n\n"
    
    # Section: GPU
    content += f"### 🎮 {t('GPU Status', 'GPU 显卡状态')}\n"
    if gpu_alerts:
        for a in gpu_alerts:
            msg_en = str(a)
            msg_zh = msg_en.replace("ALERT:", "告警:").replace("High Temperature", "温度过高").replace("Out of Memory", "显存溢出")
            content += f"❌ {t(msg_zh, msg_en)}\n"
    else:
        content += f"✅ {t('All GPUs are healthy', '所有 GPU 状态正常')}。\n"
    
    return content

if __name__ == "__main__":
    # Command line args for language and target
    # Usage: python3 daily_report.py [zh|en|bilingual] [bark|dingtalk|feishu] [credential] [secret_for_dingtalk]
    lang = sys.argv[1] if len(sys.argv) > 1 else "bilingual"
    target = sys.argv[2] if len(sys.argv) > 2 else None
    cred = sys.argv[3] if len(sys.argv) > 3 else None
    secret = sys.argv[4] if len(sys.argv) > 4 else None

    report_content = generate_report(lang)
    print(report_content)
    
    if not target or not cred:
        sys.exit(0)

    if target == "bark":
        title = "NetOps Report" if lang == "en" else "NetOps巡检日报"
        notifier.send_bark(cred, title, "Server check completed")
    elif target == "dingtalk":
        notifier.send_dingtalk(cred, report_content, secret=secret)
    elif target == "feishu":
        notifier.send_feishu(cred, report_content)
