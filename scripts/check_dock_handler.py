#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dock handler invariant audit (engine-agnostic).
================================================
History: translation/template batches once shipped the Launchpad button
markup in 58 pages while the inline controller block defining
window.toggleAppleDockLaunchpad was dropped - every click threw
ReferenceError and the language menu never opened (caught by the browser
console audit only AFTER publishing).

The site's dock engine has since been rewritten, so this gate does NOT
compare against any engine template. It enforces one invariant that must
hold for ANY engine version:

    every HTML page that calls toggleAppleDockLaunchpad from markup
    (onclick="...") must also DEFINE window.toggleAppleDockLaunchpad
    (or function toggleAppleDockLaunchpad) in that same page.

Usage:  python scripts/check_dock_handler.py
Exit 0 = invariant holds, 1 = drift detected.
"""
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CALL_RE = re.compile(r'on\s*=\s*["\'][^"\']*toggleAppleDockLaunchpad\s*\(', re.I)
DEFINE_RE = re.compile(
    r'(window\.toggleAppleDockLaunchpad\s*=\s*function'
    r'|function\s+toggleAppleDockLaunchpad\s*\()')


def tracked_html():
    out = subprocess.run(
        ['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True,
        text=True, check=True).stdout.splitlines()
    # Landing + demo pages only (top level or one language folder deep);
    # skip the _site/dist build mirrors and nested product pages.
    keep = []
    for rel in out:
        parts = rel.split('/')
        if parts[0] in ('_site', 'dist', 'downloads', 'templates',
                        'workers', 'scripts', 'deploy', 'sdk'):
            continue
        if len(parts) <= 2 and (parts[-1] in ('index.html', 'demo.html')):
            keep.append(rel)
    return sorted(keep)


def main():
    pages = tracked_html()
    bad = []
    for rel in pages:
        html = open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
        calls = len(CALL_RE.findall(html))
        if calls and not DEFINE_RE.search(html):
            bad.append((rel, calls))

    print('=' * 70)
    print('Dock handler invariant: markup calls require an in-page definition')
    print('=' * 70)
    print('  pages audited: %d' % len(pages))
    if bad:
        for rel, calls in bad:
            print('  X %s: %d markup call(s) with NO window.toggleAppleDockLaunchpad definition'
                  % (rel, calls))
        print('-' * 70)
        print('FAILED - DRIFT DETECTED: buttons wired to a missing handler.')
        return 1
    print('  every toggleAppleDockLaunchpad call site has a matching definition')
    print('=' * 70)
    print('PASSED - dock handler invariant holds.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
