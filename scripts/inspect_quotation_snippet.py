import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Phase 1: Design & Identity')
if idx != -1:
    print("Found at", idx)
    print(text[idx-300:idx+2200])
