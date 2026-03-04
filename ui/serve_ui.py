#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import socketserver
import os

PORT = 8082
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/ui"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

os.chdir(DIRECTORY)
with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving UI at http://0.0.0.0:{PORT}")
    httpd.serve_forever()
