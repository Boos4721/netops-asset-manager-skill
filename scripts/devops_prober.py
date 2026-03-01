import subprocess
import json

def get_docker_summary():
    try:
        ps_output = subprocess.check_output(['docker', 'ps', '-a', '--format', '{{json .}}']).decode('utf-8').strip()
        containers = [json.loads(line) for line in ps_output.split('\n') if line]
        
        stats_output = subprocess.check_output(['docker', 'stats', '--no-stream', '--format', '{{json .}}']).decode('utf-8').strip()
        stats_map = {json.loads(line)['Name']: json.loads(line) for line in stats_output.split('\n') if line}
        
        return {"containers": containers, "stats": stats_map}
    except Exception as e:
        return {"error": f"Docker not running or no permissions: {str(e)}"}

def get_k8s_summary():
    try:
        nodes = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'json']).decode('utf-8')
        pods_not_running = subprocess.check_output(['kubectl', 'get', 'pods', '-A', '--field-selector=status.phase!=Running', '-o', 'json']).decode('utf-8')
        
        return {
            "nodes": json.loads(nodes).get('items', []),
            "unhealthy_pods": json.loads(pods_not_running).get('items', [])
        }
    except Exception as e:
        return {"error": f"Kubectl not configured or cluster unreachable: {str(e)}"}

def check_nginx_syntax():
    try:
        output = subprocess.check_output(['nginx', '-t'], stderr=subprocess.STDOUT).decode('utf-8')
        return {"ok": "successful" in output, "output": output}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(json.dumps({
        "docker": get_docker_summary(),
        "k8s": get_k8s_summary(),
        "nginx": check_nginx_syntax()
    }, indent=2))
