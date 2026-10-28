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
S&R CoreSync For Intelligent Solutions - Publish Set Builder
===============================================================================
Builds the `_site/` directory that is uploaded to GitHub Pages.

The exact same rules are enforced by `scripts/validate_publish_set.py` and by
the "Verify no server-side material is published" step of the deploy
workflow, so the verified artifact is always the published artifact.

Usage:  python scripts/prepare_publish_set.py
Exit code 0 = the staging directory is ready to upload.
"""
import io
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publish_set import (  # noqa: E402
    ROOT, FORBIDDEN_PUBLISHED, REQUIRED_PUBLISHED, publish_set
)

STAGE = os.path.join(ROOT, '_site')


def main():
    print('=' * 70)
    print('S&R CoreSync - Building the GitHub Pages publish set')
    print('=' * 70)

    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE)

    files = publish_set()
    copied = 0
    total_bytes = 0

    for rel in files:
        src = os.path.join(ROOT, rel.replace('/', os.sep))
        dst = os.path.join(STAGE, rel.replace('/', os.sep))
        dst_dir = os.path.dirname(dst)
        if dst_dir and not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy2(src, dst)
        copied += 1
        total_bytes += os.path.getsize(src)

    print('Copied %d files (%.2f MB) into _site/' % (copied, total_bytes / 1024.0 / 1024.0))

    # Guard: nothing forbidden may exist inside the staging directory.
    failures = []
    for bad in FORBIDDEN_PUBLISHED:
        target = os.path.join(STAGE, bad)
        if os.path.exists(target):
            failures.append('Forbidden path present in the publish set: %s' % bad)

    for req in REQUIRED_PUBLISHED:
        if not os.path.exists(os.path.join(STAGE, req)):
            failures.append('Required publish file missing: %s' % req)

    if failures:
        print('-' * 70)
        print('FAILED:')
        for f in failures:
            print('  X ' + f)
        return 1

    print('Guard passed: no server-side material in the publish set.')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
