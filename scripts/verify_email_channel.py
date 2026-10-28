# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
Verify the lead-notification channel of the deployed Worker.
===========================================================
Answers one question with evidence: "if a client submits the form right now,
does anyone get told?"

  python scripts/verify_email_channel.py              # report only
  python scripts/verify_email_channel.py --send you@example.com

Without --send nothing is written anywhere: the script only reads /health.
"""
import argparse
import json
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://sr-lead-capture.sr-coresync.workers.dev'

STEPS = """
كيف تُشغّل قناة البريد (5 دقائق، مجانًا):
  1. أنشئ حسابًا على resend.com وأضف النطاق send.sr-coresync.com
  2. من لوحة Resend: API Keys → Create → انسخ المفتاح (يبدأ بـ re_)
  3. نفّذ:
       cd workers/sr-lead-capture
       npx wrangler secret put RESEND_API_KEY      # الصق المفتاح
  4. أضف سجلات DKIM/SPF التي يعرضها Resend على النطاق الفرعي send.
  5. تحقّق:
       python scripts/verify_email_channel.py
"""


UA = {'User-Agent': 'S&R-CoreSync-Check/1.0'}


def get(path, attempts=2):
    last = None
    for _ in range(attempts):
        try:
            req = urllib.request.Request(BASE + path, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as res:
                return json.loads(res.read().decode('utf-8'))
        except Exception as err:  # transient TLS/DNS right after a deploy
            last = err
    raise SystemExit('Worker unreachable: %s' % last)


def post(path, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=25) as res:
        return res.status, json.loads(res.read().decode('utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--send', metavar='EMAIL', help='send a real test lead to this address')
    args = parser.parse_args()

    print('=' * 66)
    print('S&R CoreSync - lead notification channel')
    print('=' * 66)

    health = get('/health')
    channel = health.get('emailChannel', 'unknown')

    print('  worker        : %s' % BASE)
    print('  mail channel  : %s' % channel)
    print('  mail from     : %s' % (health.get('mailFrom') or '-'))
    print('  KV ledger     : %s' % health.get('kv'))
    print('  D1 durable    : %s' % health.get('d1'))
    print('  Turnstile     : %s' % health.get('turnstile'))
    print('  public events : %s' % health.get('eventsPublic'))
    print('-' * 66)

    if channel == 'none':
        print('VERDICT: leads are stored but NOBODY IS NOTIFIED.')
        print('         The form works, the record is durable, the e-mail is silent.')
        print(STEPS)
        return 1

    print('VERDICT: a mail channel is configured (%s).' % channel)

    if args.send:
        status, body = post('/lead', {
            'clientName': 'TEST — mail channel check',
            'email': args.send,
            'notes': 'Automated delivery check. Safe to delete.',
            'language': 'en',
            'sourceUrl': BASE + '/verify-email-channel'
        })
        print('  test lead     : HTTP %s  leadId=%s  stored=%s'
              % (status, body.get('leadId'), body.get('stored')))
        print('  → check the inbox of %s (and the spam folder) within a minute.' % args.send)
    else:
        print('  (add --send you@example.com to fire a real test lead)')

    return 0


if __name__ == '__main__':
    sys.exit(main())
