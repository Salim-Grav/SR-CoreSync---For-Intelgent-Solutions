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
og:locale ↔ page language integrity (surgical, idempotent)
==========================================================
Every localized landing page carries a correct <html lang>, but the
multilingual template batches stamped the og:locale meta with "en_US"
(22 of 29 landing pages), "ar_SA" on the Sorani page, and Saudi "ar_SA"
on the Arabic root. Social scrapers (WhatsApp, Telegram, Discord, LinkedIn,
Facebook) therefore attribute the wrong language - and the wrong RTL hint -
to shared links.

This tool enforces one golden invariant on the 29 landing pages:

    og:locale must be LOCALE_MAP[<html lang>]

plus one legacy rule: any "ar_SA" (primary or alternate) becomes "ar_AR",
the generic Arabic Facebook locale that matches the site's pan-Arab audience.

Usage:  python scripts/fix_og_locale.py [--check]
Exit 0 = all landing pages in sync, 1 = drift found (with --check).
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'_site', 'dist', 'downloads', 'templates', '.git', '.agents',
             'node_modules', 'assets', 'css', 'js', 'workers', 'scripts'}

# html lang -> canonical og:locale (Facebook language_TERRITORY form;
# territories follow the language's primary country of standardisation.
# Kurdish has no Facebook locale, so the territory carries the audience:
# Sorani -> Iraq, Kurmanji -> Syria, matching this company's home market).
LOCALE_MAP = {
    'ar': 'ar_AR',
    'ckb': 'ckb_IQ',
    'ku': 'ku_SY',
    'bg': 'bg_BG', 'cs': 'cs_CZ', 'da': 'da_DK', 'de': 'de_DE',
    'el': 'el_GR', 'en': 'en_US', 'es': 'es_ES', 'et': 'et_EE',
    'fi': 'fi_FI', 'fr': 'fr_FR', 'ga': 'ga_IE', 'hr': 'hr_HR',
    'hu': 'hu_HU', 'it': 'it_IT', 'lt': 'lt_LT', 'lv': 'lv_LV',
    'mt': 'mt_MT', 'nl': 'nl_NL', 'no': 'nb_NO', 'pl': 'pl_PL',
    'pt': 'pt_PT', 'ro': 'ro_RO', 'sk': 'sk_SK', 'sl': 'sl_SI',
    'sv': 'sv_SE', 'tr': 'tr_TR',
}

HTML_LANG_RE = re.compile(r'<html[^>]*?\slang="([A-Za-z-]+)"')
OG_LOCALE_RE = re.compile(r'(<meta\s+property="og:locale"\s+content=")([^"]*)("\s*>)')
OG_ALT_AR_RE = re.compile(r'(<meta\s+property="og:locale:alternate"\s+content=")ar_SA(")')
OG_TITLE_RE = re.compile(r'(<meta\s+property="og:title"[^>]*>\s*\n)')


def landing_pages():
    pages = []
    root_index = os.path.join(ROOT, 'index.html')
    if os.path.isfile(root_index):
        pages.append('index.html')
    for name in sorted(os.listdir(ROOT)):
        sub = os.path.join(ROOT, name)
        if os.path.isdir(sub) and name not in SKIP_DIRS:
            idx = os.path.join(sub, 'index.html')
            if os.path.isfile(idx):
                pages.append(name + '/index.html')
    return pages


def page_lang(html):
    m = HTML_LANG_RE.search(html)
    return m.group(1) if m else None


def main():
    check_only = '--check' in sys.argv
    fixed = issues = 0
    details = []

    for rel in landing_pages():
        path = os.path.join(ROOT, rel)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()

        lang = page_lang(html)
        if lang not in LOCALE_MAP:
            issues += 1
            details.append('%s: unknown html lang "%r" - extend LOCALE_MAP' % (rel, lang))
            continue
        expected = LOCALE_MAP[lang]

        m = OG_LOCALE_RE.search(html)
        actual = m.group(2) if m else None

        problems = []
        if actual != expected:
            problems.append('og:locale=%s (want %s)' % (actual or 'MISSING', expected))
        if 'og:locale:alternate" content="ar_SA"' in html:
            problems.append('legacy ar_SA alternate')

        if not problems:
            continue
        issues += 1
        if check_only:
            details.append('%s: %s' % (rel, '; '.join(problems)))
            continue

        if m:
            html = OG_LOCALE_RE.sub(lambda mm: mm.group(1) + expected + mm.group(3), html, count=1)
        else:
            # Defensive: every page should already carry og:locale; if a new
            # template drops it, insert right after og:title.
            html, n = OG_TITLE_RE.subn(lambda mm: mm.group(1) + '    <meta property="og:locale" content="%s">\n' % expected, html, count=1)
            if not n:
                details.append('%s: no og:title anchor to insert after - skipped' % rel)
                issues -= 1
                continue
        html = OG_ALT_AR_RE.sub(lambda mm: mm.group(1) + 'ar_AR' + mm.group(2), html)

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        fixed += 1
        details.append('%s: %s -> fixed' % (rel, '; '.join(problems)))

    print('=' * 70)
    print('og:locale integrity (golden rule: og:locale = LOCALE_MAP[html lang])')
    print('=' * 70)
    print('  landing pages : %d' % len(landing_pages()))
    print('  out of sync   : %d %s' % (issues, '(check only)' if check_only else '(fixed)'))
    for d in details[:12]:
        print('    - ' + d)
    if len(details) > 12:
        print('    ... and %d more' % (len(details) - 12))
    print('=' * 70)
    if check_only:
        print('PASSED - every landing page declares its own language.' if issues == 0
              else 'DRIFT DETECTED - run: python scripts/fix_og_locale.py')
        return 0 if issues == 0 else 1
    print('DONE - %d page(s) rewritten.' % fixed)
    return 0


if __name__ == '__main__':
    sys.exit(main())
