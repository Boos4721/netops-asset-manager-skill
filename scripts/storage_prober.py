import subprocess
import json
import re

def get_storage_report():
    storage = {}
    
    # RAID Status
    try:
        with open('/proc/mdstat', 'r') as f:
            storage['raid_raw'] = f.read().strip()
    except:
        storage['raid_raw'] = "No RAID detected"

    # Mounts & FS Types
    try:
        lsblk = subprocess.check_output(['lsblk', '-f', '--json']).decode('utf-8')
        storage['block_devices'] = json.loads(lsblk).get('blockdevices', [])
    except:
        storage['block_devices'] = "lsblk error"

    # iSCSI Sessions
    try:
        iscsi = subprocess.check_output(['iscsiadm', '-m', 'session'], stderr=subprocess.STDOUT).decode('utf-8')
        storage['iscsi_sessions'] = iscsi.strip()
    except:
        storage['iscsi_sessions'] = "No active iSCSI sessions"

    # Network Mounts (NFS/SMB)
    try:
        mounts = subprocess.check_output(['mount']).decode('utf-8')
        net_mounts = [line for line in mounts.split('\n') if 'nfs' in line or 'cifs' in line]
        storage['network_mounts'] = net_mounts
    except:
        storage['network_mounts'] = []

    return storage

if __name__ == "__main__":
    print(json.dumps(get_storage_report(), indent=2, ensure_ascii=False))
