import os
import json
import subprocess
import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Resolve paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SKILL_DIR, 'assets')
INVENTORY_FILE = os.path.join(ASSETS_DIR, 'inventory.json')
USERS_FILE = os.path.join(ASSETS_DIR, 'users.json')
TASKS_FILE = os.path.join(ASSETS_DIR, 'tasks.json')
LOGS_DIR = os.path.join(ASSETS_DIR, 'logs')

class NetOpsAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
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
                "alerts": 3, # Mock
                "gpu_count": sum(1 for d in inventory if d.get('gpu'))
            }
            self.wfile.write(json.dumps(stats).encode())

        elif path == '/api/logs':
            self._set_headers()
            # Return last few log entries (mocked for now)
            logs = [
                {"id": 1, "time": "15:02:11", "level": "info", "message": "API Started", "detail": ""},
            ]
            self.wfile.write(json.dumps(logs).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        try:
            payload = json.loads(post_data.decode())
        except:
            payload = {}

        if path == '/api/action':
            action = payload.get('action')
            target_ip = payload.get('ip')
            
            if action == 'reboot':
                # Simulating a command execution
                # In real scenario: subprocess.run(["ssh", target_ip, "reboot"])
                result = {"status": "success", "message": f"Reboot command sent to {target_ip}"}
            elif action == 'shutdown':
                result = {"status": "success", "message": f"Shutdown command sent to {target_ip}"}
            else:
                result = {"status": "error", "message": "Unknown action"}
            
            self._set_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == '/api/inventory/add':
            inventory = self._read_json(INVENTORY_FILE)
            inventory.append(payload)
            self._write_json(INVENTORY_FILE, inventory)
            self._set_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

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
