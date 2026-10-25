# -*- coding: utf-8 -*-
"""
S&R CoreSync - PWA Infrastructure & Mobile App Generator (Stage 21)
Generates standard 192x192 and 512x512 PNG icons (any + maskable),
updates manifest.json, injects PWA manifest tags into all 29 demo.html portals,
and wires Service Worker registration into sr-software-apps.js.
"""

import os
import json
import re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, 'assets')
SRC_EMBLEM = os.path.join(ASSETS_DIR, 'sr-core-emblem-official.png')

LANGUAGES = [
    "ar", "en", "nl", "de", "fr", "tr", "sv", "no", "es", "it",
    "ku", "ckb", "pl", "pt", "da", "fi", "cs", "el", "ro", "hu",
    "bg", "sk", "hr", "lt", "sl", "lv", "et", "ga", "mt"
]

def generate_icons():
    print("--- 1. Generating PWA Standard & Maskable Icons ---")
    if not os.path.isfile(SRC_EMBLEM):
        raise FileNotFoundError(f"Source emblem not found: {SRC_EMBLEM}")
        
    img = Image.open(SRC_EMBLEM).convert("RGBA")
    
    # 1. Standard Icons (any)
    icon_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
    icon_192.save(os.path.join(ASSETS_DIR, 'icon-192.png'), 'PNG')
    
    icon_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    icon_512.save(os.path.join(ASSETS_DIR, 'icon-512.png'), 'PNG')
    print("Created icon-192.png and icon-512.png")
    
    # 2. Maskable Icons (safe zone with 15% dark background padding #010907)
    def make_maskable(target_size):
        bg = Image.new("RGBA", (target_size, target_size), (1, 9, 7, 255))
        # Inner emblem is 75% of target size to guarantee 80% safe circle
        inner_size = int(target_size * 0.75)
        resized_inner = img.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
        offset = (target_size - inner_size) // 2
        bg.paste(resized_inner, (offset, offset), resized_inner)
        return bg

    maskable_192 = make_maskable(192)
    maskable_192.save(os.path.join(ASSETS_DIR, 'icon-maskable-192.png'), 'PNG')

    maskable_512 = make_maskable(512)
    maskable_512.save(os.path.join(ASSETS_DIR, 'icon-maskable-512.png'), 'PNG')
    print("Created icon-maskable-192.png and icon-maskable-512.png")


def update_manifest():
    print("--- 2. Updating manifest.json ---")
    manifest_path = os.path.join(ROOT, 'manifest.json')
    
    manifest_data = {
        "name": "S&R CoreSync For Intelligent Solutions",
        "short_name": "CoreSync",
        "id": "/",
        "description": "برمجيات سحابية متقدمة، حلول ERP، واستشارات مالية ذكية",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "display_override": ["window-controls-overlay", "standalone", "minimal-ui"],
        "background_color": "#010907",
        "theme_color": "#010907",
        "orientation": "any",
        "lang": "ar",
        "dir": "rtl",
        "categories": ["business", "finance", "productivity"],
        "icons": [
            {
                "src": "./assets/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "./assets/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "./assets/icon-maskable-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "maskable"
            },
            {
                "src": "./assets/icon-maskable-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable"
            },
            {
                "src": "./assets/sr-core-emblem-official.png",
                "sizes": "1024x1024",
                "type": "image/png",
                "purpose": "any"
            }
        ],
        "shortcuts": [
            {
                "name": "التطبيق التجريبي Live Demo",
                "short_name": "Live Demo",
                "description": "تجربة المنصة السحابية والـ ERP",
                "url": "./demo.html",
                "icons": [{ "src": "./assets/icon-192.png", "sizes": "192x192", "type": "image/png" }]
            },
            {
                "name": "تواصل مع الإدارة",
                "short_name": "تواصل",
                "description": "مراسلة الشريكين المؤسسين عبر واتساب",
                "url": "https://wa.me/31618111116",
                "icons": [{ "src": "./assets/icon-192.png", "sizes": "192x192", "type": "image/png" }]
            },
            {
                "name": "استوديو ومحرر الشعار",
                "short_name": "محرر الشعار",
                "description": "تخصيص وتنزيل الشعار والهوية البصرية",
                "url": "./logo-studio.html",
                "icons": [{ "src": "./assets/icon-192.png", "sizes": "192x192", "type": "image/png" }]
            }
        ]
    }
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print("manifest.json updated successfully with full PWA specification.")


def inject_pwa_in_demo_portals():
    print("--- 3. Injecting PWA Tags into all 29 demo.html Portals ---")
    
    for lang in LANGUAGES:
        if lang == 'ar':
            demo_path = os.path.join(ROOT, 'demo.html')
            prefix = './'
        else:
            demo_path = os.path.join(ROOT, lang, 'demo.html')
            prefix = '../'
            
        if not os.path.isfile(demo_path):
            continue
            
        with open(demo_path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Check if already injected
        if 'rel="manifest"' in html:
            continue
            
        pwa_tags = f'''    <!-- S&R CoreSync PWA & Mobile Web App Meta -->
    <link rel="manifest" href="{prefix}manifest.json">
    <meta name="theme-color" content="#010907">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="CoreSync">
    <link rel="apple-touch-icon" href="{prefix}assets/icon-192.png">'''
        
        # Inject right after `<meta name="viewport" ...>`
        target = re.search(r'(<meta\s+name=["\']viewport["\'][^>]*>)', html, re.IGNORECASE)
        if target:
            matched = target.group(1)
            html = html.replace(matched, matched + "\n" + pwa_tags, 1)
        else:
            html = html.replace('</head>', pwa_tags + "\n</head>", 1)
            
        with open(demo_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"PWA tags injected: {os.path.relpath(demo_path, ROOT)}")


def update_sw_registration():
    print("--- 4. Updating Service Worker Registration in sr-software-apps.js ---")
    sw_apps_path = os.path.join(ROOT, 'js', 'sr-software-apps.js')
    with open(sw_apps_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    sw_snippet = """
// S&R CoreSync PWA Service Worker Automatic Loader
if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        var isSub = !!window.location.pathname.match(/\\/[a-z]{2,3}\\//);
        var swPath = isSub ? '../sw.js' : './sw.js';
        navigator.serviceWorker.register(swPath).catch(function() {});
    });
}
"""
    if 'S&R CoreSync PWA Service Worker Automatic Loader' not in content:
        content = content + "\n" + sw_snippet
        with open(sw_apps_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Service Worker auto-loader attached to sr-software-apps.js")
    else:
        print("Service Worker auto-loader already exists.")


def update_sw_cache_list():
    print("--- 5. Adding PWA Icons to sw.js Pre-cache ---")
    sw_path = os.path.join(ROOT, 'sw.js')
    with open(sw_path, 'r', encoding='utf-8') as f:
        sw_content = f.read()
        
    if "'./assets/icon-192.png'" not in sw_content:
        sw_content = sw_content.replace(
            "'./manifest.json',",
            "'./manifest.json',\n  './assets/icon-192.png',\n  './assets/icon-512.png',\n  './assets/icon-maskable-192.png',\n  './assets/icon-maskable-512.png',"
        )
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(sw_content)
        print("Updated sw.js CRITICAL_ASSETS cache list.")
    else:
        print("PWA icons already in sw.js.")


def main():
    generate_icons()
    update_manifest()
    inject_pwa_in_demo_portals()
    update_sw_registration()
    update_sw_cache_list()
    print("=== Stage 21 PWA Integration Completed Successfully! ===")

if __name__ == '__main__':
    main()
