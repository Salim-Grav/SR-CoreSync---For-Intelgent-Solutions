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
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, 'index.html'), encoding='utf-8') as f:
    c = f.read()

tags = re.findall(r'<img[^>]+>', c)
no_lazy = [t for t in tags if 'loading=' not in t]
print(f"Total img tags: {len(tags)}, without loading: {len(no_lazy)}")
for t in no_lazy:
    src_m = re.search(r'src="([^"]+)"', t)
    cls_m = re.search(r'class="([^"]+)"', t)
    src = src_m.group(1) if src_m else 'no-src'
    cls = cls_m.group(1) if cls_m else 'no-class'
    print(f"  src: {src:<40} class: {cls}")
