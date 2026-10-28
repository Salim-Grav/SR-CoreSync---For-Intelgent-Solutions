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
Product page rename: preview-*.html -> clean, root-level product names
======================================================================
GitHub Pages cannot issue 301 redirects, so the migration keeps the old URL
working with a canonical + meta-refresh stub while the real page moves to a
clean name at the same directory level (relative asset paths stay valid, which
is why the files are renamed instead of moved into subdirectories).

Usage:  python scripts/rename_product_pages.py [--dry-run]
"""
import io
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'_site', '.git', 'node_modules', '__pycache__', 'workers', 'dist'}

RENAMES = [
    ('preview-software.html', 'software.html'),
    ('preview-work.html', 'work.html'),
    ('preview-estimator.html', 'estimator.html'),
    ('preview-whitelabel-calculator.html', 'whitelabel-calculator.html'),
    ('preview-3d-mockup.html', '3d-mockup.html'),
]

STUB = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>تم نقل الصفحة | S&amp;R CoreSync For Intelligent Solutions</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://sr-coresync.com/{new}">
<meta http-equiv="refresh" content="0; url=./{new}">
<style>body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
background:#07080a;color:#e9e6df;font-family:"Alexandria","Segoe UI",system-ui,sans-serif;text-align:center}}
a{{color:#d8b25e}}</style>
</head>
<body>
<p>تم نقل هذه الصفحة إلى <a href="./{new}">/{new}</a>.</p>
</body>
</html>
"""


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith(('.html', '.xml', '.js')):
                yield os.path.join(dirpath, name)


def main():
    dry_run = '--dry-run' in sys.argv
    log = []

    for old, new in RENAMES:
        src = os.path.join(ROOT, old)
        dst = os.path.join(ROOT, new)
        if not os.path.isfile(src):
            log.append('skip %s (already renamed)' % old)
            continue
        if os.path.exists(dst):
            log.append('ABORT %s -> %s exists' % (old, new))
            return 1
        if not dry_run:
            subprocess.run(['git', 'mv', old, new], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            with io.open(src, 'w', encoding='utf-8', newline='') as fh:
                fh.write(STUB.format(new=new))
        log.append('renamed %s -> %s (+ stub)' % (old, new))

    # Rewrite every reference to the new names (pages, sitemap, sw.js).
    total = 0
    files = 0
    for path in sorted(html_files()):
        with io.open(path, encoding='utf-8', newline='') as fh:
            original = fh.read()
        text = original
        hits = 0
        for old, new in RENAMES:
            if os.path.basename(path) == old:
                continue  # never rewrite the stub itself
            text, n = re.subn(re.escape(old), new, text)
            hits += n
        if hits:
            files += 1
            total += hits
            if not dry_run:
                with io.open(path, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(text)

    print('=' * 70)
    print('S&R CoreSync - product page rename' + (' (DRY RUN)' if dry_run else ''))
    print('=' * 70)
    for line in log:
        print('  ' + line)
    print('  references rewritten: %d across %d files' % (total, files))
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
