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

"""
Sync platform cards from preview-software.html into index.html
"""

with open('preview-software.html', 'r', encoding='utf-8') as f:
    preview_software = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

start_str = '<!-- ===== منصات S&R العامة القابلة للترخيص'
end_str = '<!-- مختبر وبوابة برمجيات المؤسس'

s_idx = preview_software.find(start_str)
e_idx = preview_software.find(end_str)

if s_idx != -1 and e_idx != -1:
    platforms_cards_html = preview_software[s_idx:e_idx].strip()
    # In preview-software.html, the cards ended with:
    #                     </div>
    #                 </div>
    # which is the closing of item 9. Let's make sure it contains items 7, 8, 9.
    print(f"Extracted platforms HTML length: {len(platforms_cards_html)}")

    # In index.html, find where the cards should go: right before the </div> that closes id="softwareGridContainer"
    marker = '<!-- مختبر وبرمجيات المطور م. سليم عزيزة'
    marker_idx = index_html.find(marker)
    if marker_idx != -1:
        grid_close_idx = index_html.rfind('</div>', 0, marker_idx)
        index_html = index_html[:grid_close_idx] + '\n\n' + platforms_cards_html + '\n' + index_html[grid_close_idx:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("SUCCESS: Inserted platform cards into index.html!")
    else:
        print("ERROR: marker not found in index.html")
else:
    print(f"ERROR: Indices: s_idx={s_idx}, e_idx={e_idx}")
