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
    ar_html = f.read()

strings = []

# 1. Inside HTML tags: between > and <
for match in re.finditer(r'>([^<]*[\u0600-\u06FF]+[^<]*)<', ar_html):
    s = match.group(1).strip()
    if s:
        strings.append(s)

# 2. Inside attributes:
for match in re.finditer(r'[\s]([a-zA-Z0-9_\-]+)=["\']([^"\']*[\u0600-\u06FF]+[^"\']*)["\']', ar_html):
    s = match.group(2).strip()
    if s:
        strings.append(s)

# 3. Inside JS strings
for match in re.finditer(r'["\'`]([^"\'`\n\r]*[\u0600-\u06FF]+[^"\'`\n\r]*)["\'`]', ar_html):
    s = match.group(1).strip()
    if s:
        strings.append(s)

unique_s = sorted(list(set(strings)), key=len, reverse=True)
print(f'Total unique Arabic strings found: {len(unique_s)}')

with open('scripts/all_demo_ar_elements.json', 'w', encoding='utf-8') as f:
    json.dump(unique_s, f, ensure_ascii=False, indent=2)
print('Saved to scripts/all_demo_ar_elements.json')
