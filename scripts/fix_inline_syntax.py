import glob
import re
import os

def fix_demo_excel():
    with open('demo.html', 'r', encoding='utf-8') as f:
        demo_content = f.read()

    marker = 'const excel = `<html xmlns:o='
    if marker in demo_content:
        start_idx = demo_content.find(marker)
        style_idx = demo_content.find('<style>body{font-family:Segoe UI,Arial;', start_idx)
        if start_idx != -1 and style_idx != -1:
            clean_head = 'const excel = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8">\n    '
            demo_content = demo_content[:start_idx] + clean_head + demo_content[style_idx:]
            with open('demo.html', 'w', encoding='utf-8') as f:
                f.write(demo_content)
            print('Cleaned demo.html excel template literal successfully.')

def fix_query_selectors():
    pattern = re.compile(r'querySelector[A-Za-z\u00C0-\u017F]+')
    fixed_count = 0
    for root_dir, dirs, files in os.walk('.'):
        if any(ex in root_dir for ex in ('.git', '_site', 'node_modules')):
            continue
        for file in files:
            if not file.endswith('.html'):
                continue
            p = os.path.join(root_dir, file)
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            def replacer(match):
                word = match.group(0)
                if word in ('querySelector', 'querySelectorAll'):
                    return word
                return 'querySelectorAll'

            new_content = pattern.sub(replacer, content)
            if new_content != content:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f'Fixed querySelector in {p}')
    print(f'Total files updated for querySelector: {fixed_count}')

if __name__ == '__main__':
    fix_demo_excel()
    fix_query_selectors()
