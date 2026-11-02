"""
Script to refine toggleBlueprintAudioSynthesis and add A4 button to the blueprint card
in js/sr-inline-13eaa28e.js
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, 'js', 'sr-inline-13eaa28e.js')

with open(TARGET, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add preview button before checkout button in blueprint card
old_btn = '<button type="button" class="sr-btn-checkout"'
new_btn = '<button type="button" class="sr-btn-action sr-btn-preview-a4" data-sr-call="openBlueprintPreviewModal"><span>👁️ معاينة التقرير الرسمي A4 والختم السيادي</span></button>\\n                            <button type="button" class="sr-btn-checkout"'

if old_btn in c and 'sr-btn-preview-a4' not in c:
    c = c.replace(old_btn, new_btn)
    print("Added sr-btn-preview-a4 button to blueprint card")
else:
    print("sr-btn-preview-a4 already in blueprint card or old_btn not found")

# 2. Refine speech synthesis utterance building
old_speech_build = 'speechText=`${founderLead} قمت بتحليل فكرتك وهندسة خطة العمل التنفيذية التالية: ${n}. تشمل المنظومة الموصى بها: ${t}. ونتوقع عائداً استثمارياً نوعياً: ${o}. سننفذ المشروع عبر مراحل هندسية مدروسة مع ضمان سيادي متكامل. يمكنك تحميل الخطة كملف بي دي إف أو حجز جلسة تنفيذ فورية معنا.`;const i=new SpeechSynthesisUtterance(speechText);currentSpeechUtterance=i,i.lang="ar-SA",i.rate=.95,i.pitch=.88;'

new_speech_build = '''const docLang = (document.documentElement.getAttribute("lang") || "ar").toLowerCase();
let speechText = "";
let langCode = "ar-SA";
let targetLangPrefix = "ar";

if (docLang.startsWith("nl")) {
    targetLangPrefix = "nl";
    langCode = "nl-NL";
    speechText = `${founderLead} Ik heb uw projectidee geanalyseerd en het volgende blauwdruk opgesteld: ${n}. Aanbevolen architectuur: ${t}. Verwacht rendement: ${o}. Wij implementeren dit via soevereine engineeringfasen. U kunt het rapport als PDF downloaden of direct een executive consult boeken.`;
} else if (docLang.startsWith("de")) {
    targetLangPrefix = "de";
    langCode = "de-DE";
    speechText = `${founderLead} Ich habe Ihre Projektidee analysiert und den folgenden Entwurf erstellt: ${n}. Empfohlene Architektur: ${t}. Erwarteter ROI: ${o}. Wir setzen dies mit vollständiger Datensouveränität um. Sie können den Bericht als PDF herunterladen oder eine Beratung buchen.`;
} else if (docLang.startsWith("en") || (!docLang.startsWith("ar") && !docLang.startsWith("ckb"))) {
    targetLangPrefix = "en";
    langCode = "en-US";
    speechText = `${founderLead} I have analyzed your project concept and engineered the following executive blueprint: ${n}. Recommended Architecture: ${t}. Expected ROI impact: ${o}. We deliver this with full sovereign engineering and enterprise SLA. You can download the PDF blueprint or book an executive consultation.`;
} else {
    targetLangPrefix = "ar";
    langCode = "ar-SA";
    speechText = `${founderLead} قمت بتحليل فكرتك وهندسة خطة العمل التنفيذية التالية: ${n}. تشمل المنظومة الموصى بها: ${t}. ونتوقع عائداً استثمارياً نوعياً: ${o}. سننفذ المشروع عبر مراحل هندسية مدروسة مع ضمان سيادي متكامل. يمكنك تحميل الخطة كملف بي دي إف أو حجز جلسة تنفيذ فورية معنا.`;
}

const i = new SpeechSynthesisUtterance(speechText);
currentSpeechUtterance = i;
i.lang = langCode;
i.rate = 0.95;
i.pitch = 0.88;'''

if old_speech_build in c:
    c = c.replace(old_speech_build, new_speech_build)
    print("Replaced speechText with multilingual generator in toggleBlueprintAudioSynthesis")
else:
    print("Notice: old_speech_build not matched verbatim")

# 3. Refine voice matching to use targetLangPrefix
old_voice_match = 'let s=allVoices.find(e=>{const n=(e.name||"").toLowerCase(),t=(e.lang||"").toLowerCase();return t.startsWith("ar")&&malePreferred.some(e=>n.includes(e))&&!femaleKeywords.some(e=>n.includes(e))});s||(s=allVoices.find(e=>{const n=(e.name||"").toLowerCase(),t=(e.lang||"").toLowerCase();return t.startsWith("ar")&&!femaleKeywords.some(e=>n.includes(e))})),s||(s=allVoices.find(e=>(e.lang||"").toLowerCase().startsWith("ar")))'
new_voice_match = 'let s=allVoices.find(e=>{const n=(e.name||"").toLowerCase(),t=(e.lang||"").toLowerCase();return t.startsWith(targetLangPrefix)&&malePreferred.some(e=>n.includes(e))&&!femaleKeywords.some(e=>n.includes(e))});s||(s=allVoices.find(e=>{const n=(e.name||"").toLowerCase(),t=(e.lang||"").toLowerCase();return t.startsWith(targetLangPrefix)&&!femaleKeywords.some(e=>n.includes(e))})),s||(s=allVoices.find(e=>(e.lang||"").toLowerCase().startsWith(targetLangPrefix)))'

if old_voice_match in c:
    c = c.replace(old_voice_match, new_voice_match)
    print("Updated voice matching to respect targetLangPrefix")
else:
    print("Notice: old_voice_match not found verbatim")

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(c)

print("Saved updated js/sr-inline-13eaa28e.js")
