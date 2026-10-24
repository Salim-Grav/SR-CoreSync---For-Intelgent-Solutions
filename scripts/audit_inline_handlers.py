# -*- coding: utf-8 -*-
"""
Inline event-handler inventory (CSP readiness)
==============================================
A strict `script-src` without 'unsafe-inline' is impossible while the markup
carries inline handlers (`onclick="…"`). This tool measures exactly what is
there, classifies it, and reports how much can be migrated mechanically to
event delegation.

Classification:
  call-zero     onclick="fn()"                 -> safe to delegate (if fn has no `this`)
  call-literal  onclick="fn('a', 2, true)"     -> delegable with arguments
  call-dynamic  onclick="fn(this, event, …)"   -> needs a manual rewrite
  statement     onclick="if (…) { … }"         -> needs a manual rewrite
  expression    onclick="document…style=…"     -> needs a manual rewrite

Usage:
  python scripts/audit_inline_handlers.py            # report
  python scripts/audit_inline_handlers.py --json out.json
"""
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'_site', '.git', 'node_modules', '__pycache__', 'dist', 'downloads'}

ATTR = re.compile(r'\son([a-z]+)\s*=\s*"([^"]*)"', re.I)
CALL = re.compile(r'^\s*([A-Za-z_$][\w$]*)\s*\((.*)\)\s*;?\s*$', re.S)
LITERAL = re.compile(r"""^(\s*(?:'[^'\\]*'|"[^"\\]*"|\d+(?:\.\d+)?|true|false|null)\s*(?:,\s*(?:'[^'\\]*'|"[^"\\]*"|\d+(?:\.\d+)?|true|false|null)\s*)*)?$""")


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith('.html'):
                yield os.path.join(dirpath, name)


def js_sources():
    """Every inline <script> body and every js/*.js file, for `this` detection."""
    chunks = []
    for path in html_files():
        with io.open(path, encoding='utf-8', errors='ignore') as fh:
            doc = fh.read()
        for body in re.findall(r'(?is)<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', doc):
            chunks.append(body)
    jsdir = os.path.join(ROOT, 'js')
    if os.path.isdir(jsdir):
        for name in os.listdir(jsdir):
            if name.endswith('.js'):
                with io.open(os.path.join(jsdir, name), encoding='utf-8', errors='ignore') as fh:
                    chunks.append(fh.read())
    return '\n'.join(chunks)


def function_body(src, name):
    """Best-effort extraction of `function name(...) { … }` or `name = (...) => {…}`."""
    patterns = [
        r'function\s+' + re.escape(name) + r'\s*\([^)]*\)\s*\{',
        r'\b' + re.escape(name) + r'\s*=\s*(?:async\s*)?function\s*\([^)]*\)\s*\{',
        r'\b' + re.escape(name) + r'\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{',
    ]
    for pattern in patterns:
        match = re.search(pattern, src)
        if not match:
            continue
        start = match.end() - 1
        depth = 0
        for i in range(start, min(len(src), start + 20000)):
            if src[i] == '{':
                depth += 1
            elif src[i] == '}':
                depth -= 1
                if depth == 0:
                    return src[start:i + 1]
        return src[start:start + 20000]
    return None


def main():
    kinds = Counter()
    by_event = Counter()
    zero_arg = Counter()
    literal_arg = Counter()
    dynamic = Counter()
    per_file = defaultdict(int)
    total = 0

    for path in html_files():
        rel = os.path.relpath(path, ROOT).replace('\\', '/')
        with io.open(path, encoding='utf-8', errors='ignore') as fh:
            doc = fh.read()
        for match in ATTR.finditer(doc):
            event, value = match.group(1).lower(), match.group(2).strip()
            total += 1
            by_event[event] += 1
            per_file[rel] += 1
            call = CALL.match(value)
            if call:
                name, args = call.group(1), call.group(2).strip()
                if name == 'if':
                    kinds['statement'] += 1
                    continue
                if args == '':
                    kinds['call-zero'] += 1
                    zero_arg[name] += 1
                elif LITERAL.match(args):
                    kinds['call-literal'] += 1
                    literal_arg[name] += 1
                else:
                    kinds['call-dynamic'] += 1
                    dynamic[name] += 1
            else:
                kinds['expression'] += 1

    src = js_sources()
    this_users = set()
    unknown = set()
    for name in set(zero_arg) | set(literal_arg):
        body = function_body(src, name)
        if body is None:
            unknown.add(name)
        elif re.search(r'\bthis\b', body):
            this_users.add(name)

    migratable = [(n, c) for n, c in zero_arg.items() if n not in this_users and n not in unknown]
    migratable.sort(key=lambda kv: -kv[1])

    print('=' * 74)
    print('S&R CoreSync - inline event-handler inventory')
    print('=' * 74)
    print('HTML files                      : %d' % len(per_file))
    print('Inline handlers                 : %d' % total)
    for kind, count in kinds.most_common():
        print('  %-14s %6d  (%.1f%%)' % (kind, count, 100.0 * count / total))
    print('Events                          : %s' % ', '.join('%s=%d' % kv for kv in by_event.most_common()))
    print('-' * 74)
    print('Zero-arg handlers               : %d across %d functions' % (sum(zero_arg.values()), len(zero_arg)))
    print('  of which use `this`           : %d functions' % len(this_users))
    print('  of which body not found       : %d functions' % len(unknown))
    print('  mechanically migratable now   : %d handlers (%d functions)' % (sum(c for _, c in migratable), len(migratable)))
    print('-' * 74)
    print('Top migratable functions:')
    for name, count in migratable[:15]:
        print('  %-32s %5d' % (name, count))
    if dynamic:
        print('-' * 74)
        print('Handlers needing a manual rewrite (top 10):')
        for name, count in Counter(dynamic).most_common(10):
            print('  %-32s %5d' % (name, count))

    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json') + 1]
        payload = {
            'total': total,
            'kinds': dict(kinds),
            'events': dict(by_event),
            'migratable': migratable,
            'this_users': sorted(this_users),
            'unknown': sorted(unknown),
        }
        with io.open(out, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print('\nJSON written to %s' % out)
    print('=' * 74)
    return 0


if __name__ == '__main__':
    sys.exit(main())
