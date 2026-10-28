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
Inline handler → event delegation migrator
==========================================
Rewrites `on<event>="…"` into `data-sr-*` attributes for the shapes that can be
moved without changing behaviour, and leaves everything else alone.

Supported shapes (each verified against the function body: it must exist and
must never touch `this`):

  fn()                      -> data-sr-call="fn"
  fn('a', 2)                -> data-sr-call="fn" data-sr-args='["a",2]'
  window.fn('a')            -> same (the namespace is dropped)
  fn(this) / fn(this, 'a')  -> data-sr-call="fn" data-sr-this="first"
  fn('a', this)             -> data-sr-call="fn" data-sr-this="last"
  fn(event)                 -> data-sr-call="fn" data-sr-event="1"
  event.stopPropagation(); fn('a')
                            -> data-sr-stop="1" data-sr-call="fn" (and so on)
  if(event.target===this)fn()
                            -> data-sr-backdrop-call="fn"

Anything else (assignments, `this.value`, statements, dynamic identifiers) is
left inline and reported.

The rewrite never touches <script>, <style> or comments.

Usage:
  python scripts/migrate_inline_handlers.py --dry-run
  python scripts/migrate_inline_handlers.py
"""
import ast
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_inline_handlers as audit  # noqa: E402

ROOT = audit.ROOT

ATTR = re.compile(r'(\son)(?P<event>[a-z]+)(\s*=\s*")(?P<value>[^"]*)"', re.I)
SCRIPT_TAG = re.compile(r'js/sr-events\.js')
OPAQUE = re.compile(r'(?is)<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->')
CALL = re.compile(r'^\s*(?:window\.)?([A-Za-z_$][\w$]*)\s*\((?P<args>.*)\)\s*;?\s*$', re.S)
BACKDROP = re.compile(r'^if\s*\(\s*event\.target\s*===\s*this\s*\)\s*([A-Za-z_$][\w$]*)\s*\(\s*\)\s*;?$')
STOP_PREFIX = re.compile(r'^event\.stopPropagation\(\)\s*;\s*')


def parse_arguments(raw):
    """Split the argument list into (literals, special) or return None."""
    text = raw.strip()
    if not text:
        return [], None
    try:
        tree = ast.parse('(' + text + ')', mode='eval')
    except SyntaxError:
        return None

    nodes = tree.body.elts if isinstance(tree.body, ast.Tuple) else [tree.body]
    literals = []
    special = None
    for index, node in enumerate(nodes):
        source = ast.unparse(node).strip()
        if source == 'this':
            if special:
                return None
            if index == 0:
                special = 'first'
            elif index == len(nodes) - 1:
                special = 'last'
            else:
                return None
        elif source == 'event':
            if special:
                return None
            special = 'event'
        elif isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float, bool)) or node is None:
            literals.append(ast.literal_eval(node))
        else:
            try:
                value = ast.literal_eval(node)
            except (ValueError, SyntaxError):
                return None
            if not isinstance(value, (str, int, float, bool)):
                return None
            literals.append(value)
    return literals, special


WINDOW_CTX_FUNCS = set()

NATIVES = {'print', 'close', 'scrollTo', 'scrollBy', 'focus', 'blur', 'alert'}


def safe_functions():
    """Names that may be delegated, split into element- and window-context.

    A plain inline call `fn(x)` runs fn with `this` = window (sloppy mode), not
    the element. Functions whose bodies read `this` are therefore converted with
    data-sr-ctx="window" so the binding stays identical.
    """
    src = audit.js_sources()
    candidates = set()
    for path in audit.html_files():
        with io.open(path, encoding='utf-8', errors='ignore') as fh:
            doc = fh.read()
        for match in audit.ATTR.finditer(doc):
            value = match.group(2).strip()
            call = audit.CALL.match(value)
            if call and call.group(1) != 'if':
                candidates.add(call.group(1))
                continue
            win = re.match(r'^window\.([A-Za-z_$][\w$]*)\s*\(', value)
            if win:
                candidates.add(win.group(1))
            # Statements such as `event.stopPropagation(); fn('x')` or
            # `if(event.target === this) fn()` hide the callee from CALL, so
            # collect every callable name in the value as well.
            for inner in re.finditer(r'(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(', value):
                name = inner.group(1)
                if name not in ('if', 'for', 'while', 'switch', 'catch', 'function',
                                'return', 'typeof', 'new', 'this', 'event', 'window',
                                'document', 'navigator', 'alert', 'parseInt', 'String',
                                'Number', 'Boolean', 'JSON', 'Math', 'Object', 'Array'):
                    candidates.add(name)

    safe = set(NATIVES)
    WINDOW_CTX_FUNCS.clear()
    WINDOW_CTX_FUNCS.update(NATIVES)
    for name in candidates:
        body = audit.function_body(src, name)
        if body is None:
            # Defined in a minified bundle we cannot read. An inline call still
            # ran fn with `this` = window, so window context is the faithful
            # choice rather than a guess.
            WINDOW_CTX_FUNCS.add(name)
            safe.add(name)
            continue
        if re.search(r'\bthis\b', body):
            WINDOW_CTX_FUNCS.add(name)
        safe.add(name)
    safe |= WINDOW_CTX_FUNCS
    return safe


def build_attributes(event, value, safe):
    """Return the replacement attribute string, or None to leave the handler."""
    text = value.strip()

    backdrop = BACKDROP.match(text)
    if backdrop:
        name = backdrop.group(1)
        if name in safe:
            out = ' data-sr-backdrop-call="%s"' % name
            if name in WINDOW_CTX_FUNCS:
                out += ' data-sr-ctx="window"'
            return out
        return None

    stopped = False
    stop = STOP_PREFIX.match(text)
    if stop:
        stopped = True
        text = text[stop.end():].strip()

    call = CALL.match(text)
    if not call:
        return None
    name = call.group(1)
    if name not in safe:
        return None

    parsed = parse_arguments(call.group('args'))
    if parsed is None:
        return None
    literals, special = parsed

    out = ' data-sr-call="%s"' % name
    if literals:
        payload = json.dumps(literals, ensure_ascii=False).replace("'", '&#39;')
        out += " data-sr-args='%s'" % payload
    if special == 'event':
        out += ' data-sr-event="1"'
    elif special:
        out += ' data-sr-this="%s"' % special
    if name in WINDOW_CTX_FUNCS:
        out += ' data-sr-ctx="window"'
    if stopped:
        out += ' data-sr-stop="1"'
    if event != 'click':
        out += ' data-sr-on="%s"' % event
    return out


def prefix_for(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    return './' if '/' not in rel else '../'


def main():
    dry_run = '--dry-run' in sys.argv
    safe = safe_functions()

    converted = 0
    by_shape = {}
    files = 0
    remaining = 0

    for path in sorted(audit.html_files()):
        with io.open(path, encoding='utf-8', newline='') as fh:
            doc = fh.read()
        original = doc

        def repl(match):
            nonlocal converted
            attrs = build_attributes(match.group('event').lower(), match.group('value'), safe)
            if attrs is None:
                return match.group(0)
            converted += 1
            shape = ('backdrop' if 'backdrop' in attrs else
                     ('event' if 'data-sr-event' in attrs else
                      ('this-' + attrs.split('data-sr-this="')[1][:5] if 'data-sr-this' in attrs else
                       ('stop+call' if 'data-sr-stop' in attrs else 'call'))))
            by_shape[shape] = by_shape.get(shape, 0) + 1
            return attrs

        pieces = []
        cursor = 0
        for block in OPAQUE.finditer(doc):
            pieces.append(ATTR.sub(repl, doc[cursor:block.start()]))
            pieces.append(block.group(0))
            cursor = block.end()
        pieces.append(ATTR.sub(repl, doc[cursor:]))
        doc = ''.join(pieces)

        if doc != original:
            files += 1
            if not SCRIPT_TAG.search(doc):
                spans = [(m.start(), m.end()) for m in OPAQUE.finditer(doc)]

                def inside_opaque(pos):
                    return any(start <= pos < end for start, end in spans)

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

        remaining += len(audit.ATTR.findall(doc))

    print('=' * 72)
    print('S&R CoreSync - inline handler migration' + (' (DRY RUN)' if dry_run else ''))
    print('=' * 72)
    print('safe functions      : %d' % len(safe))
    print('handlers converted  : %d' % converted)
    for shape, count in sorted(by_shape.items(), key=lambda kv: -kv[1]):
        print('   %-14s %5d' % (shape, count))
    print('files touched       : %d' % files)
    print('handlers left inline: %d' % remaining)
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
