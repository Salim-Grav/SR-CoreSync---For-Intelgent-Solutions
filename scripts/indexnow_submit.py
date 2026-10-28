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
IndexNow submission tool (Bing / Yandex / Seznam / Naver)
=========================================================
Submits the site's URLs to the shared IndexNow endpoint so search engines
crawl changed pages in hours instead of weeks. Requires the key file to be
LIVE on the domain first - i.e. run this only after the deploy that publishes
<key>.txt.

The key lives in a single file at the repository root (32 lowercase hex
chars). This script never contains the key itself; it reads the file, so a
future key rotation needs no code change - replace the .txt file and redeploy.

Usage:
    python scripts/indexnow_submit.py            # dry-run: show the payload
    python scripts/indexnow_submit.py --send     # actually submit to the API
    python scripts/indexnow_submit.py --urls a.html b/c.html
                                                 # submit specific paths only
Exit 0 = submitted (or dry-run printed), 1 = configuration/HTTP error.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'sr-coresync.com'
ORIGIN = 'https://' + HOST
ENDPOINT = 'https://api.indexnow.org/indexnow'
KEY_FILE_RE = re.compile(r'^[0-9a-f]{32}\.txt$')
SITEMAP = os.path.join(ROOT, 'sitemap.xml')


def find_key_file():
    hits = sorted(n for n in os.listdir(ROOT) if KEY_FILE_RE.match(n))
    if not hits:
        raise SystemExit('No IndexNow key file (32-hex-char .txt) at repo root.')
    return hits[0]


def read_key(key_file):
    key = io_open(key_file).strip()
    if key != key_file[:-4]:
        raise SystemExit('Key file %s content does not match its name.' % key_file)
    return key


def io_open(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        return fh.read()


def sitemap_urls():
    if not os.path.isfile(SITEMAP):
        return []
    xml = open(SITEMAP, encoding='utf-8').read()
    urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', xml)
    # Keep only this host (the sitemap may carry alternates or external canon).
    return sorted(u for u in urls if u.startswith(ORIGIN))


def normalise(paths):
    out = []
    for p in paths:
        p = p.lstrip('/')
        if p.endswith('/'):
            p += 'index.html'
        if p == '':
            p = 'index.html'
        out.append(ORIGIN + ('/' + p if p != 'index.html' else '/'))
    return out


def main():
    args = sys.argv[1:]
    send = '--send' in args
    if '--urls' in args:
        i = args.index('--urls')
        paths = args[i + 1:]
        urls = normalise(paths)
    else:
        urls = sitemap_urls()
    if not urls:
        raise SystemExit('No URLs to submit (sitemap.xml missing or empty?).')

    key_file = find_key_file()
    key = read_key(key_file)
    payload = {
        'host': HOST,
        'key': key,
        'keyLocation': ORIGIN + '/' + key_file,
        'urlList': urls,
    }

    print('=' * 70)
    print('IndexNow submission for %s' % HOST)
    print('=' * 70)
    print('  key file   : %s (must be live at %s/%s)' % (key_file, ORIGIN, key_file))
    print('  URLs       : %d' % len(urls))
    for u in urls[:6]:
        print('    - ' + u)
    if len(urls) > 6:
        print('    ... and %d more' % (len(urls) - 6))

    if not send:
        print('-' * 70)
        print('DRY-RUN - payload shown below, nothing sent.')
        print(json.dumps(payload, indent=2)[:1200])
        print('Run again with --send to submit.')
        return 0

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8',
                 'Host': 'api.indexnow.org'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
            body = resp.read(200).decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        print('FAILED - HTTP %d: %s' % (exc.code, exc.reason))
        print('  400 bad key/format | 403 key not live yet | 422 URL not on host'
              ' | 429 too many requests')
        return 1
    except urllib.error.URLError as exc:
        print('FAILED - network: %s' % exc.reason)
        return 1
    print('-' * 70)
    print('HTTP %d %s' % (code, '- accepted' if code in (200, 202) else body))
    print('Accepted submissions are queued, not instant - expect crawls within'
          ' hours. Re-run after each significant deploy.')
    return 0 if code in (200, 202) else 1


if __name__ == '__main__':
    sys.exit(main())
