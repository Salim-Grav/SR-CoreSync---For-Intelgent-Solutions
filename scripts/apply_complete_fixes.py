import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js_path = os.path.join(ROOT, 'js', 'sr-inline-13eaa28e.js')
css_path = os.path.join(ROOT, 'css', 'enterprise-suite.css')

# 1. Update css/enterprise-suite.css
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Fix first @media print
old_first_print = "@media print{body *{visibility:hidden !important;}.es-modal-overlay,.es-quote-modal,.es-quote-paper,.es-quote-paper *{visibility:visible !important;}"
new_first_print = "@media print{body *{visibility:hidden !important;}.es-modal-overlay,.es-quote-modal,.es-quote-paper,.es-quote-paper *,#srBlueprintPreviewModal,#srBlueprintPreviewModal *{visibility:visible !important;}"

if old_first_print in css:
    css = css.replace(old_first_print, new_first_print)
    print("Fixed first @media print block!")
else:
    print("Warning: old_first_print not found directly, checking regex")
    css = re.sub(r'@media print\{body \*\{visibility:hidden !important;\}\.es-modal-overlay[\s\S]*?\{visibility:visible !important;\}', new_first_print, css)

# Fix second @media print at the end of file
last_media_print_idx = css.rfind('@media print')
new_media_print_rule = """@media print {
    @page {
        size: A4 portrait;
        margin: 12mm 15mm;
    }
    *, *::before, *::after {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    html, body {
        background: #ffffff !important;
        color: #0f172a !important;
        overflow: visible !important;
        height: auto !important;
        min-height: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    /* Hide all page content except the A4 Blueprint Preview Modal */
    body > *:not(#srBlueprintPreviewModal) {
        display: none !important;
    }
    #aiVoicePlannerModal,
    .sr-exec-modal:not(#srBlueprintPreviewModal),
    .hero-cinematic,
    header,
    footer,
    nav,
    .floating-follow,
    .floating-actions,
    .es-floating-suite {
        display: none !important;
    }
    #srBlueprintPreviewModal {
        display: block !important;
        position: static !important;
        inset: auto !important;
        width: 100% !important;
        height: auto !important;
        min-height: 100% !important;
        background: #ffffff !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible !important;
        box-shadow: none !important;
        border: none !important;
        visibility: visible !important;
    }
    #srBlueprintPreviewModal,
    #srBlueprintPreviewModal * {
        visibility: visible !important;
    }
    .sr-a4-preview-wrapper {
        display: block !important;
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
        transform: none !important;
        visibility: visible !important;
    }
    .sr-a4-sheet {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        background: #ffffff !important;
        color: #0f172a !important;
        border-radius: 0 !important;
        overflow: visible !important;
        page-break-inside: avoid !important;
        visibility: visible !important;
    }
    .sr-a4-sheet * {
        visibility: visible !important;
    }
    .sr-a4-toolbar, 
    .sr-exec-modal-backdrop, 
    .sr-exec-modal-close,
    .sr-blueprint-actions,
    .sr-voice-waves,
    .sr-voice-status,
    .sr-blueprint-audio-controls {
        display: none !important;
    }
}
"""

if last_media_print_idx != -1:
    css = css[:last_media_print_idx] + new_media_print_rule
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Fixed second @media print block in css/enterprise-suite.css!")

# 2. Update js/sr-inline-13eaa28e.js
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Update startVoiceRecording with enhanced speech recognition & feedback
old_start_recording_pattern = r'function startVoiceRecording\(\)\{[\s\S]*?voiceRecognition\.start\(\)\}[\s\S]*?catch\(e\)\{[\s\S]*?stopVoiceRecording\(\)\}\}'

