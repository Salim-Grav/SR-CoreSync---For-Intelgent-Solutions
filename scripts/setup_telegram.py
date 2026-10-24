# -*- coding: utf-8 -*-
"""
Telegram alert setup helper (zero DNS, zero mail provider)
=========================================================
Goal: you receive a phone notification the moment a lead arrives, without a
mail provider, without DNS records and without touching the domain.

Flow:
  1. In Telegram open @BotFather -> /newbot -> copy the token (123456:ABC...)
  2. Open your new bot and send it any message (e.g. "hi")
  3. Run this script and paste the token when asked (input is hidden)
  4. The script finds your chat id and prints the two commands to run

Usage:
  python scripts/setup_telegram.py
  python scripts/setup_telegram.py --test    # after the secrets are set
"""
import argparse
import getpass
import json
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://api.telegram.org/bot%s/%s'
WORKER = 'https://sr-lead-capture.sr-coresync.workers.dev'


def api(token, method):
    req = urllib.request.Request(BASE % (token, method),
                                 headers={'User-Agent': 'S&R-CoreSync-Check/1.0'})
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode('utf-8'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test', action='store_true', help='check the deployed worker instead')
    args = ap.parse_args()

    if args.test:
        req = urllib.request.Request(WORKER + '/health',
                                     headers={'User-Agent': 'S&R-CoreSync-Check/1.0'})
        health = json.loads(urllib.request.urlopen(req, timeout=20).read().decode('utf-8'))
        print('telegram channel : %s' % health.get('telegram'))
        print('mail channel     : %s' % health.get('emailChannel'))
        return 0 if health.get('telegram') else 1

    print('=' * 66)
    print('Telegram alerts — setup')
    print('=' * 66)
    token = getpass.getpass('Paste bot token (hidden): ').strip()
    if ':' not in token:
        raise SystemExit('That does not look like a bot token (expected 123456:ABC…).')

    try:
        me = api(token, 'getMe')
    except Exception as err:
        raise SystemExit('Telegram rejected the token: %s' % err)
    if not me.get('ok'):
        raise SystemExit('Telegram rejected the token: %s' % me)
    print('  bot              : @%s' % me['result'].get('username'))

    updates = api(token, 'getUpdates')
    chats = {}
    for item in updates.get('result', []):
        msg = item.get('message') or item.get('channel_post') or {}
        chat = msg.get('chat') or {}
        if chat.get('id'):
            chats[chat['id']] = chat.get('title') or chat.get('username') or chat.get('first_name') or ''

    if not chats:
        print('-' * 66)
        print('  No chat found. Send your bot any message in Telegram, then re-run.')
        print('  (e.g. open @%s and type "hi")' % me['result'].get('username'))
        return 1

    print('-' * 66)
    print('  chats found:')
    for cid, name in chats.items():
        print('    %-16s %s' % (cid, name))

    chat_id = list(chats.keys())[0]
    print('-' * 66)
    print('  Run these two commands now:')
    print()
    print('    cd "workers/sr-lead-capture"')
    print('    node node_modules/wrangler/bin/wrangler.js secret put TELEGRAM_BOT_TOKEN')
    print('    node node_modules/wrangler/bin/wrangler.js secret put TELEGRAM_CHAT_ID')
    print('      -> %s' % chat_id)
    print()
    print('  Then: python scripts/setup_telegram.py --test')
    print('=' * 66)
    return 0


if __name__ == '__main__':
    sys.exit(main())
