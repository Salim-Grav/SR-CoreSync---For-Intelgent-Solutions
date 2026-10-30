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
Critical-path delivery optimisation
===================================

Lighthouse (local, 2026-10) on the Arabic homepage reported:

    FCP 9.8 s · LCP 20.0 s · TBT 40-80 ms

A tiny TBT with a ten-second FCP means the main thread is idle: the browser is
simply not permitted to paint. The cause is ten render-blocking stylesheets
(836 KB) in `<head>`, four of them component sheets for regions that are not in
the first viewport.

Two changes, neither of which touches the design:

1. Below-the-fold component CSS stops blocking the first paint.
   `enterprise-suite` (modals, hidden until opened), `sr-software-apps`,
   `sr-footer`, `sr-trust-ribbon`, `sr-tier-matrix`, `concierge` and
   `sr-analytics` move to the `preload -> stylesheet` pattern, each with a
   `<noscript>` fallback so a JavaScript-less client still receives the full
   design.

2. The LCP resource is prioritised and its duplicate is dropped.
   The emblem was preloaded as both `.jpg` (188 KB, unused by any layout) and
   `.webp`, while the actual largest-contentful element - the founder cinema
   `<video>` poster - went unpreloaded. The `.jpg` preload is removed and the
   poster is preloaded at high priority using the exact `poster` path that the
   page already declares.

Deliberate limits:
  * Only `<link>` tags are rewritten. No HTML structure, text or styling moves.
  * Every edit is idempotent; a second run reports "already optimised".
  * Nothing is written unless --apply is passed.

Usage:
    python scripts/optimize_head_delivery.py                  # dry run, all pages
    python scripts/optimize_head_delivery.py --apply          # write changes
    python scripts/optimize_head_delivery.py --apply --only index.html
