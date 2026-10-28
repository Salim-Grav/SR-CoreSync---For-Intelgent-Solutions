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

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for fname in ['css/demo-portal.css', 'css/enterprise-suite.min.css']:
    p = os.path.join(base_dir, fname)
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()

        # Replace any variation of user-select with full comprehensive vendor prefixes
        c = c.replace(
            '-webkit-user-select: none;\n    user-select: none;',
            '-webkit-touch-callout: none;\n    -webkit-user-select: none;\n    -moz-user-select: none;\n    -ms-user-select: none;\n    user-select: none;'
        )

        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)

print("Comprehensive vendor prefixes added to CSS files!")
