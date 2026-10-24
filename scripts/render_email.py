# -*- coding: utf-8 -*-
"""
Transactional e-mail renderer
=============================
Fills a built template with real data and emits three artefacts:

  <name>.html   rendered message (send this as the HTML part)
  <name>.txt    plain-text alternative
  <name>.eml    ready-to-open message file (Gmail "open .eml", Outlook, Thunderbird)

The template must be tokenised (`{{TOKEN}}`). Anything left unresolved is a
hard error: shipping an invoice with a literal `{{TOTAL}}` is worse than not
sending it at all.

Usage:
  python scripts/render_email.py invoice-quote templates/emails/sample-invoice.json
  python scripts/render_email.py welcome-email templates/emails/sample-welcome.json
"""
import email.utils
import html as htmlmod
import io
import json
import os
import re
import sys
from email.message import EmailMessage

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import build_email_templates as builder  # noqa: E402

OUT = os.path.join(ROOT, 'dist', 'emails')
TOKEN = re.compile(r'\{\{([A-Z_]+)\}\}')

ITEM_ROW = """                                <tr>
                                    <td class="item-desc-cell">
                                        <div class="item-title">
                                            {title}
                                        </div>
                                        <div class="item-sub">
                                            {description}
                                        </div>
                                    </td>
                                    <td align="center" class="item-qty-cell">{qty}</td>
                                    <td align="left" class="item-price-cell" dir="ltr">{amount}</td>
                                </tr>
"""


def escape(value):
    return htmlmod.escape(str(value), quote=False)


def template_config(name):
    for tpl in builder.TEMPLATES:
        if tpl['name'] == name:
            return tpl
    raise SystemExit('Unknown template: %s (known: %s)'
                     % (name, ', '.join(t['name'] for t in builder.TEMPLATES)))


def items_rows(items):
    if not items:
        raise SystemExit('payload.items is empty - an invoice needs at least one line')
    rows = []
    for index, item in enumerate(items, 1):
        for field in ('title', 'qty', 'amount'):
            if field not in item or str(item[field]).strip() == '':
                raise SystemExit('items[%d] is missing "%s"' % (index - 1, field))
        rows.append(ITEM_ROW.format(
            title=escape(item['title']),
            description=escape(item.get('description', '')),
            qty=escape(item['qty']),
            amount=escape(item['amount']),
        ))
    return ''.join(rows)


def to_text(html):
    return builder.to_text(html)


def build_eml(subject, sender, recipient, html, text, reply_to=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid(domain='sr-coresync.com')
    if reply_to:
        msg['Reply-To'] = reply_to
    msg['Auto-Submitted'] = 'auto-generated'
    msg.set_content(text)
    msg.add_alternative(html, subtype='html')
    return msg.as_bytes()


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)

    name = sys.argv[1]
    payload_path = sys.argv[2]
    tpl = template_config(name)

    print('=' * 72)
    print('S&R CoreSync - render %s' % name)
    print('=' * 72)

    meta = builder.build(tpl)
    built_path = os.path.join(OUT, name + '.html')
    with io.open(built_path, encoding='utf-8') as fh:
        doc = fh.read()

    with io.open(payload_path, encoding='utf-8') as fh:
        payload = json.load(fh)

    values = {k.upper(): v for k, v in payload.items() if k != 'items'}
    if '{{ITEMS_ROWS}}' in doc:
        values['ITEMS_ROWS'] = items_rows(payload.get('items'))

    for key, value in values.items():
        doc = doc.replace('{{%s}}' % key, value if key == 'ITEMS_ROWS' else escape(value))

    leftovers = sorted(set(TOKEN.findall(doc)))
    if leftovers:
        print('FAILED - unresolved tokens: %s' % ', '.join(leftovers))
        return 1

    text = to_text(doc)
    subject = payload.get('subject') or ('فاتورة / عرض سعر رسمي معتمد • %s' % payload.get('quote_id', ''))
    sender = payload.get('from') or 'S&R CoreSync Solutions <billing@sr-coresync.com>'
    recipient = payload.get('to') or 'klant@example.com'

    base = os.path.join(OUT, '%s-rendered' % name)
    with io.open(base + '.html', 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(doc)
    with io.open(base + '.txt', 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    with open(base + '.eml', 'wb') as fh:
        fh.write(build_eml(subject, sender, recipient, doc, text,
                           reply_to=payload.get('reply_to')))

    html_kb = os.path.getsize(base + '.html') / 1024
    eml_kb = os.path.getsize(base + '.eml') / 1024
    print('  subject      : %s' % subject)
    print('  from / to    : %s -> %s' % (sender, recipient))
    print('  html         : %.1f KB' % html_kb)
    print('  text         : %.1f KB' % (os.path.getsize(base + '.txt') / 1024))
    print('  eml          : %.1f KB' % eml_kb)
    print('  tokens left  : 0')
    print('-' * 72)
    if html_kb > builder.GMAIL_CLIP_KB:
        print('FAILED - HTML part exceeds Gmail clipping threshold')
        return 1
    print('PASSED - rendered, self-contained, no unresolved tokens.')
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
