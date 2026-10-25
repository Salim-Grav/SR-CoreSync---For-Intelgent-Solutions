# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - Sovereign Global Multilingual Infrastructure
Generates and maintains 28 Languages:
- All 24 European Union Official Languages
- Norwegian (Scandinavia / EEA)
- Turkish (Strategic Regional Partner)
- Kurdish (Kurmanji & Sorani)
- Arabic (Corporate Master)

Injects the luxury Sovereign Language Dropdown with real-time search,
country flags, native typography, and zero linguistic leakage.
"""

import os
import re
import json

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

def build_dropdown_html(current_lang_code, page_type="demo", is_subfolder=False):
    """
    Builds the Sovereign Language Dropdown HTML with High-DPI Flags and Quick-Switch Pill.
    page_type: 'demo' or 'index'
    is_subfolder: True if the file is in e.g. /en/, /nl/, /de/
    """
    # Find current language
    curr = next((l for l in LANGUAGES if l["code"] == current_lang_code), LANGUAGES[0])
    
    # Path prefix
    prefix = "../" if is_subfolder else "./"
    
    # Target filename
    target_file = f"{page_type}.html"
    curr_flag = FLAG_IMG_MAP.get(curr["code"], "sa.png")
    
    html = []
    html.append(f'<!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->')
    html.append(f'<div class="sovereign-lang-dropdown" id="sovereignLangDropdown">')
    html.append(f'    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="true" title="اختر اللغة / Select Language">')
    html.append(f'        <span class="sovereign-lang-flag"><img src="{prefix}assets/flags/{curr_flag}" alt="{curr["code"].upper()}" class="sovereign-flag-img" width="20" height="14"></span>')
    html.append(f'        <span class="sovereign-lang-current-label">{curr["code"].upper()}</span>')
    html.append(f'        <svg class="sovereign-lang-chevron" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>')
    html.append(f'    </button>')
    html.append(f'    <div class="sovereign-lang-menu" id="sovereignLangMenu" role="menu">')
    html.append(f'        <div class="sovereign-lang-search-box">')
    html.append(f'            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>')
    search_placeholder = "ابحث عن لغة... / Search language" if current_lang_code == "ar" else "Search language / Wählen Sie Sprache..."
    html.append(f'            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearch" placeholder="{search_placeholder}" autocomplete="off">')
    html.append(f'        </div>')
    html.append(f'        <div class="sovereign-lang-scroll-area">')
    
    # Group: EU & Nordic
    eu_langs = [l for l in LANGUAGES if l["group"] == "eu"]
    html.append(f'            <div class="sovereign-lang-category">')
    eu_title = "الاتحاد الأوروبي والإسكندنافية (EU & Nordic)" if current_lang_code == "ar" else "European Union & Nordic"
    html.append(f'                <div class="sovereign-lang-category-title">')
    html.append(f'                    <span>{eu_title}</span>')
    html.append(f'                    <span class="badge-count">{len(eu_langs)}</span>')
    html.append(f'                </div>')
    for l in eu_langs:
        is_active = (l["code"] == current_lang_code)
        active_cls = " active" if is_active else ""
        item_flag = FLAG_IMG_MAP.get(l["code"], "sa.png")
        
        if l["code"] == "ar":
            href = f"{prefix}{target_file}"
        else:
            if is_subfolder:
                href = f"../{l['code']}/{target_file}"
            else:
                href = f"./{l['code']}/{target_file}"
                
        html.append(f'                <a href="{href}" class="sovereign-lang-item{active_cls}" data-code="{l["code"]}" data-name="{l["name_native"].lower()} {l["name_en"].lower()}" onclick="try{{localStorage.setItem(\'sr_lang_pref\',\'{l["code"]}\');}}catch(e){{}}">')
        html.append(f'                    <div class="sovereign-lang-item-left">')
        html.append(f'                        <span class="sovereign-lang-item-flag"><img src="{prefix}assets/flags/{item_flag}" alt="{l["code"].upper()}" class="sovereign-flag-img" width="20" height="14"></span>')
        html.append(f'                        <div class="sovereign-lang-item-names">')
        html.append(f'                            <span class="sovereign-lang-native">{l["name_native"]}</span>')
        html.append(f'                            <span class="sovereign-lang-english">{l["name_en"]}</span>')
        html.append(f'                        </div>')
        html.append(f'                    </div>')
        html.append(f'                    <span class="sovereign-lang-code">{l["vat"]}</span>')
        html.append(f'                </a>')
    html.append(f'            </div>')
    
    # Group: Regional & Middle East
    reg_langs = [l for l in LANGUAGES if l["group"] == "regional"]
    html.append(f'            <div class="sovereign-lang-category">')
    reg_title = "الشرق الأوسط والإقليمية (Regional & Middle East)" if current_lang_code == "ar" else "Middle East & Regional"
    html.append(f'                <div class="sovereign-lang-category-title">')
    html.append(f'                    <span>{reg_title}</span>')
    html.append(f'                    <span class="badge-count">{len(reg_langs)}</span>')
    html.append(f'                </div>')
    for l in reg_langs:
        is_active = (l["code"] == current_lang_code)
        active_cls = " active" if is_active else ""
        item_flag = FLAG_IMG_MAP.get(l["code"], "sa.png")
        
        if l["code"] == "ar":
            href = f"{prefix}{target_file}"
        else:
            if is_subfolder:
                href = f"../{l['code']}/{target_file}"
            else:
                href = f"./{l['code']}/{target_file}"
                
        html.append(f'                <a href="{href}" class="sovereign-lang-item{active_cls}" data-code="{l["code"]}" data-name="{l["name_native"].lower()} {l["name_en"].lower()}" onclick="try{{localStorage.setItem(\'sr_lang_pref\',\'{l["code"]}\');}}catch(e){{}}">')
        html.append(f'                    <div class="sovereign-lang-item-left">')
        html.append(f'                        <span class="sovereign-lang-item-flag"><img src="{prefix}assets/flags/{item_flag}" alt="{l["code"].upper()}" class="sovereign-flag-img" width="20" height="14"></span>')
        html.append(f'                        <div class="sovereign-lang-item-names">')
        html.append(f'                            <span class="sovereign-lang-native">{l["name_native"]}</span>')
        html.append(f'                            <span class="sovereign-lang-english">{l["name_en"]}</span>')
        html.append(f'                        </div>')
        html.append(f'                    </div>')
        html.append(f'                    <span class="sovereign-lang-code">{l["vat"]}</span>')
        html.append(f'                </a>')
    html.append(f'            </div>')
    
    html.append(f'        </div>')
    html.append(f'    </div>')
    html.append(f'</div>')
    
    return "\n".join(html)

def build_apple_dock_html(current_lang_code, page_type="demo", is_subfolder=False):
    """
    Builds the Apple macOS floating dock for languages and country flags.
    """
    prefix = "../" if is_subfolder else "./"
    target_file = f"{page_type}.html"
    
    primary_codes = ["ar", "en", "nl", "de", "fr", "es", "tr"]
    dock_langs = [l for l in LANGUAGES if l["code"] in primary_codes]
    
    # If the current language is not in primary_codes, include it as well
    if current_lang_code not in primary_codes:
        curr_obj = next((l for l in LANGUAGES if l["code"] == current_lang_code), None)
        if curr_obj:
            dock_langs.append(curr_obj)
            
    html = []
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
        html.append(f'        <a href="{href}" class="apple-dock-item{active_cls}" onclick="try{{localStorage.setItem(\'sr_lang_pref\',\'{l["code"]}\');}}catch(e){{}}" data-tooltip="{tooltip}" aria-label="{tooltip}">')
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
    html.append('            <span class="apple-dock-dot" style="opacity:0;"></span>')
    html.append('        </button>')
    html.append('    </div>')
    html.append('</aside>')
    
    return "\n".join(html)

def build_dropdown_js():
    """
    JavaScript to power all sovereign language dropdowns with search, keyboard navigation, and outside-click.
    """
    return """
