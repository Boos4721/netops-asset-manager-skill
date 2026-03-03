import os
import json
import subprocess
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Resolve paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SKILL_DIR, 'assets')
INVENTORY_FILE = os.path.join(ASSETS_DIR, 'inventory.json')
LOGS_DIR = os.path.join(ASSETS_DIR, 'logs')
UPLOAD_DIR = os.path.join(ASSETS_DIR, 'uploads')

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# DB config
DB_CONFIG = {
    "dbname": "netops",
    "user": "admin",
    "password": "boos",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

class NetOpsAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/inventory':
            self._set_headers()
            data = self._read_json(INVENTORY_FILE)
            self.wfile.write(json.dumps(data).encode())
        
        elif path == '/api/stats':
            self._set_headers()
            inventory = self._read_json(INVENTORY_FILE)
            stats = {
                "total": len(inventory),
                "online": sum(1 for d in inventory if d.get('status') == 'online'),
                "alerts": 0,
                "gpu_count": sum(1 for d in inventory if d.get('gpu'))
            }
            self.wfile.write(json.dumps(stats).encode())

        elif path == '/api/logs':
            self._set_headers()
            logs = [{"id": 1, "time": "System", "level": "info", "message": "API Started", "detail": ""}]
            self.wfile.write(json.dumps(logs).encode())
            
        elif path == '/api/users':
            self._set_headers()
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT id, username, role FROM users")
                users = [{"id": r[0], "username": r[1], "role": r[2]} for r in cur.fetchall()]
                cur.close()
                conn.close()
                self.wfile.write(json.dumps(users).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
                
        elif path == '/api/pm2/status':
            self._set_headers()
            try:
                # Fetch PM2 status locally (or could be remote if configured)
                result = subprocess.check_output(["pm2", "jlist"]).decode()
                pm2_list = json.loads(result)
                tasks = []
                for p in pm2_list:
                    tasks.append({
                        "name": p.get("name"),
                        "status": p.get("pm2_env", {}).get("status"),
                        "restarts": p.get("pm2_env", {}).get("restart_time"),
                        "memory": p.get("monit", {}).get("memory"),
                        "cpu": p.get("monit", {}).get("cpu")
                    })
                self.wfile.write(json.dumps(tasks).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode())
            except:
                payload = {}
        else:
            payload = {}
            
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/users/login':
            username = payload.get('username')
            password = payload.get('password')
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT id, role FROM users WHERE username=%s AND password=%s", (username, password))
                user = cur.fetchone()
                cur.close()
                conn.close()
                self._set_headers()
                if user:
                    self.wfile.write(json.dumps({"status": "success", "token": "mock_token", "role": user[1], "username": username}).encode())
                else:
                    self.wfile.write(json.dumps({"status": "error", "message": "Invalid credentials"}).encode())
            except Exception as e:
                self._set_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

        elif path == '/api/users':
            username = payload.get('username')
            password = payload.get('password')
            role = payload.get('role', 'operator')
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
                conn.commit()
                cur.close()
                conn.close()
                self._set_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self._set_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

        elif path == '/api/pm2/deploy':
            # Deploy a custom task
            # Payload: {"task_name": "my_task", "binary_path": "/path/to/bin", "args": "--port 8080", "target_ips": ["192.168.1.10"]}
            task_name = payload.get("task_name")
            binary_path = payload.get("binary_path")
            args = payload.get("args", "")
            target_ips = payload.get("target_ips", [])
            
            results = []
            for ip in target_ips:
                try:
                    # In a real implementation we would SCP the binary to the target IP, and run PM2 via SSH.
                    # Since we are making a demo/proof-of-concept, we simulate or run locally pointing to IP.
                    # Assuming passwordless SSH is set up.
                    
                    # 1. SCP the file
                    # subprocess.run(["scp", binary_path, f"root@{ip}:/tmp/{task_name}"])
                    # 2. Run PM2 on remote
                    # ssh_cmd = f"pm2 start /tmp/{task_name} --name {task_name}_{ip} -- {args}"
                    # subprocess.run(["ssh", f"root@{ip}", ssh_cmd])
                    
                    # For demonstration in local dashboard, let's run it locally but named per target
                    # Or run a dummy script representing the deployment
                    local_cmd = ["pm2", "start", "bash", "--name", f"{task_name}_{ip}", "--", "-c", f"echo Deploying {binary_path} to {ip} with {args} && sleep 3600"]
                    subprocess.check_call(local_cmd)
                    results.append({"ip": ip, "status": "deployed"})
                except Exception as e:
                    results.append({"ip": ip, "status": "failed", "error": str(e)})
                    
            self._set_headers()
            self.wfile.write(json.dumps({"status": "success", "results": results}).encode())

        else:
            self._set_headers(404)

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/users/'):
            user_id = path.split('/')[-1]
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
                conn.commit()
                cur.close()
                conn.close()
                self._set_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self._set_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
        else:
            self._set_headers(404)

    def _read_json(self, file_path):
        if not os.path.exists(file_path): return []
        try:
            with open(file_path, 'r') as f: return json.load(f)
        except: return []

    def _write_json(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

def run_api(port=8081):
    print(f"NetOps API Server running on port {port}")
    HTTPServer(('', port), NetOpsAPIHandler).serve_forever()

if __name__ == "__main__":
    run_api()
