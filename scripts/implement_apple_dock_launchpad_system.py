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
scripts/implement_apple_dock_launchpad_system.py
1. Completely removes all header dropdown remnants from all 60 pages (root + 28 languages).
2. Implements Apple macOS Launchpad Modal alongside the Apple Dock with session-aware manual lock.
3. Injects Sovereign Intelligent System Language Auto-Detector into all 60 pages for 0ms automatic device/browser routing.
"""

import os
import re
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

LANGUAGES = [
    # EU & Nordic
    {"code": "de", "name_native": "Deutsch", "name_en": "German", "flag": "🇩🇪", "group": "eu", "dir": "ltr", "vat": "MwSt 19%"},
    {"code": "fr", "name_native": "Français", "name_en": "French", "flag": "🇫🇷", "group": "eu", "dir": "ltr", "vat": "TVA 20%"},
    {"code": "nl", "name_native": "Nederlands", "name_en": "Dutch", "flag": "🇳🇱", "group": "eu", "dir": "ltr", "vat": "BTW 21%"},
    {"code": "en", "name_native": "English", "name_en": "English", "flag": "🇬🇧", "group": "eu", "dir": "ltr", "vat": "VAT 20%"},
    {"code": "es", "name_native": "Español", "name_en": "Spanish", "flag": "🇪🇸", "group": "eu", "dir": "ltr", "vat": "IVA 21%"},
    {"code": "it", "name_native": "Italiano", "name_en": "Italian", "flag": "🇮🇹", "group": "eu", "dir": "ltr", "vat": "IVA 22%"},
    {"code": "sv", "name_native": "Svenska", "name_en": "Swedish", "flag": "🇸🇪", "group": "eu", "dir": "ltr", "vat": "MOMS 25%"},
    {"code": "no", "name_native": "Norsk", "name_en": "Norwegian", "flag": "🇳🇴", "group": "eu", "dir": "ltr", "vat": "MVA 25%"},
    {"code": "da", "name_native": "Dansk", "name_en": "Danish", "flag": "🇩🇰", "group": "eu", "dir": "ltr", "vat": "MOMS 25%"},
    {"code": "fi", "name_native": "Suomi", "name_en": "Finnish", "flag": "🇫🇮", "group": "eu", "dir": "ltr", "vat": "ALV 25.5%"},
    {"code": "pl", "name_native": "Polski", "name_en": "Polish", "flag": "🇵🇱", "group": "eu", "dir": "ltr", "vat": "VAT 23%"},
    {"code": "pt", "name_native": "Português", "name_en": "Portuguese", "flag": "🇵🇹", "group": "eu", "dir": "ltr", "vat": "IVA 23%"},
    {"code": "el", "name_native": "Ελληνικά", "name_en": "Greek", "flag": "🇬🇷", "group": "eu", "dir": "ltr", "vat": "ΦΠΑ 24%"},
    {"code": "cs", "name_native": "Čeština", "name_en": "Czech", "flag": "🇨🇿", "group": "eu", "dir": "ltr", "vat": "DPH 21%"},
    {"code": "ro", "name_native": "Română", "name_en": "Romanian", "flag": "🇷🇴", "group": "eu", "dir": "ltr", "vat": "TVA 19%"},
    {"code": "hu", "name_native": "Magyar", "name_en": "Hungarian", "flag": "🇭🇺", "group": "eu", "dir": "ltr", "vat": "ÁFA 27%"},
    {"code": "bg", "name_native": "Български", "name_en": "Bulgarian", "flag": "🇧🇬", "group": "eu", "dir": "ltr", "vat": "ДДС 20%"},
    {"code": "sk", "name_native": "Slovenčina", "name_en": "Slovak", "flag": "🇸🇰", "group": "eu", "dir": "ltr", "vat": "DPH 20%"},
    {"code": "hr", "name_native": "Hrvatski", "name_en": "Croatian", "flag": "🇭🇷", "group": "eu", "dir": "ltr", "vat": "PDV 25%"},
    {"code": "lt", "name_native": "Lietuvių", "name_en": "Lithuanian", "flag": "🇱🇹", "group": "eu", "dir": "ltr", "vat": "PVM 21%"},
    {"code": "sl", "name_native": "Slovenščina", "name_en": "Slovenian", "flag": "🇸🇮", "group": "eu", "dir": "ltr", "vat": "DDV 22%"},
    {"code": "lv", "name_native": "Latviešu", "name_en": "Latvian", "flag": "🇱🇻", "group": "eu", "dir": "ltr", "vat": "PVN 21%"},
    {"code": "et", "name_native": "Eesti", "name_en": "Estonian", "flag": "🇪🇪", "group": "eu", "dir": "ltr", "vat": "KM 22%"},
    {"code": "ga", "name_native": "Gaeilge", "name_en": "Irish", "flag": "🇮🇪", "group": "eu", "dir": "ltr", "vat": "CBL 23%"},
    {"code": "mt", "name_native": "Malti", "name_en": "Maltese", "flag": "🇲🇹", "group": "eu", "dir": "ltr", "vat": "VAT 18%"},

    # Regional & Middle East
    {"code": "ar", "name_native": "العربية", "name_en": "Arabic (HQ Master)", "flag": "🇸🇦", "group": "regional", "dir": "rtl", "vat": "VAT 15%"},
    {"code": "tr", "name_native": "Türkçe", "name_en": "Turkish", "flag": "🇹🇷", "group": "regional", "dir": "ltr", "vat": "KDV 20%"},
    {"code": "ku", "name_native": "Kurdî (Kurmancî)", "name_en": "Kurdish (Kurmanji)", "flag": "☀️", "group": "regional", "dir": "ltr", "vat": "Tax 5%"},
    {"code": "ckb", "name_native": "کوردی (سۆرانی)", "name_en": "Kurdish (Sorani)", "flag": "☀️", "group": "regional", "dir": "rtl", "vat": "باج ٥٪"},
]

FLAG_IMG_MAP = {
    "ar": "sa.png", "en": "gb.png", "nl": "nl.png", "de": "de.png", "fr": "fr.png",
    "es": "es.png", "it": "it.png", "tr": "tr.png", "sv": "se.png", "no": "no.png",
    "da": "dk.png", "fi": "fi.png", "pl": "pl.png", "pt": "pt.png", "el": "gr.png",
    "cs": "cz.png", "ro": "ro.png", "hu": "hu.png", "bg": "bg.png", "sk": "sk.png",
    "hr": "hr.png", "lt": "lt.png", "sl": "si.png", "lv": "lv.png", "et": "ee.png",
    "ga": "ie.png", "mt": "mt.png", "ku": "iq.png", "ckb": "iq.png"
}

def build_auto_detect_script():
    return """<!-- Sovereign Intelligent System Language Auto-Detector (0ms Frictionless Device & Media App Routing) -->
    <script id="srLangAutoDetect">
    (function() {
        try {
            if (/bot|crawl|spider|slurp|google|bing|yandex/i.test(navigator.userAgent)) return;
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

            // 3. Automatic Device, Mobile & Browser Language Detection (Media apps, WhatsApp, in-app webviews)
            var browserLangs = navigator.languages || [navigator.language || navigator.userLanguage || navigator.browserLanguage || ''];
            var targetLang = null;

            // Check if device/browser prefers Arabic anywhere in its language profile
            for (var i = 0; i < browserLangs.length; i++) {
                var raw = (browserLangs[i] || '').toLowerCase().trim();
                var primary = raw.split('-')[0];
                if (primary === 'ar' || raw.indexOf('ar') !== -1) {
                    targetLang = 'ar';
                    break;
                }
            }

            // If not Arabic, inspect browser languages for Kurdish or matching European / Regional language
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

            // Global fallback for international visitors
            if (!targetLang) {
                targetLang = 'en';
            }

            // Route instantly if detected language differs from current page
            if (targetLang && targetLang !== currentLang && supported.indexOf(targetLang) !== -1) {
                var routePath = (targetLang === 'ar') ? targetFile : (targetLang + '/' + targetFile);
                window.location.replace(prefix + routePath + window.location.search + window.location.hash);
            }
        } catch(e) {
            // Fail-safe: stay on current page gracefully
        }
    })();
    </script>"""

def inject_or_update_auto_detect(html):
    pattern = r'(?:<!--\s*Sovereign Intelligent System Language Auto-Detector[^\n]*\n\s*)?<script id="srLangAutoDetect">[\s\S]*?</script>'
    new_script = build_auto_detect_script()
    if re.search(pattern, html):
        return re.sub(pattern, new_script, html, count=1)
    else:
        # Insert after <meta charset=...> or <head>
        meta_m = re.search(r'<meta charset=[^>]*>', html, flags=re.IGNORECASE)
        if meta_m:
            pos = meta_m.end()
            return html[:pos] + '\n    ' + new_script + html[pos:]
        head_m = re.search(r'<head[^>]*>', html, flags=re.IGNORECASE)
        if head_m:
            pos = head_m.end()
            return html[:pos] + '\n    ' + new_script + html[pos:]
        return html

def build_apple_dock_and_launchpad(current_lang_code, page_type="demo", is_subfolder=False):
    prefix = "../" if is_subfolder else "./"
    target_file = f"{page_type}.html"
    
    primary_codes = ["ar", "en", "nl", "de", "fr", "es", "tr"]
    dock_langs = [l for l in LANGUAGES if l["code"] in primary_codes]
    
    if current_lang_code not in primary_codes:
        curr_obj = next((l for l in LANGUAGES if l["code"] == current_lang_code), None)
        if curr_obj:
            dock_langs.append(curr_obj)
            
    html = []
    # 1. Floating Apple macOS Dock
    html.append('<!-- Apple macOS Sovereign Language & Flags Dock -->')
    html.append('<aside class="apple-macos-dock-wrapper" id="appleMacosDockWrapper" aria-label="Sovereign Language Quick Dock">')
    html.append('    <div class="apple-macos-dock" id="appleMacosDock">')
    
    for l in dock_langs:
        is_active = (l["code"] == current_lang_code)
        active_cls = " active" if is_active else ""
        flag_file = FLAG_IMG_MAP.get(l["code"], "sa.png")
        
        if l["code"] == "ar":
            href = f"{prefix}{target_file}"
        else:
            if is_subfolder:
                href = f"../{l['code']}/{target_file}"
            else:
                href = f"./{l['code']}/{target_file}"
                
        tooltip = f"{l['name_native']} ({l['name_en']})"
        html.append(f'        <a href="{href}" class="apple-dock-item{active_cls}" onclick="try{{sessionStorage.setItem(\'sr_user_lang_locked\',\'{l["code"]}\');localStorage.setItem(\'sr_lang_pref\',\'{l["code"]}\');}}catch(e){{}}" data-tooltip="{tooltip}" aria-label="{tooltip}">')
        html.append(f'            <img src="{prefix}assets/flags/{flag_file}" alt="{l["code"].upper()}" class="apple-dock-flag" width="28" height="19">')
        html.append(f'            <span class="apple-dock-dot"></span>')
        html.append(f'        </a>')
        
    html.append('        <div class="apple-dock-separator"></div>')
    html.append('        <button type="button" class="apple-dock-item apple-dock-launchpad-btn" id="appleDockLaunchpadBtn" data-tooltip="جميع اللغات الـ 28 (Launchpad)" aria-label="Open Full 28 Languages Menu" onclick="toggleAppleDockLaunchpad(event)">')
    html.append('            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">')
    html.append('                <circle cx="12" cy="12" r="10"></circle>')
    html.append('                <line x1="2" y1="12" x2="22" y2="12"></line>')
    html.append('                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>')
    html.append('            </svg>')
    html.append('            <span class="apple-dock-badge">28</span>')
    html.append('        </button>')
    html.append('    </div>')
    html.append('</aside>')
    
    # 2. Apple macOS Launchpad Modal (Full 28 Languages Grid)
    html.append('<!-- Apple macOS Launchpad Modal (28 Sovereign Languages Grid) -->')
    html.append('<div class="apple-launchpad-overlay" id="appleMacosLaunchpadOverlay" aria-modal="true" role="dialog" aria-label="Apple Launchpad - All 28 Languages">')
    html.append('    <div class="apple-launchpad-backdrop" onclick="toggleAppleDockLaunchpad(event)"></div>')
    html.append('    <div class="apple-launchpad-window">')
    html.append('        <div class="apple-launchpad-header">')
    html.append('            <div class="apple-launchpad-title-wrap">')
    html.append('                <div class="apple-launchpad-dots">')
    html.append('                    <span class="apple-dot apple-dot-red" onclick="toggleAppleDockLaunchpad(event)" title="إغلاق / Close"></span>')
    html.append('                    <span class="apple-dot apple-dot-yellow"></span>')
    html.append('                    <span class="apple-dot apple-dot-green"></span>')
    html.append('                </div>')
    lp_title = "🌐 اللغات السيادية المعتمدة (28 دولة ونظاماً ضريبياً)" if current_lang_code == "ar" else "🌐 Sovereign Global Languages (28 Supported Nations & VAT Regimes)"
    html.append(f'                <h3 class="apple-launchpad-title">{lp_title}</h3>')
    html.append('            </div>')
    html.append('            <button type="button" class="apple-launchpad-close-btn" onclick="toggleAppleDockLaunchpad(event)" aria-label="Close">✕</button>')
    html.append('        </div>')
    html.append('        <div class="apple-launchpad-search-wrap">')
    html.append('            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>')
    lp_search_ph = "ابحث عن دولة، لغة، أو نسبة الضريبة... / Search language, country, VAT..." if current_lang_code == "ar" else "Search country, language, or VAT rate..."
    html.append(f'            <input type="text" id="appleLaunchpadSearchInput" class="apple-launchpad-search-input" placeholder="{lp_search_ph}" autocomplete="off">')
    html.append('        </div>')
    html.append('        <div class="apple-launchpad-body">')
    html.append('            <div class="apple-launchpad-grid" id="appleLaunchpadGrid">')
    
    for l in LANGUAGES:
        is_active = (l["code"] == current_lang_code)
        active_cls = " active" if is_active else ""
        flag_file = FLAG_IMG_MAP.get(l["code"], "sa.png")
        
        if l["code"] == "ar":
            href = f"{prefix}{target_file}"
        else:
            if is_subfolder:
                href = f"../{l['code']}/{target_file}"
            else:
                href = f"./{l['code']}/{target_file}"
                
        html.append(f'                <a href="{href}" class="apple-launchpad-card{active_cls}" data-code="{l["code"]}" data-name="{l["name_native"].lower()} {l["name_en"].lower()}" onclick="try{{sessionStorage.setItem(\'sr_user_lang_locked\',\'{l["code"]}\');localStorage.setItem(\'sr_lang_pref\',\'{l["code"]}\');}}catch(e){{}}">')
        html.append(f'                    <div class="apple-launchpad-card-left">')
        html.append(f'                        <img src="{prefix}assets/flags/{flag_file}" alt="{l["code"].upper()}" class="apple-launchpad-flag" width="28" height="19">')
        html.append(f'                        <div class="apple-launchpad-text">')
        html.append(f'                            <span class="apple-launchpad-native">{l["name_native"]}</span>')
        html.append(f'                            <span class="apple-launchpad-sub">{l["name_en"]}</span>')
        html.append(f'                        </div>')
        html.append(f'                    </div>')
        html.append(f'                    <span class="apple-launchpad-vat">{l["vat"]}</span>')
        html.append(f'                </a>')
        
    html.append('            </div>')
    html.append('        </div>')
    html.append('    </div>')
    html.append('</div>')
    
    return "\n".join(html)

def build_launchpad_controller_js():
    return """
