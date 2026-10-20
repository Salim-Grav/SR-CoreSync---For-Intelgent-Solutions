# -*- coding: utf-8 -*-
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f == 'demo.html' and root != BASE_DIR and not root.endswith('ckb'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c = fh.read()

            c = re.sub(r"desc:\s*'مؤشرات[^']+'", "desc: 'Accurate real-time metrics for annual revenue, operating cash flow, and cloud automation hours saved.'", c)

            if root.endswith('en'):
                c = re.sub(r"'ar':\s*'[^']+'", "'ar': 'Hello Eng. Salim, I would like to consult on deploying S&R CoreSync ERP for my enterprise...'", c)
                c = re.sub(r"'ckb':\s*'[^']+'", "'ckb': 'Hello Eng. Salim, I would like to consult on deploying S&R CoreSync ERP for my enterprise...'", c)

            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(c)

print("Zero-leakage final sweep completed!")
