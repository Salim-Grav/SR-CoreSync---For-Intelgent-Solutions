# -*- coding: utf-8 -*-
"""
S&R CoreSync - Deploy Milestone 36:
1. Enterprise Omnichannel Social Media & 8K Visual Authority Paid Service
2. AI Voice Project Architect & Roadmap Blueprint Modal
"""
import os
import re

CSS_VOICE_AND_SOCIAL = """
/* ==========================================================================
   S&R CORESYNC - MILESTONE 36: VOICE PLANNER & 8K SOCIAL PAID SERVICE
   ========================================================================== */
.exec-stage-btn-voice-pulse {
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.32) 0%, rgba(2, 7, 5, 0.95) 100%) !important;
    border: 1px solid #c5a880 !important;
    color: #f5e5c9 !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 0 20px rgba(197, 168, 128, 0.25) !important;
    animation: voiceBtnPulse 3s infinite alternate ease-in-out !important;
}

@keyframes voiceBtnPulse {
    0% { box-shadow: 0 0 12px rgba(197, 168, 128, 0.25); border-color: rgba(197, 168, 128, 0.5); }
    100% { box-shadow: 0 0 26px rgba(197, 168, 128, 0.7); border-color: #f3dfba; }
}

.sr-voice-modal-container {
    max-width: 900px !important;
    width: 95% !important;
    background: radial-gradient(circle at 50% 0%, rgba(32, 25, 17, 0.98) 0%, rgba(2, 7, 5, 0.99) 100%) !important;
    border: 1px solid rgba(197, 168, 128, 0.38) !important;
    border-radius: 22px !important;
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.9), 0 0 45px rgba(197, 168, 128, 0.2) !important;
    padding: 32px !important;
    max-height: 90vh !important;
    overflow-y: auto !important;
    color: #f5f5f5 !important;
    position: relative !important;
}

.sr-voice-mic-box {
    text-align: center !important;
    margin: 22px 0 16px !important;
    padding: 24px 20px !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(197, 168, 128, 0.2) !important;
    border-radius: 16px !important;
    position: relative !important;
}

.sr-voice-mic-btn {
    width: 92px !important;
    height: 92px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #c5a880 0%, #8c7350 100%) !important;
    border: 3px solid #f3dfba !important;
    color: #020705 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    box-shadow: 0 0 35px rgba(197, 168, 128, 0.5) !important;
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.sr-voice-mic-btn:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 0 50px rgba(197, 168, 128, 0.85) !important;
}

.sr-voice-mic-btn.is-recording {
    background: linear-gradient(135deg, #e53935 0%, #b71c1c 100%) !important;
    border-color: #ff8a80 !important;
    color: #ffffff !important;
    animation: micRecordingPulse 1.2s infinite ease-in-out !important;
}

@keyframes micRecordingPulse {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(229, 57, 53, 0.5); }
    50% { transform: scale(1.12); box-shadow: 0 0 45px rgba(229, 57, 53, 0.95); }
    100% { transform: scale(1); box-shadow: 0 0 15px rgba(229, 57, 53, 0.5); }
}

.sr-voice-waves {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    height: 38px !important;
    margin: 16px auto !important;
}

.sr-voice-wave-bar {
    width: 5px !important;
    height: 8px !important;
    background: #c5a880 !important;
    border-radius: 3px !important;
    transition: height 0.15s ease !important;
}

.sr-voice-mic-btn.is-recording ~ .sr-voice-waves .sr-voice-wave-bar {
    animation: waveBarDance 0.8s infinite ease-in-out alternate !important;
}

.sr-voice-waves .sr-voice-wave-bar:nth-child(1) { animation-delay: 0.1s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(2) { animation-delay: 0.25s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(3) { animation-delay: 0.4s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(4) { animation-delay: 0.15s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(5) { animation-delay: 0.3s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(6) { animation-delay: 0.45s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(7) { animation-delay: 0.2s !important; }

@keyframes waveBarDance {
    0% { height: 6px; }
    100% { height: 34px; background: #f3dfba; }
}

.sr-voice-status {
    font-size: 14.5px !important;
    font-weight: 600 !important;
    color: #e2d2bb !important;
    margin: 8px 0 12px !important;
}

.sr-voice-transcript-box {
    width: 100% !important;
    min-height: 85px !important;
    background: rgba(0, 0, 0, 0.45) !important;
    border: 1px solid rgba(197, 168, 128, 0.28) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    color: #ffffff !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    box-sizing: border-box !important;
    outline: none !important;
    transition: all 0.25s ease !important;
}

.sr-voice-transcript-box:focus {
    border-color: #c5a880 !important;
    box-shadow: 0 0 18px rgba(197, 168, 128, 0.35) !important;
}

.sr-voice-chips-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    margin: 14px 0 !important;
    justify-content: center !important;
}

.sr-voice-chip {
    background: rgba(197, 168, 128, 0.08) !important;
    border: 1px solid rgba(197, 168, 128, 0.22) !important;
    border-radius: 999px !important;
    padding: 6px 14px !important;
    color: #e0d0b8 !important;
    font-size: 13px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
}

.sr-voice-chip:hover {
    background: rgba(197, 168, 128, 0.24) !important;
    color: #ffffff !important;
    border-color: #c5a880 !important;
    transform: translateY(-2px) !important;
}

.sr-voice-actions-row {
    display: flex !important;
    gap: 12px !important;
    justify-content: center !important;
    flex-wrap: wrap !important;
    margin-top: 14px !important;
}

.sr-voice-btn-primary {
    background: linear-gradient(135deg, #c5a880 0%, #997b53 100%) !important;
    color: #020705 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.25s ease !important;
}

.sr-voice-btn-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(197, 168, 128, 0.45) !important;
}

.sr-voice-btn-glass {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(197, 168, 128, 0.3) !important;
    color: #f3dfba !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-size: 14px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    transition: all 0.25s ease !important;
}

.sr-voice-btn-glass:hover {
    background: rgba(197, 168, 128, 0.15) !important;
    color: #ffffff !important;
}

/* Blueprint Result Card */
.sr-blueprint-card {
    background: rgba(8, 12, 10, 0.95) !important;
    border: 1px solid rgba(197, 168, 128, 0.4) !important;
    border-radius: 18px !important;
    padding: 26px !important;
    margin-top: 24px !important;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.7) !important;
    animation: blueprintReveal 0.4s ease-out !important;
}

@keyframes blueprintReveal {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

.sr-blueprint-header {
    border-bottom: 1px solid rgba(197, 168, 128, 0.22) !important;
    padding-bottom: 16px !important;
    margin-bottom: 20px !important;
}

.sr-blueprint-title {
    color: #f3dfba !important;
    font-size: 23px !important;
    font-weight: 700 !important;
    margin: 8px 0 4px !important;
}

.sr-blueprint-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 4px 14px !important;
    background: rgba(197, 168, 128, 0.16) !important;
    border: 1px solid rgba(197, 168, 128, 0.4) !important;
    border-radius: 999px !important;
    color: #c5a880 !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
}

.sr-blueprint-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)) !important;
    gap: 16px !important;
    margin-bottom: 20px !important;
}

.sr-blueprint-box {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.sr-blueprint-box-title {
    font-size: 14.5px !important;
    color: #c5a880 !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}

.sr-blueprint-box-desc {
    font-size: 13.5px !important;
    line-height: 1.6 !important;
    color: #e0e0e0 !important;
}

.sr-roadmap-steps {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    margin: 18px 0 !important;
}

.sr-roadmap-step {
    display: flex !important;
    align-items: center !important;
    gap: 14px !important;
    padding: 12px 16px !important;
    background: rgba(197, 168, 128, 0.06) !important;
    border-left: 3px solid #c5a880 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}

[dir="rtl"] .sr-roadmap-step {
    border-left: none !important;
    border-right: 3px solid #c5a880 !important;
}

.sr-roadmap-step-num {
    background: #c5a880 !important;
    color: #020705 !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    width: 24px !important;
    height: 24px !important;
    border-radius: 50% !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.sr-blueprint-actions {
    display: flex !important;
    gap: 12px !important;
    flex-wrap: wrap !important;
    margin-top: 20px !important;
    padding-top: 18px !important;
    border-top: 1px solid rgba(197, 168, 128, 0.22) !important;
}
"""

