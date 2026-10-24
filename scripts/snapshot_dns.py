# -*- coding: utf-8 -*-
"""
DNS snapshot and drift guard
============================
A DNS reset took the website and the mail routing down in one click today, and
nothing noticed until someone looked. This records the records that must exist
and fails when any of them disappear or change.

  python scripts/snapshot_dns.py --save     # record the current state
  python scripts/snapshot_dns.py            # compare, exit 1 on drift
  python scripts/snapshot_dns.py --verbose  # show every record it checks
"""
import argparse
import json
import os
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UA = {'User-Agent': 'S&R-CoreSync-Check/1.0'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT = os.path.join(ROOT, 'dns-snapshot.json')
DOMAIN = 'sr-coresync.com'

RESOLVERS = (
    ('https://dns.google/resolve?name=%s&type=%s', {}),
    ('https://cloudflare-dns.com/dns-query?name=%s&type=%s', {'accept': 'application/dns-json'}),
)

# name -> (record type, must exist)
CHECKS = [
    (DOMAIN, 'A'),
    (DOMAIN, 'MX'),
    (DOMAIN, 'TXT'),
    ('www.' + DOMAIN, 'CNAME'),
    ('_dmarc.' + DOMAIN, 'TXT'),
    # DKIM is published as a CNAME to Purelymail's key host; losing these
    # silently breaks outbound signing, so they are guarded too.
    ('purelymail1._domainkey.' + DOMAIN, 'CNAME'),
    ('purelymail2._domainkey.' + DOMAIN, 'CNAME'),
    ('purelymail3._domainkey.' + DOMAIN, 'CNAME'),
    ('_dmarc.' + DOMAIN, 'CNAME'),
]


def dns(name, rtype):
    values = []
    for template, extra in RESOLVERS:
        try:
            headers = dict(UA)
            headers.update(extra)
            req = urllib.request.Request(template % (name, rtype), headers=headers)
            with urllib.request.urlopen(req, timeout=20) as res:
                payload = json.loads(res.read().decode('utf-8'))
        except Exception:
            continue
        for answer in payload.get('Answer', []) or []:
            data = answer.get('data', '').strip('"')
            if data and data not in values:
                values.append(data)
    return sorted(values)


def collect():
    state = {}
    for name, rtype in CHECKS:
        state['%s %s' % (rtype, name)] = dns(name, rtype)
    return state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--save', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    current = collect()

    if args.save:
        with open(SNAPSHOT, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump({'domain': DOMAIN, 'records': current}, fh, indent=2, ensure_ascii=False)
            fh.write('\n')
        print('snapshot written: dns-snapshot.json (%d groups)' % len(current))
        for key, values in current.items():
            print('  %-28s %d record(s)' % (key, len(values)))
        return 0

    if not os.path.isfile(SNAPSHOT):
        raise SystemExit('No dns-snapshot.json yet. Run: python scripts/snapshot_dns.py --save')

    with open(SNAPSHOT, encoding='utf-8') as fh:
        expected = json.load(fh).get('records', {})

    print('=' * 70)
    print('DNS drift check — %s' % DOMAIN)
    print('=' * 70)

    problems = []
    for key, want in expected.items():
        have = current.get(key, [])
        missing = [w for w in want if w not in have]
        if not want:
            continue
        if missing:
            problems.append((key, want, have, missing))
            print('  DRIFT  %-28s missing %d of %d record(s)' % (key, len(missing), len(want)))
            for value in missing:
                print('           - %s' % value[:88])
        elif args.verbose:
            print('  OK     %-28s %d record(s)' % (key, len(have)))

    print('-' * 70)
    if problems:
        print('FAILED - %d group(s) changed since the snapshot.' % len(problems))
        print('Site: https://%s   Mail: check MX and TXT above.' % DOMAIN)
        return 1
    print('PASSED - every recorded DNS record is still published.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
