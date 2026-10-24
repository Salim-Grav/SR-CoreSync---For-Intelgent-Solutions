# -*- coding: utf-8 -*-
"""
Mail readiness checker with provider profiles
============================================
Answers "is the mail setup correct right now?" from DNS alone, per provider, and
prints the exact record sheet that has to exist in the Hostinger panel.

  python scripts/check_mail_setup.py                # auto-detect + verdict
  python scripts/check_mail_setup.py --profile zoho # check against Zoho EU
  python scripts/check_mail_setup.py --guide zoho   # print the record sheet

No credentials, no DNS writes: this only measures and instructs.
"""
import argparse
import json
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UA = {'User-Agent': 'S&R-CoreSync-Check/1.0'}
DOMAIN = 'sr-coresync.com'
ADDRESSES = ('info', 'support', 'billing')

PROFILES = {
    'zoho': {
        'label': 'Zoho Mail (EU)',
        'mx': ['mx.zoho.eu', 'mx2.zoho.eu', 'mx3.zoho.eu'],
        'spf_include': 'include:zoho.eu',
        'dkim_selector': 'zoho._domainkey',
        'guide': [
            ('MX', '@', 'mx.zoho.eu', 'priority 10  — primary'),
            ('MX', '@', 'mx2.zoho.eu', 'priority 20 — backup'),
            ('MX', '@', 'mx3.zoho.eu', 'priority 50 — backup'),
            ('TXT', '@', 'v=spf1 include:zoho.eu ~all', 'REPLACE the current SPF'),
            ('TXT', '@', 'zoho-verification=zb<id>.zmverify.zoho.eu', 'from Zoho -> Domains -> Verification'),
            ('TXT', 'zoho._domainkey', '<value from Zoho Mail Admin -> Email Authentication>', 'DKIM, 2048-bit'),
            ('TXT', '_dmarc', 'v=DMARC1; p=none; rua=mailto:dmarc@sr-coresync.com; pct=100', 'start with monitoring'),
        ],
        'note': 'Keep mx1.improvmx.com at priority 90 for one week as a fallback:',
        'note2': 'mail goes to the lowest priority first, so nothing is lost if Zoho rejects.',
    },
    'hostinger': {
        'label': 'Hostinger Email',
        'mx': ['mx1.hostinger.com', 'mx2.hostinger.com'],
        'spf_include': 'include:_spf.mail.hostinger.com',
        'dkim_selector': 'hostingermail-a._domainkey',
        'guide': [
            ('MX', '@', 'mx1.hostinger.com', 'priority 5'),
            ('MX', '@', 'mx2.hostinger.com', 'priority 10'),
            ('TXT', '@', 'v=spf1 include:_spf.mail.hostinger.com ~all', 'REPLACE the current SPF'),
            ('CNAME', 'hostingermail-a._domainkey', 'hostingermail-a._domainkey.hostinger.com', 'DKIM A'),
            ('CNAME', 'hostingermail-b._domainkey', 'hostingermail-b._domainkey.hostinger.com', 'DKIM B'),
            ('CNAME', 'autodiscover', 'autodiscover.mail.hostinger.com', 'Outlook autodiscover'),
            ('TXT', '_dmarc', 'v=DMARC1; p=none; rua=mailto:dmarc@sr-coresync.com; pct=100', 'start with monitoring'),
        ],
        'note': '',
        'note2': '',
    },
}


def dns(name, rtype):
    url = 'https://dns.google/resolve?name=%s&type=%s' % (name, rtype)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode('utf-8')).get('Answer', []) or []


def txt(name):
    return [a['data'].strip('"').replace('" "', '') for a in dns(name, 'TXT')]


def gather():
    mx_records = dns(DOMAIN, 'MX')
    mx = []
    for record in mx_records:
        parts = record['data'].split()
        mx.append((int(parts[0]), parts[-1].rstrip('.')))
    return {
        'mx': sorted(mx),
        'spf': next((t for t in txt(DOMAIN) if t.lower().startswith('v=spf1')), None),
        'dmarc': next((t for t in txt('_dmarc.' + DOMAIN) if t.lower().startswith('v=dmarc1')), None),
        'txt_root': txt(DOMAIN),
    }


