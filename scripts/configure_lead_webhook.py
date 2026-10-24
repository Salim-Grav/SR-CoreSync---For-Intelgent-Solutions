# -*- coding: utf-8 -*-
"""
Configure the independent lead relay (the second alert channel)
==============================================================
The worker already posts every lead to `LEAD_WEBHOOK_URLS`. That URL is the only
piece missing, and it lives in a workspace variable rather than a secret, so it
can be set without another prompt session.

  python scripts/configure_lead_webhook.py --url https://hook.eu1.make.com/abc
  python scripts/configure_lead_webhook.py --url https://a, https://b
  python scripts/configure_lead_webhook.py --show
  python scripts/configure_lead_webhook.py --remove

After setting it the worker is redeployed and /health reports the relay count.
"""
import argparse
import io
import os
import re
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER = os.path.join(ROOT, 'workers', 'sr-lead-capture')
WRANGLER = os.path.join(WORKER, 'node_modules', 'wrangler', 'bin', 'wrangler.js')
TOML = os.path.join(WORKER, 'wrangler.toml')
HEALTH = 'https://sr-lead-capture.sr-coresync.workers.dev/health'
UA = {'User-Agent': 'S&R-CoreSync-Check/1.0'}


def read_toml():
    raw = open(TOML, 'rb').read()
    return raw.decode('utf-8').replace('\r\n', '\n'), (b'\r\n' in raw)


def write_toml(text, had_crlf):
    out = text.replace('\n', '\r\n') if had_crlf else text
    open(TOML, 'wb').write(out.encode('utf-8'))


def current():
    text, _ = read_toml()
    match = re.search(r'(?m)^LEAD_WEBHOOK_URLS\s*=\s*"([^"]*)"', text)
    return match.group(1) if match else ''


def set_var(value):
    text, had_crlf = read_toml()
    line = 'LEAD_WEBHOOK_URLS = "%s"' % value if value else None
    pattern = re.compile(r'(?m)^#?\s*LEAD_WEBHOOK_URLS\s*=\s*"[^"]*"')
    if pattern.search(text):
        text = pattern.sub(line if line else '# LEAD_WEBHOOK_URLS = ""', text, count=1)
    elif line:
        text = text.replace('[vars]', '[vars]\n' + line, 1)
    write_toml(text, had_crlf)


def deploy():
    res = subprocess.run(['node', WRANGLER, 'deploy'], cwd=WORKER,
                         capture_output=True, text=True)
    tail = (res.stdout or '') + (res.stderr or '')
    return res.returncode == 0, tail.strip().splitlines()[-1] if tail.strip() else ''


def health():
    req = urllib.request.Request(HEALTH, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return __import__('json').loads(res.read().decode('utf-8'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='one or more comma separated https endpoints')
    ap.add_argument('--remove', action='store_true')
    ap.add_argument('--show', action='store_true')
    ap.add_argument('--no-deploy', action='store_true')
    args = ap.parse_args()

    print('=' * 68)
    print('S&R CoreSync — independent lead relay')
    print('=' * 68)

    if args.show or (not args.url and not args.remove):
        value = current()
        print('  configured urls : %s' % (value or '(none)'))
        try:
            state = health()
            print('  worker reports  : webhooks=%s' % state.get('webhooks'))
        except Exception as err:
            print('  worker          : unreachable (%s)' % err)
        return 0

    if args.remove:
        set_var('')
        print('  removed LEAD_WEBHOOK_URLS')
    else:
        urls = [u.strip().rstrip('/') for u in args.url.split(',') if u.strip()]
        bad = [u for u in urls if not u.startswith('https://')]
        if bad:
            raise SystemExit('Only https endpoints are accepted: %s' % ', '.join(bad))
        set_var(', '.join(urls))
        print('  set %d endpoint(s)' % len(urls))

    if args.no_deploy:
        print('  deploy skipped (--no-deploy)')
        return 0

    ok, line = deploy()
    print('  deploy          : %s' % ('ok' if ok else 'FAILED: ' + line))
    if ok:
        try:
            state = health()
            print('  worker reports  : webhooks=%s' % state.get('webhooks'))
        except Exception:
            pass
    print('=' * 68)
    print('Test: submit a lead and watch notify_status become sent:webhook')
    print('      when Telegram is unavailable.')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
