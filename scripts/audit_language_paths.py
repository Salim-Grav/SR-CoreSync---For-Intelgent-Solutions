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
S&R CoreSync For Intelligent Solutions - Language folder relative path auditor
================================================================
Every localized page lives in <lang>/index.html but all shared assets
(css/, js/, assets/, downloads/, manifest.json) live at the repository root.
Therefore every shared asset reference inside a language folder MUST use the
"../" prefix. A "./" prefix produces a 404 in production.

Usage: python scripts/audit_language_paths.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHARED_PREFIXES = ('./css/', './js/', './assets/', './downloads/', './templates/')
SHARED_FILES = ('./manifest.json', './sw.js', './robots.txt')

REF_RE = re.compile(
    r'\b(?:src|href|srcset|poster|data-src|data-href|action|formaction|manifest|content)'
    r'\s*=\s*["\']([^"\']+)["\']'
)

# Attributes whose value is a comma separated list of URLs.
LIST_ATTRS = ('srcset',)


def main():
    problems = []
    checked = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in ('.git', 'workers', 'scripts', 'dist',
                                    'node_modules', '__pycache__', '_site',
                                    '.github', '.agents', '.vscode', 'api',
                                    'config')
                       and not d.startswith('_')]
        for name in filenames:
            if not name.endswith('.html'):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, ROOT).replace('\\', '/')
            if '/' not in rel:
                continue  # root level pages are fine
            base = rel.split('/')[0]
            if base in ('api', 'config'):
                continue
            if not os.path.isfile(os.path.join(ROOT, base, 'index.html')):
                continue  # not a language folder (e.g. a preview/build directory)

            with io.open(full, encoding='utf-8', errors='ignore') as fh:
                html = fh.read()

            for m in REF_RE.finditer(html):
                ref = m.group(1)
                if 'srcset' in m.group(0)[:12].lower():
                    for part in ref.split(','):
                        candidate = part.strip().split(' ')[0].strip()
                        if not candidate:
                            continue
                        checked += 1
                        bad = None
                        if candidate.startswith(SHARED_PREFIXES) or candidate in SHARED_FILES:
                            bad = candidate
                        if bad:
                            line = html[:m.start()].count('\n') + 1
                            problems.append((rel, line, bad))
                    continue
                checked += 1
                bad = None
                if ref.startswith(SHARED_PREFIXES) or ref in SHARED_FILES:
                    bad = ref
                if bad:
                    line = html[:m.start()].count('\n') + 1
                    problems.append((rel, line, bad))

    print('Audited %d references across the localized pages.' % checked)
    if not problems:
        print('PASSED - every shared asset reference uses the correct "../" prefix.')
        return 0

    print('FAILED - %d broken relative reference(s):' % len(problems))
    seen = set()
    for rel, line, ref in problems:
        key = (rel, ref)
        if key in seen:
            continue
        seen.add(key)
        print('  X %-22s L%-6s %s' % (rel, line, ref))
    return 1


if __name__ == '__main__':
    sys.exit(main())
