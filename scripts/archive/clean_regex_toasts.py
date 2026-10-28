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
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

langs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and os.path.exists(os.path.join(BASE_DIR, d, 'demo.html'))]
target_langs = [d for d in langs if d not in ['ckb']]

for lang in target_langs:
    p = os.path.join(BASE_DIR, lang, 'demo.html')
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean toast regexes
    content = re.sub(r'showPortalToast\(`🔑 [^`]*\$\{key\}`\);', 'showPortalToast(`🔑 License key copied: ${key}`);', content)
    content = re.sub(r'showPortalToast\(`🏛️ [^`]*\$\{vatText\}`\);', 'showPortalToast(`🏛️ Tax model updated: ${vatText}`);', content)
    content = re.sub(r"title: '📦 [^']* الذكية',", "title: '📦 Smart Cloud ERP & Logistics',", content)
    content = re.sub(r"desc: 'مؤشرات [^']*',", "desc: 'Accurate real-time metrics for annual revenue, net operational cash flow, and cloud automation hours saved.',", content)

    # Any lingering Arabic letters inside tourSteps or JS functions
    # Let's fix in en & nl as well
    content = content.replace("desc: 'مؤشرات مالية دقيقة للإيرادات السنوية، Operatieve Netto Cashflow, en bespaarde werkuren.'", "desc: 'Nauwkeurige realtime cijfers voor jaarlijkse omzet, netto operationele cashflow en bespaarde werkuren.'")
    content = content.replace("title: '📦 ERP & Slimme Voorraadlogistiek الذكية',", "title: '📦 ERP & Slimme Voorraadlogistiek',")
    content = content.replace("showPortalToast(`🔑 Sleutel gekopieerd التجريبي: ${key}`);", "showPortalToast(`🔑 Sleutel gekopieerd: ${key}`);")

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Cleaned toasts and tour steps across all {len(target_langs)} non-Arabic portals!")
