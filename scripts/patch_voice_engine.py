import sys

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect the voice selection block in both toggleBlueprintAudioSynthesis and playBookingAudioGreeting
old_voice_logic = """    let s = nonFemaleVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        return malePreferred.some(m => n.includes(m.toLowerCase()));
    });
    if (!s && nonFemaleVoices.length > 0) {
        s = nonFemaleVoices[0];
    }

    if (s) {
        i.voice = s;
        i.pitch = 0.85;
        i.rate = 0.92;
    } else {
        // Absolutely NEVER force or fallback to a female voice
        i.voice = null;
        i.pitch = 0.78;
        i.rate = 0.92;
    }"""

new_voice_logic = """    // Priority 1: Authentic Syrian & Levantine male voice (e.g., Bassel in Edge/Windows)
    const syrianLevantineMale = ["bassel", "باسل", "syria", "سوريا", "shakir", "شاكر", "hamed", "حامد", "naayf", "نايف", "maged", "ماجد"];
    let s = targetVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        return syrianLevantineMale.some(m => n.includes(m.toLowerCase()));
    });

    if (s) {
        // Authentic verified male voice found
        i.voice = s;
        i.pitch = 0.92;
        i.rate = 0.94;
    } else {
        // If only Google عربي (which is female by default in Chrome) or general voice is available:
        // Lower pitch drastically to 0.62 to convert female formant into a deep masculine executive timbre!
        const nonExplicitFemale = targetVoices.find(v => {
            const n = (v.name || "").toLowerCase();
            return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
        });
        if (nonExplicitFemale) {
            i.voice = nonExplicitFemale;
            i.pitch = 0.62; // Masculine executive tone
            i.rate = 0.90;
        } else {
            i.voice = null;
            i.pitch = 0.60;
            i.rate = 0.90;
        }
    }"""

if old_voice_logic in code:
    code = code.replace(old_voice_logic, new_voice_logic, 1)
    print("SUCCESS: Patched toggleBlueprintAudioSynthesis voice engine!")
else:
    print("WARNING: old_voice_logic not found in toggleBlueprintAudioSynthesis")

old_booking_voice_logic = """    let matchedVoice = nonFemaleVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        return malePreferred.some(m => n.includes(m.toLowerCase()));
    });
    if (!matchedVoice && nonFemaleVoices.length > 0) {
        matchedVoice = nonFemaleVoices[0];
    }

    if (matchedVoice) {
        utt.voice = matchedVoice;
        utt.pitch = 0.85;
        utt.rate = 0.92;
    } else {
        // Absolutely NEVER force or fallback to a female voice
        utt.voice = null;
        utt.pitch = 0.78;
        utt.rate = 0.92;
    }"""

new_booking_voice_logic = """    const syrianLevantineMale = ["bassel", "باسل", "syria", "سوريا", "shakir", "شاكر", "hamed", "حامد", "naayf", "نايف", "maged", "ماجد"];
    let matchedVoice = targetVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        return syrianLevantineMale.some(m => n.includes(m.toLowerCase()));
    });

    if (matchedVoice) {
        utt.voice = matchedVoice;
        utt.pitch = 0.92;
        utt.rate = 0.94;
    } else {
        const nonExplicitFemale = targetVoices.find(v => {
            const n = (v.name || "").toLowerCase();
            return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
        });
        if (nonExplicitFemale) {
            utt.voice = nonExplicitFemale;
            utt.pitch = 0.62;
            utt.rate = 0.90;
        } else {
            utt.voice = null;
            utt.pitch = 0.60;
            utt.rate = 0.90;
        }
    }"""

if old_booking_voice_logic in code:
    code = code.replace(old_booking_voice_logic, new_booking_voice_logic, 1)
    print("SUCCESS: Patched playBookingAudioGreeting voice engine!")
else:
    print("WARNING: old_booking_voice_logic not found")

with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
    code = f.write(code)

print("File updated successfully.")
