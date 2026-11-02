import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Phase 1')
if idx != -1:
    print("Found Phase 1 at", idx)
    print(text[idx-200:idx+1500])
else:
    print("Phase 1 not found")
