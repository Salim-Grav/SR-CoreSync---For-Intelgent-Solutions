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
S&R CoreSync For Intelligent Solutions - Publish Set Validator
===============================================================================
Verifies, locally, that the GitHub Pages artifact is safe to publish.

Checks:
  1. Forbidden server-side paths are excluded from the publish set.
  2. Mandatory files (_headers, .nojekyll) are included.
  3. Every local src/href referenced by a published HTML page resolves.
  4. Pages that collect client data load the lead dispatcher.
  5. No page still points at the dead /api/lead-capture.php gateway.

The rules live in `scripts/publish_set.py`, the same module used by
`scripts/prepare_publish_set.py` that actually builds the artifact.

Usage:  python scripts/validate_publish_set.py
Exit code 0 = safe to publish.
"""
import io
import os
import re
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publish_set import (  # noqa: E402
    ROOT, FORBIDDEN_PUBLISHED, REQUIRED_PUBLISHED, publish_set
)

RESOURCE_RE = re.compile(
    r'(?:src|href)\s*=\s*["\'](?!#|data:|mailto:|tel:|javascript:|blob:)([^"\']+)["\']'
)

FORM_MARKERS = ('id="contact-name"', 'id="contact-email"', 'id="contact-phone"',
                'id="booking-name"', 'id="vip-name"')


def main():
    errors = []
    warnings = []

    publish_set_files = publish_set()
    publish_dirs = set()
    for rel in publish_set_files:
        parts = rel.split('/')
        for i in range(1, len(parts)):
            publish_dirs.add('/'.join(parts[:i]))

    print('=' * 72)
    print('S&R CoreSync - Publish Set Validation')
    print('=' * 72)
    print('Publish set: %d files, %d directories' % (len(publish_set_files), len(publish_dirs)))

    total_bytes = 0
    for rel in publish_set_files:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        try:
            total_bytes += os.path.getsize(p)
        except OSError:
            pass
    print('Publish size : %.2f MB' % (total_bytes / 1024.0 / 1024.0))

    # 1. Forbidden paths ------------------------------------------------------
    for bad in FORBIDDEN_PUBLISHED:
        if bad in publish_dirs or bad in publish_set_files:
            errors.append('Forbidden path present in publish set: %s' % bad)

    # 2. Required files -------------------------------------------------------
    for req in REQUIRED_PUBLISHED:
        if req not in publish_set_files:
            errors.append('Required publish file missing: %s' % req)

    # 3-5. Page level checks ---------------------------------------------------
    html_files = [f for f in publish_set_files if f.endswith('.html')]
    checked_refs = 0
    missing_refs = {}
    pages_without_dispatcher = []

    for rel in html_files:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        with io.open(p, encoding='utf-8', errors='ignore') as fh:
            html = fh.read()

        base = os.path.dirname(rel)

        if any(m in html for m in FORM_MARKERS) and 'js/sr-lead-dispatcher.js' not in html:
            pages_without_dispatcher.append(rel)

        if 'api/lead-capture.php' in html:
            errors.append('%s still references the dead /api/lead-capture.php gateway' % rel)

        for m in RESOURCE_RE.finditer(html):
            ref = m.group(1).strip()
            if not ref or ref.startswith('#'):
                continue
            if urlparse(ref).scheme in ('http', 'https', 'ftp', 'mailto', 'tel'):
                continue
            target = ref.split('#')[0].split('?')[0]
            if not target:
                continue
            if '${' in target or '{' in target:
                continue  # template literal, not a static path
            if target.startswith('/'):
                resolved = target.lstrip('/')
            else:
                resolved = (base + '/' + target) if base else target
            resolved = os.path.normpath(resolved).replace('\\', '/')
            checked_refs += 1
            if resolved == '.' and 'index.html' in publish_set_files:
                continue
            if resolved in publish_dirs and (resolved + '/index.html') in publish_set_files:
                continue
            if resolved not in publish_set_files:
                missing_refs.setdefault(resolved, []).append(rel)

    print('HTML pages in publish set : %d' % len(html_files))
    print('Local resource refs checked: %d' % checked_refs)

    for target, sources in sorted(missing_refs.items()):
        errors.append('Missing local resource: %s (referenced by %d page(s), e.g. %s)'
                      % (target, len(sources), sources[0]))

    if pages_without_dispatcher:
        errors.append('Pages that collect client data but lack the lead dispatcher: %s'
                      % ', '.join(pages_without_dispatcher))

    print('-' * 72)
    if warnings:
        print('WARNINGS (%d):' % len(warnings))
        for w in warnings[:40]:
            print('  ! ' + w)
        print('-' * 72)

    if errors:
        print('FAILED - %d blocking issue(s):' % len(errors))
        for e in errors[:60]:
            print('  X ' + e)
        if len(errors) > 60:
            print('  ... %d more' % (len(errors) - 60))
        print('=' * 72)
        return 1

    print('PASSED - publish set is safe. No server-side material is exposed.')
    print('=' * 72)
    import audit_secrets
    if audit_secrets.main() != 0:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
