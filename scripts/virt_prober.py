import subprocess
import json

def get_kvm_status():
    try:
        output = subprocess.check_output(['virsh', 'list', '--all', '--json'], stderr=subprocess.STDOUT).decode('utf-8')
        return json.loads(output)
    except:
        try:
            # Fallback for systems without --json support
            output = subprocess.check_output(['virsh', 'list', '--all']).decode('utf-8')
            return {"raw": output}
        except:
            return None

def get_proxmox_lxc_status():
    try:
        output = subprocess.check_output(['pct', 'list']).decode('utf-8')
        lines = output.strip().split('\n')
        if len(lines) < 2: return []
        containers = []
        for line in lines[1:]:
            parts = line.split()
            containers.append({"vmid": parts[0], "status": parts[1], "name": parts[2]})
        return containers
    except:
        return None

def get_esxi_summary():
    # Note: Requires SSH to ESXi host
    try:
        output = subprocess.check_output(['vim-cmd', 'vmsvc/getallvms']).decode('utf-8')
        return {"raw_vms": output}
    except:
        return None

if __name__ == "__main__":
    print(json.dumps({
        "kvm": get_kvm_status(),
        "lxc": get_proxmox_lxc_status(),
        "esxi_local": get_esxi_summary()
    }, indent=2, ensure_ascii=False))
