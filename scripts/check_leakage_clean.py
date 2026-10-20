# -*- coding: utf-8 -*-
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

langs = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, 'demo.html'))]
non_ar_langs = [d for d in langs if d not in ['ckb']]

arabic_pattern = re.compile(r'[\u0600-\u06FF]')

leaks = {}
for lang in non_ar_langs:
    with open(f'{lang}/demo.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    ar_lines = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('<!--') or 'العربية' in stripped or 'data-name=' in stripped or 'sovereign-lang-' in stripped:
            continue
        if arabic_pattern.search(stripped):
            ar_lines.append((idx+1, stripped[:60]))
    if ar_lines:
        leaks[lang] = len(ar_lines)

print("Non-Arabic portals with text leakage:", leaks)
