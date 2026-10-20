# -*- coding: utf-8 -*-
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('en/demo.html', 'r', encoding='utf-8') as f:
    c_en = f.read()

with open('fr/demo.html', 'r', encoding='utf-8') as f:
    c_fr = f.read()

# Let's find script tags in both
s_en = re.search(r'<script>([\s\S]*?)<\/script>\s*<div id="publishSoftwareModal"', c_en)
s_fr = re.search(r'<script>([\s\S]*?)<\/script>\s*<div id="publishSoftwareModal"', c_fr)

print('EN script found:', bool(s_en))
print('FR script found:', bool(s_fr))

if s_en and s_fr:
    en_code = s_en.group(1)
    fr_code = s_fr.group(1)
    print('EN len:', len(en_code), 'FR len:', len(fr_code))
