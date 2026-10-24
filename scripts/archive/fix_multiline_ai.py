# -*- coding: utf-8 -*-
import re

with open('fr/demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the multiline double quote string with template literal backticks
pattern = r'aiResponse = "Based on October general ledgers and Cloud ERP records:\s*\n-\s*Gross Realized Revenue: €144,500 \(\+18% record quarterly growth\)\.\s*\n-\s*Operating Margin: 27\.4%, outperforming Dutch benchmarks\.\s*\n-\s*Recommendation: Accelerate €42,000 receivable collection due October 10 to boost liquidity\.";'

replacement = 'aiResponse = `Based on October general ledgers and Cloud ERP records:\\n- Gross Realized Revenue: €144,500 (+18% record quarterly growth).\\n- Operating Margin: 27.4%, outperforming Dutch benchmarks.\\n- Recommendation: Accelerate €42,000 receivable collection due October 10 to boost liquidity.`;'

new_c = re.sub(pattern, replacement, c)
if new_c != c:
    with open('fr/demo.html', 'w', encoding='utf-8') as f:
        f.write(new_c)
    print("Successfully replaced multiline string with escaped newlines!")
else:
    print("Pattern did not match, inspecting...")
