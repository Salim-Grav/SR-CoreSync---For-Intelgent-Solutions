import glob, os, re

# For LTR portals:
# 1. SAR / AED buttons: replace 'SAR (﷼)' -> 'SAR', 'AED (د.إ)' -> 'AED'
# 2. voicePlannerLangSelect options: replace Arabic text with clean English labels

ltr_selector_html = '''            <div class="sr-voice-mic-box">
                <!-- Dialect & Language Selector -->
                <div class="sr-voice-lang-bar" style="display:flex;justify-content:center;align-items:center;gap:8px;margin-bottom:14px;flex-wrap:wrap;">
                    <span style="font-size:0.82rem;color:var(--text-muted,#94a3b8);font-weight:600;">🌍 Voice Language & Dialect:</span>
                    <select id="voicePlannerLangSelect" style="background:rgba(14,28,22,0.95);border:1px solid rgba(197,168,128,0.4);color:#f0dfbd;padding:6px 14px;border-radius:10px;font-size:0.84rem;font-family:inherit;cursor:pointer;outline:none;">
                        <option value="ar-SA" selected>🇸🇦 Arabic (Gulf / Standard)</option>
                        <option value="ar-SY">🇸🇾 Arabic (Levant / Syria)</option>
                        <option value="ar-EG">🇪🇬 Arabic (Egypt)</option>
                        <option value="ar-AE">🇦🇪 Arabic (UAE)</option>
                        <option value="nl-NL">🇳🇱 Dutch (Nederlands)</option>
                        <option value="en-US">🇬🇧 English</option>
                        <option value="de-DE">🇩🇪 German (Deutsch)</option>
                        <option value="fr-FR">🇫🇷 French (Français)</option>
                        <option value="es-ES">🇪🇸 Spanish (Español)</option>
                        <option value="it-IT">🇮🇹 Italian (Italiano)</option>
                        <option value="tr-TR">🇹🇷 Turkish (Türkçe)</option>
                    </select>
                </div>
                <button type="button" id="voicePlannerMicBtn"'''

for p in glob.glob('*/index.html'):
    if '_site' in p or 'ckb' in p or 'ar' in p:
        continue

    with open(p, 'r', encoding='utf-8') as f:
        t = f.read()

    # Clean currency buttons in LTR portals
    t = t.replace('🇸🇦 SAR (﷼)', '🇸🇦 SAR')
    t = t.replace('🇦🇪 AED (د.إ)', '🇦🇪 AED')

    # Replace voice selector with LTR-pure selector
    t = re.sub(
        r'<div class="sr-voice-mic-box">\s*<!-- Dialect & Language Selector -->.*?<button type="button" id="voicePlannerMicBtn"',
        ltr_selector_html,
        t,
        flags=re.DOTALL
    )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(t)

print('SUCCESS: Cleaned LTR language portals for purity CI')

