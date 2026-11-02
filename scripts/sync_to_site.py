import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

dirs = ['bg', 'ckb', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'tr']

count = 0
for d in dirs:
    src = f"{d}/index.html"
    dst = f"_site/{d}/index.html"
    if os.path.exists(src) and os.path.exists(f"_site/{d}"):
        shutil.copy2(src, dst)
        count += 1

# Also copy enterprise-suite css
for css_file in ['enterprise-suite.css', 'enterprise-suite.min.css']:
    src_css = f"css/{css_file}"
    dst_css = f"_site/css/{css_file}"
    if os.path.exists(src_css) and os.path.exists("_site/css"):
        shutil.copy2(src_css, dst_css)
        print(f"Copied {css_file} to _site/css/")

print(f"Synced {count} language index.html files to _site successfully.")
