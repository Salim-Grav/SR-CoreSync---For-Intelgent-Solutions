# -*- coding: utf-8 -*-
"""
Inline handler → event delegation migrator (CSP readiness, batch 1)
==================================================================
Rewrites `on<event>="fn()"` into `data-sr-call="fn"` for functions that are
provably safe to delegate:

  * the handler takes no arguments,
  * the function body exists in the tree,
  * the body never touches `this` (inline handlers bind `this` to the element;
    delegation binds it to the same element, so this check guards the rest).

Everything else (arguments, `this`, `event`, statements) is left untouched and
reported, to be rewritten by hand.

Usage:
  python scripts/migrate_inline_handlers.py --dry-run
  python scripts/migrate_inline_handlers.py            # apply
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_inline_handlers as audit  # noqa: E402

ROOT = audit.ROOT
SKIP_DIRS = audit.SKIP_DIRS

HANDLER = re.compile(r'\son(?P<event>[a-z]+)\s*=\s*"(?P<name>[A-Za-z_$][\w$]*)\s*\(\s*\)\s*;?\s*"', re.I)
SCRIPT_TAG = re.compile(r'js/sr-events\.js')
# Regions that must never be rewritten: a handler-looking string inside a script
# or a comment is data, not markup (the first run broke 4 pages this way).
OPAQUE = re.compile(r'(?is)<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->')


def migratable_functions():
    src = audit.js_sources()
    zero = {}
    for path in audit.html_files():
        with io.open(path, encoding='utf-8', errors='ignore') as fh:
            doc = fh.read()
        for match in audit.ATTR.finditer(doc):
            value = match.group(2).strip()
            call = audit.CALL.match(value)
            if not call or call.group(1) == 'if':
                continue
            if call.group(2).strip() != '':
                continue
            zero[call.group(1)] = zero.get(call.group(1), 0) + 1

    safe = set()
    for name in zero:
        body = audit.function_body(src, name)
        if body is None:
            continue
        if re.search(r'\bthis\b', body):
            continue
        safe.add(name)
    return safe, zero


def prefix_for(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    return './' if '/' not in rel else '../'


def main():
    dry_run = '--dry-run' in sys.argv
    safe, zero = migratable_functions()

    converted = 0
    files = 0
    skipped = 0
    remaining = 0
    for path in sorted(audit.html_files()):
        with io.open(path, encoding='utf-8', newline='') as fh:
            doc = fh.read()
        original = doc

        def repl(match):
            nonlocal converted, skipped
            name = match.group('name')
            if name not in safe:
                skipped += 1
                return match.group(0)
            converted += 1
            event = match.group('event').lower()
            attr = 'data-sr-call'
            out = ' %s="%s"' % (attr, name)
            if event != 'click':
                out += ' data-sr-on="%s"' % event
            return out

        def rewrite(markup):
            return HANDLER.sub(repl, markup)

        # Apply only to the gaps between <script>/<style>/comments.
        pieces = []
        cursor = 0
        for block in OPAQUE.finditer(doc):
            pieces.append(rewrite(doc[cursor:block.start()]))
            pieces.append(block.group(0))
            cursor = block.end()
        pieces.append(rewrite(doc[cursor:]))
        doc = ''.join(pieces)
        remaining += len(audit.ATTR.findall(doc))
        if doc != original:
            files += 1
            if not SCRIPT_TAG.search(doc):
                spans = [(m.start(), m.end()) for m in OPAQUE.finditer(doc)]

                def inside_opaque(pos):
                    return any(start <= pos < end for start, end in spans)

                # Pages that build e-mail/HTML templates in JS contain a
                # '</body>' string; the runtime tag must go before the real
                # closing tag, never inside a script block.
                target = -1
                for hit in re.finditer(r'</body>', doc, re.I):
                    if not inside_opaque(hit.start()):
                        target = hit.start()
                if target >= 0:
                    tag = '<script src="%sjs/sr-events.js" defer></script>\n' % prefix_for(path)
                    doc = doc[:target] + tag + doc[target:]
            if not dry_run:
                with io.open(path, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(doc)

    print('=' * 72)
    print('S&R CoreSync - inline handler migration' + (' (DRY RUN)' if dry_run else ''))
    print('=' * 72)
    print('safe functions      : %d' % len(safe))
    print('handlers converted  : %d' % converted)
    print('files touched       : %d' % files)
    print('handlers left inline: %d (need manual rewrites)' % remaining)
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
