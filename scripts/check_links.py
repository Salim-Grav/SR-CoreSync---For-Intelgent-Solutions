# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

with open('en/index.html', 'r', encoding='utf-8') as f:
    en = f.read()
with open('nl/index.html', 'r', encoding='utf-8') as f:
    nl = f.read()

print('en/index.html ../demo.html:', en.count('href="../demo.html"'), 'demo.html:', en.count('href="demo.html"'))
print('nl/index.html ../demo.html:', nl.count('href="../demo.html"'), 'demo.html:', nl.count('href="demo.html"'))
