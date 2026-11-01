import json, re

text = open('scripts/extracted_concierge_kb.json', encoding='utf-8').read()
json_like = re.sub(r'([{,])([a-zA-Z_][a-zA-Z0-9_]*):', r'\1"\2":', text)
data = json.loads(json_like)
print(f'Total items: {len(data)}')
for item in data:
    print('-', item.get('q'))
