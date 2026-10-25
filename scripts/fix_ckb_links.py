import os
import re

root_files = set(os.listdir('.'))

def fix_links(html, page_type='index'):
    def repl(m):
        attr = m.group(1)
        rel = m.group(2)
        if rel.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', 'javascript:')):
            return m.group(0)
        
        base = rel.split('?')[0].split('#')[0]
        extra = rel[len(base):]
        clean_base = base.lstrip('./')
        
        # Don't double-prefix
        if rel.startswith('../'):
            return m.group(0)

        # Same folder files
        if clean_base in (f'{page_type}.html', 'index.html' if page_type == 'index' else 'demo.html'):
            return f'{attr}="{clean_base}{extra}"'

        # Root files
        if clean_base in root_files and not clean_base.startswith('.'):
            return f'{attr}="../{clean_base}{extra}"'

        # Subdirectories
        if any(clean_base.startswith(f + '/') for f in ('assets', 'css', 'js', 'downloads')):
            return f'{attr}="../{clean_base}{extra}"'

        langs = ('ar','en','nl','de','fr','tr','sv','no','es','it','ku','ckb','pl','pt','da','fi','cs','el','ro','hu','bg','sk','hr','lt','sl','lv','et','ga','mt')
        if any(clean_base.startswith(l + '/') for l in langs):
            return f'{attr}="../{clean_base}{extra}"'

        return m.group(0)

    pattern = re.compile(r'(href|src)="([^"]+)"')
    return pattern.sub(repl, html)

if __name__ == '__main__':
    for fname, ptype in [('ckb/demo.html', 'demo'), ('ckb/index.html', 'index')]:
        with open(fname, 'r', encoding='utf-8') as f:
            c = f.read()
        fixed = fix_links(c, page_type=ptype)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f'Fixed {fname}')