<script>
// Sovereign Global Multilingual Hub Controller
(function() {
    function initSovereignLangDropdown() {
        const dropdown = document.getElementById('sovereignLangDropdown');
        if (!dropdown) return;
        
        const trigger = document.getElementById('sovereignLangTrigger');
        const menu = document.getElementById('sovereignLangMenu');
        const searchInput = document.getElementById('sovereignLangSearch');
        const items = dropdown.querySelectorAll('.sovereign-lang-item');
        
        if (!trigger || !menu) return;
        
        function toggleDropdown(e) {
            e.stopPropagation();
            const isOpen = dropdown.classList.contains('open');
            if (isOpen) {
                closeDropdown();
            } else {
                dropdown.classList.add('open');
                trigger.setAttribute('aria-expanded', 'true');
                if (searchInput) {
                    setTimeout(() => searchInput.focus(), 50);
                }
            }
        }
        
        function closeDropdown() {
            dropdown.classList.remove('open');
            trigger.setAttribute('aria-expanded', 'false');
            if (searchInput) {
                searchInput.value = '';
                filterItems('');
            }
        }
        
        function filterItems(query) {
            const q = query.toLowerCase().trim();
            items.forEach(item => {
                const name = item.getAttribute('data-name') || '';
                const code = item.getAttribute('data-code') || '';
                if (!q || name.includes(q) || code.includes(q)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        }
        
        trigger.addEventListener('click', toggleDropdown);

        items.forEach(item => {
            item.addEventListener('click', function() {
                const code = this.getAttribute('data-code');
                if (code) {
                    localStorage.setItem('sr_lang_pref', code);
                }
            });
        });

        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                filterItems(e.target.value);
            });
            searchInput.addEventListener('click', (e) => e.stopPropagation());
        }
        
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target)) {
                closeDropdown();
            }
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && dropdown.classList.contains('open')) {
                closeDropdown();
                trigger.focus();
            }
        });
    }
    
    window.toggleAppleDockLaunchpad = function(e) {
        if (e) e.stopPropagation();
        const dropdown = document.getElementById('sovereignLangDropdown');
        const trigger = document.getElementById('sovereignLangTrigger');
        if (dropdown && trigger) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => {
                dropdown.classList.add('open');
                trigger.setAttribute('aria-expanded', 'true');
                const searchInput = document.getElementById('sovereignLangSearch');
                if (searchInput) searchInput.focus();
            }, 250);
        }
    };
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSovereignLangDropdown);
    } else {
        initSovereignLangDropdown();
    }
})();
</script>
"""

print(f"Total languages configured: {len(LANGUAGES)}")
