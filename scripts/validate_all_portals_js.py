# -*- coding: utf-8 -*-
import os
import re
import subprocess
import json

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Fix multiline string in any file
multiline_pattern = r'aiResponse = "Based on October general ledgers and Cloud ERP records:\s*\n-\s*Gross Realized Revenue: €144,500 \(\+18% record quarterly growth\)\.\s*\n-\s*Operating Margin: 27\.4%, outperforming Dutch benchmarks\.\s*\n-\s*Recommendation: Accelerate €42,000 receivable collection due October 10 to boost liquidity\.";'
multiline_replacement = 'aiResponse = `Based on October general ledgers and Cloud ERP records:\\n- Gross Realized Revenue: €144,500 (+18% record quarterly growth).\\n- Operating Margin: 27.4%, outperforming Dutch benchmarks.\\n- Recommendation: Accelerate €42,000 receivable collection due October 10 to boost liquidity.`;'

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f == 'demo.html':
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c = fh.read()

            orig = c
            # Fix multiline string
            c = re.sub(multiline_pattern, multiline_replacement, c)

            # Fix orphaned else if in triggerText
            if "triggerText.innerText = '💬 Founder Hotline';" in c and "else if (lang === 'de')" in c:
                c = c.replace("triggerText.innerText = '💬 Founder Hotline';\n        \n        else if (lang === 'de')", "if (lang === 'de')")

            # Fix last week's telemetry in prompt chips
            c = c.replace("last week's telemetry", "recent weekly telemetry")
            c = c.replace("last week\'s telemetry", "recent weekly telemetry")

            # Fix currentEn attente
            c = c.replace('const currentEn attente', 'const currentPending')
            c = c.replace('currentEn attente', 'currentPending')
            c = c.replace('querySelectorTout', 'querySelectorAll')

            if c != orig:
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(c)
                print(f"Patched JS in: {os.path.relpath(p, base_dir)}")

print("All portals JS patched. Now testing with Node VM...")
