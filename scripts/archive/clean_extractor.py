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

import re
import json

with open('demo.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Separate scripts from HTML
scripts = re.findall(r'<script.*?>.*?</script>', html, flags=re.DOTALL)
html_no_scripts = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)

# HTML text nodes
html_texts = re.findall(r'>([^<]*[\u0600-\u06FF]+[^<]*)<', html_no_scripts)
html_texts = [t.strip() for t in html_texts if t.strip()]

# HTML attributes (placeholder, title, aria-label, alt, value)
attrs = re.findall(r'(?:placeholder|title|aria-label|alt|value)=["\']([^"\']*[\u0600-\u06FF]+[^"\']*)["\']', html_no_scripts)
attrs = [a.strip() for a in attrs if a.strip()]

# Now inside scripts, find string literals containing Arabic
script_texts = []
for s in scripts:
    for q in ["'", '"']:
        pattern = q + r'([^' + q + r'\n\r]*[\u0600-\u06FF]+[^' + q + r'\n\r]*)' + q
        matches = re.findall(pattern, s)
        for m in matches:
            if m.strip():
                script_texts.append(m.strip())
    # Also find backtick strings or template literal fragments
    bt_matches = re.findall(r'`([^`]*[\u0600-\u06FF]+[^`]*)`', s)
    for b in bt_matches:
        # split by newlines or HTML tags if any
        sub_parts = re.findall(r'[\u0600-\u06FF][^\n\r<>$`]*', b)
        for sp in sub_parts:
            if sp.strip():
                script_texts.append(sp.strip())

all_unique = sorted(list(set(html_texts + attrs + script_texts)), key=len, reverse=True)
print(f'HTML Text nodes: {len(html_texts)}')
print(f'HTML Attrs: {len(attrs)}')
print(f'Script string literals: {len(script_texts)}')
print(f'Total clean unique Arabic phrases: {len(all_unique)}')

with open('scripts/clean_ar_phrases.json', 'w', encoding='utf-8') as out:
    json.dump(all_unique, out, ensure_ascii=False, indent=2)
print('Saved to scripts/clean_ar_phrases.json')
