"""
S&R CoreSync For Intelligent Solutions - Lead endpoint migration
Moves the client dispatcher from api/ to js/ and repoints the lead capture
fetch from the dead PHP gateway to the Cloudflare Worker.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'workers', 'scripts', 'dist', 'node_modules', '.agents', '.vscode'}

SCRIPT_TAG_RE = re.compile(
    r'(<script\s+src=")(?:\.\./|\./)api/lead-dispatcher\.js("\s*>)'
)

FETCH_BLOCK_RE = re.compile(
    r"fetch\('/api/lead-capture\.php',\s*\{"
    r"(?P<opts>.*?)"
    r"\}\)\s*\.catch\(\s*\(\)\s*=>\s*\{\s*\}\s*\);",
    re.DOTALL
)

NEW_FETCH = (
    "const leadEndpoint = (typeof window !== 'undefined' && window.SR_LEAD_ENDPOINT) "
    "|| 'https://api.sr-coresync.com/lead';\n"
    "                    fetch(leadEndpoint, {\n"
    "                        method: 'POST',\n"
    "                        headers: { 'Content-Type': 'application/json' },\n"
    "                        body: JSON.stringify(leadPayload)\n"
    "                    }).catch((err) => console.error('[LeadCapture] Dispatch failed:', err));"
)


def migrate_html(path):
    with io.open(path, encoding='utf-8', errors='surrogateescape') as fh:
        src = fh.read()

    original = src

    def tag_sub(m):
        prefix = m.group(1)
        rel = '../' if '../' in m.group(0) else './'
        return prefix + rel + 'js/sr-lead-dispatcher.js' + m.group(2)

    src = SCRIPT_TAG_RE.sub(tag_sub, src)
    src = FETCH_BLOCK_RE.sub(lambda m: NEW_FETCH, src)

    if src != original:
        with io.open(path, 'w', encoding='utf-8', errors='surrogateescape', newline='') as fh:
            fh.write(src)
        return True
    return False


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith('.html'):
                continue
            full = os.path.join(dirpath, name)
            if migrate_html(full):
                changed.append(os.path.relpath(full, ROOT))

    print('HTML files migrated: %d' % len(changed))
    for c in sorted(changed):
        print('  ' + c)


if __name__ == '__main__':
    main()
