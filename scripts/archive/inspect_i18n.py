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

langs = ['nl', 'en', 'de']
for lang in langs:
    path = os.path.join(lang, 'index.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        has_work = 'id="work"' in content
        has_projectsDB = 'projectsDB' in content
        has_software = 'id="software-hub"' in content
        has_grid = 'id="softwareGridContainer"' in content
        has_platforms = 'CivicSync' in content
        print(f"[{lang.upper()}] size: {len(content)} | work: {has_work} | projectsDB: {has_projectsDB} | softwareHub: {has_software} | grid: {has_grid} | platforms: {has_platforms}")
    else:
        print(f"[{lang.upper()}] DOES NOT EXIST at {path}")
