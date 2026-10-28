"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import glob

files = glob.glob('**/*.html', recursive=True)
count = 0
for p in files:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    c = c.replace("data-sr-args=\\'[\"erp\"]\\'>", 'data-sr-args=\'["erp"]\'>')
    c = c.replace("data-sr-args=\\'[\"cloud\"]\\'>", 'data-sr-args=\'["cloud"]\'>')
    c = c.replace("data-sr-args=\\'[\"gov\"]\\'>", 'data-sr-args=\'["gov"]\'>')
    if c != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        count += 1

print(f"Fixed quotes in {count} files.")
