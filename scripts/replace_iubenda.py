import os
import re

files = [
    ('blog.html', './'),
    ('insights/ai-concierge-rag.html', '../'),
    ('insights/brand-identity-roi.html', '../'),
    ('insights/chart-of-accounts-erp.html', '../'),
    ('insights/cloud-cost-30.html', '../'),
    ('insights/ecommerce-conversion.html', '../'),
    ('insights/erp-selection-2026.html', '../'),
    ('insights/zero-trust.html', '../'),
    ('en/insights/chart-of-accounts-erp.html', '../../'),
]

pattern = re.compile(
    r'<!-- Iubenda Cookie Consent -->.*?'
    r'<script type="text/javascript" src="https://cdn\.iubenda\.com/cs/iubenda_cs\.js"[^>]*></script>',
    re.DOTALL
)

for rel_path, prefix in files:
    if not os.path.exists(rel_path):
        print(f'File not found: {rel_path}')
        continue
    with open(rel_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacement = (
        '<!-- S&R CoreSync Sovereign GDPR & Dutch AVG Cookie & Privacy Consent Hub -->\n'
        f'<link rel="stylesheet" href="{prefix}css/sr-privacy-banner.css?v=20261102">\n'
        f'<script src="{prefix}js/sr-privacy-banner.js?v=20261102" defer></script>'
    )

    new_content, count = pattern.subn(replacement, content)
    if count > 0:
        with open(rel_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Successfully updated: {rel_path} ({count} replacements)')
    else:
        print(f'Pattern not matched in: {rel_path}')
