# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('id="pricing"')
print("idx:", idx)
if idx != -1:
    print(c[idx-50:idx+400])
