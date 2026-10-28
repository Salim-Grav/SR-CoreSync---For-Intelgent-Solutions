# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
S&R CoreSync - International SEO & Hreflang Automation Engine (Stage 19)
Audits, injects, and synchronizes canonical URLs and reciprocal hreflang tags
across all 60 pages (root master + 28 localized directories for index.html and demo.html)
in full compliance with Google Search Central & Bing International SEO standards.
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://sr-coresync.com"

LANGUAGES = [
    "ar", "en", "nl", "de", "fr", "tr", "sv", "no", "es", "it",
    "ku", "ckb", "pl", "pt", "da", "fi", "cs", "el", "ro", "hu",
    "bg", "sk", "hr", "lt", "sl", "lv", "et", "ga", "mt"
]

def build_hreflang_block(page_type, current_lang):
    """
    page_type: 'index' or 'demo'
    current_lang: 'ar', 'en', etc.
    """
    lines = []
    lines.append(f'    <!-- S&R CoreSync Enterprise SEO: Canonical & Reciprocal Hreflang Tags -->')
    
    # 1. Canonical tag for this specific page
    if page_type == 'index':
        canonical_href = f"{BASE_URL}/" if current_lang == 'ar' else f"{BASE_URL}/{current_lang}/"
    else:
        canonical_href = f"{BASE_URL}/demo.html" if current_lang == 'ar' else f"{BASE_URL}/{current_lang}/demo.html"
    lines.append(f'    <link rel="canonical" href="{canonical_href}">')
    
    # 2. Reciprocal hreflang tags for all 29 supported languages
    for lang in LANGUAGES:
        if page_type == 'index':
            href = f"{BASE_URL}/" if lang == 'ar' else f"{BASE_URL}/{lang}/"
        else:
            href = f"{BASE_URL}/demo.html" if lang == 'ar' else f"{BASE_URL}/{lang}/demo.html"
        lines.append(f'    <link rel="alternate" hreflang="{lang}" href="{href}">')
        
    # 3. x-default fallback
    default_href = f"{BASE_URL}/" if page_type == 'index' else f"{BASE_URL}/demo.html"
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="{default_href}">')
    
    return "\n".join(lines)


# Regex to remove existing canonical and hreflang links to prevent duplicates
CLEAN_REGEX = re.compile(
    r'(?m)^\s*<!--\s*(?:SEO:|S&R CoreSync Enterprise SEO:).*?-->\s*\n|'
    r'^\s*<link\s+rel="(?:canonical|alternate)"\s+(?:hreflang="[^"]*"\s+)?href="https?://[^"]*"[^>]*>\s*\n?',
    re.IGNORECASE
)

def process_file(file_path, page_type, lang):
    if not os.path.isfile(file_path):
        print(f"WARNING: File not found: {file_path}")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Remove existing canonical and alternate hreflang tags
    cleaned_html = CLEAN_REGEX.sub('', html)
    
    # Generate the pristine, standardized block
    seo_block = build_hreflang_block(page_type, lang)
    
    # Inject right after `<meta name="viewport" ...>` or right before `</head>`
    viewport_match = re.search(r'(<meta\s+name=["\']viewport["\'][^>]*>)', cleaned_html, re.IGNORECASE)
    if viewport_match:
        target = viewport_match.group(1)
        new_html = cleaned_html.replace(target, target + "\n" + seo_block, 1)
    else:
        # Fallback before </head>
        new_html = cleaned_html.replace('</head>', seo_block + "\n</head>", 1)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f"Processed: {os.path.relpath(file_path, ROOT)} [{lang}]")
    return True


def main():
    print("=== Deploying Stage 19: Comprehensive International SEO & Hreflang Alignment ===")
    total = 0
    
    for lang in LANGUAGES:
        if lang == 'ar':
            index_path = os.path.join(ROOT, 'index.html')
            demo_path = os.path.join(ROOT, 'demo.html')
        else:
            index_path = os.path.join(ROOT, lang, 'index.html')
            demo_path = os.path.join(ROOT, lang, 'demo.html')
            
        if process_file(index_path, 'index', lang):
            total += 1
        if process_file(demo_path, 'demo', lang):
            total += 1
            
    print(f"=== Successfully updated all {total} HTML portals with synchronized SEO & hreflang! ===")

if __name__ == '__main__':
    main()
