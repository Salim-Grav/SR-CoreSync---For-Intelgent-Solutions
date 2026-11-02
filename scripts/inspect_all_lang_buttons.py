# -*- coding: utf-8 -*-
import glob, re

for p in sorted(glob.glob('*/index.html')):
    if any(k in p for k in ['_site', 'node_modules']):
        continue
    lang = p.replace('\\', '/').split('/')[0]
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    m_demo = re.search(r'hero-btn-demo[^>]*>.*?<span>(.*?)</span>', text, re.DOTALL)
    m_vip = re.search(r'hero-btn-vip[^>]*>.*?<span>(.*?)</span>', text, re.DOTALL)
    demo_txt = m_demo.group(1).strip() if m_demo else 'N/A'
    vip_txt = m_vip.group(1).strip() if m_vip else 'N/A'
    print(f'{lang:5}: DEMO="{demo_txt}" | VIP="{vip_txt}"')
