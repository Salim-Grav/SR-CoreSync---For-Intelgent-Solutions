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

count = 0
for path in glob.glob('**/*.html', recursive=True):
    if '_site' in path:
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'style="opacity:0;"' in content:
            new_content = content.replace('<span class="apple-dock-dot" style="opacity:0;"></span>', '<span class="apple-dock-dot"></span>')
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
    except Exception as e:
        print(f"Error {path}: {e}")

print(f"Successfully removed inline style from {count} HTML files.")
