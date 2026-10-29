#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_logos_and_dock_routing.py
=============================
1. Fix all emblem/logo sections in index.html to ensure the company name and
   logo labels remain in English (S&R CoreSync For Intelligent Solutions / Official Sovereign Emblem),
   and remove any Arabicized logo labels.
2. Fix srLangAutoDetect across all 58 HTML files so subfolder language pages
   NEVER auto-redirect back to Arabic when a user visits them.
3. Fix the macOS Apple Dock & Launchpad language switcher links across all pages
   so clicking any language seamlessly loads that language without getting bounced.
"""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIXED AUTO-DETECT SCRIPT
# ─────────────────────────────────────────────────────────────────────────────
NEW_AUTO_DETECT_JS = """    <!-- Sovereign Intelligent System Language Auto-Detector (0ms Frictionless Device & Media App Routing) -->
    <script id="srLangAutoDetect">
    (function() {
        try {
            if (/bot|crawl|spider|slurp|google|bing|yandex|lighthouse|headless/i.test(navigator.userAgent)) return;
            var urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('noredirect') === '1') return;
            var qLang = urlParams.get('lang');
            var supported = ["ar","en","nl","de","fr","tr","sv","no","es","it","ku","ckb","pl","pt","da","fi","cs","el","ro","hu","bg","sk","hr","lt","sl","lv","et","ga","mt"];
            
            var currentLang = (document.documentElement.getAttribute('lang') || 'ar').toLowerCase().split('-')[0];
            var isDemo = window.location.pathname.indexOf('demo.html') !== -1;
            var targetFile = isDemo ? 'demo.html' : 'index.html';
            var isSubfolder = !!window.location.pathname.match(/\\/[a-z]{2,3}\\//);
            var prefix = isSubfolder ? '../' : './';
            
            // 1. Explicit query parameter ?lang=xx (immediate manual priority)
            if (qLang && supported.indexOf(qLang.toLowerCase()) !== -1) {
                var chosen = qLang.toLowerCase();
                try {
                    sessionStorage.setItem('sr_user_lang_locked', chosen);
                    localStorage.setItem('sr_lang_pref', chosen);
                } catch(e){}
                if (chosen !== currentLang) {
                    var targetPath = (chosen === 'ar') ? targetFile : (chosen + '/' + targetFile);
                    window.location.replace(prefix + targetPath + window.location.hash);
                }
                return;
            }

            // If user is already on a dedicated language subfolder (e.g. /de/, /nl/, /fr/),
            // NEVER auto-bounce them back to another language! Respect their direct visit!
            if (isSubfolder) {
                return;
            }

            // 2. Active Session Manual Lock: User explicitly switched language during this visit
            var sessionLock = null;
            try { sessionLock = sessionStorage.getItem('sr_user_lang_locked'); } catch(e){}
            if (sessionLock && supported.indexOf(sessionLock) !== -1) {
                if (sessionLock !== currentLang) {
                    var targetPath = (sessionLock === 'ar') ? targetFile : (sessionLock + '/' + targetFile);
                    window.location.replace(prefix + targetPath + window.location.hash);
                }
                return;
            }

            // 3. Persistent user preference
            var prefLang = null;
            try { prefLang = localStorage.getItem('sr_lang_pref'); } catch(e){}
            if (prefLang && supported.indexOf(prefLang) !== -1) {
                if (prefLang !== currentLang) {
                    var targetPath = (prefLang === 'ar') ? targetFile : (prefLang + '/' + targetFile);
                    window.location.replace(prefix + targetPath + window.location.hash);
                }
                return;
            }

            // 4. Automatic Device, Mobile & Browser Language Detection (Only on root entry!)
            var browserLangs = navigator.languages || [navigator.language || navigator.userLanguage || navigator.browserLanguage || ''];
            var targetLang = null;

            for (var i = 0; i < browserLangs.length; i++) {
                var raw = (browserLangs[i] || '').toLowerCase().trim();
                var primary = raw.split('-')[0];
                if (primary === 'ar' || raw.indexOf('ar') !== -1) {
                    targetLang = 'ar';
                    break;
                }
            }

            if (!targetLang) {
                for (var j = 0; j < browserLangs.length; j++) {
                    var rawJ = (browserLangs[j] || '').toLowerCase().trim();
                    var primaryJ = rawJ.split('-')[0];
                    if (rawJ.indexOf('ckb') !== -1 || rawJ.indexOf('sorani') !== -1) {
                        targetLang = 'ckb';
                        break;
                    }
                    if (rawJ.indexOf('ku') !== -1 || rawJ.indexOf('kurmanji') !== -1) {
                        targetLang = 'ku';
                        break;
                    }
                    if (supported.indexOf(primaryJ) !== -1) {
                        targetLang = primaryJ;
                        break;
                    }
                }
            }

            if (!targetLang) {
                targetLang = 'en';
            }

            if (targetLang && targetLang !== currentLang && supported.indexOf(targetLang) !== -1) {
                var routePath = (targetLang === 'ar') ? targetFile : (targetLang + '/' + targetFile);
                window.location.replace(prefix + routePath + window.location.search + window.location.hash);
            }
        } catch(e) {
            // Fail-safe
        }
    })();
    </script>"""

def update_autodetect_scripts():
    print("[1] Updating srLangAutoDetect across all HTML pages...")
    count = 0
    pattern = re.compile(r'<!-- Sovereign Intelligent System Language Auto-Detector.*?<\/script>', re.DOTALL)
    
    for root, dirs, files in os.walk(BASE_DIR):
        if '_site' in root or '.git' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    if 'id="srLangAutoDetect"' in content:
                        new_content = pattern.sub(NEW_AUTO_DETECT_JS, content)
                        if new_content != content:
                            with open(file_path, 'w', encoding='utf-8') as fh:
                                fh.write(new_content)
                            count += 1
                except Exception as e:
                    print(f"Error updating autodetect in {file_path}: {e}")
    print(f"Updated autodetect script in {count} HTML files.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. FIX DOCK AND LAUNCHPAD LINKS IN ALL PAGES
# ─────────────────────────────────────────────────────────────────────────────
def update_dock_and_launchpad_links():
    print("[2] Updating Apple macOS Dock & Launchpad links...")
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if '_site' in root or '.git' in root:
            continue
        for f in files:
            if f in ('index.html', 'demo.html'):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    
                    is_subfolder = root != BASE_DIR
                    prefix = '../' if is_subfolder else './'
                    
                    # Update dock items
                    def fix_dock_href(match):
                        tag = match.group(0)
                        # Replace href with query params ?lang=xx&noredirect=1
                        lang_match = re.search(r'href="([^"]+)"', tag)
                        if not lang_match:
                            return tag
                        old_href = lang_match.group(1)
                        # Determine language
                        if 'de/index.html' in old_href or 'de/demo.html' in old_href:
                            new_href = prefix + 'de/' + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=de&noredirect=1'
                        elif 'fr/index.html' in old_href or 'fr/demo.html' in old_href:
                            new_href = prefix + 'fr/' + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=fr&noredirect=1'
                        elif 'nl/index.html' in old_href or 'nl/demo.html' in old_href:
                            new_href = prefix + 'nl/' + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=nl&noredirect=1'
                        elif 'en/index.html' in old_href or 'en/demo.html' in old_href:
                            new_href = prefix + 'en/' + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=en&noredirect=1'
                        elif 'es/index.html' in old_href or 'es/demo.html' in old_href:
                            new_href = prefix + 'es/' + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=es&noredirect=1'
                        elif 'tr/index.html' in old_href or 'tr/demo.html' in old_href:
                            new_href = prefix + 'tr/' + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=tr&noredirect=1'
                        elif (old_href.endswith('index.html') and not any(l in old_href for l in ['/de/','/fr/','/nl/','/en/','/es/','/tr/'])) or old_href == './index.html' or old_href == '../index.html':
                            new_href = prefix + ('demo.html' if 'demo.html' in old_href else 'index.html') + '?lang=ar&noredirect=1'
                        else:
                            return tag
                        return tag.replace(f'href="{old_href}"', f'href="{new_href}"')
                    
                    new_content = re.sub(r'<a\s+href="[^"]+"\s+class="apple-dock-item[^"]*"[^>]*>', fix_dock_href, content)
                    
                    # Also update launchpad cards
                    def fix_launchpad_href(match):
                        tag = match.group(0)
                        code_m = re.search(r'data-code="([a-z]{2,3})"', tag)
                        href_m = re.search(r'href="([^"]+)"', tag)
                        if not code_m or not href_m:
                            return tag
                        code = code_m.group(1)
                        old_href = href_m.group(1)
                        file_target = 'demo.html' if 'demo.html' in old_href else 'index.html'
                        if code == 'ar':
                            new_href = f"{prefix}{file_target}?lang=ar&noredirect=1"
                        else:
                            new_href = f"{prefix}{code}/{file_target}?lang={code}&noredirect=1"
                        return tag.replace(f'href="{old_href}"', f'href="{new_href}"')

                    new_content = re.sub(r'<a\s+href="[^"]+"\s+class="apple-launchpad-card[^"]*"[^>]*>', fix_launchpad_href, new_content)

                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as fh:
                            fh.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"Error updating dock in {file_path}: {e}")
    print(f"Updated Dock and Launchpad links in {count} HTML files.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. FIX EMBLEM / LOGO CONTENT IN ARABIC INDEX.HTML
# ─────────────────────────────────────────────────────────────────────────────
def fix_arabic_index_logos():
    print("[3] Fixing emblem & logo labels in index.html...")
    index_file = os.path.join(BASE_DIR, 'index.html')
    with open(index_file, 'r', encoding='utf-8') as fh:
        content = fh.read()

    replacements = [
        # Showcase slide 0 titles and labels
        (
            'S&amp;R CoreSync For Intelligent Solutions • الشعار الرسمي المعتمد',
            'S&amp;R CoreSync For Intelligent Solutions • Official Sovereign Emblem'
        ),
        (
            'شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync (For Intelligent Solutions)',
            'S&amp;R CoreSync For Intelligent Solutions - Official Luxury Sovereign Emblem'
        ),
        (
            'alt="شعار الهوية المؤسسية الفاخر S&amp;R CoreSync"',
            'alt="S&amp;R CoreSync Official Sovereign Emblem"'
        ),
        (
            'alt="شعار الهوية المؤسسية الفاخر"',
            'alt="S&amp;R CoreSync Official Sovereign Emblem"'
        ),
        (
            '<span>شعار الهوية الفاخر (S&amp;R Emblem) ✨</span>',
            '<span>S&amp;R CoreSync Sovereign Emblem ✨</span>'
        ),
        (
            'data-sr-args=\'["assets/sr-emblem-gold-luxury.jpg", "شعار الهوية المؤسسية الفاخر", "emblem"]\'',
            'data-sr-args=\'["assets/sr-emblem-gold-luxury.jpg", "S&R CoreSync Official Sovereign Emblem", "emblem"]\''
        ),
        (
            'data-sr-args=\'["assets/sr-emblem-gold-luxury.jpg", "شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync"]\'',
            'data-sr-args=\'["assets/sr-emblem-gold-luxury.jpg", "S&R CoreSync Official Sovereign Emblem"]\''
        ),
        (
            'data-sr-args=\'["assets/sr-emblem-gold-luxury.jpg", "شعار الهوية المؤسسية الفاخر"]\'',
            'data-sr-args=\'["assets/sr-emblem-gold-luxury.jpg", "S&R CoreSync Official Sovereign Emblem"]\''
        ),
        (
            '<div class="showcase-footer-role">الشعار الرسمي المعتمد • For Intelligent Solutions</div>',
            '<div class="showcase-footer-role">Official Sovereign Emblem • For Intelligent Solutions</div>'
        ),
        (
            '<h3 id="brandLogoModalTitle" class="sr-logo-modal-title">شعار S&amp;R CoreSync For Intelligent Solutions</h3>',
            '<h3 id="brandLogoModalTitle" class="sr-logo-modal-title">S&amp;R CoreSync For Intelligent Solutions — Official Brandmark</h3>'
        ),
        (
            'alt="S&amp;R CoreSync For Intelligent Solutions - الشعار الرسمي 2026"',
            'alt="S&amp;R CoreSync For Intelligent Solutions Official Sovereign Emblem 2026"'
        ),
        (
            'alt="S&amp;R CoreSync For Intelligent Solutions - الشعار الذهبي الرسمي 4K Ultra-DPI"',
            'alt="S&amp;R CoreSync For Intelligent Solutions Official Gold Sovereign Emblem 4K Ultra-DPI"'
        ),
        (
            'alt="بانر م. محمد سليم عزيزة"',
            'alt="Eng. Mohammad Salim Aziza Executive Banner"'
        ),
        (
            'alt="بانر أ. محمد رائد كعكة"',
            'alt="Mr. Mohammad Raed Kaakeh Executive Banner"'
        ),
        (
            'درع الشعار الرسمي',
            'S&amp;R CoreSync Official Emblem'
        ),
        (
            'تحميل الشعار بدقة 4K فائقة',
            'تحميل الشعار الرسمي بدقة 4K فائقة'
        ),
        (
            'role: \'شعار الشركة الرسمي • For Intelligent Solutions\'',
            'role: \'S&R CoreSync Official Sovereign Emblem • For Intelligent Solutions\''
        ),
        (
            '<h4 class="brand-kit-heading" id="brandKitHeadingText">حزمة أصول الشعار والهوية</h4>',
            '<h4 class="brand-kit-heading" id="brandKitHeadingText">حزمة أصول الشعار الرسمي (S&amp;R CoreSync Brand Kit)</h4>'
        ),
        (
            '<span id="brandKitBtnText">تحميل حزمة الشعار (ZIP)</span>',
            '<span id="brandKitBtnText">تحميل حزمة الشعار الرسمي (ZIP)</span>'
        ),
        (
            '<li><a href="./logo-studio.html">استوديو الشعار الرسمي ✨</a></li>',
            '<li><a href="./logo-studio.html">استوديو الشعار (S&amp;R Logo Studio) ✨</a></li>'
        ),
        (
            '<li><a href="#brandLogoLightboxModal" data-sr-call="openLogoLightbox" data-sr-event="1">معاينة الشعار الرسمي 4K ✨</a></li>',
            '<li><a href="#brandLogoLightboxModal" data-sr-call="openLogoLightbox" data-sr-event="1">معاينة الشعار الرسمي 4K (Official Emblem) ✨</a></li>'
        ),
        (
            'title="S&R CoreSync For Intelligent Solutions - الشعار الرسمي المعتمد"',
            'title="S&R CoreSync For Intelligent Solutions - Official Sovereign Brandmark"'
        ),
        (
            'aria-label="عرض شعار S&R CoreSync For Intelligent Solutions المعتمد"',
            'aria-label="View S&R CoreSync For Intelligent Solutions Official Sovereign Emblem"'
        ),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    with open(index_file, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print("Fixed emblem and logo content in index.html.")

def main():
    print("=== S&R CoreSync: Language Routing & Logo Branding Remediation ===")
    update_autodetect_scripts()
    update_dock_and_launchpad_links()
    fix_arabic_index_logos()
    print("=== Completed successfully! ===")

if __name__ == '__main__':
    main()