def detect(state):
    joined = ' '.join(host for _, host in state['mx']).lower()
    for key in ('zoho', 'hostinger'):
        if key in joined:
            return key
    if 'improvmx' in joined:
        return 'improvmx'
    if 'google' in joined:
        return 'google'
    if 'outlook' in joined:
        return 'microsoft'
    return 'unknown'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--profile', choices=sorted(PROFILES))
    ap.add_argument('--guide', choices=sorted(PROFILES))
    args = ap.parse_args()

    if args.guide:
        profile = PROFILES[args.guide]
        print('=' * 80)
        print('Record sheet — %s  (%s)' % (profile['label'], DOMAIN))
        print('=' * 80)
        print('  %-6s %-30s %-44s %s' % ('TYPE', 'HOST (Hostinger name)', 'VALUE', 'NOTE'))
        for rtype, host, value, note in profile['guide']:
            print('  %-6s %-30s %-44s %s' % (rtype, host, value[:44], note))
        if profile['note']:
            print('-' * 80)
            print(' ' + profile['note'])
            print(' ' + profile['note2'])
        print('=' * 80)
        print('Then: python scripts/check_mail_setup.py --profile %s' % args.guide)
        return 0

    state = gather()
    current = detect(state)
    profile_key = args.profile or (current if current in PROFILES else None)

    print('=' * 80)
    print('Mail readiness — %s' % DOMAIN)
    print('=' * 80)
    print('  MX      : %s' % (', '.join('%d %s' % m for m in state['mx']) or 'NONE'))
    print('  SPF     : %s' % (state['spf'] or 'MISSING'))
    print('  DMARC   : %s' % (state['dmarc'] or 'MISSING'))
    print('  detected: %s' % current)

    if not profile_key:
        print('-' * 80)
        print('  This is not a mailbox provider: forwarding only.')
        print('  Run: python scripts/check_mail_setup.py --guide zoho')
        print('=' * 80)
        return 1

    profile = PROFILES[profile_key]
    checks = []

    hosts = [host for _, host in state['mx']]
    primary = [h for h in profile['mx'][:2] if h in hosts]
    checks.append(('MX points at %s' % profile['label'], len(primary) >= 1,
                   ', '.join(hosts) or 'none'))
    stray = [h for h in hosts if h not in profile['mx'] and 'improvmx' not in h]
    checks.append(('no foreign MX left', not stray, ', '.join(stray) or 'clean'))
    fallback = [h for h in hosts if 'improvmx' in h]
    if fallback:
        checks.append(('temporary ImprovMX fallback (remove after a week)', False,
                       ', '.join(fallback)))

    spf = state['spf'] or ''
    checks.append(('SPF authorises %s' % profile['spf_include'], profile['spf_include'] in spf, spf or 'missing'))
    if 'improvmx' in spf:
        checks.append(('SPF no longer includes the forwarder', False, 'include:spf.improvmx.com still present'))

    dkim = txt(profile['dkim_selector'] + '.' + DOMAIN) or dns(profile['dkim_selector'] + '.' + DOMAIN, 'CNAME')
    checks.append(('%s publishes DKIM' % profile['dkim_selector'], bool(dkim), 'present' if dkim else 'missing'))

    checks.append(('DMARC published', bool(state['dmarc']), (state['dmarc'] or 'missing')[:60]))

    print('-' * 80)
    failed = 0
    for label, ok, detail in checks:
        print('  [%s] %-52s %s' % ('PASS' if ok else 'TODO', label[:52], detail[:40]))
        if not ok:
            failed += 1

    print('-' * 80)
    print('  addresses: %s' % ', '.join(a + '@' + DOMAIN for a in ADDRESSES))
    print('  note     : DNS cannot prove a mailbox exists - send a real test')
    print('             message to each address and check the webmail.')
    print('=' * 80)
    print('PASSED - mail records are in place' if failed == 0
          else 'INCOMPLETE - %d item(s) pending; guide: --guide %s' % (failed, profile_key))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
