import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

below_fold_classes = [
    'sr-footer-emblem',
    'brand-emblem-img-sm',
    'advisor-avatar-dual-1',
    'advisor-avatar-dual-2',
    'advisor-avatar-sm',
    'sr-logo-full-render',
    'sr-cinema-img-living',
    'sr-cinema-signature',
    'roi-pdf-emblem-img',
    'founders-qr-image'
]

class_pattern = re.compile(r'(<img\s+[^>]*class="[^"]*(?:' + '|'.join(below_fold_classes) + r')[^"]*"[^>]*>)')

updated_count = 0

for root_dir, dirs, files in os.walk(ROOT):
    if '_site' in root_dir or '.git' in root_dir:
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        def replacer(match):
            tag = match.group(1)
            if 'loading=' in tag:
                return tag
            # Insert loading="lazy" decoding="async" right before >
            if tag.endswith('/>'):
                return tag[:-2].rstrip() + ' loading="lazy" decoding="async" />'
            else:
                return tag[:-1].rstrip() + ' loading="lazy" decoding="async">'

        new_content, n = class_pattern.subn(replacer, content)
        if n > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += n

print(f"Added lazy loading to {updated_count} below-the-fold images.")
