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
Image payload optimisation
==========================

Measured with Lighthouse against a gzip server (production-like), the Arabic
homepage shipped 2,054 KB over 56 requests, of which **1,235 KB was images** -
60% of the page, and by far the largest single cost.

Two different defects were found, and they need different treatments:

1. Photographs stored as PNG.
   `founder-raed.png` is a 400x400 photograph encoded as a 196 KB PNG;
   its WebP equivalent at the same dimensions is 12 KB. `founder-salim.png`
   (256x256, 112 KB) and `icon-192.png` (192x192, 65 KB) have the same problem.
   Encoding a photograph as PNG is lossless compression of noise: the format
   cannot win.

2. WebP files written with a wasteful encoder setting.
   `about-founder-poster.webp` - the LCP resource - is 140 KB for a 720x860
   image; 65 KB is achievable at the same dimensions with no visible change.

Nothing is resized and no crop changes: the pixel dimensions of every file are
preserved exactly, so no layout, no `srcset` and no art direction is touched.
Only the encoder setting changes. That keeps the visual review trivial - the
rendered page must look identical.

Quality policy: photographs at q82, the gold emblem at q90 (it is a flat-ish
gradient mark where banding shows first).

The service worker precaches these files, so `CACHE_NAME` is bumped; otherwise
returning visitors keep the old, heavier bytes and the gain never reaches them.

Usage:
    python scripts/optimize_image_payload.py            # report only
    python scripts/optimize_image_payload.py --apply    # write the files
"""
import argparse
import io
import os
import sys

from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# file -> quality. Every entry keeps its original pixel dimensions.
# Only files whose container already IS WebP may be rewritten in place: writing
# WebP bytes into a .png filename would leave a file no browser can decode.
RECODE = {
    'assets/about-founder-poster.webp': 82,
    'assets/hero-founder-raed-chair.webp': 82,
    'assets/hero-founder-salim-chair.webp': 82,
    'assets/about-founder-raed.webp': 82,
    'assets/sr-emblem-gold-luxury.webp': 90,
}

# PNG sources that gain a .webp sibling; the <img> references are rewritten and
# the original PNG stays on disk as a fallback.
PNG_TO_WEBP = ['assets/founder-raed.png', 'assets/founder-salim.png']


def encode(path, quality):
    image = Image.open(path)
    mode = image.mode
    if mode not in ('RGB', 'RGBA'):
        image = image.convert('RGBA' if 'A' in mode else 'RGB')
    buf = io.BytesIO()
    image.save(buf, 'WEBP', quality=quality, method=6)
    return buf.getvalue(), image.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    before = after = 0
    for rel, quality in RECODE.items():
        path = os.path.join(ROOT, rel.replace('/', os.sep))
        if not os.path.exists(path):
            print('MISSING  %s' % rel)
            continue
        old = os.path.getsize(path)
        data, size = encode(path, quality)
        before += old
        after += len(data)
        print('%-40s %4dx%-4d %6d -> %6d KB  (q%d)' % (
            rel, size[0], size[1], round(old / 1024), round(len(data) / 1024), quality))
        if args.apply:
            with open(path, 'wb') as fh:
                fh.write(data)

    for rel in PNG_TO_WEBP:
        path = os.path.join(ROOT, rel.replace('/', os.sep))
        target = os.path.splitext(path)[0] + '.webp'
        if not os.path.exists(path):
            continue
        old = os.path.getsize(path)
        data, size = encode(path, 82)
        before += old
        after += len(data)
        print('%-40s %4dx%-4d %6d -> %6d KB  (new .webp sibling)' % (
            rel, size[0], size[1], round(old / 1024), round(len(data) / 1024)))
        if args.apply:
            with open(target, 'wb') as fh:
                fh.write(data)

    print('-' * 78)
    print('%s: %d KB -> %d KB  (saving %d KB, %.0f%%)' % (
        'APPLIED' if args.apply else 'DRY RUN',
        before / 1024, after / 1024, (before - after) / 1024,
        100.0 * (before - after) / before if before else 0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
