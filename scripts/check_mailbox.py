# -*- coding: utf-8 -*-
"""Read our own inbox over IMAP and report what actually arrived.

A green SMTP call only proves the server accepted the message. This opens the
mailbox and checks the message is there, that it carries our DKIM signature, and
what the receiving side recorded — the difference between "sent" and "delivered".

Credentials, in order of precedence:
  --password / PURELYMAIL_PASS env / .secrets/purelymail-pass.txt  (git-ignored)

  python scripts/check_mailbox.py                  # last 5 messages
  python scripts/check_mailbox.py --subject self-test --wait 60
  python scripts/check_mailbox.py --headers-only
"""
import argparse
import email
import email.header
import imaplib
import os
import re
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS_FILE = os.path.join(ROOT, '.secrets', 'purelymail-pass.txt')
HOST = 'imap.purelymail.com'


def read_password(explicit):
    if explicit:
        return explicit.strip()
    env = os.environ.get('PURELYMAIL_PASS', '').strip()
    if env:
        return env
    if os.path.isfile(PASS_FILE):
        with open(PASS_FILE, encoding='utf-8') as fh:
            return fh.read().strip()
    if sys.stdin is not None and sys.stdin.isatty():
        import getpass
        return getpass.getpass('Mailbox password: ').strip()
    return ''


def decode(value):
    if not value:
        return ''
    parts = email.header.decode_header(value)
    out = []
    for chunk, charset in parts:
        if isinstance(chunk, bytes):
            out.append(chunk.decode(charset or 'utf-8', 'replace'))
        else:
            out.append(chunk)
    return ''.join(out)


def fetch_headers(conn, uid):
    status, data = conn.uid('FETCH', uid, '(BODY.PEEK[HEADER] RFC822.SIZE)')
    if status != 'OK' or not data or not isinstance(data[0], tuple):
        return None
    return email.message_from_bytes(data[0][1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', default='info@sr-coresync.com')
    ap.add_argument('--password')
    ap.add_argument('--subject', help='wait for a message whose subject contains this')
    ap.add_argument('--wait', type=int, default=0, help='seconds to keep polling')
    ap.add_argument('--limit', type=int, default=5)
    args = ap.parse_args()

    password = read_password(args.password)
    if not password:
        print('No password. Set PURELYMAIL_PASS, write .secrets/purelymail-pass.txt, or run it in a terminal to be prompted.')
        return 2

    deadline = time.time() + max(args.wait, 0)
    attempt = 0
    while True:
        attempt += 1
        try:
            conn = imaplib.IMAP4_SSL(HOST, 993, timeout=30)
            conn.login(args.user, password)
        except imaplib.IMAP4.error as exc:
            print('login failed: %s' % exc)
            return 2

        try:
            conn.select('INBOX', readonly=True)
            status, data = conn.uid('SEARCH', None, 'ALL')
            uids = data[0].split() if status == 'OK' and data and data[0] else []
            matched = []
            for uid in reversed(uids[-40:]):
                msg = fetch_headers(conn, uid)
                if msg is None:
                    continue
                subject = decode(msg.get('Subject'))
                matched.append((uid, msg, subject))
                if len(matched) >= max(args.limit, 1) and not args.subject:
                    break
        finally:
            try:
                conn.logout()
            except Exception:
                pass

        if args.subject:
            hits = [row for row in matched if args.subject.lower() in row[2].lower()]
            if hits:
                matched = hits[:args.limit]
            elif time.time() < deadline:
                print('  … waiting for "%s" (%ds left)' % (args.subject, int(deadline - time.time())))
                time.sleep(8)
                continue
            else:
                print('NOT FOUND — no message with subject containing "%s"' % args.subject)
                return 1
        break

    print('=' * 74)
    print('Inbox — %s (attempt %d)' % (args.user, attempt))
    print('=' * 74)
    for uid, msg, subject in matched[:args.limit]:
        dkim = msg.get('DKIM-Signature')
        auth = msg.get('Authentication-Results')
        selector = ''
        if dkim:
            found = re.search(r's=([A-Za-z0-9._-]+)', dkim)
            domain = re.search(r'd=([A-Za-z0-9._-]+)', dkim)
            selector = 'selector=%s domain=%s' % (found.group(1) if found else '?',
                                                  domain.group(1) if domain else '?')
        print('  %s  %s' % (decode(msg.get('Date')), subject[:64]))
        print('      from   : %s' % decode(msg.get('From'))[:90])
        print('      DKIM   : %s' % ('signed — ' + selector if dkim else 'NOT signed'))
        if auth:
            print('      auth   : %s' % ' '.join(str(auth).split())[:110])
    print('-' * 74)
    print('%d message(s) listed' % len(matched[:args.limit]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
