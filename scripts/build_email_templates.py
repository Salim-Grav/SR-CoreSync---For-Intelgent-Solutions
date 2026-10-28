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
Transactional e-mail builder
============================
Turns `templates/*.html` into deliverable messages in `dist/emails/`:

  1. Inlines the external stylesheet into a <style> block - Gmail, Outlook.com
     and Apple Mail strip <link rel="stylesheet">, which is why the previous
     templates rendered unstyled outside the (dead) Node service.
  2. Adds a hidden preheader so the inbox preview line is brand copy instead of
     the first `div` text.
  3. Declares the colour scheme so clients do not auto-invert the dark palette.
  4. Replaces e-mail-hostile assets: the 1.2 MB PNG emblem -> 192 px PNG, and
     WebP signatures -> PNG (Outlook desktop cannot render WebP).
  5. Adds `bgcolor` fallbacks for Outlook, which ignores CSS backgrounds on
     nested tables.
  6. Emits a plain-text alternative (deliverability + screen readers).
  7. Fails if any message exceeds Gmail's 102 KB clipping threshold.

Usage:  python scripts/build_email_templates.py
"""
import html as htmlmod
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'dist', 'emails')
GMAIL_CLIP_KB = 102

TEMPLATES = [
    {
        'name': 'welcome-email',
        'html': 'templates/welcome-email.html',
        'css': 'css/welcome-email.css',
        'preheader': 'مرحباً بكم في S&R CoreSync For Intelligent Solutions — أنظمة ERP سحابية وأتمتة ذكية واستشارات مالية في هولندا وأوروبا.',
        'bg': [('outer-table', '#080a0f'), ('wrapper-table', '#0f131a')],
    },
    {
        'name': 'invoice-quote',
        'html': 'templates/invoice-quote-email.html',
        'css': 'css/invoice-quote-email.css',
        'preheader': 'فاتورة / عرض سعر رسمي من S&R CoreSync For Intelligent Solutions — التفاصيل والمبالغ وضريبة BTW 21%.',
        'bg': [('outer-table', '#080a0f'), ('wrapper-table', '#0f131a')],
    },
]

ASSET_SWAPS = [
    ('https://sr-coresync.com/assets/sr-core-emblem-official.png',
     'https://sr-coresync.com/assets/email-emblem-192.png'),
    ('https://sr-coresync.com/assets/signature-raed.webp',
     'https://sr-coresync.com/assets/signature-raed.png'),
    ('https://sr-coresync.com/assets/signature-salim.webp',
     'https://sr-coresync.com/assets/signature-salim.png'),
]

COLOR_META = ('    <meta name="color-scheme" content="dark">\n'
              '    <meta name="supported-color-schemes" content="dark">\n')

PREHEADER = ('<div style="display:none;font-size:1px;color:#0b0d10;line-height:1px;'
             'max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">'
             '{text}</div>\n')


def to_text(html):
    body = re.sub(r'(?is)<(script|style|head).*?</\1>', ' ', html)
    body = re.sub(r'(?is)<!--.*?-->', ' ', body)
    body = re.sub(r'(?i)<br\s*/?>', '\n', body)
    body = re.sub(r'(?i)</(p|div|tr|td|h1|h2|h3|table)>', '\n', body)
    body = re.sub(r'(?s)<[^>]+>', ' ', body)
    body = htmlmod.unescape(body)
    lines = []
    for line in body.splitlines():
        line = re.sub(r'[ \t\u00a0]+', ' ', line).strip()
        if line:
            lines.append(line)
    out = []
    for line in lines:
        if out and out[-1] == line:
            continue
        out.append(line)
    return '\n'.join(out) + '\n'


def build(tpl):
    src = os.path.join(ROOT, tpl['html'])
    css_path = os.path.join(ROOT, tpl['css'])
    with io.open(src, encoding='utf-8') as fh:
        doc = fh.read()
    with io.open(css_path, encoding='utf-8') as fh:
        css = fh.read()

    # 1. external stylesheet -> inline <style>
    link = re.compile(r'\s*<link[^>]+rel=["\']stylesheet["\'][^>]*>', re.I)
    doc, links = link.subn('', doc)

    style_block = ('    <style type="text/css">\n'
                   '    /* inlined from %s by scripts/build_email_templates.py */\n'
                   '%s\n'
                   '    .ExternalClass { width:100%%; }\n'
                   '    .ExternalClass, .ExternalClass p, .ExternalClass span,\n'
                   '    .ExternalClass font, .ExternalClass td, .ExternalClass div { line-height:100%%; }\n'
                   '    </style>\n') % (tpl['css'], css)

    doc = doc.replace('</head>', style_block + COLOR_META + '</head>', 1)

    # 2. preheader right after <body ...>
    if 'PREHEADER' not in doc:
        doc = re.sub(r'(?i)(<body[^>]*>\s*)',
                     lambda m: m.group(1) + PREHEADER.format(text=tpl['preheader']),
                     doc, count=1)

    # 3. asset swaps
    for old, new in ASSET_SWAPS:
        doc = doc.replace(old, new)

    # 4. Outlook bgcolor fallbacks
    for cls, color in tpl['bg']:
        doc = re.sub(r'(<table[^>]*class="[^"]*' + re.escape(cls) + r'[^"]*")',
                     lambda m, c=color: m.group(1) if 'bgcolor' in m.group(1) else m.group(1) + ' bgcolor="%s"' % c,
                     doc)

    text = to_text(doc)
    os.makedirs(OUT, exist_ok=True)
    html_out = os.path.join(OUT, tpl['name'] + '.html')
    txt_out = os.path.join(OUT, tpl['name'] + '.txt')
    with io.open(html_out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(doc)
    with io.open(txt_out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)

    return {
        'name': tpl['name'],
        'links_removed': links,
        'kb': os.path.getsize(html_out) / 1024,
        'text_kb': os.path.getsize(txt_out) / 1024,
        'text_lines': text.count('\n'),
        'has_preheader': 'display:none' in doc,
        'webp_left': len(re.findall(r'src="[^"]+\.webp"', doc)),
    }


def main():
    print('=' * 74)
    print('S&R CoreSync - transactional e-mail build')
    print('=' * 74)
    failures = []
    for tpl in TEMPLATES:
        r = build(tpl)
        status = 'OK'
        if r['kb'] > GMAIL_CLIP_KB:
            status = 'CLIPPED'
            failures.append('%s exceeds Gmail 102 KB (%0.1f KB)' % (r['name'], r['kb']))
        if r['links_removed'] != 1:
            failures.append('%s: expected 1 external stylesheet, removed %d' % (r['name'], r['links_removed']))
        if r['webp_left']:
            failures.append('%s: %d WebP sources remain (Outlook cannot render them)' % (r['name'], r['webp_left']))
        print('  %-16s %6.1f KB  text %5.1f KB (%3d lines)  links-removed=%d  %s'
              % (r['name'], r['kb'], r['text_kb'], r['text_lines'], r['links_removed'], status))

    print('-' * 74)
    if failures:
        print('FAILED:')
        for f in failures:
            print('  X ' + f)
        return 1
    print('PASSED - both messages are self-contained, under the clipping limit,')
    print('         and ship a plain-text alternative.')
    print('=' * 74)
    return 0


if __name__ == '__main__':
    sys.exit(main())
