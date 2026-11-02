import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

dirs = ['bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'tr']

pattern = re.compile(r'(<div class="hero-reference__actions[^"]*"[^>]*>)(.*?)(</div>(\s*<!--[^\n]*-->)?\s*</div>)', re.DOTALL)

for d in dirs:
    path = f"{d}/index.html"
    with open(path, encoding='utf-8') as f:
        content = f.read()
    m = pattern.search(content)
    if not m:
        print(f"{d}: NOT MATCHED")
    else:
        # Check if both demo and vip buttons are inside
        inner = m.group(2)
        has_demo = 'demo' in inner
        has_vip = 'vip' in inner or 'openExecutiveBookingModal' in inner
        print(f"{d}: OK (demo={has_demo}, vip={has_vip})")
