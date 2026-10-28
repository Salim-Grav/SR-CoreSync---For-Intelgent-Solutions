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
count = 0

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c = fh.read()

            orig = c

            # Fix stray / before title
            c = re.sub(r'oninput="calcPortalRoi\(\)"\s*/\s*title=', 'title=', c)
            # Reconstruct clean range inputs
            c = re.sub(
                r'<input type="range" min="3" max="250" value="20" class="roi-range-input" id="slideRoiTeam"[^>]*>',
                '<input type="range" min="3" max="250" value="20" class="roi-range-input" id="slideRoiTeam" title="Team Size / Employees" aria-label="Team Size / Employees" oninput="calcPortalRoi()" />',
                c
            )
            c = re.sub(
                r'<input type="range" min="5" max="60" value="18" class="roi-range-input" id="slideRoiHours"[^>]*>',
                '<input type="range" min="5" max="60" value="18" class="roi-range-input" id="slideRoiHours" title="Manual Hours per Week" aria-label="Manual Hours per Week" oninput="calcPortalRoi()" />',
                c
            )
            c = re.sub(
                r'<input type="range" min="15" max="150" value="45" step="5" class="roi-range-input" id="slideRoiCost"[^>]*>',
                '<input type="range" min="15" max="150" value="45" step="5" class="roi-range-input" id="slideRoiCost" title="Average Hourly Cost" aria-label="Average Hourly Cost" oninput="calcPortalRoi()" />',
                c
            )

            if c != orig:
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(c)
                count += 1

print(f"Cleaned ROI range inputs in {count} files!")
