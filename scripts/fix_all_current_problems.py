# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - Global Problem Fixer
Fixes:
1. 'charset' meta element positioned first in <head>
2. 'role="menu"' removed from sovereignLangMenu to satisfy ARIA children rule
3. Range inputs given title and aria-label
4. 'last week's telemetry' unescaped single quote in onclick attribute
5. '====================' changed to '--------------------' to avoid false merge conflict linter detection
6. WhatsApp links given rel="noopener noreferrer"
7. Hotline close button inline style removed and moved to CSS
8. CSS -webkit-user-select prefix added
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 1. Update CSS files for .hotline-close-btn and -webkit-user-select
css_additions = """
.hotline-close-btn {
    background: none;
    border: none;
    color: #c5a880;
    cursor: pointer;
    font-size: 16px;
    padding: 0;
    line-height: 1;
}
"""

for css_file in ['css/demo-portal.css', 'css/enterprise-suite.min.css']:
    css_path = os.path.join(BASE_DIR, css_file)
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        if '.hotline-close-btn' not in css_content:
            css_content += '\n' + css_additions
        if '-webkit-user-select: none;' not in css_content:
            css_content = css_content.replace('user-select: none;', '-webkit-user-select: none;\n    user-select: none;')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)

print("Updated CSS files with .hotline-close-btn and -webkit-user-select!")

# 2. Process all HTML files
html_files = []
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Auditing and fixing {len(html_files)} HTML files...")

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # Fix 1: Ensure <meta charset="UTF-8"> is the first element right after <head>
    if '<head>' in content:
        # Check if charset is already right after head
        if not re.search(r'<head>\s*<meta charset=["\']?UTF-8["\']?>', content, re.IGNORECASE):
            # Remove any existing charset meta
            content = re.sub(r'<meta charset=["\']?UTF-8["\']?>\s*', '', content, flags=re.IGNORECASE)
            # Insert right after <head>
            content = re.sub(r'(<head\b[^>]*>)', r'\1\n    <meta charset="UTF-8">', content, count=1, flags=re.IGNORECASE)

    # Fix 2: Remove role="menu" from sovereignLangMenu
    content = content.replace('id="sovereignLangMenu" role="menu"', 'id="sovereignLangMenu"')
    content = content.replace('role="menu" id="sovereignLangMenu"', 'id="sovereignLangMenu"')

    # Fix 3: Fix onclick with unescaped single quote in last week's telemetry
    content = content.replace("last week's telemetry", "recent weekly telemetry")
    content = content.replace("last week\'s telemetry", "recent weekly telemetry")

    # Fix 4: Fix fake merge conflict marker in download package
    content = content.replace('=====================================================', '-----------------------------------------------------')

    # Fix 5: Add rel="noopener noreferrer" to hotline WhatsApp links
    content = content.replace('target="_blank" class="hotline-btn-wa"', 'target="_blank" rel="noopener noreferrer" class="hotline-btn-wa"')

    # Fix 6: Remove inline styles from hotline close button
    content = re.sub(
        r'<button type="button" class="btn-modal-close-sm font-num" onclick="toggleHotlineWidget\(event\)" style="[^"]*">✕</button>',
        '<button type="button" class="btn-modal-close-sm font-num hotline-close-btn" onclick="toggleHotlineWidget(event)" aria-label="Close">✕</button>',
        content
    )

    # Fix 7: Ensure ROI range inputs have title and aria-label
    content = re.sub(
        r'<input type="range" min="3" max="250" value="20" class="roi-range-input" id="slideRoiTeam"([^>]*)>',
        r'<input type="range" min="3" max="250" value="20" class="roi-range-input" id="slideRoiTeam"\1 title="Team Size / Employees" aria-label="Team Size / Employees">',
        content
    )
    # Remove duplicates if any
    content = re.sub(r'(title="[^"]*")\s+title="[^"]*"', r'\1', content)
    content = re.sub(r'(aria-label="[^"]*")\s+aria-label="[^"]*"', r'\1', content)

    content = re.sub(
        r'<input type="range" min="5" max="60" value="18" class="roi-range-input" id="slideRoiHours"([^>]*)>',
        r'<input type="range" min="5" max="60" value="18" class="roi-range-input" id="slideRoiHours"\1 title="Manual Hours per Week" aria-label="Manual Hours per Week">',
        content
    )
    content = re.sub(r'(title="[^"]*")\s+title="[^"]*"', r'\1', content)
    content = re.sub(r'(aria-label="[^"]*")\s+aria-label="[^"]*"', r'\1', content)

    content = re.sub(
        r'<input type="range" min="15" max="150" value="45" step="5" class="roi-range-input" id="slideRoiCost"([^>]*)>',
        r'<input type="range" min="15" max="150" value="45" step="5" class="roi-range-input" id="slideRoiCost"\1 title="Average Hourly Cost" aria-label="Average Hourly Cost">',
        content
    )
    content = re.sub(r'(title="[^"]*")\s+title="[^"]*"', r'\1', content)
    content = re.sub(r'(aria-label="[^"]*")\s+aria-label="[^"]*"', r'\1', content)

    if content != orig:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Global problem fixes applied across all HTML files!")
