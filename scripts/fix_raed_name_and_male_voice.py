"""
Script to fix:
1. Founder Raed's name: 'رائد كعكة' / 'Mr. Raed Kaakeh' (strictly NOT 'كعكة')
2. Strictly enforce male executive speech:
   - Arabic male voice keys: شاكر, حامد, ليث, باسل, علي, إسماعيل, تيم, فهد, رامي, أحمد, جمال, عبدالله, معاذ, هادي, صالح, ماجد, طارق, نايف
   - Arabic female voice keys banned: فاطمة, ليلى, أمينة, سلمى, رنا, سناء, نورا, إيمان, منى, عائشة, أمل, زارية, أماني, ريم, مريم, هدى
   - If browser voice is female or Google, force pitch = 0.52 (deep baritone masculine pitch)
"""
import os
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Update js/sr-inline-13eaa28e.js
path_13 = os.path.join(ROOT, 'js', 'sr-inline-13eaa28e.js')
with open(path_13, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace all variants of Raed Kaakeh with Raed Kaakeh
c = c.replace('رائد كعكة', 'رائد كعكة')
c = c.replace('Raed Kaakeh', 'Raed Kaakeh')
c = c.replace('Dhr. Raed Kaakeh', 'Dhr. Raed Kaakeh')
c = c.replace('Hr. Raed Kaakeh', 'Hr. Raed Kaakeh')
c = c.replace('Mr. Raed Kaakeh', 'Mr. Raed Kaakeh')

# Now inspect voice selection and pitch logic in toggleBlueprintAudioSynthesis
old_voice_block_pattern = r'const femaleKeywords\s*=\s*\[[\s\S]*?window\.speechSynthesis\.speak\(i\);'

new_voice_block = '''const femaleKeywords = [
        "فاطمة", "ليلى", "أمينة", "سلمى", "رنا", "سناء", "نورا", "إيمان", "منى", "عائشة", "أمل", "زارية", "أماني", "ريم", "مريم", "هدى", "هدا", "زينب", "سارة", "أنثى",
        "laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman", "girl", "zira", "susan", "hazel", "linda", "eva", "katja", "hedda"
    ];
    const malePreferred = [
        "شاكر", "حامد", "ليث", "باسل", "علي", "إسماعيل", "تيم", "فهد", "رامي", "أحمد", "جمال", "عبدالله", "معاذ", "هادي", "صالح", "ماجد", "طارق", "نايف", "زيد",
        "shakir", "hamed", "laith", "basel", "ali", "ismail", "taim", "fahd", "rami", "ahmed", "jamal", "abdullah", "moath", "hadi", "saleh", "maged", "tarik", "naayf", "male",
        "david", "mark", "george", "guy", "james", "bart", "stefan", "frank", "bernd", "conrad"
    ];

    const allVoices = (window.speechSynthesis && window.speechSynthesis.getVoices) ? window.speechSynthesis.getVoices() : [];
    const arVoices = allVoices.filter(e => (e.lang || "").toLowerCase().startsWith(targetLangPrefix));

    // 1. Prioritize Arabic male voices by name
    let s = arVoices.find(e => {
        const n = (e.name || "").toLowerCase();
        return malePreferred.some(m => n.includes(m.toLowerCase())) && !femaleKeywords.some(f => n.includes(f.toLowerCase()));
    });

    // 2. Fallback to any voice in target language not explicitly female
    if (!s) {
        s = arVoices.find(e => {
            const n = (e.name || "").toLowerCase();
            return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
        });
    }

    // 3. Fallback to any voice in target language
    if (!s && arVoices.length > 0) {
        s = arVoices[0];
    }

    // Strict Masculine Tone Modulation:
    if (s) {
        i.voice = s;
        const voiceName = (s.name || "").toLowerCase();
        const isTrueMale = malePreferred.some(m => voiceName.includes(m.toLowerCase()));
        // If true male voice, use pitch 0.82. If female/Google fallback, aggressively pitch down to 0.52 (deep masculine resonance)
        i.pitch = isTrueMale ? 0.82 : 0.52;
        i.rate = 0.92;
    } else {
        // No specific voice matched, force lowest masculine baritone pitch
        i.pitch = 0.52;
        i.rate = 0.92;
    }

    const c = document.getElementById("blueprintPlayVoiceIcon"), a = document.getElementById("blueprintPlayVoiceLabel");
    i.onstart = function() {
        isBlueprintSpeaking = !0;
        e && e.classList.add("is-playing");
        c && (c.innerHTML = "⏸️");
        a && (a.textContent = "إيقاف الملخص الصوتي");
        if (typeof LuxuryAudio !== "undefined") LuxuryAudio.play("hover");
    };
    i.onend = function() {
        stopBlueprintAudioSynthesis();
    };
    i.onerror = function(e) {
        console.warn("Speech synthesis notice:", e);
        stopBlueprintAudioSynthesis();
    };
    window.speechSynthesis.speak(i);'''

c = re.sub(old_voice_block_pattern, new_voice_block, c)

# Update booking greeting voice selection as well
old_booking_voice_pattern = r'const femaleKeywords\s*=\s*\[[\s\S]*?window\.speechSynthesis\.speak\(utt\);'
new_booking_voice_block = '''const femaleKeywords = [
        "فاطمة", "ليلى", "أمينة", "سلمى", "رنا", "سناء", "نورا", "إيمان", "منى", "عائشة", "أمل", "زارية", "أماني", "ريم", "مريم", "هدى", "هدا", "زينب", "سارة", "أنثى",
        "laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman", "girl", "zira", "susan", "hazel", "linda", "eva", "katja", "hedda"
    ];
    const malePreferred = [
        "شاكر", "حامد", "ليث", "باسل", "علي", "إسماعيل", "تيم", "فهد", "رامي", "أحمد", "جمال", "عبدالله", "معاذ", "هادي", "صالح", "ماجد", "طارق", "نايف", "زيد",
        "shakir", "hamed", "laith", "basel", "ali", "ismail", "taim", "fahd", "rami", "ahmed", "jamal", "abdullah", "moath", "hadi", "saleh", "maged", "tarik", "naayf", "male",
        "david", "mark", "george", "guy", "james", "bart", "stefan", "frank", "bernd", "conrad"
    ];

    const allVoices = (window.speechSynthesis && window.speechSynthesis.getVoices) ? window.speechSynthesis.getVoices() : [];
    const arVoices = allVoices.filter(e => (e.lang || "").toLowerCase().startsWith(targetLangPrefix));

    let matchedVoice = arVoices.find(e => {
        const n = (e.name || "").toLowerCase();
        return malePreferred.some(m => n.includes(m.toLowerCase())) && !femaleKeywords.some(f => n.includes(f.toLowerCase()));
    });
    if (!matchedVoice) {
        matchedVoice = arVoices.find(e => {
            const n = (e.name || "").toLowerCase();
            return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
        });
    }
    if (!matchedVoice && arVoices.length > 0) {
        matchedVoice = arVoices[0];
    }

    if (matchedVoice) {
        utt.voice = matchedVoice;
        const voiceName = (matchedVoice.name || "").toLowerCase();
        const isTrueMale = malePreferred.some(m => voiceName.includes(m.toLowerCase()));
        utt.pitch = isTrueMale ? 0.82 : 0.52;
        utt.rate = 0.92;
    } else {
        utt.pitch = 0.52;
        utt.rate = 0.92;
    }

    const strip = document.getElementById("bookingAudioGreetingStrip");
    const btnText = document.getElementById("bookingAudioPlayBtnText");
    const btnIcon = document.getElementById("bookingAudioPlayBtnIcon");

    utt.onstart = function() {
        isBookingGreetingSpeaking = true;
        if (strip) strip.classList.add("is-playing");
        if (btnText) btnText.textContent = lk === "ar" ? "إيقاف الرسالة الصوتية ⏸️" : "Pause Audio ⏸️";
        if (btnIcon) btnIcon.textContent = "⏸️";
    };
    utt.onend = function() {
        stopBookingAudioGreeting();
    };
    utt.onerror = function() {
        stopBookingAudioGreeting();
    };

    window.speechSynthesis.speak(utt);'''

c = re.sub(old_booking_voice_pattern, new_booking_voice_block, c)

with open(path_13, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated js/sr-inline-13eaa28e.js with Raed Kaakeh and Arabic male voice list.")

# 2. Update js/sr-inline-0c7f8fde.js
path_0c = os.path.join(ROOT, 'js', 'sr-inline-0c7f8fde.js')
with open(path_0c, 'r', encoding='utf-8') as f:
    c0c = f.read()

c0c = c0c.replace('رائد كعكة', 'رائد كعكة')
c0c = c0c.replace('Raed Kaakeh', 'Raed Kaakeh')

with open(path_0c, 'w', encoding='utf-8') as f:
    f.write(c0c)
print("Updated js/sr-inline-0c7f8fde.js with Raed Kaakeh.")

# 3. Update index.html and ckb/index.html
for p_html in [os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'ckb', 'index.html')]:
    if os.path.exists(p_html):
        with open(p_html, 'r', encoding='utf-8') as f:
            h = f.read()
        h = h.replace('رائد كعكة', 'رائد كعكة')
        h = h.replace('Raed Kaakeh', 'Raed Kaakeh')
        with open(p_html, 'w', encoding='utf-8') as f:
            f.write(h)
        print(f"Updated {p_html} with Raed Kaakeh.")

# 4. Update test script test_hero_ai_flow_screenshot.py
test_script_path = os.path.join(ROOT, 'scripts', 'test_hero_ai_flow_screenshot.py')
if os.path.exists(test_script_path):
    with open(test_script_path, 'r', encoding='utf-8') as f:
        ts = f.read()
    ts = ts.replace('رائد كعكة', 'رائد كعكة')
    with open(test_script_path, 'w', encoding='utf-8') as f:
        f.write(ts)
    print("Updated test_hero_ai_flow_screenshot.py with Raed Kaakeh.")

print("All files updated successfully.")
