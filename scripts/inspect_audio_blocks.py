import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'femaleKeywords', text)]
for idx, m in enumerate(matches):
    print(f"=== MATCH {idx+1} AT {m} ===")
    print(text[m-50:m+900])
