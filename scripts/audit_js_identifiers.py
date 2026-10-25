"""
S&R CoreSync For Intelligent Solutions - JavaScript identifier corruption scanner
===============================================================================
The multilingual generation pass translates page copy. When it touches an
inline <script> block it can translate JavaScript *built-ins* as well, e.g.

    new Date()   ->   new Datum()   /  new Fecha()  /  new Tarih()  /  new Dato()

which throws a TypeError at runtime and silently destroys the lead payload.

This scanner walks every inline <script> block in every published HTML page,
extracts the JavaScript, strips strings/comments, and reports any non-ASCII
identifier or any known built-in that was replaced by a foreign translation.

Usage: python scripts/audit_js_identifiers.py
Exit code 0 = no corruption detected.
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {'.git', '_site', 'workers', 'scripts', 'dist', 'node_modules',
             '__pycache__', '.github', '.agents', '.vscode', 'api', 'config'}

SCRIPT_RE = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S | re.I)
NON_ASCII_RE = re.compile(r'[^\x00-\x7F]')
# Identifiers that are valid JS but were produced by translating a built-in.
SUSPECT_BUILTINS = {
    'Datum', 'Fecha', 'Data', 'Tarih', 'Dato', 'Drok', 'Dřok', 'Datum',
    'Datum', 'Дата', '日期', '日付', '날짜', 'Tarih', 'Datum',
    'Массив', 'Объект', 'Строка', 'Число', 'Математика', 'Json',
}


def strip_js(text):
    """Remove strings, template literals and comments from JavaScript source."""
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
            out.append('""')
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
            out.append('""')
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


def main():
    problems = []
    scripts_scanned = 0
    identifiers_scanned = 0

    targets = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith('_')]
        for name in filenames:
            if name.endswith('.html'):
                targets.append(os.path.join(dirpath, name))

    for full in targets:
        rel = os.path.relpath(full, ROOT).replace('\\', '/')
        with io.open(full, encoding='utf-8', errors='ignore') as fh:
            html = fh.read()
        for m in SCRIPT_RE.finditer(html):
            body = m.group(1)
            if not body.strip():
                continue
            scripts_scanned += 1
            line = html[:m.start()].count('\n') + 1
            clean = strip_js(body)

            for ident in re.findall(r'\b[A-Za-z_$][\w$]*\b', clean):
                identifiers_scanned += 1
                if NON_ASCII_RE.search(ident):
                    problems.append((rel, line, 'non-ASCII identifier: %r' % ident))
                elif ident in SUSPECT_BUILTINS:
                    problems.append((rel, line, 'translated JavaScript built-in: %s' % ident))

    print('=' * 72)
    print('S&R CoreSync - JavaScript Identifier Integrity Audit')
    print('=' * 72)
    print('HTML files scanned      : %d' % len(targets))
    print('Inline scripts scanned : %d' % scripts_scanned)
    print('Identifiers inspected  : %d' % identifiers_scanned)

    if not problems:
        print('PASSED - no translated or corrupted JavaScript identifiers found.')
        print('=' * 72)
        return 0

    unique = []
    seen = set()
    for rel, line, msg in problems:
        key = (rel, msg)
        if key in seen:
            continue
        seen.add(key)
        unique.append((rel, line, msg))

    print('FAILED - %d corrupted identifier(s) in %d file(s):' % (len(problems), len(unique)))
    for rel, line, msg in unique:
        print('  X %-34s L%-7s %s' % (rel, line, msg))
    print('=' * 72)
    return 1


if __name__ == '__main__':
    sys.exit(main())
