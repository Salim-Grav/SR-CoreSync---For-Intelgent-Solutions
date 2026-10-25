"""
S&R CoreSync For Intelligent Solutions - Precise localized path repair
================================================================
Resolves every "./..." reference inside a localized page (<lang>/*.html)
against the repository root. When the target does not exist inside the
language folder but does exist at the root, the reference is rewritten to
"../...". This is the exact fix for the Kurdish (ckb) portal, which shipped
with a broken language switcher, broken prefetch hints and a broken 3D
mockup button.

Usage: python scripts/fix_language_paths.py [--check]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHARED_PREFIXES = ('css/', 'js/', 'assets/', 'downloads/', 'templates/')
SHARED_FILES = ('manifest.json', 'sw.js', 'robots.txt')

# Every attribute that can carry a URL.
URL_ATTRS = ('src', 'href', 'srcset', 'poster', 'data-src', 'data-href',
             'action', 'formaction', 'manifest')
ATTR_GROUP = '(?:' + '|'.join(URL_ATTRS) + ')'

ATTR_RE = re.compile(
    r'((?:' + '|'.join(URL_ATTRS) + r')\s*=\s*["\'])\./(' +
    '|'.join(re.escape(p) for p in SHARED_PREFIXES) +
    r')', re.IGNORECASE
)

FILE_ATTR_RE = re.compile(
    r'((?:' + '|'.join(URL_ATTRS) + r')\s*=\s*["\'])\./(' +
    '|'.join(re.escape(f) for f in SHARED_FILES) +
    r')(["\'])', re.IGNORECASE
)

LANG_DIRS = [
    'bg', 'ckb', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga',
    'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro',
    'sk', 'sl', 'sv', 'tr'
]

# Matches any quoted attribute value that starts with "./"
DOT_REF_RE = re.compile(r'(' + ATTR_GROUP + r'\s*=\s*["\'])(\./[^"\']+)(["\'])')

# Matches any quoted attribute value that is a bare relative path
BARE_REF_RE = re.compile(r'(' + ATTR_GROUP + r'\s*=\s*["\'])([^"\'#:\s][^"\']*?)(["\'])')

SKIP_PREFIXES = ('//', 'http', 'mailto:', 'tel:', 'javascript:', 'data:', 'blob:')


def repair(text, lang):
    def fix_shared(m):
        return m.group(1) + '../' + m.group(2)

    def fix_file(m):
        return m.group(1) + '../' + m.group(2) + m.group(3)

    out = ATTR_RE.sub(fix_shared, text)
    out = FILE_ATTR_RE.sub(fix_file, out)

    # Generic pass: a "./" reference that only resolves at the repository root.
    def fix_generic(m):
        prefix, ref, quote = m.group(1), m.group(2), m.group(3)
        target = ref[2:].split('#')[0].split('?')[0]
        if not target:
            return m.group(0)
        if os.path.exists(os.path.join(ROOT, lang, target.replace('/', os.sep))):
            return m.group(0)
        if os.path.exists(os.path.join(ROOT, target.replace('/', os.sep))):
            return prefix + '../' + ref[2:] + quote
        return m.group(0)

    out = DOT_REF_RE.sub(fix_generic, out)

    # Bare relative references ("card.html", "manifest.json", "downloads/x.zip")
    # that only resolve at the repository root.
    def fix_bare(m):
        prefix, ref, quote = m.group(1), m.group(2), m.group(3)
        if ref.startswith('./') or ref.startswith('../'):
            return m.group(0)
        if ref.lower().startswith(SKIP_PREFIXES):
            return m.group(0)
        if ref.endswith(('.js', '.css')) is False and '/' not in ref and '.' not in ref:
            return m.group(0)
        target = ref.split('#')[0].split('?')[0]
        if not target:
            return m.group(0)
        if os.path.exists(os.path.join(ROOT, lang, target.replace('/', os.sep))):
            return m.group(0)
        if os.path.exists(os.path.join(ROOT, target.replace('/', os.sep))):
            return prefix + '../' + ref + quote
        return m.group(0)

    out = BARE_REF_RE.sub(fix_bare, out)
    return out


def main():
    check_only = '--check' in sys.argv
    total = 0
    files = 0

    for lang in LANG_DIRS:
        lang_dir = os.path.join(ROOT, lang)
        if not os.path.isdir(lang_dir):
            continue
        for name in sorted(os.listdir(lang_dir)):
            if not name.endswith('.html'):
                continue
            full = os.path.join(lang_dir, name)
            with io.open(full, encoding='utf-8', errors='surrogateescape') as fh:
                src = fh.read()
            out = repair(src, lang)
            if out == src:
                continue
            files += 1
            delta = sum(1 for a, b in zip(src.split('\n'), out.split('\n')) if a != b)
            total += delta
            print('  repaired %-22s (%d line(s))' % (lang + '/' + name, delta))
            if not check_only:
                with io.open(full, 'w', encoding='utf-8', errors='surrogateescape', newline='') as fh:
                    fh.write(out)

    print('=' * 60)
    print('Files repaired: %d   Lines changed: %d' % (files, total))
    if check_only and files:
        print('Re-run without --check to apply the repair.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
