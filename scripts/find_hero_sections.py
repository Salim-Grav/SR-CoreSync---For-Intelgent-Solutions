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

import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:1200]):
    lower = line.lower()
    if 'hero' in lower or 'emblem' in lower:
        # safe print without unicode error
        safe_line = line.strip().encode('ascii', 'replace').decode('ascii')
        print(f"{i+1}: {safe_line[:120]}")
