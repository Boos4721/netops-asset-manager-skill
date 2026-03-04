#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import socketserver
import os
import http.client
import json

PORT = 8082
API_PORT = 8081
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/ui"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def proxy_request(self, method):
        if not self.path.startswith('/api/'):
            return False
        
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None
        
        # Connect to API server
        conn = http.client.HTTPConnection("localhost", API_PORT)
        
        # Forward headers (except host)
        headers = {}
        for key, value in self.headers.items():
            if key.lower() != 'host':
                headers[key] = value
        
        try:
            conn.request(method, self.path, body, headers)
            resp = conn.getresponse()
            
            self.send_response(resp.status)
            self.send_header('Content-Type', resp.getheader('Content-Type', 'application/json'))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = resp.read()
            if data:
                self.wfile.write(data)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        finally:
            conn.close()
        return True
    
    def do_GET(self):
        if self.path.startswith('/api/'):
            if self.proxy_request('GET'):
                return
        elif self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            if self.proxy_request('POST'):
                return
        return super().do_POST()
    
    def do_DELETE(self):
        if self.path.startswith('/api/'):
            if self.proxy_request('DELETE'):
                return
        return super().do_DELETE()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

os.chdir(DIRECTORY)
with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
    print(f"Serving UI at http://0.0.0.0:{PORT}, proxying /api/* to port {API_PORT}")
    httpd.serve_forever()
