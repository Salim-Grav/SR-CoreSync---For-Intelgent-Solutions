# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - Raster asset optimiser (WebP)
======================================================
The service / work / founder imagery is stored as multi-hundred-KB JPEGs and
referenced with a plain `<img src="...jpg">`. This script produces a WebP
sibling for every heavy card image and points the markup at it, while keeping
the original JPEG in the repository (social cards, downloads and older
browsers keep working).

Rules:
  * Only `<img src="...">` is rewritten. `<source srcset>`, `href=` (download
    links), `og:image` and `twitter:image` keep the JPEG.
  * Images that already ship a `.webp` sibling are reused, never re-encoded.
  * Encoding is deterministic (Pillow, quality 82, method 6, max 1600 px wide).

Usage:  python scripts/optimize_images_webp.py [--dry-run]
"""
import io
import os
import re
import sys

from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')
SKIP_DIRS = {'_site', '.git', 'node_modules', '__pycache__', 'workers', 'dist'}

MAX_WIDTH = 1600
QUALITY = 82

# Card / hero imagery that is still served as JPEG.
TARGETS = [
    'service-identity-3d',
    'service-website-3d',
    'service-ecommerce-3d',
    'service-cloud-software-3d',
    'service-erp-finance-3d',
    'service-mobile-apps-3d',
    'service-ai-automation-3d',
    'service-finance-advisory-3d',
    'service-cybersecurity-3d',
    'work-web-hintham',
    'work-web-cleaning',
    'work-omnibakery-hero',
    'work-healthbridge-hero',
    'work-civicsync-hero',
    'work-bakery-pos',
    'work-bakery-hero',
    'about-founder-raed',
    'hero-founder-salim-chair',
    'hero-founder-raed-chair',
]


def encode(name):
    src = os.path.join(ASSETS, name + '.jpg')
    dst = os.path.join(ASSETS, name + '.webp')
    if not os.path.isfile(src):
        return None, 'missing source'
    if os.path.isfile(dst):
        return os.path.getsize(dst), 'reused'
    im = Image.open(src).convert('RGB')
    w, h = im.size
    if w > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(h * MAX_WIDTH / w)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=QUALITY, method=6)
    return os.path.getsize(dst), 'encoded %dx%d' % im.size


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith('.html'):
                yield os.path.join(dirpath, name)


def main():
    dry_run = '--dry-run' in sys.argv

    print('=' * 74)
    print('S&R CoreSync - WebP asset pass' + (' (DRY RUN)' if dry_run else ''))
    print('=' * 74)

    saved = 0
    for name in TARGETS:
        size, note = encode(name)
        if size is None:
            print('  ! %-34s %s' % (name, note))
            continue
        jpg = os.path.getsize(os.path.join(ASSETS, name + '.jpg'))
        saved += max(0, jpg - size)
        print('  %-34s %7.0f KB -> %6.0f KB  (%s)' % (name, jpg / 1024, size / 1024, note))

    print('-' * 74)
    print('Per-visit saving if all are seen: %.1f MB' % (saved / 1048576))

    total = 0
    files = 0
    for path in sorted(html_files()):
        with open(path, encoding='utf-8', newline='') as fh:
            original = fh.read()
        text = original
        hits = 0
        for name in TARGETS:
            pattern = re.compile(r'src="((?:\.\./|\./)?assets/)' + re.escape(name) + r'\.jpg"')
            text, n = pattern.subn(r'src="\1' + name + '.webp"', text)
            hits += n
        if hits and not dry_run:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(text)
        if hits:
            files += 1
            total += hits

    print('img references rewritten: %d across %d files' % (total, files))
    print('=' * 74)
    return 0


if __name__ == '__main__':
    sys.exit(main())
