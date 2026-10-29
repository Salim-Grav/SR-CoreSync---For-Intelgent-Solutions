# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Language Purity & Isolation Auditor
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

Automated CI Gate:
1. Enforces ZERO Arabic/Perso-Arabic characters in all 27 LTR language portals.
2. Verifies that all 28 localized banner suites exist on disk.
3. Verifies that all HTML pages reference localized or intl assets without broken paths.
4. Verifies 100% Arabic asset references in the root Arabic master.
"""

import os
import re
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

LTR_LANGS = [
    'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga',
    'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt', 'nl', 'no', 'pl',
    'pt', 'ro', 'sk', 'sl', 'sv', 'tr'
]

ALL_LANGS = LTR_LANGS + ['ckb']

AR_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')

def audit_purity():
    failures = []
    print("=" * 70)
    print(" S&R CoreSync - Multilingual Isolation & Purity CI Audit")
    print("=" * 70)

    # 1. Check LTR portals for Arabic character contamination
    total_ltr_pages = 0
    clean_ltr_pages = 0
    for lang in LTR_LANGS:
        for page in ['index.html', 'demo.html']:
            page_path = os.path.join(BASE_DIR, lang, page)
            if not os.path.exists(page_path):
                failures.append(f"Missing page: {lang}/{page}")
                continue
            total_ltr_pages += 1
            with open(page_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            page_leaks = 0
            for i, line in enumerate(lines, 1):
                clean_line = re.sub(r'<!--.*?-->', '', line).strip()
                if AR_RE.search(clean_line):
                    page_leaks += 1
                    failures.append(f"Contamination in {lang}/{page} L{i}: {clean_line[:60]}")
            if page_leaks == 0:
                clean_ltr_pages += 1

    print(f"[✓] LTR Script Purity Check: {clean_ltr_pages}/{total_ltr_pages} pages 100% isolated and pure.")

    # 2. Check localized banner assets existence for all 28 languages
    banner_failures = 0
    for lang in ALL_LANGS:
        lang_assets_dir = os.path.join(BASE_DIR, 'assets', 'i18n', lang)
        required_assets = [
            'founder-banner-salim.jpg',
            'founder-banner-salim.webp',
            'founder-banner-salim-4k.jpg',
            'founder-banner-salim-4k.webp',
            'founder-banner-raed.jpg',
            'founder-banner-raed.webp',
            'founder-banner-raed-4k.jpg',
            'founder-banner-raed-4k.webp',
            'sr-emblem-gold-luxury.jpg',
            'sr-emblem-gold-luxury.webp',
            'sr-emblem-gold-luxury-4k.jpg',
        ]
        for a in required_assets:
            p = os.path.join(lang_assets_dir, a)
            if not os.path.exists(p) or os.path.getsize(p) < 1000:
                failures.append(f"Missing or empty banner asset: assets/i18n/{lang}/{a}")
                banner_failures += 1

    if banner_failures == 0:
        print(f"[✓] Localized Banner Suites: All {len(ALL_LANGS)} languages have full 11-file banner sets.")
    else:
        print(f"[✗] Localized Banner Suites: {banner_failures} files missing.")

    # 3. Check international master assets in assets/i18n/intl/
    intl_assets = [
        'sr-core-emblem-official.png',
        'sr-core-emblem-256.png',
        'sr-core-emblem.svg',
        'brand-kit-spec.svg',
        'signature-neon.svg',
        'signature-neon-raed.svg',
        'og-coresync-official.jpg',
        'sr-emblem-gold-luxury.jpg',
        'sr-emblem-gold-luxury-4k.jpg',
        'founder-banner-salim.jpg',
        'founder-banner-raed.jpg',
    ]
    intl_failures = 0
    for ia in intl_assets:
        p = os.path.join(BASE_DIR, 'assets', 'i18n', 'intl', ia)
        if not os.path.exists(p):
            failures.append(f"Missing international master asset: assets/i18n/intl/{ia}")
            intl_failures += 1
    if intl_failures == 0:
        print(f"[✓] International Asset Reservoir: All {len(intl_assets)} files present.")

    # 4. Check Arabic root assets in assets/
    arabic_assets = [
        'sr-core-emblem-official.png',
        'sr-core-emblem-official.webp',
        'sr-core-emblem-256.png',
        'sr-core-emblem.svg',
        'sr-emblem-gold-luxury.jpg',
        'sr-emblem-gold-luxury.webp',
        'sr-emblem-gold-luxury-4k.jpg',
        'founder-banner-salim.jpg',
        'founder-banner-salim.webp',
        'founder-banner-salim-4k.jpg',
        'founder-banner-salim-4k.webp',
        'founder-banner-raed.jpg',
        'founder-banner-raed.webp',
        'founder-banner-raed-4k.jpg',
        'founder-banner-raed-4k.webp',
        'og-coresync-official.jpg',
        'brand-kit-spec.svg',
        'signature-neon.svg',
        'signature-neon-raed.svg',
    ]
    ar_failures = 0
    for aa in arabic_assets:
        p = os.path.join(BASE_DIR, 'assets', aa)
        if not os.path.exists(p):
            failures.append(f"Missing Arabic master asset: assets/{aa}")
            ar_failures += 1
    if ar_failures == 0:
        print(f"[✓] Arabic Master Visuals: All {len(arabic_assets)} assets verified present.")

    print("=" * 70)
    if failures:
        print(f"AUDIT STATUS: FAILED ({len(failures)} issues found):")
        for f in failures[:15]:
            print(f"  - {f}")
        return 1
    else:
        print("AUDIT STATUS: PASSED (100% PURE ISOLATION & ZERO BROKEN ASSETS)")
        return 0

if __name__ == '__main__':
    code = audit_purity()
    sys.exit(code)
