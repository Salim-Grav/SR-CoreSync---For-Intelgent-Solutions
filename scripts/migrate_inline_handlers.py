# -*- coding: utf-8 -*-
"""
Inline handler → event delegation migrator
==========================================
Rewrites `on<event>="fn(...)"` into `data-sr-call` / `data-sr-args` for the
handlers that can be moved without changing behaviour:

  * the argument list is empty, or made only of literals (strings, numbers,
    booleans, null) that parse cleanly,
  * the function body exists in the tree,
  * the body never touches `this` (inline handlers bind `this` to the element;
    delegation binds the same element, so the check keeps semantics identical).

Handlers that read `this`, `event`, DOM globals, or contain statements are left
alone and reported.

The rewrite never runs inside <script>, <style> or comments: a handler-looking
string there is data, not markup.

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

HANDLER = re.compile(
    r'\son(?P<event>[a-z]+)\s*=\s*"(?P<name>(?:window\.)?[A-Za-z_$][\w$]*)\s*\((?P<args>[^"]*)\)\s*;?\s*"',
    re.I)
SCRIPT_TAG = re.compile(r'js/sr-events\.js')
OPAQUE = re.compile(r'(?is)<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->')

LITERAL_SAFE = re.compile(r"""^[\s'"[\]{}\d.,:eE+\-truefalsnul]*$""")


def parse_args(raw):
    """Return a list of literals, or None when the arguments are not literal."""
    text = raw.strip()
    if not text or text == ',':
        return []
    try:
        tree = ast.parse('(' + text + ')', mode='eval')
    except SyntaxError:
        return None
    try:
        node = tree.body
        if isinstance(node, ast.Tuple):
            values = [ast.literal_eval(elt) for elt in node.elts]
        else:
            values = [ast.literal_eval(node)]
    except (ValueError, SyntaxError):
        return None
    for v in values:
        if isinstance(v, (str, int, float, bool)) or v is None:
            continue
        return None
    return values


def safe_functions():
    """Functions whose bodies exist and never use `this`."""
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

    safe = set()
    for name in candidates:
        body = audit.function_body(src, name)
        if body is None:
            continue
        if re.search(r'\bthis\b', body):
            continue
        safe.add(name)
    return safe


def prefix_for(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    return './' if '/' not in rel else '../'


def main():
    dry_run = '--dry-run' in sys.argv
    safe = safe_functions()

    converted_zero = 0
    converted_args = 0
    converted_this = 0
    files = 0
    left = 0
    remaining = 0

    for path in sorted(audit.html_files()):
        with io.open(path, encoding='utf-8', newline='') as fh:
            doc = fh.read()
        original = doc

        def repl(match):
            nonlocal converted_zero, converted_args, converted_this, left
            name = match.group('name')
            if name.startswith('window.'):
                name = name[len('window.'):]
            raw = match.group('args')
            if name not in safe:
                left += 1
                return match.group(0)
            pass_element = False

            # onclick="window.print()" is the same call as print(); strip the
            # namespace so the delegated form stays identical.
            win_ns = re.match(r'^\s*window\.([A-Za-z_$][\w$]*)\s*\(', raw)
            if win_ns and raw.lstrip().startswith('window.'):
                name = win_ns.group(1)

            stripped = raw.lstrip()
            if stripped.startswith('this'):
                remainder = stripped[4:]
                if remainder.strip() == '':
                    raw, pass_element = '', True
                elif remainder.lstrip().startswith(','):
                    raw, pass_element = remainder.lstrip()[1:], True
                else:
                    left += 1
                    return match.group(0)

            values = parse_args(raw)
            if values is None:
                left += 1
                return match.group(0)

            event = match.group('event').lower()
            if values:
                payload = json.dumps(values, ensure_ascii=False).replace("'", '&#39;')
                out = ' data-sr-call="%s" data-sr-args=\'%s\'' % (name, payload)
                converted_args += 1
            else:
                out = ' data-sr-call="%s"' % name
                converted_zero += 1
            if pass_element:
                out += ' data-sr-this="1"'
                converted_this += 1
            if event != 'click':
                out += ' data-sr-on="%s"' % event
            return out

        def rewrite(markup):
            # event.stopPropagation() carries no function call to delegate: the
            # runtime only has to reproduce the stop, not preventDefault.
            markup = re.sub(r'\son[a-z]+\s*=\s*"\s*event\.stopPropagation\(\)\s*;?\s*"',
                            ' data-sr-stop="1"', markup, flags=re.I)
            return HANDLER.sub(repl, markup)

        pieces = []
        cursor = 0
        for block in OPAQUE.finditer(doc):
            pieces.append(rewrite(doc[cursor:block.start()]))
            pieces.append(block.group(0))
            cursor = block.end()
        pieces.append(rewrite(doc[cursor:]))
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
    print('safe functions        : %d' % len(safe))
    print('converted (no args)   : %d' % converted_zero)
    print('converted (with args) : %d' % converted_args)
    print('converted (this-aware): %d' % converted_this)
    print('files touched         : %d' % files)
    print('handlers left inline  : %d' % remaining)
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
