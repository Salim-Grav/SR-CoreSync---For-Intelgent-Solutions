import glob, os, re

selector_html = '''            <div class="sr-voice-mic-box">
                <!-- Dialect & Language Selector -->
                <div class="sr-voice-lang-bar" style="display:flex;justify-content:center;align-items:center;gap:8px;margin-bottom:14px;flex-wrap:wrap;">
                    <span style="font-size:0.82rem;color:var(--text-muted,#94a3b8);font-weight:600;">🌍 Voice Language / لغة التحدث:</span>
                    <select id="voicePlannerLangSelect" style="background:rgba(14,28,22,0.95);border:1px solid rgba(197,168,128,0.4);color:#f0dfbd;padding:6px 14px;border-radius:10px;font-size:0.84rem;font-family:inherit;cursor:pointer;outline:none;">
                        <option value="ar-SA" selected>🇸🇦 العربية (الخليج والفصحى)</option>
                        <option value="ar-SY">🇸🇾 العربية (بلاد الشام وسوريا)</option>
                        <option value="ar-EG">🇪🇬 العربية (مصر)</option>
                        <option value="ar-AE">🇦🇪 العربية (الإمارات)</option>
                        <option value="nl-NL">🇳🇱 Nederlands</option>
                        <option value="en-US">🇬🇧 English</option>
                        <option value="de-DE">🇩🇪 Deutsch</option>
                        <option value="fr-FR">🇫🇷 Français</option>
                        <option value="es-ES">🇪🇸 Español</option>
                        <option value="it-IT">🇮🇹 Italiano</option>
                        <option value="tr-TR">🇹🇷 Türkçe</option>
                    </select>
                </div>
                <button type="button" id="voicePlannerMicBtn"'''

count = 0
for p in glob.glob('*/index.html'):
    if '_site' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        t = f.read()

    if 'voicePlannerLangSelect' not in t and 'sr-voice-mic-box' in t:
        t = re.sub(r'<div class=[\x22\x27]sr-voice-mic-box[\x22\x27]>\s*<button type=[\x22\x27]button[\x22\x27] id=[\x22\x27]voicePlannerMicBtn[\x22\x27]', selector_html, t, count=1)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(t)
        count += 1

print(f'Propagated dialect selector to {count} language portals.')

