with open('de/demo.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<link[^>]+>', text)
for m in matches:
    if 'stylesheet' in m:
        print('de/demo.html css:', m)

