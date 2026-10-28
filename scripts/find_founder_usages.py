"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<img[^>]*src=[\'"]([^\'"]*(?:founder|salim|raed)[^\'"]*)[\'"][^>]*>', text, re.I):
    print("IMG:", m.group(0)[:160])

for m in re.finditer(r'<source[^>]*srcset=[\'"]([^\'"]*(?:founder|salim|raed)[^\'"]*)[\'"][^>]*>', text, re.I):
    print("SOURCE:", m.group(0)[:160])
