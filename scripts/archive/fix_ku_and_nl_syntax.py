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

import os
import re

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f == 'demo.html':
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c = fh.read()

            orig = c

            # Fix countAll / countPaid variables
            c = re.sub(r'const\s+count\w+(\s+\w+)?\s*=\s*document\.getElementById\(\'count-all\'\);', "const countAll = document.getElementById('count-all');", c)
            c = re.sub(r'const\s+count\w+(\s+\w+)?\s*=\s*document\.getElementById\(\'count-paid\'\);', "const countPaid = document.getElementById('count-paid');", c)
            c = re.sub(r'if\s*\(count[^\)]+\)\s*count[^\.]+\.innerText\s*=\s*parseInt\(count[^\.]+\.innerText\s*\|\|\s*\'3\'\)\s*\+\s*1;', "if (countAll) countAll.innerText = parseInt(countAll.innerText || '3') + 1;", c)
            c = re.sub(r'if\s*\(count[^\)]+\)\s*count[^\.]+\.innerText\s*=\s*parseInt\(count[^\.]+\.innerText\s*\|\|\s*\'2\'\)\s*\+\s*1;', "if (countPaid) countPaid.innerText = parseInt(countPaid.innerText || '2') + 1;", c)

            # Fix kassa's in Dutch
            c = c.replace("kassa's", "kassa\\'s")
            c = c.replace("kassa\\\\\\'s", "kassa\\'s")

            if c != orig:
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(c)
                print(f"Patched: {os.path.relpath(p, base_dir)}")

print("Fixed KU and NL syntax!")
