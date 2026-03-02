import os
import sys
import time
import subprocess
import json

def test_speed(server_id=None):
    """
    Run speedtest-cli and return results.
    Requires: pip install speedtest-cli
    """
    try:
        cmd = ["speedtest-cli", "--json"]
        if server_id:
            cmd.extend(["--server", str(server_id)])
        
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        return json.loads(output)
    except Exception as e:
        return {"error": f"speedtest-cli failed or not installed: {str(e)}"}

def trace_route(target):
    """
    Run mtr or traceroute to check path hops.
    """
    try:
        # Use mtr for better quality if available, else traceroute
        if subprocess.call(["which", "mtr"], stdout=subprocess.DEVNULL) == 0:
            cmd = ["mtr", "-rw", "-c", "1", target]
        else:
            cmd = ["traceroute", "-w", "1", target]
            
        output = subprocess.check_output(cmd).decode('utf-8')
        return output
    except Exception as e:
        return f"Trace failed: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        print(f"--- Speedtest Results ---")
        print(json.dumps(test_speed(), indent=2))
        print(f"\n--- Routing Trace to {target} ---")
        print(trace_route(target))
    else:
        print("Usage: python3 network_perf.py <trace_target_ip>")
