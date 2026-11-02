import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/sr-geo-lang.js', 'r', encoding='utf-8') as f:
    print(f.read())

