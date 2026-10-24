# -*- coding: utf-8 -*-
"""
Enable / disable the live trust feed across every portal
=======================================================
`js/sr-live-feed.js` stays completely silent until `window.SR_FEED_BASE` is set,
so nothing calls the network while the worker is undeployed. Once the worker is
live, this script inserts (or removes) the one-line config ahead of the module
in every page.

Usage:
  python scripts/enable_live_feed.py                       # enable with the default endpoint
  python scripts/enable_live_feed.py --base https://api.sr-coresync.com
  python scripts/enable_live_feed.py --disable
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BASE = 'https://api.sr-coresync.com'
SKIP_DIRS = {'_site', '.git', 'node_modules', '__pycache__', 'workers', 'dist'}

CONFIG_RE = re.compile(
    r'[ \t]*<script>\s*window\.SR_FEED_BASE\s*=\s*[^<]*?</script>\r?\n?'
    r'|[ \t]*<meta\s+name="sr-feed-base"[^>]*>\r?\n?', re.I)
MODULE_RE = re.compile(r'(?P<indent>[ \t]*)<script src="(?P<prefix>(?:\.\./|\./)?)js/sr-live-feed\.js"')


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith('.html'):
                yield os.path.join(dirpath, name)


def main():
    args = sys.argv[1:]
    disable = '--disable' in args
    base = DEFAULT_BASE
    if '--base' in args:
        base = args[args.index('--base') + 1].rstrip('/')

    touched = 0
    for path in sorted(html_files()):
        with io.open(path, encoding='utf-8', newline='') as fh:
            doc = fh.read()

        stripped = CONFIG_RE.sub('', doc)

        if disable:
            if stripped != doc:
                with io.open(path, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(stripped)
                touched += 1
            continue

        match = MODULE_RE.search(stripped)
        if not match:
            continue
        if CONFIG_RE.search(doc) and doc.index('window.SR_FEED_BASE') < doc.index('sr-live-feed.js'):
            continue  # already configured

        line = '%s<meta name="sr-feed-base" content="%s">\n' % (match.group('indent'), base)
        doc_new = stripped[:match.start()] + line + stripped[match.start():]
        if doc_new != doc:
            with io.open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(doc_new)
            touched += 1

    action = 'disabled' if disable else 'enabled (%s)' % base
    print('=' * 60)
    print('Live feed %s' % action)
    print('pages updated: %d' % touched)
    print('=' * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
