"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import json
import re

with open('scripts/remaining_ar.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

unique_texts = set()
for line_no, line in items:
    # find inner text in tags
    inner = re.findall(r'>([^<]+)<', line)
    for t in inner:
        s = t.strip()
        if re.search(r'[\u0600-\u06FF]', s):
            unique_texts.add(s)
    # find attributes
    attrs = re.findall(r'(?:title|placeholder|aria-label|value)=["\']([^"\']+)["\']', line)
    for a in attrs:
        s = a.strip()
        if re.search(r'[\u0600-\u06FF]', s):
            unique_texts.add(s)
    # find js strings
    js_strs = re.findall(r'["\']([^"\']+)["\']', line)
    for j in js_strs:
        s = j.strip()
        if re.search(r'[\u0600-\u06FF]', s):
            unique_texts.add(s)

print(f'Found {len(unique_texts)} unique text strings')
with open('scripts/unique_ar_strings.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(list(unique_texts)), f, ensure_ascii=False, indent=2)
