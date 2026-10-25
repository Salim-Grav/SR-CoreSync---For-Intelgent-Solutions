import json, os, tempfile

p = os.path.join(tempfile.gettempdir(), 'sr-lh-budget.json')
d = json.load(open(p, encoding='utf-8'))
items = d['audits']['network-requests']['details']['items']
for i in items:
    if 'flags/pt.png' in i.get('url', ''):
        print("Flag pt.png found:")
        print("  url:", i.get('url'))
        print("  initiator:", json.dumps(i.get('initiator'), indent=2))
        print("  resourceType:", i.get('resourceType'))
        print("  statusCode:", i.get('statusCode'))
        break
