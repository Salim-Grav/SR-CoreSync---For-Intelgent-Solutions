import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

VERSION_TAG = "v=20261102-p0-matrix"

TARGET_ASSETS = [
    "enterprise-suite.css",
    "enterprise-suite.min.css",
    "enterprise-suite.min.js",
    "sr-agent-widget.css",
    "sr-agent-widget.js",
    "sr-privacy-banner.css",
    "sr-privacy-banner.js",
    "sr-header-support.css",
    "sr-header-support.js"
]

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    for asset in TARGET_ASSETS:
        # Regex matches (href|src)="([^"]*asset(?:\?v=[^"]*)?)"
        # Replace query param with VERSION_TAG
        pattern = re.compile(rf'((?:href|src)=["\'][^"\']*{re.escape(asset)})(?:\?[^"\']*)?(["\'])')
        content = pattern.sub(rf'\1?{VERSION_TAG}\2', content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Scan all html files in root, language directories, and insights
html_files = []
for root, dirs, files in os.walk('.'):
    # Skip _site, .git, etc.
    if any(p in root.replace('\\', '/').split('/') for p in ['_site', '.git', 'node_modules', 'dist', 'scratch']):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Scanning {len(html_files)} HTML files for cache busting...")
updated_count = 0
for hf in html_files:
    if update_file(hf):
        updated_count += 1
        print(f"  • Updated cache tags in: {hf}")

print(f"\nDone! Updated {updated_count}/{len(html_files)} HTML files with ?{VERSION_TAG}.")