new_start_recording = """function startVoiceRecording() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    const btn = document.getElementById("voicePlannerMicBtn");
    const status = document.getElementById("voicePlannerStatus");
    const transcript = document.getElementById("voicePlannerTranscript");

    if (!SpeechRec) {
        if (status) status.innerHTML = "⚠️ المتصفح لا يدعم التسجيل الصوتي المباشر، يمكنك كتابة فكرتك في المربع أدناه وسيتولى الذكاء الاصطناعي هندستها فوراً!";
        if (transcript) transcript.focus();
        return;
    }

    try {
        if (voiceRecognition) {
            try { voiceRecognition.abort(); } catch(e) {}
            voiceRecognition = null;
        }
        voiceRecognition = new SpeechRec();
        voiceRecognition.continuous = true;
        voiceRecognition.interimResults = true;
        voiceRecognition.lang = document.documentElement.getAttribute("lang") || "ar-SA";

        voiceRecognition.onstart = function() {
            isVoiceRecording = true;
            if (btn) btn.classList.add("is-recording");
            if (status) status.innerHTML = "🔴 <strong>جاري الاستماع لصوتك الآن...</strong> تحدث بحرية عن فكرة مشروعك ومتطلباتك وسيقوم النظام بتفريغها لحظياً!";
            if (typeof LuxuryAudio !== "undefined") LuxuryAudio.play("tap");
        };

        voiceRecognition.onresult = function(e) {
            let text = "";
            for (let i = 0; i < e.results.length; i++) {
                text += e.results[i][0].transcript + " ";
            }
            if (transcript) transcript.value = text.trim();
        };

        voiceRecognition.onerror = function(e) {
            console.warn("Speech recognition notice:", e);
            isVoiceRecording = false;
            if (btn) btn.classList.remove("is-recording");
            if (status) {
                if (e.error === 'not-allowed') {
                    status.innerHTML = "⚠️ تم حظر إذن الميكروفون في المتصفح. يُرجى السماح بالمايك أو كتابة الفكرة مباشرة.";
                } else if (e.error === 'no-speech') {
                    status.innerHTML = "لم نسمع صوتاً. اضغط على المايك وتحدث بوضوح أو اكتب فكرتك مباشرة.";
                } else {
                    status.innerHTML = "اضغط على المايكروفون وتحدث أو اكتب فكرتك مباشرة في المربع أدناه.";
                }
            }
        };

        voiceRecognition.onend = function() {
            isVoiceRecording = false;
            if (btn) btn.classList.remove("is-recording");
            if (status && transcript && transcript.value.trim().length > 0) {
                status.innerHTML = "✓ تم تسجيل فكرتك بنجاح! اضغط على الزر الذهبي بالأسفل لتوليد خطة العمل فوراً.";
            }
        };

        voiceRecognition.start();
        if (status) status.innerHTML = "🎙️ جاري فتح الميكروفون والاتصال بمحرك الصوت...";
    } catch(err) {
        console.error("Speech recognition start error:", err);
        isVoiceRecording = false;
        if (btn) btn.classList.remove("is-recording");
        if (status) status.innerHTML = "⚠️ تعذر تشغيل المايكروفون. يمكنك كتابة فكرتك مباشرة وسيقوم النظام بهندستها.";
    }
}"""

js = re.sub(old_start_recording_pattern, new_start_recording, js)
print("Updated startVoiceRecording successfully!")

# Ensure exportBlueprintPdf has overflow reset
new_export_blueprint_pdf = """function exportBlueprintPdf(e) {
    if (typeof openBlueprintPreviewModal === "function") {
        openBlueprintPreviewModal();
    }
    const prevBodyOverflow = document.body.style.overflow;
    const prevHtmlOverflow = document.documentElement.style.overflow;
    document.body.style.overflow = "visible";
    document.documentElement.style.overflow = "visible";
    setTimeout(() => {
        window.print();
        setTimeout(() => {
            document.body.style.overflow = prevBodyOverflow;
            document.documentElement.style.overflow = prevHtmlOverflow;
        }, 800);
    }, 400);
}"""

js = re.sub(r'function exportBlueprintPdf\(e\)\{[\s\S]*?window\.print\(\);[\s\S]*?\}', new_export_blueprint_pdf, js)
print("Updated exportBlueprintPdf successfully!")

# Ensure global exports at the end of js/sr-inline-13eaa28e.js
global_exports = """
// =============================================================================
// S&R CoreSync - Global Window Bindings for Strict CSP & Delegated Events
// =============================================================================
window.toggleVoiceRecording = toggleVoiceRecording;
window.startVoiceRecording = startVoiceRecording;
window.stopVoiceRecording = stopVoiceRecording;
window.resetVoicePlanner = resetVoicePlanner;
window.generateAiProjectBlueprint = generateAiProjectBlueprint;
window.fillVoiceSample = fillVoiceSample;
window.exportBlueprintPdf = exportBlueprintPdf;
window.dispatchBlueprintToWhatsApp = dispatchBlueprintToWhatsApp;
window.dispatchBlueprintToTelegram = dispatchBlueprintToTelegram;
window.bookBlueprintConsultation = bookBlueprintConsultation;
window.openExecutiveCheckoutModal = openExecutiveCheckoutModal;
window.closeExecutiveCheckoutModal = closeExecutiveCheckoutModal;
window.toggleBlueprintAudioSynthesis = toggleBlueprintAudioSynthesis;
window.stopBlueprintAudioSynthesis = stopBlueprintAudioSynthesis;
window.downloadBlueprintArchitectureJson = downloadBlueprintArchitectureJson;
window.dispatchBlueprintToClientAndManagement = dispatchBlueprintToClientAndManagement;
"""

if 'window.toggleVoiceRecording = toggleVoiceRecording;' in js:
    # Replace existing global exports block
    js = re.sub(r'// =============================================================================\s*// S&R CoreSync - Global Window Bindings[\s\S]*', global_exports.strip(), js)
else:
    js += "\n" + global_exports.strip()

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Saved js/sr-inline-13eaa28e.js successfully!")
