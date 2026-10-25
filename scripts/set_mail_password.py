# -*- coding: utf-8 -*-
"""Set the mailbox password as a Worker secret, then prove it works.

The password is read with getpass (never echoed, never written to disk, never
part of the command line), so it does not end up in the shell history or in a
chat log. After storing it, the script authenticates against Purelymail through
the deployed worker and prints the outcome.

  python scripts/set_mail_password.py
  python scripts/set_mail_password.py --user support@sr-coresync.com

Use it after changing the mailbox password in Purelymail, which is the one step
that cannot be automated: their API exposes createAppPassword and modifyUser but
no password endpoint.
"""
import argparse
import getpass
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER_DIR = os.path.join(ROOT, 'workers', 'sr-lead-capture')
WRANGLER = os.path.join(WORKER_DIR, 'node_modules', 'wrangler', 'bin', 'wrangler.js')
BASE = 'https://sr-lead-capture.sr-coresync.workers.dev'
UA = 'SR-CoreSync-QA/1.0 (+https://sr-coresync.com)'


def set_secret(value):
    res = subprocess.run(
        ['node', WRANGLER, 'secret', 'put', 'PURELYMAIL_PASS'],
        cwd=WORKER_DIR, input=value + '\n',
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    ok = res.returncode == 0 and 'Success' in (res.stdout or '')
    return ok, (res.stdout or res.stderr or '')[-300:]


def verify():
    req = urllib.request.Request(BASE + '/mail/check?deep=1',
                                 headers={'origin': 'https://sr-coresync.com', 'user-agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as res:
            return json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        return json.loads(exc.read().decode('utf-8', 'replace') or '{}')
    except OSError as exc:
        return {'ok': False, 'reason': str(exc)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', default='info@sr-coresync.com')
    ap.add_argument('--skip-verify', action='store_true')
    args = ap.parse_args()

    value = os.environ.get('PURELYMAIL_NEW_PASS')
    if not value:
        if not sys.stdin.isatty():
            print('No terminal to prompt on. Set PURELYMAIL_NEW_PASS or run it interactively.')
            return 2
        print('Mailbox: %s' % args.user)
        value = getpass.getpass('New password (hidden): ')
        again = getpass.getpass('Repeat to be sure      : ')
        if value != again:
            print('The two entries differ — nothing was changed.')
            return 2
    value = value.strip()
    if not value:
        print('Empty password — nothing was changed.')
        return 2

    ok, detail = set_secret(value)
    if not ok:
        print('Could not store the secret:\n%s' % detail)
        return 1
    print('Secret PURELYMAIL_PASS stored.')

    if args.skip_verify:
        return 0

    print('Authenticating against smtp.purelymail.com …')
    result = verify()
    if result.get('reason') == 'throttled':
        # The worker allows one real handshake every five minutes. Waiting is
        # better than reporting "unknown" right after the owner rotated a key.
        wait = min(int(result.get('retryInSeconds') or 20), 120)
        print('  a check ran recently; waiting %ds for a fresh one …' % wait)
        time.sleep(wait + 1)
        result = verify()

    if result.get('verified'):
        print('Verified — steps: %s' % ','.join(result.get('steps') or []))
        print('Mail notifications now send from %s.' % result.get('user'))
        return 0

    reason = result.get('reason') or 'unknown'
    print('Not verified: %s' % reason)
    print('  steps reached: %s' % (','.join(result.get('steps') or []) or '—'))
    if reason == 'throttled':
        print('  A real check ran in the last five minutes; wait a moment and retry.')
    elif '535' in str(reason):
        print('  The mailbox rejected this password. Check it in Purelymail → Users.')
    return 3


if __name__ == '__main__':
    sys.exit(main())
