# -*- coding: utf-8 -*-
"""Check that every address the site publishes really exists as a mailbox.

DNS proves routing, not mailboxes: MX 50 can point at Purelymail while
support@ is missing and every message to it bounces.  The site publishes
info@ / support@ / billing@ in dozens of places, so this compares that list
against Purelymail's own account API.

Token (Purelymail -> Settings -> API tokens), one of:
    setx PURELYMAIL_API_TOKEN "..."          # permanent, new shells only
    $env:PURELYMAIL_API_TOKEN = "..."        # this shell
    .secrets/purelymail-token.txt            # git-ignored file, one line

  python scripts/check_mailboxes.py
  python scripts/check_mailboxes.py --verbose      # show every scanned address
  python scripts/check_mailboxes.py --only info@sr-coresync.com
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'sr-coresync.com'
API = 'https://purelymail.com/api/v0/listUser'
TOKEN_FILE = os.path.join(ROOT, '.secrets', 'purelymail-token.txt')
ADDRESS_RE = re.compile(r'[a-z0-9._%+-]+@' + re.escape(DOMAIN), re.I)
SKIP_DIRS = {'.git', 'node_modules', '.zwork', '.venv', '__pycache__'}
# Files that never reach a visitor: runbooks, worker code and deploy config.
INTERNAL_DIRS = ('workers', 'scripts', 'dist', '.github')
INTERNAL_FILES = {'MAIL-MIGRATION-STATE.md', 'dns-snapshot.json'}


def api(token, endpoint=API, payload=None):
    body = json.dumps(payload or {}).encode('utf-8')
    req = urllib.request.Request(
        endpoint, data=body, method='POST',
        headers={'Purelymail-Api-Token': token, 'content-type': 'application/json'})
    with urllib.request.urlopen(req, timeout=25) as res:
        return json.loads(res.read().decode('utf-8'))


def read_token(explicit):
    if explicit:
        return explicit.strip()
    env = os.environ.get('PURELYMAIL_API_TOKEN', '').strip()
    if env:
        return env
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, encoding='utf-8') as fh:
            return fh.read().strip()
    return ''


def published_addresses():
    """@sr-coresync.com addresses, split into what a visitor can see and what cannot.

    A bouncing support@ is a customer problem; a bouncing security@ inside a
    runbook is not, so only publicly served files count as required mailboxes.
    """
    found = {}
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in INTERNAL_FILES or not name.lower().endswith(
                    ('.html', '.js', '.json', '.md', '.txt', '.xml', '.yml', '.yaml', '.py')):
                continue
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ROOT)
            internal = rel.lower().endswith(('.md', '.py', '.yml', '.yaml')) or \
                rel.split(os.sep)[0].lower() in INTERNAL_DIRS
            try:
                if os.path.getsize(path) > 4 * 1024 * 1024:
                    continue
                with open(path, encoding='utf-8', errors='ignore') as fh:
                    text = fh.read()
            except OSError:
                continue
            for match in ADDRESS_RE.findall(text):
                bucket = found.setdefault(match.lower(), {'public': set(), 'internal': set()})
                bucket['internal' if internal else 'public'].add(rel)
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--token')
    ap.add_argument('--only', nargs='*', help='check these addresses instead of scanning')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--scan-only', action='store_true', help='list published addresses without calling the API')
    args = ap.parse_args()

    if args.scan_only:
        published = published_addresses()
        print('%d address(es) reference %s' % (len(published), DOMAIN))
        for addr in sorted(published, key=lambda a: (-len(published[a]['public']), a)):
            bucket = published[addr]
            print('  %-30s public: %-3d internal: %d' % (addr, len(bucket['public']), len(bucket['internal'])))
        return 0

    token = read_token(args.token)
    if not token:
        print('No API token.')
        print('  Purelymail -> Settings -> API tokens -> create one, then:')
        print('  $env:PURELYMAIL_API_TOKEN = "..."     (or write it to .secrets/purelymail-token.txt)')
        return 2

    try:
        reply = api(token)
    except urllib.error.HTTPError as exc:
        print('API rejected the request: HTTP %s' % exc.code)
        return 2
    except (urllib.error.URLError, OSError) as exc:
        print('cannot reach the Purelymail API: %s' % exc)
        return 2

    if reply.get('type') == 'error':
        print('API error: %s — %s' % (reply.get('code'), reply.get('message')))
        if reply.get('code') == 'invalidToken':
            print('  the token was revoked or mistyped; create a fresh one in Settings -> API tokens.')
        return 2

    users = {u.get('user', '').lower() for u in reply.get('result', {}).get('users', []) or []}
    if args.only:
        required = {a.lower() for a in args.only}
        sources = {}
    else:
        published = published_addresses()
        # only addresses a visitor can read must have a mailbox
        required = {a for a, b in published.items() if b['public']}
        sources = published

    print('=' * 72)
    print('Mailboxes on Purelymail — %s' % DOMAIN)
    print('=' * 72)
    print('  %d mailbox(es) in the account' % len(users))
    if args.verbose:
        for user in sorted(users):
            print('    - %s' % user)

    missing = sorted(a for a in required if a not in users)
    print('-' * 72)
    for addr in sorted(required):
        ok = addr in users
        mark = 'OK  ' if ok else 'MISS'
        note = ''
        if not ok and sources.get(addr):
            where = sorted(sources[addr]['public'])
            note = '  ← on the website: %s%s' % (
                ', '.join(where[:3]), '…' if len(where) > 3 else '')
        print('  [%s] %s%s' % (mark, addr, note))

    print('-' * 72)
    if missing:
        print('MISSING - %d published address(es) have no mailbox:' % len(missing))
        for addr in missing:
            print('  %s  ->  Purelymail -> Users -> Create new user -> username "%s"'
                  % (addr, addr.split('@')[0]))
        print('Mail sent to those addresses bounces. Create them, or add a routing rule.')
        return 1

    print('PASSED - every published address has a mailbox.')
    extra = sorted(u for u in users if u.endswith('@' + DOMAIN) and u not in required)
    if extra:
        print('  (also present, not published on the site: %s)' % ', '.join(extra))
    internal_only = sorted(a for a, b in sources.items() if not b['public'])
    if internal_only:
        print('  (runbook/config only, mail not required: %s)' % ', '.join(internal_only))
    return 0


if __name__ == '__main__':
    sys.exit(main())