MODAL_HTML = """
    <!-- ======================================================================= -->
    <!-- 10. نافذة مهندس المشاريع الصوتي الذكي (AI Voice Project Architect Modal) -->
    <!-- ======================================================================= -->
    <div class="sr-exec-modal" id="aiVoicePlannerModal" role="dialog" aria-modal="true" aria-labelledby="voicePlannerModalTitle">
        <div class="sr-exec-modal-backdrop" data-sr-call="closeAiVoicePlannerModal"></div>
        <div class="sr-exec-modal-container sr-voice-modal-container">
            <div class="sr-exec-modal-header">
                <div>
                    <div class="sr-exec-modal-badge">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                        <span>محرك التخطيط الصوتي الذكي للمشاريع 2026 • AI Voice Project Architect</span>
                    </div>
                    <h3 class="sr-exec-modal-title" id="voicePlannerModalTitle">تحدث بفكرة مشروعك... وسيقوم الذكاء الاصطناعي ببناء خطة عملك فوراً!</h3>
                    <p class="sr-exec-modal-subtitle">لا داعي لكتابة ملفات معقدة. اضغط على المايك وتحدث بعفوية بأي لغة، وسيقوم نظامنا بتحليل فكرتك وهندسة خطة عمل رقمية وخارطة طريق تقنية وتنفيذية في ثوانٍ.</p>
                </div>
                <button type="button" class="sr-exec-modal-close" data-sr-call="closeAiVoicePlannerModal" aria-label="إغلاق">&times;</button>
            </div>

            <div class="sr-voice-mic-box">
                <button type="button" id="voicePlannerMicBtn" class="sr-voice-mic-btn" data-sr-call="toggleVoiceRecording" title="اضغط لبدء التحدث أو إيقافه">
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

                <div class="sr-voice-status" id="voicePlannerStatus">اضغط على المايكروفون وتحدث بفكرة أو متطلبات مشروعك...</div>

                <textarea id="voicePlannerTranscript" class="sr-voice-transcript-box" placeholder="الكلمات المنطوقة ستظهر هنا لحظياً أثناء حديثك... (أو يمكنك كتابة فكرتك هنا مباشرة)"></textarea>

                <div class="sr-voice-chips-row">
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["متجر سحابي أوروبي متكامل مع تطبيق PWA وربط محاسبي أوتوماتيكي ومخازن"]'>💡 متجر وتطبيق مع ربط محاسبي</span>
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["أتمتة العمليات ونظام ERP كامل وربط الضرائب والفواتير لشركة استيراد وتصدير"]'>📊 أتمتة ERP لشركة استيراد</span>
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["تأسيس شركة تقنية جديدة مع بناء قنوات السوشيال ميديا وحزمة الهوية 8K كاملة"]'>🌐 تأسيس شركة وهوية سوشيال 8K</span>
                    <span class="sr-voice-chip" data-sr-call="fillVoiceSample" data-sr-args='["تطبيق سحابي ذكي للعيادات وحجز المواعيد مع دفع إلكتروني وأتمتة AI"]'>📱 تطبيق ذكي لحجز المواعيد</span>
                </div>

                <div class="sr-voice-actions-row">
                    <button type="button" class="sr-voice-btn-primary" data-sr-call="generateAiProjectBlueprint">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                        <span>توليد خطة العمل وخارطة الطريق بالذكاء الاصطناعي ⚡</span>
                    </button>
                    <button type="button" class="sr-voice-btn-glass" data-sr-call="resetVoicePlanner">
                        <span>↺ مسح وإعادة</span>
                    </button>
                </div>
            </div>

            <!-- Blueprint Generated Result -->
            <div id="voicePlannerResult" style="display: none;"></div>
        </div>
    </div>
"""

