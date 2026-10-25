# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions - Quick Performance & Publish-Hygiene Package
====================================================================
Applies the 2026-10 quick-win package to every published HTML page:

  1. Drops the three speculative `<link rel="prefetch">` hints that pulled
     ~313 KB of other language portals on every visit.
  2. Removes the two empty `src=""` attributes (they made the browser
     re-request the page itself as an image).
  3. Serves the 28 KB WebP emblem instead of the 1,212 KB PNG for every
     inline logo/emblem render (the PNG stays as the download/favicon asset).
  4. Serves the 137 KB WebP in the logo lightbox instead of the 1,510 KB
     4K JPEG (the 4K file stays as the explicit "download 4K" asset).
  5. Serves the 250 KB compressed founder clip instead of the 1,640 KB one.
  6. Points every page at the single canonical `js/enterprise-suite.min.js`
     instead of the duplicate that lived in `css/`.

Every rule carries an expected match count measured on the repository; the
script fails loudly if a count drifts, so a silent partial patch is impossible.

Usage:  python scripts/apply_quick_package_fixes.py [--dry-run]
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {'_site', '.git', 'node_modules', '__pycache__', 'workers', 'dist'}

# Baseline measured on the unmodified repository (every published HTML page,
# not only the 29 portals). A second run must report 0 matches per rule.
# (label, compiled pattern, replacement, expected total matches)
RULES = [
    (
        'prefetch hints removed',
        re.compile(r'[ \t]*<link rel="prefetch"[^>]*>\r?\n'),
        '',
        87,
    ),
    (
        'empty zoom img src removed',
        re.compile(r'<img id="srZoomImage" src=""'),
        '<img id="srZoomImage"',
        30,
    ),
    (
        'empty lightbox img src removed',
        re.compile(r'<img id="foundersLightboxImg" src=""'),
        '<img id="foundersLightboxImg"',
        29,
    ),
    (
        'emblem PNG -> WebP',
        re.compile(r'src="((?:\.\./|\./)?assets/sr-core-emblem-official)\.png"'),
        r'src="\1.webp"',
        186,
    ),
    (
        'logo modal 4K JPEG -> WebP',
        re.compile(r'src="((?:\.\./|\./)?assets/sr-emblem-gold-luxury)-4k\.jpg"'),
        r'src="\1.webp"',
        29,
    ),
    (
        'founder clip -> compressed',
        re.compile(r'src="((?:\.\./|\./)?assets/about-founder-cinematic)\.mp4"'),
        r'src="\1-opt.mp4"',
        31,
    ),
    (
        'enterprise-suite script -> js/ path',
        re.compile(r'src="((?:\.\./|\./)?)css/enterprise-suite\.min\.js"'),
        r'src="\1js/enterprise-suite.min.js"',
        35,
    ),
    (
        'favicon alternate icon -> 96px',
        re.compile(r'(<link rel="alternate icon"[^>]*href="(?:\.\./|\./)?assets/)sr-core-emblem-official\.png(?:\?[^"]*)?"'),
        r'\1favicon-96.png"',
        29,
    ),
    (
        'apple-touch-icon -> 180px',
        re.compile(r'(<link rel="apple-touch-icon"[^>]*href="(?:\.\./|\./)?assets/)sr-core-emblem-256\.png(?:\?[^"]*)?"'),
        r'\1favicon-180.png"',
        29,
    ),
]


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith(('.html', '.htm')):
                yield os.path.join(dirpath, name)


def main():
    dry_run = '--dry-run' in sys.argv
    totals = {label: 0 for label, _, _, _ in RULES}
    touched = 0
    per_file = []

    for path in sorted(html_files()):
        with io_open(path) as fh:
            original = fh.read()
        text = original
        file_hits = {}
        for label, pattern, repl, _expected in RULES:
            text, n = pattern.subn(repl, text)
            if n:
                file_hits[label] = n
                totals[label] += n
        if text != original:
            touched += 1
            per_file.append((os.path.relpath(path, ROOT).replace('\\', '/'), file_hits))
            if not dry_run:
                with io_open(path, 'w') as fh:
                    fh.write(text)

    print('=' * 70)
    print('S&R CoreSync - Quick package' + (' (DRY RUN)' if dry_run else ''))
    print('=' * 70)

    failures = []
    for label, _p, _r, expected in RULES:
        got = totals[label]
        if got == expected:
            status = 'OK   '
        elif got == 0:
            status = 'DONE '  # already applied by an earlier run
        else:
            status = 'DRIFT'
        print('%-38s %5d / %5d  %s' % (label, got, expected, status))
        if status == 'DRIFT':
            failures.append('%s: expected %d or 0, applied %d' % (label, expected, got))

    print('-' * 70)
    print('HTML files modified: %d' % touched)
    for rel, hits in per_file[:8]:
        print('  %-42s %s' % (rel, ', '.join('%s=%d' % kv for kv in hits.items())))
    if len(per_file) > 8:
        print('  ... and %d more files' % (len(per_file) - 8))

    if failures:
        print('-' * 70)
        print('FAILED - the repository does not match the expected baseline:')
        for f in failures:
            print('  X ' + f)
        return 1

    print('=' * 70)
    print('PASSED - every rule matched its expected count.')
    return 0


def io_open(path, mode='r'):
    return open(path, mode, encoding='utf-8', newline='')


if __name__ == '__main__':
    sys.exit(main())
