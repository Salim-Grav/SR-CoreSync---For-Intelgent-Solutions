import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<img[^>]*src=[\'"]([^\'"]*(?:founder|salim|raed)[^\'"]*)[\'"][^>]*>', text, re.I):
    print(m.group(0))

for m in re.finditer(r'<source[^>]*srcset=[\'"]([^\'"]*(?:founder|salim|raed)[^\'"]*)[\'"][^>]*>', text, re.I):
    print(m.group(0))
