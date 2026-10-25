# -*- coding: utf-8 -*-
import os
import re
import glob

# All 29 root and localized directories
languages = [
    '', 'bg', 'ckb', 'cs', 'da', 'de', 'el', 'en', 'es', 'et',
    'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt',
    'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'tr'
]

pattern = re.compile(r'[ \t]*<div class="hero-emblem-actions-bar">.*?</div>\s*(?=</div>\s*</div>\s*</div>)', re.DOTALL)

count = 0
for lang in languages:
    path = os.path.join(lang, 'index.html') if lang else 'index.html'
    if not os.path.exists(path):
        print(f"Skipping non-existent: {path}")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, n = pattern.subn('', content)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated {path} (removed {n} occurrences)")
        count += 1
    else:
        print(f"WARNING: Pattern did not match in {path}")

print(f"\nTotal files updated: {count} of {len(languages)}")
