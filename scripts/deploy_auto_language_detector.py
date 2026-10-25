# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - 0ms Sovereign System Language Auto-Detector
Detects visitor device/browser locale and instantly routes them to their native language portal.
- Arabic device (ar) -> stays on root index.html (Arabic Master)
- English device (en) -> routes to en/index.html
- Dutch (nl), German (de), French (fr), Spanish (es), etc. -> routes to their respective native portal
- Respects user manual selection via localStorage ('sr_lang_pref').
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

AUTO_DETECT_SCRIPT = """    <!-- Sovereign Intelligent System Language Auto-Detector (0ms Frictionless Device Routing) -->
    <script id="srLangAutoDetect">
    (function() {
        try {
            var urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('noredirect') === '1') return;
            var qLang = urlParams.get('lang');
            var supported = ["ar","en","nl","de","fr","tr","sv","no","es","it","ku","ckb","pl","pt","da","fi","cs","el","ro","hu","bg","sk","hr","lt","sl","lv","et","ga","mt"];
            
            // 1. User manual override from localStorage
            var savedPref = localStorage.getItem('sr_lang_pref');
            var targetLang = savedPref;
            
            // 2. Query param ?lang=xx
            if (qLang && supported.indexOf(qLang.toLowerCase()) !== -1) {
                targetLang = qLang.toLowerCase();
                localStorage.setItem('sr_lang_pref', targetLang);
            }
            
            // 3. Auto-detect from visitor device / OS / browser system language
            if (!targetLang) {
                var browserLangs = navigator.languages || [navigator.language || navigator.userLanguage || ''];
                for (var i = 0; i < browserLangs.length; i++) {
                    var raw = (browserLangs[i] || '').toLowerCase().trim();
                    var primary = raw.split('-')[0];
                    if (raw.indexOf('ckb') !== -1 || raw.indexOf('ku-iq') !== -1 || raw.indexOf('sorani') !== -1) {
                        targetLang = 'ckb';
                        break;
                    }
                    if (supported.indexOf(primary) !== -1) {
                        targetLang = primary;
                        break;
                    }
                }
                // If device is not Arabic and no specific language matched, fallback to English
                if (!targetLang && browserLangs.length > 0) {
                    var first = (browserLangs[0] || '').toLowerCase();
                    targetLang = (first.indexOf('ar') !== -1) ? 'ar' : 'en';
                }
            }
            
            // 4. Compare with current page language and route immediately
            var currentLang = document.documentElement.getAttribute('lang') || 'ar';
            if (targetLang && targetLang !== currentLang && supported.indexOf(targetLang) !== -1) {
                var isDemo = window.location.pathname.indexOf('demo.html') !== -1;
                var targetFile = isDemo ? 'demo.html' : 'index.html';
                var targetPath = (targetLang === 'ar') ? targetFile : (targetLang + '/' + targetFile);
                var isSubfolder = window.location.pathname.match(/\\/[a-z]{2,3}\\//);
                var prefix = isSubfolder ? '../' : './';
                var destUrl = prefix + targetPath + window.location.search + window.location.hash;
                window.location.replace(destUrl);
            }
        } catch(e) {}
    })();
    </script>
"""

# Function to inject auto-detector into any HTML file
def inject_detector(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Remove older detector versions if present
    c = re.sub(r'<!-- Sovereign Intelligent System Language Auto-Detector[\s\S]*?<\/script>\n?', '', c)
    c = re.sub(r'<!-- Language Auto-Redirect[\s\S]*?<\/script>\n?', '', c)
    c = re.sub(r'<script id="srLangAutoDetect">[\s\S]*?<\/script>\n?', '', c)
    
    # Inject right after <meta charset="utf-8">
    if '<meta charset="utf-8">' in c:
        c = c.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + AUTO_DETECT_SCRIPT, 1)
    elif '<meta charset="UTF-8">' in c:
        c = c.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + AUTO_DETECT_SCRIPT, 1)
    elif '<head>' in c:
        c = c.replace('<head>', '<head>\n' + AUTO_DETECT_SCRIPT, 1)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Injected Auto-Detector into: {os.path.relpath(file_path, BASE_DIR)}")

# Inject into root files
inject_detector(os.path.join(BASE_DIR, 'index.html'))
inject_detector(os.path.join(BASE_DIR, 'demo.html'))

# Inject across all language folders
from deploy_sovereign_multilingual import LANGUAGES
for l in LANGUAGES:
    code = l["code"]
    if code == "ar":
        continue
    inject_detector(os.path.join(BASE_DIR, code, 'index.html'))
    inject_detector(os.path.join(BASE_DIR, code, 'demo.html'))

print("\nDevice Language Auto-Detection Engine successfully deployed across all 29 language portals!")
