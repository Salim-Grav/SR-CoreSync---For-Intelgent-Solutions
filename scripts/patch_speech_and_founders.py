# -*- coding: utf-8 -*-
"""
Patch speech synthesis, founder specialization (Salim vs Raed), and Arabic company name pronunciation ("شركة إس آند آر"):
1. js/sr-inline-13eaa28e.js
2. js/sr-agent-widget.js
"""
import io, re

def patch_inline_js():
    with io.open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update founder classification in generateAiProjectBlueprint
    # Find classification logic
    old_classif_needle = 'const e=o.toLowerCase();let i="منظومة سحابية وحلول متكاملة للأعمال 2026",s="التحول الرقمي وأتمتة الشركات",c="بنية سحابية فائقة السرعة مع لوحة تحكم ذكية",a="+42% توفير بالتكاليف التشغيلية و 3.8x سرعة في إنجاز العمليات";'
    new_classif = '''const e=o.toLowerCase();
let i="منظومة سحابية وحلول متكاملة للأعمال 2026",s="التحول الرقمي وأتمتة الشركات",c="بنية سحابية فائقة السرعة مع لوحة تحكم ذكية",a="+42% توفير بالتكاليف التشغيلية و 3.8x سرعة في إنجاز العمليات";
const isRaed=e.includes("erp")||e.includes("محاسب")||e.includes("ضريب")||e.includes("ضرائب")||e.includes("vat")||e.includes("btw")||e.includes("تشغيل")||e.includes("عمليات")||e.includes("إدار")||e.includes("ادارة")||e.includes("عقد")||e.includes("عقود")||e.includes("توسع")||e.includes("شركاء")||e.includes("مالي")||e.includes("تمويل")||e.includes("مخازن")||e.includes("امداد")||e.includes("سلاسل")||e.includes("سوشيال")||e.includes("8k")||e.includes("تسويق")||e.includes("هوية")||e.includes("براند")||e.includes("business")||e.includes("operation")||e.includes("finance")||e.includes("logistics")||e.includes("supply");
const founderName=isRaed?"أ. رائد عزيزة":"م. محمد سليم عزيزة";
const founderRole=isRaed?"المسؤول التنفيذي للعمليات وتطوير الأعمال":"كبير مهندسي السحابة والذكاء الاصطناعي";
const founderImg=isRaed?"./assets/founder-raed.webp":"./assets/founder-salim.webp";
const founderAlt=isRaed?"Mr. Raed Aziza - Chief Operating Officer":"Eng. Mohammad Salim Aziza - Chief Technology & AI Officer";
const founderBadge=isRaed?"🎙️ صوت الأستاذ رائد الرقمي • AI Executive Audio":"🎙️ صوت المهندس سليم الرقمي • AI Executive Audio";
const founderLead=isRaed?"أهلاً بك، معك الأستاذ رائد عزيزة، المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر.":"أهلاً بك، معك المهندس محمد سليم عزيزة، كبير مهندسي السحابة والذكاء الاصطناعي في شركة إس آند آر.";'''
    
    if old_classif_needle in code:
        code = code.replace(old_classif_needle, new_classif)
        print("Updated founder classification logic in generateAiProjectBlueprint")
    else:
        print("WARNING: old_classif_needle not found!")

    # 2. Update audio player HTML template inside generateAiProjectBlueprint
    old_player_regex = r'<div class="sr-blueprint-audio-player".*?<!-- ── Blueprint Instant Dispatch Buttons & Checkout ── -->'
    new_player_html = '''<div class="sr-blueprint-audio-player" id="blueprintAudioPlayer"
                             data-project-name="${encodeURIComponent(i)}"
                             data-sys-rec="${encodeURIComponent(c)}"
                             data-roi-value="${encodeURIComponent(a)}"
                             data-founder-type="${isRaed ? 'raed' : 'salim'}"
                             data-founder-lead="${encodeURIComponent(founderLead)}">
                            <div class="sr-blueprint-audio-info">
                                <div class="sr-blueprint-audio-avatar">
                                    <img src="${founderImg}" alt="${founderAlt}" class="sr-blueprint-audio-img" loading="lazy" decoding="async">
                                    <span class="sr-blueprint-audio-status-dot" id="audioSpeakingDot"></span>
                                </div>
                                <div class="sr-blueprint-audio-texts">
                                    <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                        <span class="sr-blueprint-audio-badge">${founderBadge}</span>
                                        <span style="font-size: 11px; color: #cbd5e1; font-weight: 600;">${founderRole}</span>
                                        <a href="https://www.linkedin.com/company/146883282/" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; background: rgba(10, 102, 194, 0.25); border: 1px solid rgba(96, 165, 250, 0.45); border-radius: 999px; color: #93c5fd; font-size: 11px; font-weight: 700; text-decoration: none; transition: all 0.2s ease;">
                                            <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76c-.95 0-1.72.77-1.72 1.72s.77 1.73 1.72 1.73a1.73 1.73 0 0 0 1.73-1.73c0-.95-.78-1.72-1.73-1.72m1.39 9.74v-8.37H5.07v8.37h2.78Z"/></svg>
                                            <span>LinkedIn</span>
                                        </a>
                                    </div>
                                    <div class="sr-blueprint-audio-title">الاستماع للملخص التنفيذي للخطة (${founderName})</div>
                                </div>
                            </div>
                            <div class="sr-blueprint-audio-controls">
                                <button type="button" class="sr-blueprint-audio-btn" id="blueprintPlayVoiceBtn" onclick="toggleBlueprintAudioSynthesis()">
                                    <span id="blueprintPlayVoiceIcon">▶️</span>
                                    <span id="blueprintPlayVoiceLabel">استمع للخطة بالصوت التنفيذي</span>
                                </button>
                                <div class="sr-blueprint-audio-waves" id="blueprintAudioWaves">
                                    <span class="sr-audio-bar"></span>
                                    <span class="sr-audio-bar"></span>
                                    <span class="sr-audio-bar"></span>
                                    <span class="sr-audio-bar"></span>
                                    <span class="sr-audio-bar"></span>
                                    <span class="sr-audio-bar"></span>
                                    <span class="sr-audio-bar"></span>
                                </div>
                            </div>
                        </div>

                        <!-- ── Blueprint Instant Dispatch Buttons & Checkout ── -->'''

    # Let's replace the audio player template
    p1 = code.find('<div class="sr-blueprint-audio-player"')
    p2 = code.find('<!-- ── Blueprint Instant Dispatch Buttons & Checkout ── -->')
    if p1 != -1 and p2 != -1:
        code = code[:p1] + new_player_html + code[p2 + len('<!-- ── Blueprint Instant Dispatch Buttons & Checkout ── -->'):]
        print("Updated audio player HTML template")
    else:
        print("WARNING: audio player HTML template boundaries not found!")

    # 3. Replace toggleBlueprintAudioSynthesis and dispatchBlueprintToWhatsApp
    old_speech_fn_start = code.find('function toggleBlueprintAudioSynthesis(){')
    old_speech_fn_end = code.find('function dispatchBlueprintToTelegram(){')
    
    new_speech_fns = '''function toggleBlueprintAudioSynthesis(){
    if(isBlueprintSpeaking) return void stopBlueprintAudioSynthesis();
    if(!("speechSynthesis" in window)) return void alert("عذراً، المتصفح الحالي لا يدعم التوليف الصوتي المباشر. يمكنك قراءة الخطة أو تنزيلها بصيغة PDF.");
    stopBlueprintAudioSynthesis();
    const e = document.getElementById("blueprintAudioPlayer"),
          n = e ? decodeURIComponent(e.getAttribute("data-project-name")||"") : "مشروعك الذكي",
          t = e ? decodeURIComponent(e.getAttribute("data-sys-rec")||"") : "البنية السحابية الموصى بها",
          o = e ? decodeURIComponent(e.getAttribute("data-roi-value")||"") : "عائد استثماري نوعي",
          founderLead = e ? decodeURIComponent(e.getAttribute("data-founder-lead")||"") : "أهلاً بك، معك المستشار التنفيذي في شركة إس آند آر.",
          speechText = `${founderLead} قمت بتحليل فكرتك وهندسة خطة العمل التنفيذية التالية: ${n}. تشمل المنظومة الموصى بها: ${t}. ونتوقع عائداً استثمارياً نوعياً: ${o}. سننفذ المشروع عبر مراحل هندسية مدروسة مع ضمان سيادي متكامل. يمكنك تحميل الخطة كملف بي دي إف أو حجز جلسة تنفيذ فورية معنا.`;
    
    const i = new SpeechSynthesisUtterance(speechText);
    currentSpeechUtterance = i;
    i.lang = "ar-SA";
    i.pitch = 0.88; // Deep masculine executive pitch
    i.rate = 0.95;  // Authoritative cadence

    const femaleKeywords = ["laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman"];
    const malePreferred = ["maged", "tarik", "naayf", "shakir", "zayd", "hamed", "bassam", "male"];
    const allVoices = (window.speechSynthesis && window.speechSynthesis.getVoices) ? window.speechSynthesis.getVoices() : [];

    let s = allVoices.find(v => {
        const name = (v.name || "").toLowerCase(), lang = (v.lang || "").toLowerCase();
        return lang.startsWith("ar") && malePreferred.some(m => name.includes(m)) && !femaleKeywords.some(f => name.includes(f));
    });
    if (!s) {
        s = allVoices.find(v => {
            const name = (v.name || "").toLowerCase(), lang = (v.lang || "").toLowerCase();
            return lang.startsWith("ar") && !femaleKeywords.some(f => name.includes(f));
        });
    }
    if (!s) {
        s = allVoices.find(v => (v.lang || "").toLowerCase().startsWith("ar"));
    }
    if (s) i.voice = s;

    const c = document.getElementById("blueprintPlayVoiceIcon"), a = document.getElementById("blueprintPlayVoiceLabel");
    i.onstart = function(){
        isBlueprintSpeaking = !0;
        e && e.classList.add("is-playing");
        c && (c.innerHTML = "⏸️");
        a && (a.textContent = "إيقاف الملخص الصوتي");
        "undefined" != typeof LuxuryAudio && LuxuryAudio.play("hover");
    };
    i.onend = function(){ stopBlueprintAudioSynthesis(); };
    i.onerror = function(err){ console.warn("Speech synthesis notice:", err); stopBlueprintAudioSynthesis(); };
    window.speechSynthesis.speak(i);
}

function dispatchBlueprintToWhatsApp(){
    const e = document.getElementById("blueprintAudioPlayer"),
          n = e ? decodeURIComponent(e.getAttribute("data-project-name")||"") : "مشروع ذكي",
          t = e ? decodeURIComponent(e.getAttribute("data-sys-rec")||"") : "بنية سحابية متقدمة",
          o = e ? decodeURIComponent(e.getAttribute("data-roi-value")||"") : "+42% توفير تشغيلي",
          isRaed = e ? (e.getAttribute("data-founder-type") === "raed") : false,
          targetFounder = isRaed ? "الأستاذ رائد عزيزة (مسؤول العمليات والـ ERP)" : "المهندس محمد سليم عزيزة (المسؤول التقني والسحابي)",
          msg = `مرحباً فريق شركة إس آند آر، قمت بهندسة خطة مشروعي بإشراف ${targetFounder}:\\n\\n📋 *المشروع:* ${n}\\n⚙️ *المنظومة المقترحة:* ${t}\\n📈 *العائد الاستثماري:* ${o}\\n\\nأرغب باعتماد الخطة وحجز جلسة تنفيذ فورية.`;
    window.open(`https://wa.me/31618111116?text=${encodeURIComponent(msg)}`, "_blank");
    "undefined" != typeof LuxuryAudio && LuxuryAudio.play("success");
}
'''
    if old_speech_fn_start != -1 and old_speech_fn_end != -1:
        code = code[:old_speech_fn_start] + new_speech_fns + code[old_speech_fn_end:]
        print("Updated speech synthesis and WhatsApp dispatch in 13eaa28e")
    else:
        print("WARNING: speech function boundaries not found!")

    with io.open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8', newline='\n') as f:
        f.write(code)
    print("Saved js/sr-inline-13eaa28e.js")

