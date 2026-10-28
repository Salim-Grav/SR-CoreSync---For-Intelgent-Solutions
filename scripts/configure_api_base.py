# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
Point the site at a deployed Worker
===================================
Once the Worker is live (custom domain or *.workers.dev), the site still posts
to `api.sr-coresync.com`, which only exists after the zone moves to Cloudflare.
This script rewires everything to whichever base URL actually answers:

  1. js/sr-lead-dispatcher.js  -> DEFAULT_ENDPOINTS
  2. _headers                  -> connect-src allowlist (and form-action if needed)
  3. js/sr-live-feed.js config -> via scripts/enable_live_feed.py

Usage:
  python scripts/configure_api_base.py --base https://sr-lead-capture.example.workers.dev
  python scripts/configure_api_base.py --base https://api.sr-coresync.com
  python scripts/configure_api_base.py --show
"""
import io
import os
import re
import subprocess
import sys
from urllib.parse import urlsplit

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISPATCHER = os.path.join(ROOT, 'js', 'sr-lead-dispatcher.js')
HEADERS = os.path.join(ROOT, '_headers')

ENDPOINTS_RE = re.compile(r'const DEFAULT_ENDPOINTS = \[[^\]]*\];')
CONNECT_RE = re.compile(r'(connect-src [^;]+;)')


def read(path):
    with io.open(path, encoding='utf-8', newline='') as fh:
        return fh.read()


def write(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)


def current_base():
    doc = read(DISPATCHER)
    match = re.search(r"'(https?://[^']+)/lead'", doc)
    return match.group(1) if match else None


def main():
    args = sys.argv[1:]

    if '--show' in args or '--base' not in args:
        base = current_base()
        print('Current API base : %s' % (base or 'not set'))
        headers = read(HEADERS)
        connect = CONNECT_RE.search(headers)
        print('CSP connect-src  : %s' % (connect.group(1) if connect else 'missing'))
        return 0

    raw = args[args.index('--base') + 1].strip().rstrip('/')
    parts = urlsplit(raw)
    if parts.scheme != 'https' or not parts.netloc:
        raise SystemExit('Base must be an absolute https URL, got: %r' % raw)
    host = parts.netloc

    # 1. Lead dispatcher
    doc = read(DISPATCHER)
    block = ("const DEFAULT_ENDPOINTS = [\n"
             "        '%s/lead',\n"
             "        '/api/lead'\n"
             "    ];" % raw)
    if not ENDPOINTS_RE.search(doc):
        raise SystemExit('Could not find DEFAULT_ENDPOINTS in %s' % DISPATCHER)
    doc = ENDPOINTS_RE.sub(block, doc, count=1)
    write(DISPATCHER, doc)

    # 2. CSP: make sure the host is allowed to be called
    headers = read(HEADERS)
    connect = CONNECT_RE.search(headers)
    if not connect:
        raise SystemExit('No connect-src directive in _headers')
    directive = connect.group(1)
    if 'https://' + host not in directive:
        directive = directive[:-1] + ' https://' + host + ';'
        headers = headers.replace(connect.group(1), directive, 1)
        write(HEADERS, headers)
        csp_note = 'connect-src updated'
    else:
        csp_note = 'connect-src already allows it'

    # 3. Live feed goes to the same host
    subprocess.run([sys.executable,
                    os.path.join(ROOT, 'scripts', 'enable_live_feed.py'),
                    '--base', raw], cwd=ROOT)

    print('=' * 66)
    print('API base configured')
    print('=' * 66)
    print('  base            : %s' % raw)
    print('  lead endpoint   : %s/lead' % raw)
    print('  CSP             : %s' % csp_note)
    print('  live feed       : enabled for all portals')
    print('=' * 66)
    print('Next: python scripts/prepare_publish_set.py && git commit -am "chore(api): point site at live worker"')
    return 0


if __name__ == '__main__':
    sys.exit(main())
