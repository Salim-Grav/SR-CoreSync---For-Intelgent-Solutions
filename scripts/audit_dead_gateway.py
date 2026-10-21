#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit that nothing published still points at the retired PHP gateway.

The retired endpoint used to be reachable as ``/api/lead-capture.php``.  On
GitHub Pages the file was served verbatim, so the browser could read the
whole PHP source and the lead form silently posted to a gateway that
answered ``405``.  The replacement is the Cloudflare Worker in
``workers/sr-lead-capture``.

This audit looks for *real references* only: HTML/JS comments that merely
mention the old path in prose are legitimate (they document the incident)
and must not fail the build.  Therefore comments are stripped before the
search.
"""

from __future__ import print_function

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publish_set import iter_publish_files  # noqa: E402

DEAD_GATEWAY = 'api/lead-capture.php'
SCANNED_SUFFIXES = ('.html', '.js', '.mjs', '.xml', '.json', '.webmanifest')

BLOCK_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
LINE_COMMENT = re.compile(r'(^|[^:])//[^\n]*')
HTML_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)
CSS_BLOCK_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)


def strip_comments(text, suffix):
    if suffix in ('.html', '.xml', '.webmanifest'):
        text = HTML_COMMENT.sub(' ', text)
    if suffix in ('.js', '.mjs'):
        text = BLOCK_COMMENT.sub(' ', text)
        text = LINE_COMMENT.sub(r'\1', text)
    if suffix == '.json':
        text = CSS_BLOCK_COMMENT.sub(' ', text)
    return text


def main():
    offenders = []
    scanned = 0

    for rel in iter_publish_files():
        if not rel.endswith(SCANNED_SUFFIXES):
            continue
        path = os.path.join(ROOT, rel.replace('/', os.sep))
        try:
            with io.open(path, encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
        except OSError:
            continue

        scanned += 1
        cleaned = strip_comments(content, os.path.splitext(rel)[1])
        if DEAD_GATEWAY in cleaned:
            offenders.append(rel)

    if offenders:
        print('=' * 72)
        print('FAIL - the retired PHP gateway is still referenced by published files:')
        for rel in offenders:
            print('  - %s' % rel)
        print('=' * 72)
        return 1

    print('PASS - no published file references %s (%d files scanned).' % (DEAD_GATEWAY, scanned))
    return 0


if __name__ == '__main__':
    sys.exit(main())
