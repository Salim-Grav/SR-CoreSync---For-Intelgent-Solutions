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

# We want exactly 8 closing divs from hero-emblem-frame (line 640):
# 1: closes hero-emblem-frame
# 2: closes hero-emblem-card-3d
# 3: closes heroEmblemStage
# 4: closes hero-reference__emblem-col
# 5: closes hero-reference__grid
# 6: closes container-hero-luxury
# 7: closes content-wrap
# 8: closes section-hero-v1
# 9: closes hero-editorial hero-cinematic

# In commit 590adcc, there were 9 closing divs after glare.
target = """                                            <div class="hero-emblem-glare" aria-hidden="true"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>"""

correct = """                                            <div class="hero-emblem-glare" aria-hidden="true"></div>
                                        </div>
                                    </div>
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
    
    if target in content:
        content = content.replace(target, correct)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed extra closing div in {path}")
    else:
        print(f"Target not found in {path}")
