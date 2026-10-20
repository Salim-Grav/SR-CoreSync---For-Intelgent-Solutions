# -*- coding: utf-8 -*-
with open('css/demo-portal.css', 'r', encoding='utf-8') as f:
    demo_css = f.read()

start_marker = 'Sovereign Global Multilingual Hub'
idx = demo_css.find(start_marker)
if idx != -1:
    idx_start = demo_css.rfind('/*', 0, idx)
    idx_end = demo_css.find('html[dir="ltr"] body {', idx)
    hub_css = demo_css[idx_start:idx_end].strip()

    with open('css/enterprise-suite.min.css', 'r', encoding='utf-8') as f:
        ent_css = f.read()

    if start_marker not in ent_css:
        with open('css/enterprise-suite.min.css', 'a', encoding='utf-8') as f:
            f.write('\n\n' + hub_css + '\n')
        print('Appended Sovereign Lang Hub CSS to enterprise-suite.min.css!')
    else:
        print('Already present in enterprise-suite.min.css!')
else:
    print('Marker not found in demo-portal.css')
