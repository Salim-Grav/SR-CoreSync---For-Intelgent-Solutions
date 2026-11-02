import re

with open('en/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', c)
for s in scripts:
    print(s)
