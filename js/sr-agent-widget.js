/**
 * ==============================================================================
 * S&R CoreSync Sovereign Agent Floating Widget
 * ==============================================================================
 */

(function () {
    'use strict';

    // منع التكرار إذا كان الويدجت محملاً مسبقاً
    if (window.__SR_AGENT_WIDGET_INITIALIZED__) return;
    window.__SR_AGENT_WIDGET_INITIALIZED__ = true;

    // الحصول على معرّف الجلسة المستمر أو إنشاؤه
    let sessionId = localStorage.getItem('sr_agent_session_id');
    if (!sessionId) {
        sessionId = 'sr_sess_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
        localStorage.setItem('sr_agent_session_id', sessionId);
    }

    const API_ENDPOINT = (typeof localStorage !== 'undefined' && localStorage.getItem('sr_agent_endpoint')) || 'http://127.0.0.1:8000/api/ai-concierge';

    // حقن رابط ملف التنسيقات CSS تلقائياً إن لم يكن موجوداً
    if (!document.querySelector('link[href*="sr-agent-widget.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'css/sr-agent-widget.css';
        document.head.appendChild(link);
    }

    // بناء عناصر الواجهة
    function buildWidgetUI() {
        const wrapper = document.createElement('div');
        wrapper.id = 'sr-agent-widget-container';
        wrapper.innerHTML = `
            <!-- Floating Launcher Trigger -->
            <button class="sr-agent-launcher" id="sr-agent-launcher" title="المستشار الذكي التنفيذي لـ S&R CoreSync" aria-label="فتح محادثة المستشار الذكي">
                <span class="sr-agent-pulse-dot"></span>
                <svg class="sr-agent-launcher-icon" viewBox="0 0 24 24" fill="none" stroke="#c5a880" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </button>

            <!-- Chat Window -->
            <div class="sr-agent-window" id="sr-agent-window" role="dialog" aria-modal="false" aria-label="نافذة المستشار الذكي">
                <div class="sr-agent-header">
                    <div class="sr-agent-header-brand">
                        <div class="sr-agent-avatar">
                            <span class="sr-agent-logo-text">S&R</span>
                        </div>
                        <div class="sr-agent-title">
                            <h3>المستشار الذكي التنفيذي</h3>
                            <span><span class="sr-agent-status-indicator"></span> متصل (Google Antigravity)</span>
                        </div>
                    </div>
                    <div class="sr-agent-header-actions">
                        <button id="sr-agent-voice-lang" class="sr-voice-lang-btn" title="تغيير لغة الصوت (AR / EN)">AR</button>
                        <button id="sr-agent-export" title="تصدير الاستشارة كملف نصي">⬇</button>
                        <button id="sr-agent-clear" title="مسح المحادثة">↺</button>
                        <button id="sr-agent-close" title="إغلاق النافذة">✕</button>
                    </div>
                </div>

                <div class="sr-agent-messages" id="sr-agent-messages">
                    <div class="sr-msg sr-msg-agent">
                        مرحباً بك! أنا المستشار الذكي التنفيذي لمنظومة <strong>S&R CoreSync</strong>. كيف يمكنني مساعدة منشأتكم اليوم بخصوص حلولنا المؤسسية، الباقات، أو بوابات المنظومة؟
                    </div>
                    <div class="sr-typing" id="sr-typing-indicator">
                        <div class="sr-typing-dot"></div>
                        <div class="sr-typing-dot"></div>
                        <div class="sr-typing-dot"></div>
                    </div>
                </div>

                <div class="sr-agent-chips">
                    <button class="sr-chip" data-query="ما هي باقة السوشيال ميديا 8K؟">باقة السوشيال 8K</button>
                    <button class="sr-chip" data-query="ما هي تكلفة الموقع المؤسسي؟">الموقع المؤسسي</button>
                    <button class="sr-chip" data-query="استعرض أهم بوابات المنظومة">بوابات المنظومة</button>
                    <button class="sr-chip" data-query="كيف أطلب عرض سعر مخصص؟">طلب عرض سعر</button>
                </div>

                <form class="sr-agent-input-box" id="sr-agent-form">
                    <button type="button" class="sr-agent-mic-btn" id="sr-agent-mic" title="تحدث بالصوت (Speech-to-Text)">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                            <line x1="12" y1="19" x2="12" y2="23"></line>
                            <line x1="8" y1="23" x2="16" y2="23"></line>
                        </svg>
                    </button>
                    <input type="text" class="sr-agent-input" id="sr-agent-input" placeholder="اكتب سؤالك أو تحدث بالصوت..." autocomplete="off">
                    <button type="submit" class="sr-agent-send-btn" title="إرسال">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </form>
            </div>
        `;
        document.body.appendChild(wrapper);

        // ربط الأحداث
        const launcher = document.getElementById('sr-agent-launcher');
        const windowEl = document.getElementById('sr-agent-window');
        const closeBtn = document.getElementById('sr-agent-close');
        const clearBtn = document.getElementById('sr-agent-clear');
        const exportBtn = document.getElementById('sr-agent-export');
        const langBtn = document.getElementById('sr-agent-voice-lang');
        const micBtn = document.getElementById('sr-agent-mic');
        const form = document.getElementById('sr-agent-form');
        const input = document.getElementById('sr-agent-input');
        const messagesEl = document.getElementById('sr-agent-messages');
        const typingEl = document.getElementById('sr-typing-indicator');

        // حالة الصوت ثنائي اللغة (Bilingual Voice State)
        let currentVoiceLang = 'ar-SA';
        let isListening = false;
        let recognition = null;

        // تبديل لغة الصوت
        langBtn.addEventListener('click', () => {
            if (currentVoiceLang === 'ar-SA') {
                currentVoiceLang = 'en-US';
                langBtn.textContent = 'EN';
                langBtn.title = 'Current voice language: English (Click for Arabic)';
                input.placeholder = 'Type your question or speak...';
            } else {
                currentVoiceLang = 'ar-SA';
                langBtn.textContent = 'AR';
                langBtn.title = 'تغيير لغة الصوت (AR / EN)';
                input.placeholder = 'اكتب سؤالك أو تحدث بالصوت...';
            }
            if (recognition) {
                recognition.lang = currentVoiceLang;
            }
        });

        // تهيئة محرك الإدخال الصوتي (Speech-to-Text via Web Speech API)
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRec) {
            recognition = new SpeechRec();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = currentVoiceLang;

            function stopListening() {
                isListening = false;
                micBtn.classList.remove('sr-listening');
                input.placeholder = currentVoiceLang === 'ar-SA' ? 'اكتب سؤالك أو تحدث بالصوت...' : 'Type your question or speak...';
            }

            recognition.onstart = () => {
                isListening = true;
                micBtn.classList.add('sr-listening');
                input.placeholder = currentVoiceLang === 'ar-SA' ? '🎙️ جارٍ الاستماع... تحدث الآن' : '🎙️ Listening... Speak now';
            };

            recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                const spoken = (finalTranscript || interimTranscript).trim();
                if (spoken) {
                    input.value = spoken;
                }
            };

            recognition.onerror = (event) => {
                console.warn('[S&R Voice] Recognition error:', event.error);
                stopListening();
            };

            recognition.onend = () => {
                stopListening();
            };

            micBtn.addEventListener('click', () => {
                if (isListening) {
                    recognition.stop();
                } else {
                    recognition.lang = currentVoiceLang;
                    try {
                        recognition.start();
                    } catch (e) {
                        console.warn('[S&R Voice] Could not start recognition:', e);
                    }
                }
            });
        } else {
            micBtn.addEventListener('click', () => {
                alert(currentVoiceLang === 'ar-SA' ? 'المتصفح الحالي لا يدعم ميزة الإدخال الصوتي المباشر Web Speech API.' : 'Your browser does not support Web Speech API voice input.');
            });
        }

        // تحويل النص إلى صوت (Text-to-Speech via Web Speech API)
        function speakText(rawText, ttsButton) {
            if (!('speechSynthesis' in window)) return;

            if (window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
                document.querySelectorAll('.sr-agent-tts-btn').forEach(b => b.classList.remove('sr-speaking'));
                return;
            }

            const cleanText = rawText
                .replace(/<[^>]*>/g, ' ')
                .replace(/\*\*(.*?)\*\*/g, '$1')
                .replace(/https?:\/\/\S+/g, '')
                .replace(/[•\-_#]/g, ' ')
                .replace(/\s+/g, ' ')
                .trim();

            if (!cleanText) return;

            const utterance = new SpeechSynthesisUtterance(cleanText);
            const isEnglish = /^[A-Za-z0-9\s.,!?'"()-]+$/.test(cleanText.slice(0, 50));
            utterance.lang = isEnglish ? 'en-US' : 'ar-SA';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;

            if (ttsButton) ttsButton.classList.add('sr-speaking');

            utterance.onend = () => {
                if (ttsButton) ttsButton.classList.remove('sr-speaking');
            };
            utterance.onerror = () => {
                if (ttsButton) ttsButton.classList.remove('sr-speaking');
            };

            window.speechSynthesis.speak(utterance);
        }

        // إضافة زر الاستماع الصوتي لرسالة الترحيب الأولى
        const firstAgentMsg = messagesEl.querySelector('.sr-msg-agent');
        if (firstAgentMsg) {
            const initTts = document.createElement('button');
            initTts.type = 'button';
            initTts.className = 'sr-agent-tts-btn';
            initTts.title = 'استماع للترحيب (Text-to-Speech)';
            initTts.innerHTML = `
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                    <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                </svg>
                <span>استماع</span>
            `;
            initTts.addEventListener('click', () => speakText(firstAgentMsg.textContent, initTts));
            firstAgentMsg.appendChild(initTts);
        }

        launcher.addEventListener('click', () => {
            windowEl.classList.toggle('sr-open');
            if (windowEl.classList.contains('sr-open')) {
                input.focus();
            }
        });

        closeBtn.addEventListener('click', () => {
            windowEl.classList.remove('sr-open');
        });

        clearBtn.addEventListener('click', () => {
            // مسح الرسائل محلياً
            messagesEl.querySelectorAll('.sr-msg:not(:first-child)').forEach(m => m.remove());
            // تجديد معرّف الجلسة
            sessionId = 'sr_sess_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
            localStorage.setItem('sr_agent_session_id', sessionId);
        });

        exportBtn.addEventListener('click', () => {
            const msgs = messagesEl.querySelectorAll('.sr-msg');
            if (!msgs || msgs.length === 0) return;

            const now = new Date();
            const dateStr = now.toISOString().replace(/T/, ' ').replace(/\..+/, '');
            let content = '======================================================================\n';
            content += 'S&R CoreSync For Intelligent Solutions - سجل الاستشارة التنفيذية\n';
            content += 'التاريخ والوقت: ' + dateStr + '\n';
            content += 'المقر المؤسسي: أمستردام - الرياض - دبي | واتساب VIP: +31 618111116\n';
            content += 'الموقع الرسمي: https://sr-coresync.com\n';
            content += '======================================================================\n\n';

            msgs.forEach(m => {
                const isUser = m.classList.contains('sr-msg-user');
                const role = isUser ? 'المستخدم' : 'المستشار الذكي التنفيذي';
                // تنظيف النص من عناصر HTML والأزرار
                const clone = m.cloneNode(true);
                const actions = clone.querySelector('.sr-msg-actions');
                if (actions) actions.remove();
                const plainText = clone.textContent.trim().replace(/\s+/g, ' ');
                content += `[${role}]:\n${plainText}\n\n`;
            });

            content += '----------------------------------------------------------------------\n';
            content += 'تم استخراج هذا التقرير تلقائياً عبر المستشار الذكي التنفيذي لـ S&R CoreSync.\n';
            content += '======================================================================\n';

            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `SR-CoreSync-Executive-Consultation-${now.toISOString().slice(0, 10)}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });

        // النقر على الرقاقات السريعة
        document.querySelectorAll('.sr-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const query = chip.getAttribute('data-query');
                if (query) {
                    sendMessage(query);
                }
            });
        });

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = input.value.trim();
            if (text) {
                sendMessage(text);
                input.value = '';
            }
        });

        function appendMessage(text, isUser = false, actions = []) {
            const msg = document.createElement('div');
            msg.className = `sr-msg ${isUser ? 'sr-msg-user' : 'sr-msg-agent'}`;
            msg.innerHTML = text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

            if (!isUser && actions && actions.length > 0) {
                const actWrap = document.createElement('div');
                actWrap.className = 'sr-msg-actions';
                actions.forEach(a => {
                    const btn = document.createElement('a');
                    btn.className = 'sr-action-btn';
                    btn.textContent = a.label;
                    if (a.url) {
                        btn.href = a.url;
                        btn.target = '_blank';
                        btn.rel = 'noopener noreferrer';
                    } else if (a.action === 'open_rfq') {
                        btn.href = '#';
                        btn.addEventListener('click', (ev) => {
                            ev.preventDefault();
                            if (typeof window.openRFQModal === 'function') {
                                window.openRFQModal();
                            } else {
                                window.location.href = 'https://wa.me/31618111116?text=' + encodeURIComponent('أرغب في طلب عرض سعر رسمي مخصص.');
                            }
                        });
                    }
                    actWrap.appendChild(btn);
                });
                msg.appendChild(actWrap);
            }

            if (!isUser) {
                const ttsBtn = document.createElement('button');
                ttsBtn.type = 'button';
                ttsBtn.className = 'sr-agent-tts-btn';
                ttsBtn.title = 'استماع للرد بالصوت (Text-to-Speech)';
                ttsBtn.innerHTML = `
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                        <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                    </svg>
                    <span>استماع</span>
                `;
                ttsBtn.addEventListener('click', () => speakText(text, ttsBtn));
                msg.appendChild(ttsBtn);
            }

            messagesEl.insertBefore(msg, typingEl);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        async function sendMessage(text) {
            appendMessage(text, true);
            typingEl.style.display = 'inline-flex';
            messagesEl.scrollTop = messagesEl.scrollHeight;

            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 25000);

                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: text,
                        session_id: sessionId,
                        channel: 'web_widget'
                    }),
                    signal: controller.signal
                });
                clearTimeout(timeoutId);

                if (!response.ok) {
                    throw new Error('HTTP ' + response.status);
                }

                const data = await response.json();
                typingEl.style.display = 'none';
                appendMessage(data.reply, false, data.actions);
            } catch (err) {
                typingEl.style.display = 'none';
                console.warn('[S&R Agent Widget]: Falling back to local responder due to:', err);
                appendMessage(
                    "بصفتي المستشار الذكي التنفيذي لـ S&R CoreSync، أحيطكم علماً بأن المنظومة توفر 9 ركائز سيادية معتمدة تشمل السحابية والـ ERP، التحكيم الدولي، جسر الـ CBDC، وحزمة السوشيال ميديا 8K (€890). للتواصل المباشر مع مكتب القيادة: +31 618111116.",
                    false,
                    [
                        { label: '💬 محادثة واتساب VIP المباشرة', url: 'https://wa.me/31618111116' },
                        { label: '📋 طلب عرض سعر مخصص', action: 'open_rfq' }
                    ]
                );
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildWidgetUI);
    } else {
        buildWidgetUI();
    }
})();

