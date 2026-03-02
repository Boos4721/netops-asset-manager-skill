import os
import sys
import subprocess
import json
import re

def scan_subnet(subnet):
    """
    Perform a quick discovery scan on a subnet.
    Requires: nmap
    """
    try:
        # Use nmap for fast host discovery and OS fingerprinting
        cmd = ["nmap", "-sn", "-T4", subnet]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        
        # Regex to find IPs and Hostnames
        hosts = []
        host_blocks = re.split(r'Nmap scan report for ', output)[1:]
        for block in host_blocks:
            lines = block.strip().split('\n')
            first_line = lines[0]
            
            # Extract IP and Hostname
            match = re.search(r'(?P<host>.*) \((?P<ip>\d+\.\d+\.\d+\.\d+)\)', first_line)
            if match:
                hosts.append({"name": match.group('host'), "ip": match.group('ip')})
            else:
                ip_only = re.search(r'(\d+\.\d+\.\d+\.\d+)', first_line)
                if ip_only:
                    hosts.append({"name": "Unknown", "ip": ip_only.group(1)})
                    
        return {"subnet": subnet, "alive_hosts": len(hosts), "hosts": hosts}
    except Exception as e:
        return {"error": f"Scan failed: {str(e)} (Ensure nmap is installed)"}

def detect_conflicts():
    """
    Scan local ARP table to find potential IP/MAC conflicts.
    """
    try:
        output = subprocess.check_output(['arp', '-an']).decode('utf-8')
        # Logic to find multiple IPs for one MAC or vice-versa
        # This is a simplified version
        return {"arp_table": output.strip()}
    except:
        return {"error": "ARP check failed"}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(scan_subnet(sys.argv[1]), indent=2))
    else:
        print("Usage: python3 ip_discover.py <subnet_cidr> (e.g., 192.168.1.0/24)")
