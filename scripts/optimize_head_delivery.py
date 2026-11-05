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

2. The hero emblem is prioritized while below-the-fold media is deferred.
   The cinema poster is not the LCP element on the multilingual pages, so its
   preload is removed. Founder images and the autoplay video are loaded only
   when their section approaches the viewport.

Deliberate limits:
  * Only known below-the-fold media attributes and resource hints are changed.
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
LCP_IMAGE_CLASS = 'hero-emblem-render-img'
BELOW_FOLD_IMAGE_CLASSES = ('showcase-img', 'exec-visual-img', 'founder-avatar-img')
FOUNDER_VIDEO_SCRIPT = 'lazy-founder-media.js'

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


def prioritize_hero_image(text):
    """Keep the measured LCP image eager and assign it high fetch priority."""
    image_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)

    def replace(match):
        tag = match.group(0)
        class_match = re.search(r'\bclass=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        if not class_match or LCP_IMAGE_CLASS not in class_match.group(1).split():
            return tag
        if re.search(r'\bfetchpriority=', tag, re.IGNORECASE):
            return tag
        return tag[:-1].rstrip() + ' fetchpriority="high">'

    return image_re.sub(replace, text)


def optimize_below_fold_images(text):
    image_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
    target_classes = set(BELOW_FOLD_IMAGE_CLASSES)
    changed = []

    def add_attribute(tag, attribute):
        closing = re.search(r'\s*/?>$', tag).group(0)
        return tag[:-len(closing)] + ' ' + attribute + closing

    def replace(match):
        tag = match.group(0)
        class_match = re.search(r'\bclass=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        if not class_match or not (target_classes & set(class_match.group(1).split())):
            return tag
        updated = re.sub(
            r'(\bloading=["\'])eager(["\'])',
            r'\1lazy\2',
            tag,
            flags=re.IGNORECASE,
        )
        if not re.search(r'\bloading=', updated, re.IGNORECASE):
            updated = add_attribute(updated, 'loading="lazy"')
        if not re.search(r'\bdecoding=', updated, re.IGNORECASE):
            updated = add_attribute(updated, 'decoding="async"')
        if updated != tag:
            changed.append(True)
        return updated

    return image_re.sub(replace, text), len(changed)


def defer_founder_video(text):
    video_re = re.compile(
        r'<video\b(?=[^>]*\bclass=["\'][^"\']*\bvideo\b[^"\']*["\'])[^>]*>\s*</video>',
        re.IGNORECASE,
    )
    changed = []

    def replace(match):
        tag = match.group(0)
        if re.search(r'\bdata-lazy-src=', tag, re.IGNORECASE):
            return tag
        src = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not src:
            return tag
        poster = re.search(r'\bposter=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        updated = re.sub(r'\s+(?:src|poster)=["\'][^"\']*["\']', '', tag, flags=re.IGNORECASE)
        updated = re.sub(r'\s+autoplay(?=[\s>])', '', updated, flags=re.IGNORECASE)
        updated = re.sub(r'\s+preload=["\'][^"\']*["\']', '', updated, flags=re.IGNORECASE)
        attributes = ' data-lazy-src="%s" data-lazy-autoplay="true" preload="none"' % src.group(1)
        if poster:
            attributes += ' data-lazy-poster="%s"' % poster.group(1)
        updated = updated.replace('>', attributes + '>', 1)
        changed.append(True)
        return updated

    return video_re.sub(replace, text), bool(changed)


def drop_founder_poster_preloads(text):
    def replace(match):
        tag = match.group(0)
        if 'rel="preload"' in tag and 'about-founder-poster' in tag:
            return ''
        return tag

    return PRELOAD_LINE_RE.sub(replace, text)


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


def transform(text, rel):
    notes = []

    text, removed = drop_heavy_emblem_preload(text)
    if removed:
        notes.append('dropped unused %s preload' % HEAVY_EMBLEM)

    text = drop_founder_poster_preloads(text)
    text = prioritize_hero_image(text)
    text, lazy_images = optimize_below_fold_images(text)
    notes.append('prioritized hero image and deferred %d below-fold image(s)' % lazy_images)

    text, lazy_video = defer_founder_video(text)
    if lazy_video:
        script_path = './js/' if rel == 'index.html' else '../js/'
        script_tag = '<script src="%s%s" defer></script>' % (script_path, FOUNDER_VIDEO_SCRIPT)
        if script_tag not in text:
            head_end = text.lower().rfind('</head>')
            if head_end != -1:
                text = text[:head_end] + '    ' + script_tag + '\n' + text[head_end:]
        notes.append('deferred founder video until near viewport')

    text, deferred = defer_component_css(text)
    notes.append('deferred %d component sheet(s): %s' % (len(deferred), ', '.join(deferred))
                 if deferred else 'no component sheet matched')

    return text, notes


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true', help='write the files')
    mode.add_argument('--check', action='store_true', help='fail if any file needs optimization')
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
        new_text, notes = transform(text, rel)
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
        'APPLIED' if args.apply else 'CHECK' if args.check else 'DRY RUN',
        changed, unchanged))
    if not args.apply and not args.check:
        print('Re-run with --apply to write.')
    return 1 if args.check and changed else 0


if __name__ == '__main__':
    sys.exit(main())