<!-- Sovereign Global Multilingual Hub Controller (Apple macOS Launchpad Edition) -->
<script>
(function() {
    function initAppleLaunchpad() {
        const overlay = document.getElementById('appleMacosLaunchpadOverlay');
        const searchInput = document.getElementById('appleLaunchpadSearchInput');
        const grid = document.getElementById('appleLaunchpadGrid');
        if (!overlay) return;
        
        window.toggleAppleDockLaunchpad = function(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            const isOpen = overlay.classList.contains('active');
            if (isOpen) {
                overlay.classList.remove('active');
                if (searchInput) {
                    searchInput.value = '';
                    filterCards('');
                }
            } else {
                overlay.classList.add('active');
                if (searchInput) {
                    setTimeout(() => searchInput.focus(), 80);
                }
            }
        };
        
        function filterCards(query) {
            if (!grid) return;
            const q = query.toLowerCase().trim();
            const cards = grid.querySelectorAll('.apple-launchpad-card');
            cards.forEach(card => {
                const name = card.getAttribute('data-name') || '';
                const code = card.getAttribute('data-code') || '';
                const vat = (card.querySelector('.apple-launchpad-vat') || {}).textContent || '';
                if (!q || name.includes(q) || code.includes(q) || vat.toLowerCase().includes(q)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        }
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => filterCards(e.target.value));
            searchInput.addEventListener('click', (e) => e.stopPropagation());
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && overlay.classList.contains('active')) {
                window.toggleAppleDockLaunchpad();
            }
        });
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAppleLaunchpad);
    } else {
        initAppleLaunchpad();
    }
})();
</script>
"""

def clean_header(html, is_demo=True):
    if is_demo:
        # demo.html header cleanup: between btn-sync-consultation and btn-return-main
        p1 = html.find('btn-sync-consultation')
        if p1 != -1:
            p1_close = html.find('</button>', p1) + 9
            p2 = html.find('btn-return-main')
            if p2 != -1:
                p2_start = html.rfind('<a', 0, p2)
                if p2_start > p1_close:
                    html = html[:p1_close] + '\n\n            ' + html[p2_start:]
    else:
        # index.html header cleanup:
        # Check Case 1: junk between header-col-actions and btn-live-sandbox-header
        p_act = html.find('header-col-actions')
        p_demo = html.find('btn-live-sandbox-header')
        p_menu = html.find('btn-mobile-menu')
        
        if p_act != -1 and p_demo != -1 and p_demo > p_act:
            p_act_open = html.find('>', p_act) + 1
            p_demo_start = html.rfind('<a', 0, p_demo)
            if p_demo_start > p_act_open + 50:
                html = html[:p_act_open] + '\n                                ' + html[p_demo_start:]
                
        # Check Case 2: junk between btn-live-sandbox-header and btn-mobile-menu
        p_demo = html.find('btn-live-sandbox-header')
        p_menu = html.find('btn-mobile-menu')
        if p_demo != -1 and p_menu != -1 and p_menu > p_demo:
            p_demo_close = html.find('</a>', p_demo) + 4
            p_menu_start = html.rfind('<button', 0, p_menu)
            if p_menu_start > p_demo_close + 50:
                html = html[:p_demo_close] + '\n\n                                ' + html[p_menu_start:]
                
    return html

def update_page(file_path, code, is_demo=True, is_subfolder=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Clean header
    html = clean_header(html, is_demo=is_demo)

    # 2. Inject or update intelligent automatic language detector in <head>
    html = inject_or_update_auto_detect(html)

    # 3. Strip any old dock, launchpad overlay, and controller script
    html = re.sub(r'<!--\s*Apple macOS Sovereign Language & Flags Dock\s*-->[\s\S]*?</aside>', '', html)
    html = re.sub(r'<!--\s*Apple macOS Launchpad Modal\s*-->[\s\S]*?</div>\s*</div>\s*</div>\s*</div>', '', html)
    html = re.sub(r'<aside class="apple-macos-dock-wrapper"[\s\S]*?</aside>', '', html)
    html = re.sub(r'<div class="apple-launchpad-overlay"[\s\S]*?</div>\s*</div>\s*</div>\s*</div>', '', html)
    html = re.sub(r'<script>\s*// Sovereign Global Multilingual Hub Controller[\s\S]*?</script>', '', html)
    html = re.sub(r'<!-- Sovereign Global Multilingual Hub Controller \(Apple macOS Launchpad Edition\) -->[\s\S]*?</script>', '', html)

    # 4. Build and inject Apple macOS Dock + Launchpad Modal + Controller JS
    page_type = "demo" if is_demo else "index"
    dock_and_modal = build_apple_dock_and_launchpad(code, page_type=page_type, is_subfolder=is_subfolder)
    controller_js = build_launchpad_controller_js()
    injection = f"\n{dock_and_modal}\n{controller_js}\n"
    last_body_idx = html.rfind('</body>')
    if last_body_idx != -1:
        html = html[:last_body_idx] + injection + html[last_body_idx:]
    else:
        html += injection

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Processed: {file_path} [{code}]")

def main():
    print("=== Deploying Automatic Device Language Detection + Apple Dock/Launchpad ===")
    
    # 1. Master Pages
    update_page(os.path.join(BASE_DIR, 'demo.html'), 'ar', is_demo=True, is_subfolder=False)
    update_page(os.path.join(BASE_DIR, 'index.html'), 'ar', is_demo=False, is_subfolder=False)
    
    # 2. Localized Pages
    for lang in LANGUAGES:
        code = lang["code"]
        if code == "ar":
            continue
            
        demo_path = os.path.join(BASE_DIR, code, 'demo.html')
        index_path = os.path.join(BASE_DIR, code, 'index.html')
        
        if os.path.exists(demo_path):
            update_page(demo_path, code, is_demo=True, is_subfolder=True)
        if os.path.exists(index_path):
            update_page(index_path, code, is_demo=False, is_subfolder=True)
            
    print("=== All 60 pages updated with automatic device language detection! ===")

if __name__ == '__main__':
    main()
