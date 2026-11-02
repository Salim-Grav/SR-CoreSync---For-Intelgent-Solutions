"""
Re-inject the complete aiVoicePlannerModal (including #voicePlannerResult)
into all 28 language directories.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, 'index.html'), 'r', encoding='utf-8') as f:
    root_html = f.read()

start = root_html.find('<div class="sr-exec-modal" id="aiVoicePlannerModal"')
res_pos = root_html.find('id="voicePlannerResult"', start)
end = root_html.find('</div>\n    </div>', res_pos) + len('</div>\n    </div>')
clean_modal = root_html[start:end]

lang_dirs = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and len(d) in (2, 3) and d not in ('css', 'js')]

for lang in lang_dirs:
    p = os.path.join(ROOT, lang, 'index.html')
    if not os.path.isfile(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    # If aiVoicePlannerModal is already there, remove whatever truncated version was there
    if '<div class="sr-exec-modal" id="aiVoicePlannerModal"' in c:
        m_start = c.find('<div class="sr-exec-modal" id="aiVoicePlannerModal"')
        # find where it ends
        if 'id="voicePlannerResult"' in c:
            m_res = c.find('id="voicePlannerResult"', m_start)
            m_end = c.find('</div>\n    </div>', m_res) + len('</div>\n    </div>')
        else:
            # find next modal or div
            m_end = c.find('</div>\n    </div>', m_start) + len('</div>\n    </div>')
        c = c[:m_start] + c[m_end:]

    # Inject the complete modal with proper relative asset paths
    sub_modal = clean_modal.replace('./assets/', '../assets/')

    if '<div class="sr-exec-modal" id="executiveBookingModal"' in c:
        c = c.replace('<div class="sr-exec-modal" id="executiveBookingModal"', sub_modal + '\n    <div class="sr-exec-modal" id="executiveBookingModal"')
    elif '</body>' in c:
        c = c.replace('</body>', sub_modal + '\n</body>')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

    print(f"[{lang}] Injected complete aiVoicePlannerModal (length {len(sub_modal)})")

print("Completed re-injecting complete modal to all language pages.")
