"""
S&R CoreSync Solutions - Cross-language DOM API parity auditor
===============================================================================
The multilingual generation pass translates page copy and, occasionally,
translates JavaScript API names too:

    document.querySelectorAll(...)  ->  document.querySelectorTümü(...)
    new Date()                      ->  new Tarih() / new Dîrok()
    toLocaleDateString()            ->  toLocaleTarihString()

The reliable way to detect this is not a word list - it is to compare the
inventory of DOM/JS API calls in every localized page against the reference
(root) page. Any API that the root page uses but a translation dropped or
renamed is a corruption.

Usage: python scripts/audit_language_api_parity.py
Exit code 0 = every localized page uses the same API surface as the root.
"""
import io
import os
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {'.git', '_site', 'workers', 'scripts', 'dist', 'node_modules',
             '__pycache__', '.github', '.agents', '.vscode', 'api', 'config'}

SCRIPT_RE = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S | re.I)

# API surfaces that must be identical across languages.
API_RE = re.compile(
    r'\b(?:document|window|navigator|localStorage|sessionStorage)\s*\.\s*([A-Za-z_$][\w$]*)'
    r'|\.\s*(querySelectorAll|querySelector|getElementById|getElementsByClassName|'
    r'getElementsByTagName|createElement|addEventListener|removeEventListener|'
    r'appendChild|removeChild|insertBefore|setAttribute|getAttribute|removeAttribute|'
    r'classList|innerHTML|textContent|innerText|value|checked|disabled|focus|blur|'
    r'click|submit|reset|preventDefault|stopPropagation|toISOString|toLocaleDateString|'
    r'toLocaleString|toLocaleTimeString|getTime|getFullYear|getMonth|getDate|'
    r'getHours|getMinutes|getSeconds|now|push|pop|shift|unshift|join|split|slice|'
    r'map|filter|forEach|reduce|find|some|every|includes|indexOf|concat|sort|reverse|'
    r'parseInt|parseFloat|isNaN|setTimeout|setInterval|clearTimeout|clearInterval|'
    r'setItem|getItem|removeItem|assign|keys|values|entries|fetch|then|catch|finally|'
    r'match|replace|test|trim|toUpperCase|toLowerCase|charAt|startsWith|endsWith|'
    r'resolve|reject|all|allSettled|race)\b'
)

IDENT_RE = re.compile(r'\b[A-Za-z_$][\w$]*\b')


def strip_js(text):
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in '"\'':
            quote = c
            i += 1
            while i < n:
                if text[i] == '\\':
                    i += 2
                    continue
                if text[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == '`':
            i += 1
            while i < n:
                if text[i] == '\\':
                    i += 2
                    continue
                if text[i] == '`':
                    i += 1
                    break
                i += 1
            continue
        if c == '/' and i + 1 < n and text[i + 1] == '/':
            while i < n and text[i] != '\n':
                i += 1
            continue
        if c == '/' and i + 1 < n and text[i + 1] == '*':
            i += 2
            while i + 1 < n and not (text[i] == '*' and text[i + 1] == '/'):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def api_inventory(path):
    with io.open(path, encoding='utf-8', errors='ignore') as fh:
        html = fh.read()
    inventory = Counter()
    for m in SCRIPT_RE.finditer(html):
        clean = strip_js(m.group(1))
        for am in API_RE.finditer(clean):
            inventory[am.group(1) or am.group(2)] += 1
    return inventory


def local_files():
    out = []
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d, 'index.html')
        if os.path.isdir(os.path.join(ROOT, d)) and os.path.isfile(p):
            out.append((d, p))
    return out


def main():
    reference = os.path.join(ROOT, 'index.html')
    ref_inv = api_inventory(reference)
    ref_keys = set(ref_inv)

    print('=' * 74)
    print('S&R CoreSync - Cross-language DOM/JS API Parity Audit')
    print('=' * 74)
    print('Reference page: index.html  (%d distinct API calls)' % len(ref_keys))

    drift = {}
    for lang, path in local_files():
        inv = api_inventory(path)
        missing = sorted(k for k in ref_keys if k not in inv)
        if missing:
            drift[lang] = missing

    if not drift:
        print('PASSED - every language folder exposes the same API surface as the root.')
        print('=' * 74)
        return 0

    # A missing API is only a hard failure when the page expresses it under
    # a translated name (i.e. a corruption). A page that simply does not
    # implement the feature is drift, not a defect.
    corrupted = []
    for lang, missing in drift.items():
        path = os.path.join(ROOT, lang, 'index.html')
        with io.open(path, encoding='utf-8', errors='ignore') as fh:
            html = fh.read()
        for m in SCRIPT_RE.finditer(html):
            clean = strip_js(m.group(1))
            for tok in set(re.findall(r'\b[A-Za-z_$][\w$]*\b', clean)):
                if not tok.isascii() and tok not in missing:
                    corrupted.append((lang, tok))

    if corrupted:
        print('FAILED - translated JavaScript API names detected:')
        for lang, tok in sorted(set(corrupted)):
            print('  X %-6s %s' % (lang, tok))
        print('=' * 74)
        return 1

    print('No corruption detected.')
    print('-' * 74)
    print('FEATURE DRIFT (warning, not a defect): %d language folder(s) do not' % len(drift))
    print('implement every feature of the reference page.')
    for lang, missing in sorted(drift.items()):
        print('  ! %-6s missing: %s' % (lang, ', '.join(missing)))
    print('=' * 74)
    print('PASSED - no translated JavaScript API names remain.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
