import http.server
import socketserver
import os
import sys

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class SmartDevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and optimize caching for assets vs dynamic pages
        self.send_header('Access-Control-Allow-Origin', '*')
        if self.path.endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg', '.mp4', '.woff2', '.css', '.js')):
            self.send_header('Cache-Control', 'public, max-age=86400')
        else:
            self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    print(f"Starting High-Performance Multi-threaded Server on port {PORT}...", flush=True)
    with ThreadedHTTPServer(("0.0.0.0", PORT), SmartDevHandler) as httpd:
        print(f"Server is listening on http://localhost:{PORT} and network interfaces.", flush=True)
        print(f"Main site: http://localhost:{PORT}/index.html", flush=True)
        print(f"Banner showcase: http://localhost:{PORT}/preview-founders-showcase.html", flush=True)
        httpd.serve_forever()

