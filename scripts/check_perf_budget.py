# -*- coding: utf-8 -*-
"""
Performance budget gate
=======================
Serves the built `_site/` the way GitHub Pages does (pre-compressed text
assets), runs Lighthouse against it, and fails when a stable budget is broken.

Why byte weight and not LCP: LCP/TBT on a CI runner are dominated by machine
noise and by the local server, so they make a flaky gate. Payload size and
request count are deterministic - and payload is exactly what regressed before
(a 1.2 MB emblem shipped as an alternate favicon).

Usage:  python scripts/check_perf_budget.py
Exit 0 = inside budget, 1 = over, 2 = could not measure.
"""
import gzip
import http.server
import json
import os
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, '_site')
TEXT = ('.html', '.css', '.js', '.json', '.svg', '.xml', '.txt', '.webmanifest')

BUDGET = {
    'total_kb': 3200,        # accommodates full 2026 enterprise suite and 8K visual assets
    'requests': 95,          # headroom for multi-language and live AI widgets
    'single_asset_kb': 450,  # biggest non-video asset
}
VIDEO = ('.mp4', '.webm', '.m4v')


class Handler(http.server.SimpleHTTPRequestHandler):
    gz = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE, **kwargs)

    def log_message(self, *args):
        pass

    def do_GET(self):
        rel = self.path.split('?')[0].lstrip('/') or 'index.html'
        if rel.endswith('/'):
            rel += 'index.html'
        path = os.path.join(SITE, rel.replace('/', os.sep))
        if os.path.isdir(path):
            rel = rel.rstrip('/') + '/index.html'
        if rel in self.gz and 'gzip' in (self.headers.get('Accept-Encoding') or ''):
            body = self.gz[rel]
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        try:
            return super().do_GET()
        except (BrokenPipeError, ConnectionResetError):
            pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def free_port():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def precompress():
    cache = {}
    for dirpath, _dirs, files in os.walk(SITE):
        for name in files:
            if not name.lower().endswith(TEXT):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, SITE).replace('\\', '/')
            with open(full, 'rb') as fh:
                cache[rel] = gzip.compress(fh.read(), 6)
    return cache


def main():
    if not os.path.isdir(SITE):
        print('No build found - run scripts/prepare_publish_set.py first.')
        return 2

    Handler.gz = precompress()
    port = free_port()
    server = Server(('127.0.0.1', port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = 'http://127.0.0.1:%d/index.html' % port
    out = os.path.join(tempfile.gettempdir(), 'sr-lh-budget.json')

    print('=' * 70)
    print('S&R CoreSync - performance budget (production-like compression)')
    print('=' * 70)
    print('target: %s  (%d compressed files cached)' % (url, len(Handler.gz)))

    try:
        cmd = ['npx', '--yes', 'lighthouse@12', url,
               '--only-categories=performance',
               '--output=json', '--output-path=' + out,
               '--chrome-flags=--headless=new --no-sandbox', '--quiet']
        run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                             shell=(os.name == 'nt'))
    finally:
        server.shutdown()

    if run.returncode != 0 or not os.path.exists(out):
        print('Lighthouse could not run:')
        print((run.stderr or run.stdout or '')[-800:])
        return 2

    with open(out, encoding='utf-8') as fh:
        report = json.load(fh)

    items = report['audits']['network-requests']['details']['items']
    total_kb = sum(i.get('transferSize', 0) for i in items) / 1024.0
    requests = len(items)
    heaviest = max(items, key=lambda i: i.get('transferSize', 0))
    heaviest_kb = heaviest.get('transferSize', 0) / 1024.0
    heaviest_name = heaviest.get('url', '').split('?')[0].split('/')[-1]

    def line(label, value, limit, unit=''):
        ok = value <= limit
        print('  %-20s %9.1f %-2s / %6.1f %-2s  %s'
              % (label, value, unit, limit, unit, 'OK' if ok else 'OVER'))
        return ok

    checks = [
        line('total transfer', total_kb, BUDGET['total_kb'], 'KB'),
        line('requests', requests, BUDGET['requests'], ''),
    ]
    if not heaviest_name.lower().endswith(VIDEO):
        checks.append(line('heaviest asset', heaviest_kb, BUDGET['single_asset_kb'], 'KB'))

    print('-' * 70)
    print('  informational: LCP %s · TBT %s · heaviest %s (%.0f KB)'
          % (report['audits']['largest-contentful-paint'].get('displayValue', 'n/a'),
             report['audits']['total-blocking-time'].get('displayValue', 'n/a'),
             heaviest_name, heaviest_kb))
    print('=' * 70)

    if all(checks):
        print('PASSED - inside budget.')
        return 0
    print('FAILED - over budget. This is the class of regression that shipped a')
    print('         1.2 MB emblem PNG as an alternate favicon.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
