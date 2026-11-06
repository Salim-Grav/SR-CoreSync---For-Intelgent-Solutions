#!/usr/bin/env python3
"""
link_api_docs_globally.py
Adds links to api-docs.html in index.html and all 28 multilingual portals (29 languages total):
- Main desktop navigation (nav-menu-main)
- Offcanvas mobile menu
- Footer navigation (sr-footer-nav-list)
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Localized labels for API Docs
API_LABELS = {
    'ar': {'nav': 'توثيق API', 'footer': 'توثيق الـ API السيادي (OpenAPI 3.1)', 'tag': 'مطورين ⚡', 'mobile': 'توثيق الـ API السيادي (29 لغة)'},
    'nl': {'nav': 'API Docs', 'footer': 'Sovereign API Documentatie (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'API Documentatie (29 Talen)'},
    'en': {'nav': 'API Docs', 'footer': 'Sovereign API Documentation (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'Sovereign API Documentation (29 Languages)'},
    'de': {'nav': 'API-Doku', 'footer': 'Souveräne API-Dokumentation (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'API-Dokumentation (29 Sprachen)'},
    'fr': {'nav': 'Docs API', 'footer': 'Documentation API Souveraine (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'Documentation API (29 Langues)'},
    'es': {'nav': 'Docs API', 'footer': 'Documentación API Soberana (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'Documentación API (29 Idiomas)'},
    'it': {'nav': 'API Docs', 'footer': 'Documentazione API Sovrana (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'Documentazione API (29 Lingue)'},
    'pt': {'nav': 'Docs API', 'footer': 'Documentação API Soberana (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'Documentação API (29 Idiomas)'},
    'tr': {'nav': 'API Docs', 'footer': 'Egemen API Dokümantasyonu (OpenAPI 3.1)', 'tag': 'Geliştirici ⚡', 'mobile': 'API Dokümantasyonu (29 Dil)'},
    'ku': {'nav': 'API Docs', 'footer': 'Belgekirina API ya Serwer (OpenAPI 3.1)', 'tag': 'Pêşvebir ⚡', 'mobile': 'Belgekirina API (29 Ziman)'},
    'ckb': {'nav': 'بەڵگەنامەی API', 'footer': 'بەڵگەنامەی فەرمی API (OpenAPI 3.1)', 'tag': 'گەشەپێدەر ⚡', 'mobile': 'بەڵگەنامەی API (29 زمان)'},
}

DEFAULT_LABEL = {'nav': 'API Docs', 'footer': 'Sovereign API Documentation (OpenAPI 3.1)', 'tag': 'Dev ⚡', 'mobile': 'API Documentation (29 Languages)'}

def update_page(file_path, lang_code, is_root=False):
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Prevent duplicate injection
    if 'api-docs.html' in html:
        print(f"Skipping {file_path} - already contains api-docs.html link")
        return True

    labels = API_LABELS.get(lang_code, DEFAULT_LABEL)
    rel_path = './api-docs.html' if is_root else '../api-docs.html'
    nav_title = labels['footer']
    nav_text = labels['nav']
    footer_text = labels['footer']
    footer_tag = labels['tag']
    mobile_text = labels['mobile']

    # 1. Update Desktop Nav (nav-menu-main)
    nav_item = f'<li class="menu-item"><a href="{rel_path}" class="item-link link text-caption gold-accent" title="{nav_title}"><span>09 /</span>{nav_text}</a></li>\n                                    </ul>'
    html = re.sub(r'</ul>(?=\s*</div>\s*</div>\s*<!-- 3\.)', nav_item, html, count=1)

    # 2. Update Footer (sr-footer-nav-list inside Platform Map or Systems)
    footer_item = f'<li><a href="{rel_path}">{footer_text} <span class="sr-footer-pill-tag">{footer_tag}</span></a></li>\n                        </ul>'
    html = re.sub(r'</ul>(?=\s*</div>\s*<!-- العمود 3|\s*</div>\s*<!-- Column 3|\s*</div>\s*<!--\s*Column\s*3)', footer_item, html, count=1)

    # 3. Update Mobile Menu (offcanvas mobile-menu-list)
    mobile_item = f'<li><a href="{rel_path}" class="gold-accent" data-sr-call="closeMobileMenu"><span class="menu-label">{mobile_text}</span><span class="mobile-menu-num">12 /</span></a></li>\n        </ul>'
    html = re.sub(r'</ul>(?=\s*<div class="offcanvas-resizer-box")', mobile_item, html, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"SUCCESS: Injected API Docs links into {file_path}")
    return True

def main():
    # 1. Root index.html
    root_index = os.path.join(BASE_DIR, 'index.html')
    update_page(root_index, 'ar', is_root=True)

    # 2. All 28 language portals
    from deploy_sovereign_multilingual import LANGUAGES
    count = 1
    for l in LANGUAGES:
        code = l['code']
        if code == 'ar':
            continue
        portal_path = os.path.join(BASE_DIR, code, 'index.html')
        if update_page(portal_path, code, is_root=False):
            count += 1

    print(f"\nCompleted! Linked api-docs.html across {count} language portals.")

if __name__ == '__main__':
    main()
