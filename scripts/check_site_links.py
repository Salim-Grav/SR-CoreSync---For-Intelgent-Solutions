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
Local link & asset integrity checker
====================================
Scans the built publish set (`_site/`) and verifies that every local
`href`/`src` resolves to a file that actually ships. External URLs, anchors,
`mailto:` and `tel:` are ignored by design.

Replaces the earlier ad-hoc `scripts/check_links.py`, which only printed two
counts.

Usage:  python scripts/check_site_links.py [root]
Exit code 1 when any reference is broken.
"""
import collections
import os
import re
import sys
from urllib.parse import unquote, urlsplit

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"')


def is_external(url):
    return bool(re.match(r'^(?:[a-zA-Z][a-zA-Z0-9+.\-]*:|//|#)', url))


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_site')
    if not os.path.isdir(target):
        print('No build found at %s - run scripts/prepare_publish_set.py first.' % target)
        return 2

    checked = 0
    broken = collections.Counter()
    broken_sources = collections.defaultdict(set)
    pages = 0

    for dirpath, _dirnames, filenames in os.walk(target):
        for name in filenames:
            if not name.lower().endswith('.html'):
                continue
            pages += 1
            page = os.path.join(dirpath, name)
            with open(page, encoding='utf-8', errors='ignore') as fh:
                html = fh.read()
            for raw in REF.findall(html):
                url = raw.strip()
                if not url or is_external(url):
                    continue
                if '${' in url or '{{' in url:
                    continue  # JS template placeholder, not a real path
                path = unquote(urlsplit(url).path)
                if not path:
                    continue
                if path.startswith('/'):
                    resolved = os.path.join(target, path.lstrip('/'))
                else:
                    resolved = os.path.normpath(os.path.join(dirpath, path))
                checked += 1
                if os.path.isdir(resolved):
                    resolved = os.path.join(resolved, 'index.html')
                if not os.path.exists(resolved):
                    rel = os.path.relpath(page, target).replace('\\', '/')
                    broken[url] += 1
                    broken_sources[url].add(rel)

    print('=' * 70)
    print('S&R CoreSync - local link integrity (%s)' % os.path.basename(target))
    print('=' * 70)
    print('HTML pages scanned : %d' % pages)
    print('Local refs checked : %d' % checked)
    print('Broken refs        : %d' % len(broken))
    if broken:
        for url, count in broken.most_common(25):
            srcs = ', '.join(sorted(broken_sources[url])[:3])
            print('  X %-52s x%d  (%s)' % (url[:52], count, srcs))
        print('=' * 70)
        return 1
    print('PASSED - every local reference resolves.')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
