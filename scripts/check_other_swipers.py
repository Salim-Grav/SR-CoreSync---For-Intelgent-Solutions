import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'new\s+Swiper\s*\([^)]*\)', text):
    print(m.group(0))
