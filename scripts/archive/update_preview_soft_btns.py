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

with open('preview-software.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'href="./preview-work.html#platforms-civicsync" class="software-btn-download"',
    'type="button" class="software-btn-download" onclick="openSoftwareLiveApp(\'civicsync\')"'
)
c = c.replace(
    'href="./preview-work.html#platforms-healthbridge" class="software-btn-download"',
    'type="button" class="software-btn-download" onclick="openSoftwareLiveApp(\'healthbridge\')"'
)
c = c.replace(
    'href="./preview-work.html#platforms-omnibakery" class="software-btn-download"',
    'type="button" class="software-btn-download" onclick="openSoftwareLiveApp(\'omnibakery\')"'
)

# Also ensure the button text is updated to تشغيل فوري and add the case study secondary button
for slug in ['civicsync', 'healthbridge', 'omnibakery']:
    target = f'onclick="openSoftwareLiveApp(\'{slug}\')"'
    # Check if case study button already exists next to it
    if target in c and f'preview-work.html#platforms-{slug}' not in c:
        old_block = f'<button type="button" class="software-btn-download" {target} title="استعراض دراسة الحالة الكاملة">\n                                        <span>📄 دراسة الحالة</span>\n                                    </a>'
        alt_old_block = f'<button type="button" class="software-btn-download" {target} title="استعراض دراسة الحالة الكاملة">\n                                        <span>📄 دراسة الحالة</span>\n                                    </button>'
        new_block = f'''<button type="button" class="software-btn-download" {target} title="تشغيل فوري تفاعلي في المتصفح">
                                        <span>⚡ تشغيل فوري</span>
                                    </button>
                                    <a href="./preview-work.html#platforms-{slug}" class="btn-live-preview software-btn-sim" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>'''
        if old_block in c:
            c = c.replace(old_block, new_block)
        elif alt_old_block in c:
            c = c.replace(alt_old_block, new_block)

with open('preview-software.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated preview-software.html successfully!")
