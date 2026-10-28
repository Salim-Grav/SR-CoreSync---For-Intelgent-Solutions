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
        orig = content
        content = content.replace('id="sovereignLangMenu" role="menu"', 'id="sovereignLangMenu" aria-label="Select Language"')
        content = content.replace('id="sovereignLangMenu" role="dialog" aria-label="Select Language"', 'id="sovereignLangMenu" aria-label="Select Language"')
        content = content.replace('id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="dialog"', 'id="sovereignLangTrigger" aria-expanded="false"')
        content = content.replace('id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="true"', 'id="sovereignLangTrigger" aria-expanded="false"')
        if content != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
    except Exception as e:
        print(f"Error {path}: {e}")

print(f"Successfully fixed ARIA role in {count} HTML files.")
