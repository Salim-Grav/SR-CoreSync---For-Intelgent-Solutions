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
import glob
import re

def remove_dropdown(html):
    pattern = r'(?:<!--\s*(?:محول اللغة|Sovereign Global Multilingual Hub)[^>]*-->\s*)?<div class="sovereign-lang-(?:dropdown|hub-wrap)"[^>]*>'
    m = re.search(pattern, html)
    if not m:
        return html
    
    start_idx = m.start()
    div_start = m.group(0).find('<div')
    actual_div_start = start_idx + div_start
    
    depth = 0
    i = actual_div_start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                end_idx = i
                # Strip trailing whitespace or newline if any
                while end_idx < len(html) and html[end_idx] in ' \t\r\n':
                    end_idx += 1
                return html[:start_idx] + html[end_idx:]
        else:
            i += 1
    return html

count = 0
for path in glob.glob('**/*.html', recursive=True):
    if '_site' in path:
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = remove_dropdown(content)
        # In case there's another occurrence
        new_content = remove_dropdown(new_content)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
    except Exception as e:
        print(f"Error {path}: {e}")

print(f"Successfully cleaned header in {count} HTML files!")
