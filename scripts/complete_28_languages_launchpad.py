import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

LANGUAGES_METADATA = [
    {
        'code': 'ar',
        'native': 'العربية',
        'sub': 'Arabic (HQ Master)',
        'flag': 'sa.png',
        'vat': 'VAT 0% / 15%',
        'search': 'العربية arabic saudi uae qatar kuwait'
    },
    {
        'code': 'en',
        'native': 'English',
        'sub': 'English (UK / Global)',
        'flag': 'gb.png',
        'vat': 'VAT 20%',
        'search': 'english uk global united kingdom'
    },
    {
        'code': 'nl',
        'native': 'Nederlands',
        'sub': 'Dutch (HQ Amsterdam)',
        'flag': 'nl.png',
        'vat': 'BTW 21%',
        'search': 'nederlands dutch holland netherlands amsterdam'
    },
    {
        'code': 'de',
        'native': 'Deutsch',
        'sub': 'German',
        'flag': 'de.png',
        'vat': 'MwSt 19%',
        'search': 'deutsch german germany austria'
    },
    {
        'code': 'fr',
        'native': 'Français',
        'sub': 'French',
        'flag': 'fr.png',
        'vat': 'TVA 20%',
        'search': 'français french france belgium'
    },
    {
        'code': 'es',
        'native': 'Español',
        'sub': 'Spanish',
        'flag': 'es.png',
        'vat': 'IVA 21%',
        'search': 'español spanish spain'
    },
    {
        'code': 'it',
        'native': 'Italiano',
        'sub': 'Italian',
        'flag': 'it.png',
        'vat': 'IVA 22%',
        'search': 'italiano italian italy'
    },
    {
        'code': 'tr',
        'native': 'Türkçe',
        'sub': 'Turkish',
        'flag': 'tr.png',
        'vat': 'KDV 20%',
        'search': 'türkçe turkish turkey türkiye'
    },
    {
        'code': 'sv',
        'native': 'Svenska',
        'sub': 'Swedish',
        'flag': 'se.png',
        'vat': 'MOMS 25%',
        'search': 'svenska swedish sweden'
    },
    {
        'code': 'no',
        'native': 'Norsk',
        'sub': 'Norwegian',
        'flag': 'no.png',
        'vat': 'MVA 25%',
        'search': 'norsk norwegian norway'
    },
    {
        'code': 'da',
        'native': 'Dansk',
        'sub': 'Danish',
        'flag': 'dk.png',
        'vat': 'MOMS 25%',
        'search': 'dansk danish denmark'
    },
    {
        'code': 'fi',
        'native': 'Suomi',
        'sub': 'Finnish',
        'flag': 'fi.png',
        'vat': 'ALV 25.5%',
        'search': 'suomi finnish finland'
    },
    {
        'code': 'pl',
        'native': 'Polski',
        'sub': 'Polish',
        'flag': 'pl.png',
        'vat': 'VAT 23%',
        'search': 'polski polish poland'
    },
    {
        'code': 'pt',
        'native': 'Português',
        'sub': 'Portuguese',
        'flag': 'pt.png',
        'vat': 'IVA 23%',
        'search': 'português portuguese portugal brazil'
    },
    {
        'code': 'el',
        'native': 'Ελληνικά',
        'sub': 'Greek',
        'flag': 'gr.png',
        'vat': 'ΦΠΑ 24%',
        'search': 'ελληνικά greek greece'
    },
    {
        'code': 'cs',
        'native': 'Čeština',
        'sub': 'Czech',
        'flag': 'cz.png',
        'vat': 'DPH 21%',
        'search': 'čeština czech czechia prague'
    },
    {
        'code': 'ro',
        'native': 'Română',
        'sub': 'Romanian',
        'flag': 'ro.png',
        'vat': 'TVA 19%',
        'search': 'română romanian romania'
    },
    {
        'code': 'hu',
        'native': 'Magyar',
        'sub': 'Hungarian',
        'flag': 'hu.png',
        'vat': 'ÁFA 27%',
        'search': 'magyar hungarian hungary'
    },
    {
        'code': 'bg',
        'native': 'Български',
        'sub': 'Bulgarian',
        'flag': 'bg.png',
        'vat': 'ДДС 20%',
        'search': 'български bulgarian bulgaria'
    },
    {
        'code': 'sk',
        'native': 'Slovenčina',
        'sub': 'Slovak',
        'flag': 'sk.png',
        'vat': 'DPH 20%',
        'search': 'slovenčina slovak slovakia'
    },
    {
        'code': 'hr',
        'native': 'Hrvatski',
        'sub': 'Croatian',
        'flag': 'hr.png',
        'vat': 'PDV 25%',
        'search': 'hrvatski croatian croatia'
    },
    {
        'code': 'lt',
        'native': 'Lietuvių',
        'sub': 'Lithuanian',
        'flag': 'lt.png',
        'vat': 'PVM 21%',
        'search': 'lietuvių lithuanian lithuania'
    },
    {
        'code': 'sl',
        'native': 'Slovenščina',
        'sub': 'Slovenian',
        'flag': 'si.png',
        'vat': 'DDV 22%',
        'search': 'slovenščina slovenian slovenia'
    },
    {
        'code': 'lv',
        'native': 'Latviešu',
        'sub': 'Latvian',
        'flag': 'lv.png',
        'vat': 'PVN 21%',
        'search': 'latviešu latvian latvia'
    },
    {
        'code': 'et',
        'native': 'Eesti',
        'sub': 'Estonian',
        'flag': 'ee.png',
        'vat': 'KM 22%',
        'search': 'eesti estonian estonia'
    },
    {
        'code': 'ga',
        'native': 'Gaeilge',
        'sub': 'Irish',
        'flag': 'ie.png',
        'vat': 'CBL 23%',
        'search': 'gaeilge irish ireland eire'
    },
    {
        'code': 'mt',
        'native': 'Malti',
        'sub': 'Maltese',
        'flag': 'mt.png',
        'vat': 'VAT 18%',
        'search': 'malti maltese malta'
    },
    {
        'code': 'ku',
        'native': 'Kurdî',
        'sub': 'Kurdish',
        'flag': 'iq.png',
        'vat': 'باجی هەرێمی',
        'search': 'kurdî kurdish kurdistan kurdi'
    },
    {
        'code': 'ckb',
        'native': 'کوردی سۆرانی',
        'sub': 'Central Kurdish',
        'flag': 'iq.png',
        'vat': 'باجی هەرێمی',
        'search': 'سۆرانی sorani kurdish ckb'
    }
]

