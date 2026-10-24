import collections
import json
import sys
import urllib.request

sys.path.insert(0, 'scripts')

UA = {'User-Agent': 'S&R-CoreSync-Check/1.0'}
DOMAIN = 'sr-coresync.com'
ADDRESSES = ['info@sr-coresync.com', 'support@sr-coresync.com', 'billing@sr-coresync.com']


def dns(name, rtype):
    url = 'https://dns.google/resolve?name=%s&type=%s' % (name, rtype)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode('utf-8')).get('Answer', []) or []


def txt(name):
    return [a['data'].strip('"').replace('" "', '') for a in dns(name, 'TXT')]


def main():
    print('=' * 74)
    print('S&R CoreSync — mail readiness for %s' % DOMAIN)
    print('=' * 74)

    mx = sorted(a['data'].split()[-1].rstrip('.') for a in dns(DOMAIN, 'MX'))
    print('MX              : %s' % (', '.join(mx) or 'NONE'))

    spf = next((t for t in txt(DOMAIN) if t.lower().startswith('v=spf1')), None)
    print('SPF             : %s' % (spf or 'MISSING'))

    dmarc = next((t for t in txt('_dmarc.' + DOMAIN) if t.lower().startswith('v=dmarc1')), None)
    print('DMARC           : %s' % (dmarc or 'MISSING'))

    dkim = []
    for selector in ('hostingermail-a', 'hostingermail-b', 'resend', 'mail', 'zoho', 'google', 'selector1', 'selector2'):
        name = '%s._domainkey.%s' % (selector, DOMAIN)
        if dns(name, 'TXT') or dns(name, 'CNAME'):
            dkim.append(selector)
    print('DKIM selectors  : %s' % (', '.join(dkim) or 'MISSING'))

    print('-' * 74)
    print('adresses that must answer: %s' % ', '.join(a.split('@')[0] for a in ADDRESSES))

    provider = 'unknown'
    joined = ' '.join(mx).lower()
    if 'improvmx' in joined:
        provider = 'improvmx (forwarding only: no mailbox, no sending)'
    elif 'hostinger' in joined:
        provider = 'hostinger (real mailboxes)'
    elif 'zoho' in joined:
        provider = 'zoho (real mailboxes)'
    elif 'google' in joined:
        provider = 'google workspace (real mailboxes)'
    elif 'outlook' in joined or 'protection.outlook' in joined:
        provider = 'microsoft 365 (real mailboxes)'
    print('provider        : %s' % provider)
    print('=' * 74)

    verdict = []
    if 'forwarding' in provider or not mx:
        verdict.append('Receiving: forwarding only - info@/support@/billing@ must be created as')
        verdict.append('           aliases, and replies leave from the fallback inbox.')
        verdict.append('Sending  : impossible from the domain itself (no SMTP, no DKIM).')
    else:
        verdict.append('Receiving: mailbox provider in MX - verify each address exists.')
        if not dkim:
            verdict.append('Sending  : SMTP possible but DKIM is missing -> deliverability risk.')
    if not dmarc:
        verdict.append('DMARC    : absent -> no spoofing protection, Gmail bulk rules unmet.')

    for line in verdict:
        print(line)
    print('=' * 74)
    return 0


if __name__ == '__main__':
    sys.exit(main())
