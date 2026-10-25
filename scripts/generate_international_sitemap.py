# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions - International XML Sitemap Generator
Generates an exhaustive, search-engine-ready sitemap with all 28 multilingual portals
and hreflang alternate links conforming to Google & Bing international SEO standards.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')

from deploy_sovereign_multilingual import LANGUAGES

BASE_URL = "https://sr-coresync.com"
RELEASE_DATE = "2026-10-20"

xml = []
xml.append('<?xml version="1.0" encoding="UTF-8"?>')
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
xml.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
xml.append('')
xml.append('  <!-- ========================================================')
xml.append('       1. International Landing Pages (28 Languages)')
xml.append('       ======================================================== -->')

for lang in LANGUAGES:
    code = lang["code"]
    loc = f"{BASE_URL}/" if code == "ar" else f"{BASE_URL}/{code}/"
    priority = "1.0" if code in ["ar", "en", "nl", "de", "fr"] else "0.90"
    
    xml.append('  <url>')
    xml.append(f'    <loc>{loc}</loc>')
    xml.append(f'    <lastmod>{RELEASE_DATE}</lastmod>')
    xml.append('    <changefreq>weekly</changefreq>')
    xml.append(f'    <priority>{priority}</priority>')
    
    # Hreflang alternates
    for alt in LANGUAGES:
        alt_code = alt["code"]
        alt_href = f"{BASE_URL}/" if alt_code == "ar" else f"{BASE_URL}/{alt_code}/"
        xml.append(f'    <xhtml:link rel="alternate" hreflang="{alt_code}" href="{alt_href}"/>')
    xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>')
    xml.append('  </url>')
    xml.append('')

xml.append('  <!-- ========================================================')
xml.append('       2. Interactive Cloud ERP Demo Portals (28 Languages)')
xml.append('       ======================================================== -->')

for lang in LANGUAGES:
    code = lang["code"]
    loc = f"{BASE_URL}/demo.html" if code == "ar" else f"{BASE_URL}/{code}/demo.html"
    
    xml.append('  <url>')
    xml.append(f'    <loc>{loc}</loc>')
    xml.append(f'    <lastmod>{RELEASE_DATE}</lastmod>')
    xml.append('    <changefreq>weekly</changefreq>')
    xml.append('    <priority>0.85</priority>')
    
    # Hreflang alternates for demo
    for alt in LANGUAGES:
        alt_code = alt["code"]
        alt_href = f"{BASE_URL}/demo.html" if alt_code == "ar" else f"{BASE_URL}/{alt_code}/demo.html"
        xml.append(f'    <xhtml:link rel="alternate" hreflang="{alt_code}" href="{alt_href}"/>')
    xml.append('  </url>')
    xml.append('')

xml.append('  <!-- ========================================================')
xml.append('       3. Executive Suites & Software Hub')
xml.append('       ======================================================== -->')
# Only pages that are actually published AND linked from a public page may be
# listed here: an orphan URL in the sitemap just tells Google to index a page
# the navigation never reaches.
features = [
    ("software.html", "0.90", "weekly"),
    ("work.html", "0.85", "weekly"),
    ("estimator.html", "0.80", "monthly"),
    ("whitelabel-calculator.html", "0.75", "monthly"),
    ("3d-mockup.html", "0.70", "monthly"),
    ("logo-studio.html", "0.75", "monthly"),
    ("status.html", "0.60", "daily"),
]

for feat, prio, freq in features:
    xml.append('  <url>')
    xml.append(f'    <loc>{BASE_URL}/{feat}</loc>')
    xml.append(f'    <lastmod>{RELEASE_DATE}</lastmod>')
    xml.append(f'    <changefreq>{freq}</changefreq>')
    xml.append(f'    <priority>{prio}</priority>')
    xml.append('  </url>')

xml.append('</urlset>')

with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
    f.write("\n".join(xml))

print(f"International sitemap generated with {len(LANGUAGES) * 2 + len(features)} indexed URLs at: {SITEMAP_PATH}")
