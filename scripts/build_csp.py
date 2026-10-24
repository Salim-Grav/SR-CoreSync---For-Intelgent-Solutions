# -*- coding: utf-8 -*-
"""
Generate the CSP script hashes for the published site
====================================================
A static site that carries JSON-LD cannot use `script-src 'self'` alone: every
inline <script> needs either 'unsafe-inline' or its own sha256 hash. Delegating
the handlers removed the onclick class of violations; what remains is one
JSON-LD block per portal.

This script hashes every inline <script> block in the publish set and writes a
ready-to-paste CSP fragment. Regenerate it whenever a page's inline script
changes - the deploy check verifies the file is in sync.

  python scripts/build_csp.py            # write csp-hashes.txt + print the policy
  python scripts/build_csp.py --check    # fail when the file is stale (CI)
"""
import base64
import hashlib
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, '_site')
OUT = os.path.join(ROOT, 'csp-hashes.txt')

INLINE = re.compile(r'(?is)<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>')

HOSTS = {
    'script': "'self' https://cdn.jsdelivr.net https://cdn.tailwindcss.com https://unpkg.com https://js.stripe.com",
    'style': "'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.tailwindcss.com",
    'img': "'self' data: blob:",
    'font': "'self' data: https://fonts.gstatic.com",
    'connect': "'self' https://sr-lead-capture.sr-coresync.workers.dev https://fonts.googleapis.com https://api.telegram.org",
    'frame': "'self' https://js.stripe.com https://hooks.stripe.com https://www.mollie.com",
}


def collect():
    hashes = set()
    pages = 0
    if not os.path.isdir(SITE):
        raise SystemExit('No _site build - run scripts/prepare_publish_set.py first.')
    for dirpath, _dirs, files in os.walk(SITE):
        for name in files:
            if not name.lower().endswith('.html'):
                continue
            pages += 1
            doc = io.open(os.path.join(dirpath, name), encoding='utf-8', errors='ignore').read()
            for body in INLINE.findall(doc):
                if body.strip() == '':
                    continue
                digest = hashlib.sha256(body.encode('utf-8')).digest()
                hashes.add("'sha256-" + base64.b64encode(digest).decode() + "'")
    return pages, sorted(hashes)


def build_policy(hashes):
    directives = [
        "default-src 'self'",
        'script-src ' + HOSTS['script'] + (' ' + ' '.join(hashes) if hashes else ''),
        'style-src ' + HOSTS['style'],
        'img-src ' + HOSTS['img'],
        'font-src ' + HOSTS['font'],
        'media-src \'self\' data: blob:',
        'connect-src ' + HOSTS['connect'],
        "worker-src 'self' blob:",
        'frame-src ' + HOSTS['frame'],
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self' https://wa.me",
        "frame-ancestors 'self'",
        'upgrade-insecure-requests',
    ]
    return '; '.join(directives)


def main():
    check = '--check' in sys.argv
    pages, hashes = collect()
    policy = build_policy(hashes)

    payload = {
        'generated_from': '_site inline <script> blocks',
        'pages': pages,
        'hash_count': len(hashes),
        'script_hashes': hashes,
        'content_security_policy': policy,
    }

    if check:
        if not os.path.isfile(OUT):
            print('FAILED - csp-hashes.txt is missing; run python scripts/build_csp.py')
            return 1
        current = io.open(OUT, encoding='utf-8').read()
        if json.loads(current).get('script_hashes') != hashes:
            print('FAILED - csp-hashes.txt is stale; run python scripts/build_csp.py')
            return 1
        print('PASSED - csp-hashes.txt matches the publish set (%d hashes).' % len(hashes))
        return 0

    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write('\n')

    print('=' * 74)
    print('S&R CoreSync - CSP hashes')
    print('=' * 74)
    print('pages scanned : %d' % pages)
    print('inline scripts: %d unique hash(es)' % len(hashes))
    print('written       : csp-hashes.txt')
    print('-' * 74)
    print(policy)
    print('=' * 74)
    return 0


if __name__ == '__main__':
    sys.exit(main())
