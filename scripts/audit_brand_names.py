# -*- coding: utf-8 -*-
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
variations = Counter()

for dirpath, dirs, files in os.walk(ROOT):
    if any(x in dirpath for x in ['.git', '_site', 'node_modules', '.tempmediaStorage', '.system_generated']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.md', '.py')):
            fp = os.path.join(dirpath, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    txt = fh.read()
                    matches = re.findall(r'S&R\s+CoreSync[^\n<"\',.\t]{0,50}', txt, re.I)
                    for m in matches:
                        clean = re.sub(r'\s+', ' ', m).strip()
                        variations[clean] += 1
            except Exception:
                pass

print("=" * 60)
print("Top 30 brand name strings found:")
print("=" * 60)
for k, v in variations.most_common(30):
    print(f"{v:5d} : {k}")
