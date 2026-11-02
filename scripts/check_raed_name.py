import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
found = []

for root, dirs, files in os.walk(ROOT):
    if any(x in root for x in ['.git', 'node_modules', '_site', '.gemini', 'chrome_launchpad_profile']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.py', '.css', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    if 'رائد عزيزة' in content:
                        found.append((os.path.relpath(p, ROOT), 'رائد عزيزة'))
                    if 'Raed Aziza' in content:
                        found.append((os.path.relpath(p, ROOT), 'Raed Aziza'))
            except Exception:
                pass

print(f"Total occurrences found: {len(found)}")
for item in found:
    print(item)
