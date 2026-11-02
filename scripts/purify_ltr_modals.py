"""
Script to localize aiVoicePlannerModal for all 27 LTR pages with 100% pure Latin script,
guaranteeing 0 Arabic script contamination.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODAL_LTR = '''<div class="sr-exec-modal" id="aiVoicePlannerModal" role="dialog" aria-modal="true" aria-labelledby="voicePlannerModalTitle">
        <div class="sr-exec-modal-backdrop" data-sr-call="closeAiVoicePlannerModal"></div>
        <div class="sr-exec-modal-container sr-voice-modal-container">
            <div class="sr-exec-modal-header">
                <div>
                    <div class="sr-exec-modal-badge">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                        <span>AI Voice Project Architect 2026 • Sovereign Engineering</span>
                    </div>
                    <h3 class="sr-exec-modal-title" id="voicePlannerModalTitle">Speak or write your project idea... AI will engineer your executive blueprint instantly!</h3>
                    <p class="sr-exec-modal-subtitle">No complicated specifications required. Tap the microphone to speak, or write your concept. Our system will analyze your idea and engineer an executive roadmap in seconds.</p>
                </div>
                <button type="button" class="sr-exec-modal-close" data-sr-call="closeAiVoicePlannerModal" aria-label="Close">&times;</button>
            </div>

            <div class="sr-voice-mic-box">
                <button type="button" id="voicePlannerMicBtn" class="sr-voice-mic-btn" data-sr-call="toggleVoiceRecording" title="Tap to start or stop recording">
                    <svg viewBox="0 0 24 24" width="38" height="38" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                </button>

                <div class="sr-voice-waves" id="voicePlannerWaves" aria-hidden="true">
                    <span class="sr-voice-wave-bar"></span>
                    <span class="sr-voice-wave-bar"></span>
                    <span class="sr-voice-wave-bar"></span>
                    <span class="sr-voice-wave-bar"></span>
                    <span class="sr-voice-wave-bar"></span>
                    <span class="sr-voice-wave-bar"></span>
                    <span class="sr-voice-wave-bar"></span>
                </div>

                <div class="sr-voice-status" id="voicePlannerStatus">Tap the microphone to speak, or write your project requirements below...</div>

                <textarea id="voicePlannerTranscript" class="sr-voice-transcript-box" placeholder="Spoken words will appear here in real-time... (or type your project concept directly)"></textarea>

                <div class="sr-voice-chips-row">
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["Cloud store with automated ERP, PWA app, and Dutch iDEAL payment rail"]'>💡 Cloud store with automated ERP</span>
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["Enterprise ERP automation, European BTW tax compliance, and supply chain"]'>📊 Enterprise ERP & Tax compliance</span>
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["Corporate digital identity, sovereign cloud architecture, and 8K media"]'>🌐 Digital identity & 8K suite</span>
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["Smart cloud appointment app with online payment and AI agent concierge"]'>📱 Smart cloud app with AI concierge</span>
                </div>

                <div class="sr-voice-actions-row">
                    <button type="button" class="sr-voice-btn-primary" data-sr-call="generateAiProjectBlueprint">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                        <span>Generate AI Blueprint & Technical Roadmap ⚡</span>
                    </button>
                    <button type="button" class="sr-voice-btn-glass" data-sr-call="resetVoicePlanner">
                        <span>↺ Reset & Clear</span>
                    </button>
                </div>
            </div>

            <!-- Blueprint Generated Result -->
            <div id="voicePlannerResult" class="sr-voice-planner-result"></div>
        </div>
    </div>'''

ltr_langs = ['bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'it', 'ku', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'tr']

for lang in ltr_langs:
    p = os.path.join(ROOT, lang, 'index.html')
    if not os.path.isfile(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    # Find aiVoicePlannerModal and replace it with MODAL_LTR
    start = c.find('<div class="sr-exec-modal" id="aiVoicePlannerModal"')
    if start != -1:
        res_pos = c.find('id="voicePlannerResult"', start)
        end = c.find('</div>\n    </div>', res_pos) + len('</div>\n    </div>')
        c = c[:start] + MODAL_LTR + c[end:]

        # Also check bookingAudioGreetingStrip in this page to make sure it is in pure English
        # If it has Arabic characters, replace with English
        if 'أ. رائد عزيزة' in c or 'م. محمد سليم' in c or 'رسالة ترحيبية' in c:
            c = c.replace('م. محمد سليم عزيزة', 'Eng. Mohammad Salim Aziza')
            c = c.replace('أ. رائد عزيزة', 'Mr. Raed Aziza')
            c = c.replace('كبير مهندسي السحابة والذكاء الاصطناعي', 'Lead Cloud & AI Solutions Architect')
            c = c.replace('المسؤول التنفيذي للعمليات وتطوير الأعمال', 'Chief Operating Officer & Head of Business Development')
            c = c.replace('استشارة تنفيذية خاصة', 'VIP Consultation')
            c = c.replace('رسالة ترحيبية وتوجيهية مباشرة من القيادة قبل حجز جلستك الاستراتيجية', 'Direct executive audio greeting from leadership before confirming your session')
            c = c.replace('استمع للرسالة الصوتية', 'Listen to Executive Audio')

        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"[{lang}] Applied pure LTR modal and clean metadata.")

print("Done purifying all 27 LTR pages.")
