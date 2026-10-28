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

languages = [
    '', 'bg', 'ckb', 'cs', 'da', 'de', 'el', 'en', 'es', 'et',
    'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt',
    'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'tr'
]

# Clean up indentation of closing tags after hero-emblem-frame
target_pattern = re.compile(
    r'(<div class="hero-emblem-glare" aria-hidden="true"></div>\s*</div>\s*</div>)\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>',
    re.DOTALL
)

replacement = """\\1
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

for lang in languages:
    path = os.path.join(lang, 'index.html') if lang else 'index.html'
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, n = target_pattern.subn(replacement, content)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Normalized indentation in {path}")
    else:
        print(f"Pattern did not match in {path}")
