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

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

targets = [
    re.compile(r'S&R\s+CoreSync\s+Solutions\s+&\s+Engineering', re.I),
    re.compile(r'S&R\s+CoreSync\s+Solutions\s+B\.V\.', re.I),
    re.compile(r'S&R\s+CoreSync™?\s+Solutions', re.I),
]

results = []

for dirpath, dirs, files in os.walk(ROOT):
    if any(x in dirpath for x in ['.git', '_site', 'node_modules', '.tempmediaStorage', '.system_generated']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.md', '.py')):
            fp = os.path.join(dirpath, f)
            rel = os.path.relpath(fp, ROOT)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    txt = fh.read()
                count = 0
                for t in targets:
                    count += len(t.findall(txt))
                if count > 0:
                    results.append((rel, count))
            except Exception:
                pass

print(f"Total files matched: {len(results)}")
print(f"Total occurrences: {sum(c for _, c in results)}")
for r, c in sorted(results, key=lambda x: -x[1])[:20]:
    print(f"{c:4d} : {r}")