"""
import argparse
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGUAGES = [
    'en', 'nl', 'de', 'tr', 'ckb', 'ku', 'bg', 'cs', 'da', 'el', 'es', 'et',
    'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'lt', 'lv', 'mt', 'no', 'pl', 'pt',
    'ro', 'sk', 'sl', 'sv',
]

# Component stylesheets that are never needed to paint the first viewport.
#
# Deliberately empty, and the reason matters more than the list:
# every candidate was audited for `position: fixed` and all but two style UI
# that is visible in the first viewport - `.es-gdpr-banner`, `.floating-actions`,
# `.srx-concierge-fab`, `.sr-consent`, `.sr-floating-back-btn`. Loading those
# asynchronously swaps them to the non-blocking preload pattern, which makes a
# consent banner and a floating dock paint unstyled for a frame on a brand site
# whose whole argument is finish. The two genuinely safe sheets (`sr-footer`,
# `sr-tier-matrix`, `sr-trust-ribbon`) total 37 KB - under 2% of the page - and
# do not justify the risk. The mechanism stays here, gated, for a future sheet
# that is provably below the fold.
DEFERRABLE_CSS = []

# The largest-contentful element on the homepage is this video poster.
LCP_POSTER_NAME = 'about-founder-poster.webp'

# Preloaded at high priority but never rendered by any layout: the layout uses
# the .webp sibling or a localized copy under assets/i18n/<lang>/.
HEAVY_EMBLEM = 'sr-emblem-gold-luxury.jpg'

STYLESHEET_RE = re.compile(r'(?is)^[ \t]*<link\b[^>]*\brel="stylesheet"[^>]*>[ \t]*\r?\n?', re.M)
PRELOAD_LINE_RE = re.compile(r'(?is)^[ \t]*<link\b[^>]*\brel="preload"[^>]*>[ \t]*\r?\n?', re.M)
NOSCRIPT_RE = re.compile(r'(?is)<noscript>.*?</noscript>')


def page_list(only=None):
    if only:
        return [only]
    return ['index.html'] + [lang + '/index.html' for lang in LANGUAGES]


def drop_heavy_emblem_preload(text):
    """Delete only the <link> line that preloads the unused 188 KB emblem."""
    removed = []

    def repl(match):
        tag = match.group(0)
        if HEAVY_EMBLEM in tag and 'rel="preload"' in tag:
            removed.append(HEAVY_EMBLEM)
            return ''
        return tag

    return PRELOAD_LINE_RE.sub(repl, text), removed


def poster_preload(text):
    """Build the LCP preload tag from the poster path the page already uses."""
    m = re.search(r'poster="([^"]*' + re.escape(LCP_POSTER_NAME) + r')"', text)
    if not m:
        return None, None
    href = m.group(1)
    return href, '<link rel="preload" as="image" href="%s" fetchpriority="high">' % href


def has_poster_preload(text, href):
    return re.search(r'rel="preload"[^>]*href="' + re.escape(href) + r'"', text) is not None


def insert_poster_preload(text, tag):
    """Place the preload immediately before the first stylesheet in <head>."""
    m = STYLESHEET_RE.search(text)
    if not m:
        return text, False
    line_start = text.rfind('\n', 0, m.start()) + 1
    indent = re.match(r'[ \t]*', text[line_start:m.start()]).group(0)
    newline = '\r\n' if '\r\n' in text[:4000] else '\n'
    text = text[:line_start] + indent + tag + newline + text[line_start:]
    return text, True


def defer_component_css(text):
    deferred = []
    noscript_links = []

    # The <noscript> fallback deliberately keeps plain stylesheet links. Shield
    # every existing <noscript> block so a second run cannot rewrite its links
    # into preloads (which would leave a JavaScript-less client with no styles).
    stashed = []

    def stash(match):
        stashed.append(match.group(0))
        return '<!--sr-noscript-%d-->' % (len(stashed) - 1)

    text = NOSCRIPT_RE.sub(stash, text)

    def repl(match):
        tag = match.group(0)
        href_m = re.search(r'href="([^"]+)"', tag)
        if not href_m:
            return tag
        href = href_m.group(1)
        if os.path.basename(href.split('?')[0]) not in DEFERRABLE_CSS:
            return tag
        stripped = tag.strip()
        new_tag = (
            '<link rel="preload" as="style" href="%s" '
            'onload="this.onload=null;this.rel=\'stylesheet\'">' % href
        )
        trailing = tag[len(tag.rstrip('\r\n')):]
        deferred.append(os.path.basename(href.split('?')[0]))
        noscript_links.append(stripped)
        return new_tag + trailing

    text = STYLESHEET_RE.sub(repl, text)

    for index, block in enumerate(stashed):
        text = text.replace('<!--sr-noscript-%d-->' % index, block)

    if noscript_links:
        newline = '\r\n' if '\r\n' in text[:4000] else '\n'
        block = (newline + '    <noscript>' + newline
                 + ''.join('        ' + link + newline for link in noscript_links)
                 + '    </noscript>' + newline)
        idx = text.lower().rfind('</head>')
        if idx != -1:
            text = text[:idx] + block + text[idx:]

    return text, deferred


def transform(text):
    notes = []

    text, removed = drop_heavy_emblem_preload(text)
    if removed:
        notes.append('dropped unused %s preload' % HEAVY_EMBLEM)

    href, tag = poster_preload(text)
    if not href:
        notes.append('no cinema poster on this page - skipped LCP preload')
    elif has_poster_preload(text, href):
        notes.append('LCP poster already preloaded')
    else:
        text, ok = insert_poster_preload(text, tag)
        notes.append('LCP poster preloaded' if ok else 'could not place LCP preload')

    text, deferred = defer_component_css(text)
    notes.append('deferred %d component sheet(s): %s' % (len(deferred), ', '.join(deferred))
                 if deferred else 'no component sheet matched')

    return text, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='write the files')
    ap.add_argument('--only', default=None, help='single page, repository-relative')
    args = ap.parse_args()

    changed = 0
    unchanged = 0

    for rel in page_list(args.only):
        path = os.path.join(ROOT, rel.replace('/', os.sep))
        if not os.path.exists(path):
            print('MISSING  %s' % rel)
            continue
        with io.open(path, 'r', encoding='utf-8', newline='') as fh:
            text = fh.read()
        new_text, notes = transform(text)
        if new_text == text:
            unchanged += 1
            print('SKIP     %-22s %s' % (rel, ' | '.join(notes)))
            continue
        changed += 1
        print('CHANGE   %-22s %+d B  %s' % (rel, len(new_text) - len(text), ' | '.join(notes)))
        if args.apply:
            with io.open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(new_text)

    print('-' * 78)
    print('%s: %d changed, %d unchanged' % (
        'APPLIED' if args.apply else 'DRY RUN', changed, unchanged))
    if not args.apply:
        print('Re-run with --apply to write.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
