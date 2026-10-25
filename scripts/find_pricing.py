with open('index.html', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'id="pricing"' in line or 'pricing-table' in line or 'tf-pricing' in line:
            print(f'{i+1}: {line.strip()[:100]}')
