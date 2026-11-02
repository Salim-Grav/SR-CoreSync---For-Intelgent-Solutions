"""
Script to inject:
1. #bookingAudioGreetingStrip into #executiveBookingModal across index.html and all 28 languages
2. Ensure sr-inline-13eaa28e.js is loaded in all 28 language pages
3. Ensure #aiVoicePlannerModal is present in all 28 language pages
"""
import os
import glob
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GREETING_STRIP_AR = '''
            <!-- رسالة المستشار الصوتية الترحيبية -->
            <div class="sr-booking-audio-greeting" id="bookingAudioGreetingStrip">
                <div class="sr-booking-audio-avatar-wrap">
                    <img src="./assets/founder-salim.webp" id="bookingAudioAvatar" class="sr-booking-audio-avatar" alt="المستشار التنفيذي" width="48" height="48">
                    <span class="sr-booking-audio-pulse-dot" id="bookingAudioPulseDot"></span>
                </div>
                <div class="sr-booking-audio-info">
                    <div class="sr-booking-audio-title" id="bookingAudioAdvisorName">م. محمد سليم عزيزة • استشارة تنفيذية خاصة</div>
                    <div class="sr-booking-audio-desc" id="bookingAudioAdvisorSubtitle">رسالة ترحيبية وتوجيهية مباشرة من القيادة قبل حجز جلستك الاستراتيجية</div>
                </div>
                <button type="button" class="sr-booking-audio-play-btn" id="bookingAudioPlayBtn" data-sr-call="toggleBookingAudioGreeting" title="استمع للرسالة التنفيذية">
                    <span id="bookingAudioPlayBtnIcon">🎙️</span>
                    <span id="bookingAudioPlayBtnText">استمع للرسالة الصوتية</span>
                </button>
            </div>
'''

GREETING_STRIP_EN = '''
            <!-- Executive Audio Greeting Strip -->
            <div class="sr-booking-audio-greeting" id="bookingAudioGreetingStrip">
                <div class="sr-booking-audio-avatar-wrap">
                    <img src="../assets/founder-salim.webp" id="bookingAudioAvatar" class="sr-booking-audio-avatar" alt="Executive Advisor" width="48" height="48">
                    <span class="sr-booking-audio-pulse-dot" id="bookingAudioPulseDot"></span>
                </div>
                <div class="sr-booking-audio-info">
                    <div class="sr-booking-audio-title" id="bookingAudioAdvisorName">Eng. Mohammad Salim Aziza • VIP Consultation</div>
                    <div class="sr-booking-audio-desc" id="bookingAudioAdvisorSubtitle">Direct executive audio greeting from leadership before confirming your session</div>
                </div>
                <button type="button" class="sr-booking-audio-play-btn" id="bookingAudioPlayBtn" data-sr-call="toggleBookingAudioGreeting" title="Listen to Executive Audio">
                    <span id="bookingAudioPlayBtnIcon">🎙️</span>
                    <span id="bookingAudioPlayBtnText">Listen to Executive Audio</span>
                </button>
            </div>
'''

def patch_index():
    index_path = os.path.join(ROOT, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update founder name on line 6597
    c = c.replace('أ. محمد رائد كعكة', 'أ. رائد عزيزة')
    c = c.replace('المستشار المالي ومطور نظم المؤسسات والضرائب', 'المسؤول التنفيذي للعمليات وتطوير الأعمال')

    # 2. Add greeting strip into #executiveBookingModal
    target_marker = '<!-- اختيار المستشار -->'
    if 'id="bookingAudioGreetingStrip"' not in c and target_marker in c:
        c = c.replace(target_marker, GREETING_STRIP_AR + '\n            ' + target_marker)
        print("Injected bookingAudioGreetingStrip into root index.html")
    else:
        print("bookingAudioGreetingStrip already in index.html or marker missing")

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(c)

def patch_language_pages():
    # Extract aiVoicePlannerModal from root index.html
    with open(os.path.join(ROOT, 'index.html'), 'r', encoding='utf-8') as f:
        root_html = f.read()
    
    idx1 = root_html.find('<div class="sr-exec-modal" id="aiVoicePlannerModal"')
    idx2 = root_html.find('<!-- ========================================================================\n         STRICT CSP SECURE MODAL DISPATCHER', idx1)
    if idx2 == -1:
        idx2 = root_html.find('<!-- ========================================================================\r\n         STRICT CSP SECURE MODAL DISPATCHER', idx1)
    if idx2 == -1:
        idx2 = root_html.find('</div>\n    </div>\n    <!-- ========================================================================', idx1) + len('</div>\n    </div>')

    # We extract the clean modal
    modal_m = re.search(r'(<div class="sr-exec-modal" id="aiVoicePlannerModal"[\s\S]*?</div>\s*</div>)', root_html)
    if not modal_m:
        print("ERROR: could not extract aiVoicePlannerModal from root index.html")
        return
    modal_template = modal_m.group(1)

    lang_dirs = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and len(d) in (2, 3) and d not in ('css', 'js')]
    print(f"Found {len(lang_dirs)} language directories:", lang_dirs)

    script_tag = '<script src="../js/sr-inline-13eaa28e.js?v=20261102-p0-matrix" defer></script>'

    for lang in lang_dirs:
        p = os.path.join(ROOT, lang, 'index.html')
        if not os.path.isfile(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()

        changed = False

        # 1. Ensure script is loaded
        if 'sr-inline-13eaa28e.js' not in c:
            # Insert before </head> or before last script
            if '</body>' in c:
                c = c.replace('</body>', f'    {script_tag}\n</body>')
                changed = True
                print(f"[{lang}] Added script sr-inline-13eaa28e.js")

        # 2. Ensure aiVoicePlannerModal is present
        if 'id="aiVoicePlannerModal"' not in c:
            # Adjust relative asset paths for subdirectories
            lang_modal = modal_template.replace('./assets/', '../assets/')
            # Insert before #executiveBookingModal or before </body>
            if 'id="executiveBookingModal"' in c:
                c = c.replace('<div class="sr-exec-modal" id="executiveBookingModal"', lang_modal + '\n    <div class="sr-exec-modal" id="executiveBookingModal"')
                changed = True
                print(f"[{lang}] Injected aiVoicePlannerModal")
            elif '</body>' in c:
                c = c.replace('</body>', lang_modal + '\n</body>')
                changed = True
                print(f"[{lang}] Injected aiVoicePlannerModal before </body>")

        # 3. Ensure bookingAudioGreetingStrip is in #executiveBookingModal
        if 'id="bookingAudioGreetingStrip"' not in c and 'id="executiveBookingModal"' in c:
            # Look for advisor selection
            target = re.search(r'(<div class="sr-advisor-select-grid"|<label class="sr-exec-label mb-2 d-block">)', c)
            if target:
                insert_pos = target.start()
                strip_html = GREETING_STRIP_EN if lang != 'ckb' else GREETING_STRIP_AR.replace('./assets/', '../assets/')
                c = c[:insert_pos] + strip_html + '\n            ' + c[insert_pos:]
                changed = True
                print(f"[{lang}] Injected bookingAudioGreetingStrip")

        # 4. Clean founder names in executiveBookingModal
        if 'أ. محمد رائد كعكة' in c:
            c = c.replace('أ. محمد رائد كعكة', 'أ. رائد عزيزة')
            changed = True

        if changed:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)

if __name__ == '__main__':
    patch_index()
    patch_language_pages()
    print("Completed deployment to all index files.")
