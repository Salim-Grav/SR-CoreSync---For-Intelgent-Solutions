import json
import os
import tempfile

p = os.path.join(tempfile.gettempdir(), 'sr-lh-budget.json')
if not os.path.exists(p):
    print("Report file not found:", p)
    exit(1)

with open(p, encoding='utf-8') as f:
    d = json.load(f)

items = d['audits']['network-requests']['details']['items']
print(f"Total requests: {len(items)}")
total_bytes = sum(i.get('transferSize', 0) for i in items)
print(f"Total transfer: {total_bytes / 1024:.1f} KB")

# Group by resourceType
by_type = {}
for i in items:
    rtype = i.get('resourceType', 'Other')
    by_type.setdefault(rtype, []).append(i)

for rtype, reqs in sorted(by_type.items()):
    r_bytes = sum(i.get('transferSize', 0) for i in reqs)
    print(f"\n--- {rtype} ({len(reqs)} requests, {r_bytes / 1024:.1f} KB) ---")
    for req in sorted(reqs, key=lambda x: x.get('transferSize', 0), reverse=True):
        url = req.get('url', '')
        size = req.get('transferSize', 0) / 1024
        print(f"  {size:6.1f} KB : {url}")