def build_grid_html(is_root=True, current_lang='ar'):
    cards_html = []
    for meta in LANGUAGES_METADATA:
        code = meta['code']
        is_active = (code == current_lang)
        active_class = ' active' if is_active else ''
        
        # Build href
        if is_root:
            flag_src = f"./assets/flags/{meta['flag']}"
            if code == 'ar':
                href = "./index.html?lang=ar&noredirect=1"
            else:
                href = f"./{code}/index.html?lang={code}&noredirect=1"
        else:
            flag_src = f"../assets/flags/{meta['flag']}"
            if code == 'ar':
                href = "../index.html?lang=ar&noredirect=1"
            else:
                href = f"../{code}/index.html?lang={code}&noredirect=1"
                
        card = f'''                <a href="{href}" class="apple-launchpad-card{active_class}" data-code="{code}" data-name="{meta['search']}" onclick="try{{sessionStorage.setItem('sr_user_lang_locked','{code}');localStorage.setItem('sr_lang_pref','{code}');}}catch(e){{}}">
                    <div class="apple-launchpad-card-left">
                        <img src="{flag_src}" alt="{code.upper()}" class="apple-launchpad-flag" width="28" height="19" loading="lazy" decoding="async">
                        <div class="apple-launchpad-text">
                            <span class="apple-launchpad-native">{meta['native']}</span>
                            <span class="apple-launchpad-sub">{meta['sub']}</span>
                        </div>
                    </div>
                    <span class="apple-launchpad-vat">{meta['vat']}</span>
                </a>'''
        cards_html.append(card)
        
    return '\n'.join(cards_html)

def update_page_launchpad(file_path, is_root=True, current_lang='ar'):
    if not os.path.exists(file_path):
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Pattern to find appleLaunchpadGrid content
    pattern = re.compile(r'(<div class="apple-launchpad-grid" id="appleLaunchpadGrid">)(.*?)(</div>\s*</div>\s*</div>\s*</div>)', re.DOTALL)
    
    match = pattern.search(content)
    if not match:
        # Try alternate pattern
        pattern2 = re.compile(r'(<div class="apple-launchpad-grid" id="appleLaunchpadGrid">)(.*?)(</div>\s*</div>\s*<div class="apple-launchpad-footer")', re.DOTALL)
        match = pattern2.search(content)
        if not match:
            print(f'⚠️ [WARNING] appleLaunchpadGrid not found in {file_path}')
            return False
        new_grid = build_grid_html(is_root=is_root, current_lang=current_lang)
        new_content = pattern2.sub(rf'\1\n{new_grid}\n            \3', content)
    else:
        new_grid = build_grid_html(is_root=is_root, current_lang=current_lang)
        new_content = pattern.sub(rf'\1\n{new_grid}\n            \3', content)
        
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# 1. Update root index.html
print('Updating root index.html...')
res_root = update_page_launchpad('index.html', is_root=True, current_lang='ar')
print(f'index.html updated: {res_root}')

# 2. Update all language pages
langs = [
    'ar', 'ckb', 'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et',
    'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt',
    'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'tr'
]

updated_count = 0
for l in langs:
    if l == 'ar':
        continue
    p = f'{l}/index.html'
    if update_page_launchpad(p, is_root=False, current_lang=l):
        updated_count += 1

print(f'Successfully updated {updated_count}/28 language index.html files with all 29 sovereign languages!')

