# -*- coding: utf-8 -*-
import re
with open('demo.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('sovereign-hotline-widget')
sub = text[:idx]

tokens = re.finditer(r'(<div[^>]*>|</div>)', sub)
stack = []
for m in tokens:
    t = m.group(1)
    if t.startswith('<div'):
        m_id = re.search(r'id=["\']([^"\']+)["\']', t)
        m_cls = re.search(r'class=["\']([^"\']+)["\']', t)
        desc = (m_id.group(1) if m_id else '') + ' ' + (m_cls.group(1) if m_cls else '')
        line_no = sub[:m.start()].count('\n') + 1
        stack.append((line_no, desc.strip()))
    else:
        if stack:
            stack.pop()

print("Unclosed divs on stack:")
for l, d in stack:
    print(f"Line {l}: {d}")
