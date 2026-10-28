# -*- coding: utf-8 -*-
"""
SEO discovery assets audit (IndexNow / vCard / OfferCatalog)
============================================================
The three discovery assets added in 2026-10 are each load-bearing and each
silently breakable by template batches:

  1. IndexNow key file  - submissions are validated against /<key>.txt on the
     host; a missing/mismatched file makes every future submission fail.
  2. vCard contact card - must stay RFC 6350 compliant (CRLF, 75-octet fold)
     and discoverable via <link rel="alternate" type="text/vcard">.
  3. OfferCatalog JSON-LD - the service catalog search engines read; a
     dropped marker or broken JSON silently removes the rich result.

Usage:  python scripts/check_seo_assets.py [--check]
Exit 0 = all assets intact, 1 = drift/regression found.
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from publish_set import REQUIRED_PUBLISHED  # noqa: E402

KEY_RE = re.compile(r'^[0-9a-f]{32}\.txt$')
VCARD_LINK = '<link rel="alternate" type="text/vcard" href="/SR-CoreSync.vcf"'
LD_BEGIN = '<!-- SRX:BEGIN:offer_catalog_ld -->'
LD_END = '<!-- SRX:END:offer_catalog_ld -->'
LANDING_PAIRS = [('index.html', 'ar'), ('en/index.html', 'en')]

issues = []


def check(cond, msg):
    if not cond:
        issues.append(msg)


def audit_indexnow():
    hits = [n for n in os.listdir(ROOT) if KEY_RE.match(n)]
    check(len(hits) == 1, 'IndexNow: expected exactly one 32-hex key file, found %d' % len(hits))
    if len(hits) != 1:
        return
    name = hits[0]
    body = open(os.path.join(ROOT, name), encoding='utf-8').read().strip()
    check(body == name[:-4], 'IndexNow: %s content does not match its name' % name)
    check(name in REQUIRED_PUBLISHED,
          'IndexNow: %s missing from REQUIRED_PUBLISHED (publish_set.py)' % name)


def audit_vcard():
    path = os.path.join(ROOT, 'SR-CoreSync.vcf')
    if not check_or('vCard: SR-CoreSync.vcf missing', os.path.isfile(path)):
        return
    raw = open(path, 'rb').read()
    check(b'\n' not in raw.replace(b'\r\n', b''), 'vCard: bare LF found - wire format must be CRLF only')
    lines = raw.decode('utf-8').split('\r\n')
    check(all(len(l.encode('utf-8')) <= 75 for l in lines),
          'vCard: line longer than 75 octets - fold it per RFC 6350')
    check(lines[0] == 'BEGIN:VCARD' and lines[-1] == 'END:VCARD',
          'vCard: BEGIN/END structure broken')
    unfolded = []
    for l in lines:
        if l.startswith(' ') and unfolded:
            unfolded[-1] += l[1:]
        else:
            unfolded.append(l)
    props = {l.split(':', 1)[0].upper() for l in unfolded if ':' in l}
    check(any(l.upper() == 'VERSION:4.0' for l in unfolded),
          'vCard: VERSION:4.0 property missing')
    for required in ('FN', 'ORG', 'URL', 'EMAIL', 'TEL'):
        check(any(p == required or p.startswith(required + ';') for p in props),
              'vCard: required property %s missing' % required)
    check('SR-CoreSync.vcf' in REQUIRED_PUBLISHED,
          'vCard: SR-CoreSync.vcf missing from REQUIRED_PUBLISHED (publish_set.py)')
    for rel, _lang in LANDING_PAIRS:
        html = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        check(VCARD_LINK in html, 'vCard: discovery <link> missing on %s' % rel)


def check_or(msg, cond):
    check(cond, msg)
    return cond


def audit_offer_catalog():
    seen_ids = set()
    for rel, lang in LANDING_PAIRS:
        path = os.path.join(ROOT, rel)
        if not check_or('OfferCatalog: %s missing' % rel, os.path.isfile(path)):
            continue
        html = open(path, encoding='utf-8').read()
        check(html.count(LD_BEGIN) == 1 and html.count(LD_END) == 1,
              'OfferCatalog: SRX markers missing/duplicated on %s' % rel)
        m = re.search(re.escape(LD_BEGIN) + r'(.*?)' + re.escape(LD_END), html, re.S)
        if not m:
            continue
        jm = re.search(r'<script type="application/ld\+json">(.*?)</script>', m.group(1), re.S)
        if not check_or('OfferCatalog: JSON-LD block not found in markers on %s' % rel, bool(jm)):
            continue
        try:
            data = json.loads(jm.group(1))
        except ValueError as exc:
            issues.append('OfferCatalog: JSON broken on %s - %s' % (rel, exc))
            continue
        check(data.get('@type') == 'OfferCatalog',
              'OfferCatalog: wrong @type %r on %s' % (data.get('@type'), rel))
        items = data.get('itemListElement', [])
        check(len(items) >= 5, 'OfferCatalog: only %d offers on %s' % (len(items), rel))
        for it in items:
            svc = (it.get('itemOffered') or {})
            check(it.get('@type') == 'Offer' and svc.get('@type') == 'Service'
                  and svc.get('name') and svc.get('serviceType'),
                  'OfferCatalog: malformed itemListElement on %s' % rel)
        check(str(data.get('provider', {}).get('@id', '')).endswith('#organization'),
              'OfferCatalog: provider does not reference the Organization on %s' % rel)
        cid = data.get('@id')
        check(cid and cid not in seen_ids, 'OfferCatalog: @id missing/duplicated (%s) on %s' % (cid, rel))
        seen_ids.add(cid)
        check('FAQPage' in html and '#organization' in html,
              'OfferCatalog: pre-existing FAQPage/Organization blocks lost on %s' % rel)


def main():
    audit_indexnow()
    audit_vcard()
    audit_offer_catalog()

    print('=' * 70)
    print('SEO discovery assets: IndexNow key / vCard / OfferCatalog')
    print('=' * 70)
    if issues:
        for i in issues:
            print('  X ' + i)
        print('-' * 70)
        print('FAILED - %d issue(s). See scripts/check_seo_assets.py docstring.' % len(issues))
        return 1
    print('  IndexNow key file: present, name/content match, publish-required')
    print('  vCard: RFC 6350 wire format + discovery links on %d landing pages'
          % len(LANDING_PAIRS))
    print('  OfferCatalog: valid JSON-LD with %d+ services on %d landing pages'
          % (5, len(LANDING_PAIRS)))
    print('=' * 70)
    print('PASSED - discovery assets intact.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
