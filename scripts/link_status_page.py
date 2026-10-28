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

"""Link the status page from every language portal's footer.

The Arabic root and /en/ were linked by hand; the remaining 27 portals need the
same entry or the page stays an orphan for most visitors. Each portal has one
footer list whose last item is the brand-identity lightbox, so that line is the
anchor — it exists in every portal and does not move with translations.

Idempotent: a portal that already links ../status.html is skipped.

  python scripts/link_status_page.py            # apply
  python scripts/link_status_page.py --dry-run  # report only
"""
import argparse
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANCHOR = 'href="#brandLogoLightboxModal"'
ALREADY = '../status.html'
LINK = '                                <li><a href="../status.html?lang=en" class="link letter-space--2 h5 gold-accent">%s 🟢</a></li>\n'

LABELS = {
    'bg': 'Състояние на платформата',
    'ckb': 'دۆخی پلاتفۆرم',
    'cs': 'Stav platformy',
    'da': 'Plattformstatus',
    'de': 'Plattformstatus',
    'el': 'Κατάσταση πλατφόρμας',
    'es': 'Estado de la plataforma',
    'et': 'Platvormi olek',
    'fi': 'Alustan tila',
    'fr': 'État de la plateforme',
    'ga': 'Stádas an ardáin',
    'hr': 'Status platforme',
    'hu': 'Platform állapota',
    'it': 'Stato della piattaforma',
    'ku': 'Rewşa platformê',
    'lt': 'Platformos būsena',
    'lv': 'Platformas statuss',
    'mt': 'L-istat tal-pjattaforma',
    'nl': 'Platformstatus',
    'no': 'Plattformstatus',
    'pl': 'Status platformy',
    'pt': 'Estado da plataforma',
    'ro': 'Starea platformei',
    'sk': 'Stav platformy',
    'sl': 'Stanje platforme',
    'sv': 'Plattformsstatus',
    'tr': 'Platform durumu',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    done = skipped = failed = 0
    for code, label in LABELS.items():
        path = os.path.join(ROOT, code, 'index.html')
        if not os.path.isfile(path):
            print('  MISSING PORTAL %s' % path)
            failed += 1
            continue

        with io.open(path, encoding='utf-8') as fh:
            source = fh.read()

        if ALREADY in source:
            print('  skip   %-3s already linked' % code)
            skipped += 1
            continue

        lines = source.split('\n')
        hits = [i for i, line in enumerate(lines) if ANCHOR in line]
        if len(hits) != 1:
            print('  FAIL   %-3s %d anchors found (expected 1)' % (code, len(hits)))
            failed += 1
            continue

        lines.insert(hits[0] + 1, LINK % label)
        updated = '\n'.join(lines)

        # Cheap structural check: the list must stay balanced.
        if updated.count('<li>') != source.count('<li>') + 1:
            print('  FAIL   %-3s <li> count did not grow by one' % code)
            failed += 1
            continue

        if not args.dry_run:
            with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(updated)
        print('  add    %-3s %s' % (code, label))
        done += 1

    print('-' * 60)
    print('%s: %d added, %d already present, %d failed'
          % ('dry run' if args.dry_run else 'done', done, skipped, failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
