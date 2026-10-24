# -*- coding: utf-8 -*-
"""
Telegram alert setup — one command
=================================
Turns four manual steps into one:

    python scripts/setup_telegram.py --apply

  1. asks for the bot token with hidden input (never echoed, never written)
  2. calls getMe + getUpdates to find your chat id
  3. writes both secrets with `wrangler secret put` (token on stdin only)
  4. redeploys the worker and confirms /health now reports telegram: true

Without --apply it only inspects and prints the commands, so nothing is written.

Usage:
  python scripts/setup_telegram.py              # inspect + instructions
  python scripts/setup_telegram.py --apply      # do it
  python scripts/setup_telegram.py --test       # check the deployed worker
"""
import argparse
import getpass
import json
import os
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER_DIR = os.path.join(ROOT, 'workers', 'sr-lead-capture')
WRANGLER = os.path.join(WORKER_DIR, 'node_modules', 'wrangler', 'bin', 'wrangler.js')
API = 'https://api.telegram.org/bot%s/%s'
HEALTH = 'https://sr-lead-capture.sr-coresync.workers.dev/health'
UA = {'User-Agent': 'S&R-CoreSync-Check/1.0'}


def telegram(token, method):
    req = urllib.request.Request(API % (token, method), headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode('utf-8'))


def health():
    req = urllib.request.Request(HEALTH, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode('utf-8'))


def notify_check():
    req = urllib.request.Request(HEALTH.replace('/health', '/notify/check'), headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode('utf-8'))


def wrangler(args, stdin_text=None):
    res = subprocess.run(['node', WRANGLER] + args, cwd=WORKER_DIR,
                         input=stdin_text, capture_output=True, text=True)
    return res.returncode, (res.stdout or '') + (res.stderr or '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--test', action='store_true')
    ap.add_argument('--verify-only', action='store_true',
                    help='check a token against Telegram without writing anything')
    ap.add_argument('--token-env', metavar='VAR', help='read the token from this environment variable instead of prompting')
    args = ap.parse_args()

    if args.test:
        state = health()
        check = notify_check()
        print('telegram config  : %s' % state.get('telegram'))
        print('telegram valid   : %s' % check.get('ok'))
        print('bot              : %s' % (check.get('bot') or '-'))
        print('reason           : %s' % (check.get('reason') or '-'))
        print('mail channel     : %s' % state.get('emailChannel'))
        print('d1               : %s' % state.get('d1'))
        if not check.get('ok'):
            print()
            print('The token is stored but Telegram rejects it:')
            print('  python scripts/setup_telegram.py --verify-only   # check a new one')
            print('  python scripts/setup_telegram.py --apply         # then store it')
        return 0 if check.get('ok') else 1

    print('=' * 68)
    print('Telegram alerts' + (' — applying' if args.apply else ' — setup info'))
    print('=' * 68)

    env_name = args.token_env
    if env_name:
        token = (os.environ.get(env_name) or '').strip()
        if not token:
            raise SystemExit('Environment variable %s is empty.' % env_name)
        print('  token source       : $%s' % env_name)
    else:
        token = getpass.getpass('Paste bot token from @BotFather (hidden): ').strip()
    if ':' not in token:
        raise SystemExit('Not a bot token (expected something like 123456:ABC-…).')

    try:
        me = telegram(token, 'getMe')
    except Exception as err:
        detail = str(err)
        print('  RESULT             : INVALID')
        print('  telegram says      : %s' % detail)
        print('  -> the token is revoked, mistyped, or not the current one.')
        print('  -> in @BotFather send /token, pick the bot, copy the value it prints now.')
        raise SystemExit(1)

    if args.verify_only:
        print('  RESULT             : VALID')
        print('  bot                : @%s' % me['result'].get('username'))
        print('  nothing was written; run --apply to store it.')
        return 0
    if not me.get('ok'):
        raise SystemExit('Telegram rejected the token: %s' % me)
    bot = me['result'].get('username')
    print('  bot                : @%s' % bot)

    updates = telegram(token, 'getUpdates')
    chats = {}
    for item in updates.get('result', []):
        chat = ((item.get('message') or item.get('channel_post') or {}).get('chat') or {})
        if chat.get('id'):
            chats[chat['id']] = chat.get('title') or chat.get('username') or chat.get('first_name') or ''

    if not chats:
        print('-' * 68)
        print('  No chat yet: open @%s in Telegram, send it any message, re-run.' % bot)
        return 1

    for cid, name in chats.items():
        print('  chat found         : %-16s %s' % (cid, name))
    chat_id = list(chats.keys())[0]

    if not args.apply:
        print('-' * 68)
        print('  Run with --apply to write the secrets and deploy, or do it by hand:')
        print('    cd "workers/sr-lead-capture"')
        print('    node node_modules/wrangler/bin/wrangler.js secret put TELEGRAM_BOT_TOKEN')
        print('    node node_modules/wrangler/bin/wrangler.js secret put TELEGRAM_CHAT_ID   # %s' % chat_id)
        print('=' * 68)
        return 0

    print('-' * 68)
    code, out = wrangler(['secret', 'put', 'TELEGRAM_BOT_TOKEN'], stdin_text=token + '\n')
    print('  secret TELEGRAM_BOT_TOKEN : %s' % ('ok' if code == 0 else 'FAILED\n' + out[-400:]))
    code, out = wrangler(['secret', 'put', 'TELEGRAM_CHAT_ID'], stdin_text=str(chat_id) + '\n')
    print('  secret TELEGRAM_CHAT_ID   : %s' % ('ok' if code == 0 else 'FAILED\n' + out[-400:]))

    code, out = wrangler(['deploy'])
    print('  deploy                    : %s' % ('ok' if code == 0 else 'FAILED\n' + out[-400:]))

    state = health()
    print('  /health telegram          : %s' % state.get('telegram'))
    print('=' * 68)
    if state.get('telegram'):
        print('DONE — the next lead will notify you on Telegram.')
        return 0
    print('Secrets written but the worker still reports no channel; check the deploy output above.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