JS_VOICE_PLANNER = """
        // =======================================================================
        // محرك التخطيط الصوتي الذكي للمشاريع (AI Voice Project Architect Engine)
        // =======================================================================
        let voiceRecognition = null;
        let isVoiceRecording = false;

        function openAiVoicePlannerModal() {
            const modal = document.getElementById('aiVoicePlannerModal');
            if (!modal) return;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            if (typeof LuxuryAudio !== 'undefined') LuxuryAudio.play('open');
        }

        function closeAiVoicePlannerModal() {
            const modal = document.getElementById('aiVoicePlannerModal');
            if (modal && modal.classList.contains('active')) {
                stopVoiceRecording();
                modal.classList.remove('active');
                document.body.style.overflow = '';
                if (typeof LuxuryAudio !== 'undefined') LuxuryAudio.play('close');
            }
        }

        function toggleVoiceRecording() {
            if (isVoiceRecording) {
                stopVoiceRecording();
            } else {
                startVoiceRecording();
            }
        }

        function startVoiceRecording() {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            const btn = document.getElementById('voicePlannerMicBtn');
            const status = document.getElementById('voicePlannerStatus');
            const transcriptBox = document.getElementById('voicePlannerTranscript');

            if (!SpeechRec) {
                if (status) status.innerHTML = '⚠️ المتصفح لا يدعم التسجيل الصوتي المباشر، يمكنك كتابة فكرتك في المربع أدناه!';
                if (transcriptBox) transcriptBox.focus();
                return;
            }

            try {
                voiceRecognition = new SpeechRec();
                voiceRecognition.continuous = true;
                voiceRecognition.interimResults = true;
                voiceRecognition.lang = document.documentElement.getAttribute('lang') || 'ar-SA';

                voiceRecognition.onstart = function() {
                    isVoiceRecording = true;
                    if (btn) btn.classList.add('is-recording');
                    if (status) status.innerHTML = '🔴 جاري الاستماع... تحدث بحرية عن فكرة مشروعك ومتطلباتك الآن!';
                };

                voiceRecognition.onresult = function(event) {
                    let fullText = '';
                    for (let i = 0; i < event.results.length; i++) {
                        fullText += event.results[i][0].transcript + ' ';
                    }
                    if (transcriptBox) transcriptBox.value = fullText.trim();
                };

                voiceRecognition.onerror = function(err) {
                    console.warn('Speech recognition notice:', err);
                    stopVoiceRecording();
                    if (status) status.innerHTML = 'اضغط على المايكروفون للتحدث أو اكتب فكرتك مباشرة.';
                };

                voiceRecognition.onend = function() {
                    stopVoiceRecording();
                };

                voiceRecognition.start();
            } catch (e) {
                console.error(e);
                stopVoiceRecording();
            }
        }

        function stopVoiceRecording() {
            isVoiceRecording = false;
            const btn = document.getElementById('voicePlannerMicBtn');
            const status = document.getElementById('voicePlannerStatus');
            if (btn) btn.classList.remove('is-recording');
            if (status) status.innerHTML = '✓ تم تسجيل الفكرة. انقر على الزر الذهبي أدناه لتوليد خطة العمل!';
            if (voiceRecognition) {
                try { voiceRecognition.stop(); } catch (e) {}
                voiceRecognition = null;
            }
        }

        function fillVoiceSample(text) {
            const transcriptBox = document.getElementById('voicePlannerTranscript');
            if (transcriptBox) {
                transcriptBox.value = text;
                generateAiProjectBlueprint();
            }
        }

        function resetVoicePlanner() {
            stopVoiceRecording();
            const transcriptBox = document.getElementById('voicePlannerTranscript');
            const resultBox = document.getElementById('voicePlannerResult');
            const status = document.getElementById('voicePlannerStatus');
            if (transcriptBox) transcriptBox.value = '';
            if (resultBox) {
                resultBox.innerHTML = '';
                resultBox.style.display = 'none';
            }
            if (status) status.innerHTML = 'اضغط على المايكروفون وتحدث بفكرة أو متطلبات مشروعك...';
        }

        function generateAiProjectBlueprint() {
            const transcriptBox = document.getElementById('voicePlannerTranscript');
            const resultBox = document.getElementById('voicePlannerResult');
            const status = document.getElementById('voicePlannerStatus');

            const text = (transcriptBox ? transcriptBox.value.trim() : '');
            if (!text || text.length < 5) {
                if (status) status.innerHTML = '⚠️ الرجاء التحدث بصوتك أو كتابة نبذة بسيطة عن فكرتك أولاً لتوليد الخطة!';
                if (transcriptBox) transcriptBox.focus();
                return;
            }

            if (status) status.innerHTML = '⚡ جاري المعالجة وهندسة خطة العمل التنفيذية بواسطة الذكاء الاصطناعي...';

            setTimeout(() => {
                // Determine Industry & Architecture tailored to user text
                const t = text.toLowerCase();
                let projectName = 'منظومة سحابية وحلول متكاملة للأعمال 2026';
                let industry = 'التحول الرقمي وأتمتة الشركات';
                let sysRec = 'بنية سحابية فائقة السرعة مع لوحة تحكم ذكية';
                let roiValue = '+42% توفير بالتكاليف التشغيلية و 3.8x سرعة في إنجاز العمليات';
                let addSocial = true;

                if (t.includes('متجر') || t.includes('تجارة') || t.includes('شحن') || t.includes('بيع') || t.includes('store') || t.includes('shop')) {
                    projectName = 'منصة تجارة إلكترونية سحابية PWA مع ربط محاسبي ومخازن';
                    industry = 'التجارة الرقمية وسلاسل الإمداد الأوروبية';
                    sysRec = 'متجر PWA فائق السرعة + ربط بوابات الدفع الأوروبية (iDEAL/Stripe) + تكامل المخازن التلقائي';
                    roiValue = '+55% زيادة في معدل التحويل والمبيعات وتوفير 80 ساعة عمل شهرياً';
                } else if (t.includes('محاسب') || t.includes('erp') || t.includes('ضرائب') || t.includes('فاتور') || t.includes('استيراد') || t.includes('تصدير')) {
                    projectName = 'منظومة ERP سحابية لإدارة الحسابات والضرائب والعمليات المؤسسية';
                    industry = 'الأنظمة المالية والإدارية وحوكمة الموارد (ERP)';
                    sysRec = 'نظام CoreSync ERP مخصص + شجرة حسابات متوافقة مع BTW/VAT + أتمتة الفواتير والتقارير الفورية';
                    roiValue = 'خفض تكاليف الأخطاء المحاسبية بنسبة 95% وتوفير ما يعادل 2.5 موظف إداري سنوياً';
                } else if (t.includes('تطبيق') || t.includes('جوال') || t.includes('مواعيد') || t.includes('عياد') || t.includes('حجز') || t.includes('app')) {
                    projectName = 'تطبيق سحابي ذكي لحجز المواعيد وإدارة العملاء عبر الذكاء الاصطناعي';
                    industry = 'التطبيقات الخدمية ومنصات الحجز الذكية';
                    sysRec = 'تطبيق ويب PWA متجاوب + محرك حجز ودفع فوري + روبوت ذكاء اصطناعي لإشعارات المواعيد عبر واتساب وتيليجرام';
                    roiValue = 'القضاء على الغياب وإلغاء المواعيد بنسبة 85% وزيادة التدفقات النقدية اللحظية';
                } else if (t.includes('سوشيال') || t.includes('هوية') || t.includes('تأسيس') || t.includes('8k') || t.includes('براند')) {
                    projectName = 'باقة التأسيس السيادي لقنوات السوشيال ميديا وحزمة الهوية البصرية 8K';
                    industry = 'الهوية الرقمية وحضور العلامات التجارية الكبرى';
                    sysRec = 'تأسيس 9 منصات تواصل موحدة + 23 أصلاً فائق الدقة 8K + قوالب فيديو ريلز 9:16 + استوديو تسليم رقمي';
                    roiValue = 'مضاعفة ثقة المستثمرين والعملاء بمعدل 5.4x وتسليم كامل خلال 48 إلى 72 ساعة';
                }

                const html = `
                    <div class="sr-blueprint-card">
                        <div class="sr-blueprint-header">
                            <span class="sr-blueprint-badge">
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                                خطة عمل ومخطط تنفيذي معتمد بالذكاء الاصطناعي 2026
                            </span>
                            <h4 class="sr-blueprint-title">${projectName}</h4>
                            <p class="text-white-64 font-size-14 mb-0">المجال: <strong class="text-white">${industry}</strong> • تم التحليل والصياغة بناءً على فكرتك المنطوقة.</p>
                        </div>

                        <div class="sr-blueprint-grid">
                            <div class="sr-blueprint-box">
                                <div class="sr-blueprint-box-title">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                                    1. الرؤية ونطاق المعالجة
                                </div>
                                <div class="sr-blueprint-box-desc">
                                    تحويل الفكرة إلى منظومة برمجية متماسكة تنافس عالمياً، مع التركيز على تجربة مستخدم سلسة وأمان مصرفي للبيانات وربط إداري متكامل.
                                </div>
                            </div>

                            <div class="sr-blueprint-box">
                                <div class="sr-blueprint-box-title">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>
                                    2. البنية البرمجية الموصى بها
                                </div>
                                <div class="sr-blueprint-box-desc">
                                    ${sysRec}
                                </div>
                            </div>

                            <div class="sr-blueprint-box">
                                <div class="sr-blueprint-box-title">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                                    3. العائد الاستثماري المتوقع (ROI)
                                </div>
                                <div class="sr-blueprint-box-desc">
                                    ${roiValue}
                                </div>
                            </div>
                        </div>

                        <div class="sr-roadmap-steps">
                            <div class="sr-roadmap-step">
                                <span class="sr-roadmap-step-num">1</span>
                                <div><strong>المرحلة الأولى (الأسبوع 1-2):</strong> التأسيس الهيكلي، حجز وتوحيد قنوات السوشيال ميديا 9 منصات، وتوليد حزمة الهوية البصرية 8K.</div>
                            </div>
                            <div class="sr-roadmap-step">
                                <span class="sr-roadmap-step-num">2</span>
                                <div><strong>المرحلة الثانية (الأسبوع 3-5):</strong> هندسة وتطوير الأنظمة السحابية والـ ERP، وتكامل بوابات الدفع والفواتير والربط الآلي.</div>
                            </div>
                            <div class="sr-roadmap-step">
                                <span class="sr-roadmap-step-num">3</span>
                                <div><strong>المرحلة الثالثة (الأسبوع 6+):</strong> تدقيق الأمان والسرعة، التدريب الميداني للمؤسسين، والإطلاق التجاري وبدء استلام الأرباح.</div>
                            </div>
                        </div>

                        <div class="sr-blueprint-actions">
                            <button type="button" class="sr-voice-btn-primary" onclick="exportBlueprintPdf('${projectName.replace(/'/g, "\\'")}')">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                                <span>تحميل خطة العمل التنفيذية (PDF Export) 📄</span>
                            </button>
                            <button type="button" class="sr-voice-btn-glass" onclick="bookBlueprintConsultation('${projectName.replace(/'/g, "\\'")}')">
                                <span>👔 اعتماد الخطة وحجز جلسة تنفيذ فورية</span>
                            </button>
                        </div>
                    </div>
                `;

                if (resultBox) {
                    resultBox.innerHTML = html;
                    resultBox.style.display = 'block';
                    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }

                if (status) status.innerHTML = '✨ تم بناء وتوليد خطة عملك بنجاح تام! يمكنك تحميلها كـ PDF أو حجز التنفيذ فوراً.';
                if (typeof LuxuryAudio !== 'undefined') LuxuryAudio.play('success');
            }, 700);
        }

        function exportBlueprintPdf(title) {
            window.print();
        }

        function bookBlueprintConsultation(title) {
            closeAiVoicePlannerModal();
            setTimeout(() => {
                if (typeof openExecutiveBookingModal === 'function') {
                    openExecutiveBookingModal('both');
                    const notes = document.getElementById('bookingClientNotes');
                    if (notes) {
                        notes.value = 'أرغب بتنفيذ خطة العمل المتولدة بالصوت: ' + title;
                    }
                }
            }, 300);
        }
"""

