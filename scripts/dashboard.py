import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Resolve paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_FILE = os.path.join(SKILL_DIR, 'assets/inventory.json')

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Load inventory data
            devices = []
            if os.path.exists(INVENTORY_FILE):
                try:
                    with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
                        devices = json.load(f)
                except:
                    pass

            # Simple HTML Template
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>NetOps Asset Dashboard</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f4f7f6; }}
                    h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                    .card {{ background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 20px; margin-top: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ text-align: left; padding: 12px; border-bottom: 1px solid #eee; }}
                    th {{ background-color: #3498db; color: white; }}
                    tr:hover {{ background-color: #f9f9f9; }}
                    .tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
                    .vendor-huawei {{ background: #ebedef; color: #e41e26; }}
                    .vendor-h3c {{ background: #ebedef; color: #005bac; }}
                    .status-online {{ color: #27ae60; font-weight: bold; }}
                    .status-offline {{ color: #e74c3c; font-weight: bold; }}
                </style>
            </head>
            <body>
                <h1>🚀 NetOps Asset Manager Dashboard</h1>
                <div class="card">
                    <h2>Device Inventory ({len(devices)} devices)</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>IP Address</th>
                                <th>Vendor</th>
                                <th>Model</th>
                                <th>Location</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            for d in devices:
                vendor_class = f"vendor-{d.get('vendor', '').lower()}"
                html += f"""
                            <tr>
                                <td><strong>{d.get('name', 'N/A')}</strong></td>
                                <td><code>{d.get('ip', 'N/A')}</code></td>
                                <td><span class="tag {vendor_class}">{d.get('vendor', 'UNKNOWN')}</span></td>
                                <td>{d.get('model', '-')}</td>
                                <td>{d.get('location', '-')}</td>
                            </tr>
                """
            
            html += """
                        </tbody>
                    </table>
                </div>
                <footer style="margin-top: 40px; font-size: 12px; color: #95a5a6; text-align: center;">
                    Powered by OpenClaw NetOps Skill | CC BY-NC 4.0
                </footer>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

def run_dashboard(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"Dashboard running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    import sys
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_dashboard(p)
