#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import socketserver
import os
import urllib.request
import urllib.error

PORT = 8082
API_PORT = 8081
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/ui"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            # Proxy to API server
            try:
                req = urllib.request.Request(
                    f'http://localhost:{API_PORT}{self.path}',
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    self.send_response(resp.status)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(resp.read())
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.end_headers()
            return
        elif self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                req = urllib.request.Request(
                    f'http://localhost:{API_PORT}{self.path}',
                    data=body,
                    headers={
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    self.send_response(resp.status)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(resp.read())
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(e.read() if e.fp else b'{}')
            return
        return super().do_POST()
    
    def do_DELETE(self):
        if self.path.startswith('/api/'):
            try:
                req = urllib.request.Request(
                    f'http://localhost:{API_PORT}{self.path}',
                    headers={'Content-Type': 'application/json'},
                    method='DELETE'
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    self.send_response(resp.status)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(resp.read())
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.end_headers()
            return
        return super().do_DELETE()
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

os.chdir(DIRECTORY)
with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
    print(f"Serving UI at http://0.0.0.0:{PORT}, proxying /api/* to port {API_PORT}")
    httpd.serve_forever()
