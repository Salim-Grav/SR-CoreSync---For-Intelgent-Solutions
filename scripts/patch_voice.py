import os

p = 'js/sr-inline-13eaa28e.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace block 1
old_b1 = """    let s = targetVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        return malePreferred.some(m => n.includes(m.toLowerCase())) && !femaleKeywords.some(f => n.includes(f.toLowerCase()));
    });
    if (!s) {
        s = targetVoices.find(v => {
            const n = (v.name || "").toLowerCase();
            return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
        });
    }
    if (!s && targetVoices.length > 0) {
        s = targetVoices[0];
    }

    if (s) {
        i.voice = s;
        const voiceName = (s.name || "").toLowerCase();
        const isTrueMale = malePreferred.some(m => voiceName.includes(m.toLowerCase()));
        i.pitch = isTrueMale ? 0.82 : 0.50;
        i.rate = 0.90;
    } else {
        i.pitch = 0.50;
        i.rate = 0.90;
    }"""

new_b1 = """    const nonFemaleVoices = targetVoices.filter(v => {
        const n = (v.name || "").toLowerCase();
        return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
    });

    let s = nonFemaleVoices.find(v => {
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

old_b2 = """    let matchedVoice = targetVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        return malePreferred.some(m => n.includes(m.toLowerCase())) && !femaleKeywords.some(f => n.includes(f.toLowerCase()));
    });
    if (!matchedVoice) {
        matchedVoice = targetVoices.find(v => {
            const n = (v.name || "").toLowerCase();
            return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
        });
    }
    if (!matchedVoice && targetVoices.length > 0) {
        matchedVoice = targetVoices[0];
    }

    if (matchedVoice) {
        utt.voice = matchedVoice;
        const voiceName = (matchedVoice.name || "").toLowerCase();
        const isTrueMale = malePreferred.some(m => voiceName.includes(m.toLowerCase()));
        utt.pitch = isTrueMale ? 0.82 : 0.50;
        utt.rate = 0.90;
    } else {
        utt.pitch = 0.50;
        utt.rate = 0.90;
    }"""

new_b2 = """    const nonFemaleVoices = targetVoices.filter(v => {
        const n = (v.name || "").toLowerCase();
        return !femaleKeywords.some(f => n.includes(f.toLowerCase()));
    });

    let matchedVoice = nonFemaleVoices.find(v => {
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

text_norm = text.replace('\r\n', '\n')
old_b1_norm = old_b1.replace('\r\n', '\n')
new_b1_norm = new_b1.replace('\r\n', '\n')
old_b2_norm = old_b2.replace('\r\n', '\n')
new_b2_norm = new_b2.replace('\r\n', '\n')

print("b1 found:", old_b1_norm in text_norm)
print("b2 found:", old_b2_norm in text_norm)

text_norm = text_norm.replace(old_b1_norm, new_b1_norm)
text_norm = text_norm.replace(old_b2_norm, new_b2_norm)

with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text_norm)
print("Updated successfully!")
