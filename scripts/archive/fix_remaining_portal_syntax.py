# -*- coding: utf-8 -*-
import os
import re

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f == 'demo.html':
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c = fh.read()

            orig = c

            # Fix 1: const current... = 35000 + total;
            c = re.sub(
                r'const current[^\n=]+=\s*35000\s*\+\s*total;\s*\n\s*pendingEl\.innerText\s*=\s*`€ \$\{current[^\}]+\.toLocaleString\(\)\}`;',
                'const currentPending = 35000 + total;\n            pendingEl.innerText = `€ ${currentPending.toLocaleString()}`;',
                c
            )

            # Fix 2: previewInvoiceModal net/vat variables
            c = re.sub(
                r'previewInvoiceModal\(invNum,\s*client,\s*net\w+,\s*vat\w+,',
                'previewInvoiceModal(invNum, client, netAmount, vatAmount,',
                c
            )

            # Fix 3: Multiline aiResponse = "..." in Dutch or any other language
            # Match aiResponse = "..." where string contains newline before closing quote
            def fix_ai_multiline(m):
                content_inner = m.group(1)
                # replace real newlines with \n
                escaped = content_inner.replace('\r\n', '\\n').replace('\n', '\\n')
                return f'aiResponse = `{escaped}`;'

            c = re.sub(r'aiResponse = "([^"]*\n[^"]*)";', fix_ai_multiline, c)

            if c != orig:
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(c)
                print(f"Fixed syntax anomalies in: {os.path.relpath(p, base_dir)}")

print("Done fixing syntax anomalies!")
