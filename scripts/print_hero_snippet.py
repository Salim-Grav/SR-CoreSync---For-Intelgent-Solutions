import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for d in ['en', 'fr', 'de']:
    path = f"{d}/index.html"
    with open(path, encoding='utf-8') as f:
        content = f.read()
    idx = content.find('hero-reference__actions')
    idx_end = content.find('</div>', content.find('</div>', idx) + 1)
    print(f"=== {d} ===")
    print(content[idx:idx_end+6])

