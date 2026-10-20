# -*- coding: utf-8 -*-
with open('en/index.html', 'r', encoding='utf-8') as f:
    en = f.read()
with open('nl/index.html', 'r', encoding='utf-8') as f:
    nl = f.read()

print('en/index.html ../demo.html:', en.count('href="../demo.html"'), 'demo.html:', en.count('href="demo.html"'))
print('nl/index.html ../demo.html:', nl.count('href="../demo.html"'), 'demo.html:', nl.count('href="demo.html"'))
