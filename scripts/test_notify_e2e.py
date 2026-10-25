# -*- coding: utf-8 -*-
"""End-to-end check of the notification path: form -> D1 -> Telegram -> mailbox.

The site's promise is "a real enquiry reaches a human". DNS checks cannot see
that promise, and neither can a screenshot, so this posts one enquiry carrying a
TEST marker, reads back what the worker recorded, asks the worker to prove the
mailbox sends, and can remove its own trace afterwards.

  python scripts/test_notify_e2e.py             # post, verify, keep the row
  python scripts/test_notify_e2e.py --cleanup   # ... and delete it again
  python scripts/test_notify_e2e.py --cleanup-only

Only rows carrying this run's marker are deleted.
"""
import argparse
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
MARKER = 'SR Self-Test'
# Cloudflare answers 1010 to the default Python-urllib signature, so the probe
# identifies itself instead of pretending to be a browser.
UA = 'SR-CoreSync-QA/1.0 (+https://sr-coresync.com)'


def _request(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status, json.loads(res.read().decode('utf-8') or '{}')
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode('utf-8', 'replace')
        try:
            return exc.code, json.loads(raw or '{}')
        except json.JSONDecodeError:
            return exc.code, {'status': 'error', 'reason': raw.strip()[:200]}


def post_lead(lead):
    body = json.dumps(lead).encode('utf-8')
    return _request(urllib.request.Request(
        BASE + '/lead', data=body, method='POST',
        headers={'content-type': 'application/json', 'origin': 'https://sr-coresync.com',
                 'user-agent': UA}), 30)


def get_json(path, timeout=60):
    return _request(urllib.request.Request(
        BASE + path,
        headers={'origin': 'https://sr-coresync.com', 'user-agent': UA}), timeout)


def d1(sql):
    res = subprocess.run(
        ['node', WRANGLER, 'd1', 'execute', 'sr-coresync', '--remote', '--json', '--command', sql],
        cwd=WORKER_DIR, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        raise SystemExit('D1 failed:\n%s' % (res.stderr or res.stdout)[-500:])
    text = res.stdout
    return json.loads(text[text.find('['):])[0].get('results', [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleanup', action='store_true', help='delete the test row when finished')
    ap.add_argument('--cleanup-only', action='store_true', help='only delete test rows')
    ap.add_argument('--wait', type=int, default=6, help='seconds to wait before reading D1')
    ap.add_argument('--notes', default='Automated end-to-end test of the notification path. Not a real enquiry.',
                    help='enquiry text; keyword routing reads this')
    args = ap.parse_args()

    if args.cleanup_only:
        rows = d1("SELECT lead_id FROM leads WHERE client_name LIKE '%" + MARKER + "%'")
        print('test rows found: %d' % len(rows))
        if rows:
            d1("DELETE FROM leads WHERE client_name LIKE '%" + MARKER + "%'")
            print('deleted %d row(s)' % len(rows))
        return 0

    stamp = time.strftime('%Y%m%d-%H%M%S')
    lead = {
        'clientName': '%s %s' % (MARKER, stamp),
        'email': 'self-test@sr-coresync.com',
        'phone': '+31000000000',
        'companyName': 'Internal QA',
        'package': 'self-test',
        'language': 'ar',
        'sourceUrl': 'https://sr-coresync.com/status.html',
        'notes': args.notes,
        'website': ''
    }

    print('=' * 74)
    print('Notification path — end to end')
    print('=' * 74)

    status, body = post_lead(lead)
    lead_id = body.get('leadId')
    print('  POST /lead            -> %s  leadId=%s  recorded=%s  announced=%s'
          % (status, lead_id, body.get('recorded'), body.get('announced')))
    if status != 200 or not lead_id:
        print('  the worker rejected the enquiry: %s' % json.dumps(body, ensure_ascii=False)[:300])
        return 1

    time.sleep(args.wait)

    safe_id = str(lead_id).replace("'", '')
    rows = d1("SELECT lead_id, client_name, notify_status, notified_at FROM leads "
              "WHERE lead_id = '" + safe_id + "'")
    if not rows:
        print('  D1 row                -> NOT found')
    else:
        row = rows[0]
        print('  D1 row                -> %s | notify_status=%s | notified_at=%s'
              % (row.get('lead_id'), row.get('notify_status'), row.get('notified_at')))

    _h, health = get_json('/health')
    print('  /health               -> telegram=%s  emailChannel=%s  purelymail=%s'
          % (health.get('telegram'), health.get('emailChannel'), health.get('purelymail')))

    _c, check = get_json('/mail/check?deep=1', timeout=90)
    if not check.get('configured'):
        print('  /mail/check           -> email channel NOT configured (%s)' % check.get('reason'))
    else:
        print('  /mail/check?deep=1    -> verified=%s  steps=%s  reason=%s'
              % (check.get('verified'), ','.join(check.get('steps') or []) or '—', check.get('reason') or '—'))

    _s, self_test = get_json('/mail/selftest', timeout=180)
    if self_test.get('ok'):
        print('  /mail/selftest        -> SENT to %s via %s (steps: %s)'
              % (self_test.get('to'), self_test.get('provider'),
                 ','.join(self_test.get('steps') or [])))
    elif self_test.get('reason') == 'throttled':
        print('  /mail/selftest        -> throttled (a real message went out <10 min ago)')
    else:
        print('  /mail/selftest        -> not sent (%s)' % self_test.get('reason'))

    print('-' * 74)
    telegram_ok = bool(rows and rows[0].get('notify_status') in ('sent', 'resent', 'sent:webhook'))
    mail_ok = bool(self_test.get('ok')) or self_test.get('reason') == 'throttled'
    print('  verdict: enquiry %s · telegram %s · email %s'
          % ('captured' if rows else 'NOT captured',
             'sent' if telegram_ok else 'not marked sent',
             'sent' if self_test.get('ok') else ('working (throttled)' if mail_ok else 'not configured')))

    if args.cleanup:
        d1("DELETE FROM leads WHERE client_name LIKE '%" + MARKER + "%'")
        print('  cleanup: test rows deleted')

    return 0 if (rows and telegram_ok and mail_ok) else 2


if __name__ == '__main__':
    sys.exit(main())
