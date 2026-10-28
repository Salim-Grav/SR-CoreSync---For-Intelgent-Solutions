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

fixed = 0
for root, dirs, files in os.walk('.'):
    for f in files:
        if f == 'demo.html':
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                content = fh.read()

            idx_chk = content.find('id="softwareCheckoutModal"')
            idx_tour = content.find('id="tourBackdrop"')
            if idx_chk != -1 and idx_tour != -1:
                sub = content[idx_chk:idx_tour]
                diff = sub.count('<div') - sub.count('</div>')
                if diff > 0:
                    # Let's see what is right before tourBackdrop or comment
                    # In demo.html it was:
                    #         </div>
                    #     <!-- حاوية الجولة
                    # or in english:
                    #         </div>
                    #     <!-- Spotlight Guided Tour
                    idx_comment = content.rfind('<!--', idx_chk, idx_tour)
                    if idx_comment != -1:
                        content = content[:idx_comment] + '</div>\n    ' + content[idx_comment:]
                        with open(p, 'w', encoding='utf-8') as fh:
                            fh.write(content)
                        fixed += 1

print(f"Fixed missing modal-overlay </div> in {fixed} portals!")