def patch_agent_widget_js():
    with io.open('js/sr-agent-widget.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # In speakText:
    old_tts_start = code.find('function speakText(rawText, ttsButton) {')
    old_tts_end = code.find('// Attach TTS to first welcome message')
    
    new_tts = '''function speakText(rawText, ttsButton) {
            if (!('speechSynthesis' in window)) return;

            if (window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
                document.querySelectorAll('.sr-agent-tts-btn').forEach(b => b.classList.remove('sr-speaking'));
                return;
            }

            let cleanText = rawText
                .replace(/<[^>]*>/g, ' ')
                .replace(/\\*\\*(.*?)\\*\\*/g, '$1')
                .replace(/\\*(.*?)\\*/g, '$1')
                .replace(/`(.*?)`/g, '$1')
                .replace(/#{1,6}\\s/g, '')
                .replace(/https?:\\/\\/\\S+/g, '')
                .replace(/S&R\\s*CoreSync/gi, 'شركة إس آند آر')
                .replace(/S&R/gi, 'إس آند آر')
                .trim();

            if (!cleanText) return;

            const utterance = new SpeechSynthesisUtterance(cleanText);
            const isEnglish = /^[A-Za-z0-9\\s.,!?\\'\"()-]+$/.test(cleanText.slice(0, 50));
            utterance.lang = isEnglish ? 'en-US' : 'ar-SA';
            utterance.pitch = 0.88; // Deep masculine tone
            utterance.rate = 0.95;  // Authoritative executive cadence

            const femaleKeywords = ["laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman"];
            const malePreferred = ["maged", "tarik", "naayf", "shakir", "zayd", "hamed", "bassam", "male"];
            const allVoices = (window.speechSynthesis && window.speechSynthesis.getVoices) ? window.speechSynthesis.getVoices() : [];

            let maleVoice = allVoices.find(v => {
                const name = (v.name || "").toLowerCase(), lang = (v.lang || "").toLowerCase();
                if (!lang.startsWith(isEnglish ? 'en' : 'ar')) return false;
                if (femaleKeywords.some(f => name.includes(f))) return false;
                return isEnglish ? true : malePreferred.some(m => name.includes(m));
            });
            if (!maleVoice) {
                maleVoice = allVoices.find(v => {
                    const name = (v.name || "").toLowerCase(), lang = (v.lang || "").toLowerCase();
                    return lang.startsWith(isEnglish ? 'en' : 'ar') && !femaleKeywords.some(f => name.includes(f));
                });
            }
            if (maleVoice) utterance.voice = maleVoice;

            if (ttsButton) ttsButton.classList.add('sr-speaking');

            utterance.onend = () => {
                if (ttsButton) ttsButton.classList.remove('sr-speaking');
            };
            utterance.onerror = () => {
                if (ttsButton) ttsButton.classList.remove('sr-speaking');
            };

            window.speechSynthesis.speak(utterance);
        }

        '''

    if old_tts_start != -1 and old_tts_end != -1:
        code = code[:old_tts_start] + new_tts + code[old_tts_end:]
        print("Updated speakText in js/sr-agent-widget.js")
        with io.open('js/sr-agent-widget.js', 'w', encoding='utf-8', newline='\n') as f:
            f.write(code)
        print("Saved js/sr-agent-widget.js")
    else:
        print("WARNING: speakText boundaries not found in js/sr-agent-widget.js!")

if __name__ == '__main__':
    patch_inline_js()
    patch_agent_widget_js()