def update_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add CSS before </head>
    if 'S&R CORESYNC - MILESTONE 36' not in html:
        css_tag = f"<style>\n{CSS_VOICE_AND_SOCIAL}\n</style>\n</head>"
        html = html.replace('</head>', css_tag, 1)

    # 2. Add Voice Planner button to .exec-stage-actions
    voice_btn = """                            <button type="button" class="exec-stage-btn exec-stage-btn-voice-pulse" data-sr-call="openAiVoicePlannerModal" title="تحدث بفكرة مشروعك وسيقوم الذكاء الاصطناعي ببناء خطة عملك فوراً">
                                <span>🎙️ خطط لمشروعك بالصوت (AI Voice)</span>
                            </button>"""
    if 'data-sr-call="openAiVoicePlannerModal"' not in html:
        html = html.replace(
            '<div class="exec-stage-actions">',
            f'<div class="exec-stage-actions">\n{voice_btn}',
            1
        )

    # 3. Add Modal HTML before </body>
    if 'id="aiVoicePlannerModal"' not in html:
        html = html.replace('</body>', f"{MODAL_HTML}\n<script>\n{JS_VOICE_PLANNER}\n</script>\n</body>", 1)

    # 4. Add Omnichannel 8K card to projectsDB.identity
    omnichannel_project_js = """                {
                    id: "omnichannel-8k",
                    name: "Omnichannel 8K Social Authority",
                    subtitle: "باقة التأسيس السيادي لقنوات السوشيال ميديا وحزمة الهوية البصرية 8K (23 أصلاً ملكياً)",
                    heroImg: "./assets/social-8k-branding/linkedin-8k/linkedin-company-cover-8k.webp",
                    tags: ["9 منصات عالمية", "دقة فائقة 8K", "قوالب فيديو 9:16", "استوديو رقمي خاص"],
                    year: "2026",
                    client: "S&R CoreSync Enterprise Service",
                    type: "خدمة تأسيس وهوية رقمية مأجورة",
                    loc: "أوروبا والشرق الأوسط",
                    preview: "social-8k-studio.html",
                    desc: "خدمة مؤسسية شاملة لتأسيس وتوثيق 9 منصات تواصل اجتماعي رسمية بالمعرف الموحد، وتصميم حزمة هوية بصرية فائقة 8K تشمل 23 أصلاً معتمداً (أغلفة، أفاتار، بطاقات إعلانية، أغلفة قصص وهايلايتس، وطبقات فيديو Master شفافة للريلز والشورتس 9:16 مع قالب مناطق الأمان)، مع تزويد العميل ببوابة استوديو رقمية خاصة لمعاينة وتحميل الأصول بضغطة زر واحدة.",
                    quote: "حضور رقمي استثنائي يمنح شركتك هيبة ومصداقية فورية ويضاعف تفاعل وثقة العملاء والشركاء من اللحظة الأولى.",
                    kpiConversion: '+280%', kpiSpeed: '48 ساعة تسليم', kpiSales: '+5.4x مصداقية وتفاعل',
                    techs: ['8K UHD Assets', '9 Unified Platforms', 'Video Shorts 9:16 Overlays', 'Interactive Studio Portal'],
                    gallery: [
                        "./assets/social-8k-branding/linkedin-8k/linkedin-company-cover-8k.webp",
                        "./assets/social-8k-branding/youtube-8k/youtube-channel-banner-8k.webp",
                        "./assets/social-8k-branding/universal-8k/sr-coresync-profile-avatar-8k.webp"
                    ]
                },"""
    if 'id: "omnichannel-8k"' not in html:
        html = html.replace('identity: [', f"identity: [\n{omnichannel_project_js}", 1)

    # 5. Add 4th card to #pricing-pane-creative
    pricing_card_8k = """                            <!-- الباقة 4: باقة التأسيس السيادي للسوشيال ميديا وهوية الـ 8K (خدمة مأجورة) -->
                            <div class="wg-plan style-2">
                                <div class="plan-badge">
                                    <span class="plan-badge__icon" aria-hidden="true">
                                        <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 3.6l2.5 5.2 5.7.8-4.1 4 1 5.6L12 16.5l-5.1 2.7 1-5.6-4.1-4 5.7-.8z"/></svg>
                                    </span>
                                    حزمة 8K السيادية 2026
                                </div>
                                <div class="bg-img bg-img_1 d-xl-block"></div>
                                <div class="bg-img bg-img_2">
                                    <img loading="lazy" decoding="async" width="416" height="625" src="./assets/bg-2-gold.png" alt="زخرفة ذهبية">
                                </div>
                                <div class="br-line bg-primary br-line-gold"></div>
                                <p class="plan-name letter-space--1 fw-medium">تأسيس قنوات السوشيال ميديا وهوية 8K</p>
                                <h4 class="plan-price font-latin">
                                    <span><span class="text-primary gold-accent">€</span><span class="plan-price__amount" data-eur-price="890">890</span></span>
                                    <span class="text-body-2 fw-normal text-white-64 letter-space--1">/ للمشروع</span>
                                </h4>
                                <p class="plan-desc text-white-64">
                                    تأسيس وتوثيق 9 منصات تواصل موحدة وتوليد 23 أصلاً فائق الدقة 8K مع قوالب ريلز واستوديو تسليم خاص
                                </p>
                                <div class="pricing-card-actions">
                                    <a href="https://wa.me/31687764998?text=مرحباً%20فريق%20CoreSync،%20أود%20طلب%20باقة%20تأسيس%20قنوات%20السوشيال%20ميديا%20وهوية%20الـ%208K%20(€890)" target="_blank" rel="noopener noreferrer" class="pricing-card-btn-gold">
                                        <span>طلب حجز الباقة عبر واتساب 💬</span>
                                    </a>
                                    <button type="button" class="pricing-card-btn-pdf" data-sr-call="openExecutiveBookingModal" data-sr-args='["social_8k"]'>
                                        <span>طلب عرض سعر رسمي (PDF) 📄</span>
                                    </button>
                                </div>
                                <ul class="benefit-list tf-list vertical">
                                    <li class="benefit_title text-white-64">متضمن</li>
                                    <li><span class="text-primary gold-accent">//</span> تأسيس وتوثيق رسمي موحد لـ 9 منصات تواصل اجتماعي</li>
                                    <li><span class="text-primary gold-accent">//</span> تصميم وتصدير 23 أصلاً فائق الدقة 8K & 4K لجميع المنصات</li>
                                    <li><span class="text-primary gold-accent">//</span> قوالب مونتاج شورتس وريلز 9:16 شفافة مع شريط سفلي فاخر</li>
                                    <li><span class="text-primary gold-accent">//</span> قالب مناطق الأمان المعتمد (Safe Zones Guide) لمصممي الفيديو</li>
                                    <li><span class="text-primary gold-accent">//</span> بوابة استوديو رقمي خاص بالعميل للتحميل المباشر بضغطة زر</li>
                                    <li><span class="text-primary gold-accent">//</span> صياغة البايو الاحترافي وربط كتالوج واتساب للأعمال</li>
                                    <li><span class="text-primary gold-accent">//</span> تسليم سريع متكامل خلال 48 إلى 72 ساعة عمل</li>
                                </ul>
                            </div>"""

    if 'data-eur-price="890"' not in html:
        # insert before the closing </div> of pricing-pane-creative
        target = 'id="pricing-pane-creative">\n                        <div class="tf-grid-layout md-col-2 lg-col-3">'
        if target in html:
            html = html.replace(target, f"{target}\n{pricing_card_8k}", 1)
        else:
            # alternative matching
            target2 = 'id="pricing-pane-creative">'
            html = html.replace(target2, f'{target2}\n<div class="tf-grid-layout md-col-2 lg-col-3">\n{pricing_card_8k}', 1)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully updated index.html with Milestone 36 features!")

update_index()
