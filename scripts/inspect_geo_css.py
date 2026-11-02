import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('css/sr-geo-lang.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.sr-geolang-banner')
print(text[idx:idx+2500])
