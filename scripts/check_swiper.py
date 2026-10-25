# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script[^>]*src=[^>]*>', text, re.I)
for s in scripts:
    if 'swiper' in s.lower():
        print("Swiper script:", s)

print("Total scripts found:", len(scripts))

links = re.findall(r'<link[^>]*href=[^>]*>', text, re.I)
for l in links:
    if 'swiper' in l.lower():
        print("Swiper link:", l)

# Check if Swiper is bundled in dananajmah-bundle or somewhere
for path in ['css/dananajmah-bundle.min.css', 'js/enterprise-suite.min.js']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            t = f.read()
        print(f"Swiper in {path}:", 'swiper' in t.lower())
    except Exception as e:
        print(e)
