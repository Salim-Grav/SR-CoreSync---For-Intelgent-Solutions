let voiceRecognition=null,isVoiceRecording=!1;function openAiVoicePlannerModal(){const e=document.getElementById("aiVoicePlannerModal");e&&(e.classList.add("active"),document.body.style.overflow="hidden","undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("open"))}function closeAiVoicePlannerModal(){const e=document.getElementById("aiVoicePlannerModal");e&&e.classList.contains("active")&&(stopVoiceRecording(),stopBlueprintAudioSynthesis(),e.classList.remove("active"),document.body.style.overflow="","undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("close"))}function toggleVoiceRecording(){isVoiceRecording?stopVoiceRecording():startVoiceRecording()}function startVoiceRecording(){const e=window.SpeechRecognition||window.webkitSpeechRecognition,n=document.getElementById("voicePlannerMicBtn"),t=document.getElementById("voicePlannerStatus"),o=document.getElementById("voicePlannerTranscript");if(!e)return t&&(t.innerHTML="⚠️ المتصفح لا يدعم التسجيل الصوتي المباشر، يمكنك كتابة فكرتك في المربع أدناه!"),void(o&&o.focus());try{voiceRecognition=new e,voiceRecognition.continuous=!0,voiceRecognition.interimResults=!0,voiceRecognition.lang=document.documentElement.getAttribute("lang")||"ar-SA",voiceRecognition.onstart=function(){isVoiceRecording=!0,n&&n.classList.add("is-recording"),t&&(t.innerHTML="🔴 جاري الاستماع... تحدث بحرية عن فكرة مشروعك ومتطلباتك الآن!")},voiceRecognition.onresult=function(e){let n="";for(let t=0;t<e.results.length;t++)n+=e.results[t][0].transcript+" ";o&&(o.value=n.trim())},voiceRecognition.onerror=function(e){console.warn("Speech recognition notice:",e),stopVoiceRecording(),t&&(t.innerHTML="اضغط على المايكروفون للتحدث أو اكتب فكرتك مباشرة.")},voiceRecognition.onend=function(){stopVoiceRecording()},voiceRecognition.start()}catch(e){console.error(e),stopVoiceRecording()}}function stopVoiceRecording(){isVoiceRecording=!1;const e=document.getElementById("voicePlannerMicBtn"),n=document.getElementById("voicePlannerStatus");if(e&&e.classList.remove("is-recording"),n&&(n.innerHTML="✓ تم تسجيل الفكرة. انقر على الزر الذهبي أدناه لتوليد خطة العمل!"),voiceRecognition){try{voiceRecognition.stop()}catch(e){}voiceRecognition=null}}function fillVoiceSample(e){const n=document.getElementById("voicePlannerTranscript");n&&(n.value=e,generateAiProjectBlueprint())}function resetVoicePlanner(){stopVoiceRecording(),stopBlueprintAudioSynthesis();const e=document.getElementById("voicePlannerTranscript"),n=document.getElementById("voicePlannerResult"),t=document.getElementById("voicePlannerStatus");e&&(e.value=""),n&&(n.innerHTML="",n.style.display="none"),t&&(t.innerHTML="اضغط على المايكروفون وتحدث بفكرة أو متطلبات مشروعك...")}function generateAiProjectBlueprint(){stopBlueprintAudioSynthesis();const e=document.getElementById("voicePlannerTranscript"),n=document.getElementById("voicePlannerResult"),t=document.getElementById("voicePlannerStatus"),o=e?e.value.trim():"";if(!o||o.length<5)return t&&(t.innerHTML="⚠️ الرجاء التحدث بصوتك أو كتابة نبذة بسيطة عن فكرتك أولاً لتوليد الخطة!"),void(e&&e.focus());t&&(t.innerHTML="⚡ جاري المعالجة وهندسة خطة العمل التنفيذية بواسطة الذكاء الاصطناعي..."),setTimeout(()=>{const e=o.toLowerCase();let i="منظومة سحابية وحلول متكاملة للأعمال 2026",s="التحول الرقمي وأتمتة الشركات",c="بنية سحابية فائقة السرعة مع لوحة تحكم ذكية",a="+42% توفير بالتكاليف التشغيلية و 3.8x سرعة في إنجاز العمليات";const isRaed=e.includes("erp")||e.includes("محاسب")||e.includes("ضريب")||e.includes("ضرائب")||e.includes("vat")||e.includes("btw")||e.includes("تشغيل")||e.includes("عمليات")||e.includes("إدار")||e.includes("ادارة")||e.includes("عقد")||e.includes("عقود")||e.includes("توسع")||e.includes("شركاء")||e.includes("مالي")||e.includes("تمويل")||e.includes("مخازن")||e.includes("امداد")||e.includes("سلاسل")||e.includes("سوشيال")||e.includes("8k")||e.includes("تسويق")||e.includes("هوية")||e.includes("براند")||e.includes("business")||e.includes("operation")||e.includes("finance")||e.includes("logistics")||e.includes("supply");const founderName=isRaed?"أ. رائد كعكة":"م. محمد سليم عزيزة";const founderRole=isRaed?"المسؤول التنفيذي للعمليات وتطوير الأعمال":"كبير مهندسي السحابة والذكاء الاصطناعي";const founderImg=isRaed?"./assets/founder-raed.webp":"./assets/founder-salim.webp";const founderAlt=isRaed?"Mr. Raed Kaakeh - Chief Operating Officer":"Eng. Mohammad Salim Aziza - Chief Technology & AI Officer";const founderBadge=isRaed?"🎙️ صوت الأستاذ رائد الرقمي • AI Executive Audio":"🎙️ صوت المهندس سليم الرقمي • AI Executive Audio";const founderLead=isRaed?"أهلاً بك، معك الأستاذ رائد كعكة، المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر.":"أهلاً بك، معك المهندس محمد سليم عزيزة، كبير مهندسي السحابة والذكاء الاصطناعي في شركة إس آند آر.";e.includes("متجر")||e.includes("تجارة")||e.includes("شحن")||e.includes("بيع")||e.includes("store")||e.includes("shop")?(i="منصة تجارة إلكترونية سحابية PWA مع ربط محاسبي ومخازن",s="التجارة الرقمية وسلاسل الإمداد الأوروبية",c="متجر PWA فائق السرعة + ربط بوابات الدفع الأوروبية (iDEAL/Stripe) + تكامل المخازن التلقائي",a="+55% زيادة في معدل التحويل والمبيعات وتوفير 80 ساعة عمل شهرياً"):e.includes("محاسب")||e.includes("erp")||e.includes("ضرائب")||e.includes("فاتور")||e.includes("استيراد")||e.includes("تصدير")?(i="منظومة ERP سحابية لإدارة الحسابات والضرائب والعمليات المؤسسية",s="الأنظمة المالية والإدارية وحوكمة الموارد (ERP)",c="نظام CoreSync ERP مخصص + شجرة حسابات متوافقة مع BTW/VAT + أتمتة الفواتير والتقارير الفورية",a="خفض تكاليف الأخطاء المحاسبية بنسبة 95% وتوفير ما يعادل 2.5 موظف إداري سنوياً"):e.includes("تطبيق")||e.includes("جوال")||e.includes("مواعيد")||e.includes("عياد")||e.includes("حجز")||e.includes("app")?(i="تطبيق سحابي ذكي لحجز المواعيد وإدارة العملاء عبر الذكاء الاصطناعي",s="التطبيقات الخدمية ومنصات الحجز الذكية",c="تطبيق ويب PWA متجاوب + محرك حجز ودفع فوري + روبوت ذكاء اصطناعي لإشعارات المواعيد عبر واتساب وتيليجرام",a="القضاء على الغياب وإلغاء المواعيد بنسبة 85% وزيادة التدفقات النقدية اللحظية"):(e.includes("سوشيال")||e.includes("هوية")||e.includes("تأسيس")||e.includes("8k")||e.includes("براند"))&&(i="باقة التأسيس السيادي لقنوات السوشيال ميديا وحزمة الهوية البصرية 8K",s="الهوية الرقمية وحضور العلامات التجارية الكبرى",c="تأسيس 9 منصات تواصل موحدة + 23 أصلاً فائق الدقة 8K + قوالب فيديو ريلز 9:16 + استوديو تسليم رقمي",a="مضاعفة ثقة المستثمرين والعملاء بمعدل 5.4x وتسليم كامل خلال 48 إلى 72 ساعة");const r=`\n                    <div class="sr-blueprint-card">\n                        <div class="sr-blueprint-header">\n                            <span class="sr-blueprint-badge">\n                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>\n                                خطة عمل ومخطط تنفيذي معتمد بالذكاء الاصطناعي 2026\n                            </span>\n                            <h4 class="sr-blueprint-title">${i}</h4>\n                            <p class="text-white-64 font-size-14 mb-0">المجال: <strong class="text-white">${s}</strong> • تم التحليل والصياغة بناءً على فكرتك المنطوقة.</p>\n                        </div>\n\n                        \x3c!-- 🎙️ مشغل الرد الصوتي التنفيذي الذكي (AI Executive Audio Synthesis) --\x3e\n                        <div class="sr-blueprint-audio-player" id="blueprintAudioPlayer"\n                             data-project-name="${encodeURIComponent(i)}"\n                             data-sys-rec="${encodeURIComponent(c)}"\n                             data-roi-value="${encodeURIComponent(a)}" data-founder-type="${isRaed ? 'raed' : 'salim'}" data-founder-lead="${encodeURIComponent(founderLead)}">\n                            <div class="sr-blueprint-audio-info">\n                                <div class="sr-blueprint-audio-avatar">\n                                    <img src="${founderImg}" alt="${founderAlt}" class="sr-blueprint-audio-img" / loading="lazy" decoding="async">\n                                    <span class="sr-blueprint-audio-status-dot" id="audioSpeakingDot"></span>\n                                </div>\n                                <div class="sr-blueprint-audio-texts">\n                                    <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">\n                                        <span class="sr-blueprint-audio-badge">${founderBadge}</span><span style="font-size:11px;color:#cbd5e1;font-weight:600;">${founderRole}</span>\n                                        <a href="https://www.linkedin.com/company/146883282/" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; background: rgba(10, 102, 194, 0.25); border: 1px solid rgba(96, 165, 250, 0.45); border-radius: 999px; color: #93c5fd; font-size: 11px; font-weight: 700; text-decoration: none; transition: all 0.2s ease;">\n                                            <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76c-.95 0-1.72.77-1.72 1.72s.77 1.73 1.72 1.73a1.73 1.73 0 0 0 1.73-1.73c0-.95-.78-1.72-1.73-1.72m1.39 9.74v-8.37H5.07v8.37h2.78Z"/></svg>\n                                            <span>LinkedIn</span>\n                                        </a>\n                                    </div>\n                                    <div class="sr-blueprint-audio-title">الاستماع للملخص التنفيذي للخطة (${founderName})</div>\n                                </div>\n                            </div>\n                            <div class="sr-blueprint-audio-controls">\n                                <button type="button" class="sr-blueprint-audio-btn" id="blueprintPlayVoiceBtn" onclick="toggleBlueprintAudioSynthesis()">\n                                    <span id="blueprintPlayVoiceIcon">▶️</span>\n                                    <span id="blueprintPlayVoiceLabel">استمع للخطة الآن</span>\n                                </button>\n                                <div class="sr-blueprint-audio-waves" id="blueprintAudioWaves">\n                                    <span class="sr-audio-bar"></span>\n                                    <span class="sr-audio-bar"></span>\n                                    <span class="sr-audio-bar"></span>\n                                    <span class="sr-audio-bar"></span>\n                                    <span class="sr-audio-bar"></span>\n                                    <span class="sr-audio-bar"></span>\n                                    <span class="sr-audio-bar"></span>\n                                </div>\n                            </div>\n                        </div>\n\n                        <div class="sr-blueprint-grid">\n                            <div class="sr-blueprint-box">\n                                <div class="sr-blueprint-box-title">\n                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>\n                                    1. الرؤية ونطاق المعالجة\n                                </div>\n                                <div class="sr-blueprint-box-desc">\n                                    تحويل الفكرة إلى منظومة برمجية متماسكة تنافس عالمياً، مع التركيز على تجربة مستخدم سلسة وأمان مصرفي للبيانات وربط إداري متكامل.\n                                </div>\n                            </div>\n\n                            <div class="sr-blueprint-box">\n                                <div class="sr-blueprint-box-title">\n                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>\n                                    2. البنية البرمجية الموصى بها\n                                </div>\n                                <div class="sr-blueprint-box-desc">\n                                    ${c}\n                                </div>\n                            </div>\n\n                            <div class="sr-blueprint-box">\n                                <div class="sr-blueprint-box-title">\n                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>\n                                    3. العائد الاستثماري المتوقع (ROI)\n                                </div>\n                                <div class="sr-blueprint-box-desc">\n                                    ${a}\n                                </div>\n                            </div>\n                        </div>\n\n                        <div class="sr-roadmap-steps">\n                            <div class="sr-roadmap-step">\n                                <span class="sr-roadmap-step-num">1</span>\n                                <div><strong>المرحلة الأولى (الأسبوع 1-2):</strong> التأسيس الهيكلي، حجز وتوحيد قنوات السوشيال ميديا 9 منصات، وتوليد حزمة الهوية البصرية 8K.</div>\n                            </div>\n                            <div class="sr-roadmap-step">\n                                <span class="sr-roadmap-step-num">2</span>\n                                <div><strong>المرحلة الثانية (الأسبوع 3-5):</strong> هندسة وتطوير الأنظمة السحابية والـ ERP، وتكامل بوابات الدفع والفواتير والربط الآلي.</div>\n                            </div>\n                            <div class="sr-roadmap-step">\n                                <span class="sr-roadmap-step-num">3</span>\n                                <div><strong>المرحلة الثالثة (الأسبوع 6+):</strong> تدقيق الأمان والسرعة، التدريب الميداني للمؤسسين، والإطلاق التجاري وبدء استلام الأرباح.</div>\n                            </div>\n                        </div>\n\n                        <div class="sr-blueprint-actions">\n                            <button type="button" class="sr-voice-btn-primary" onclick="exportBlueprintPdf('${i.replace(/'/g,"'")}')">\n                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>\n                                <span>تحميل الخطة (PDF) 📄</span>\n                            </button>\n                            <button type="button" class="sr-btn-whatsapp" onclick="dispatchBlueprintToWhatsApp()">\n                                <span>📱 إرسال لواتساب للأعمال</span>\n                            </button>\n                            <button type="button" class="sr-btn-telegram" onclick="dispatchBlueprintToTelegram()">\n                                <span>✈️ إرسال لتيليجرام</span>\n                            </button>\n                            <a href="https://www.linkedin.com/company/146883282/" target="_blank" rel="noopener noreferrer" class="sr-btn-linkedin">\n                                <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76c-.95 0-1.72.77-1.72 1.72s.77 1.73 1.72 1.73a1.73 1.73 0 0 0 1.73-1.73c0-.95-.78-1.72-1.73-1.72m1.39 9.74v-8.37H5.07v8.37h2.78Z"/></svg>\n                                <span>💼 صفحة LinkedIn</span>\n                            </a>\n                            <button type="button" class="sr-btn-action sr-btn-preview-a4" data-sr-call="openBlueprintPreviewModal"><span>👁️ معاينة التقرير الرسمي A4 والختم السيادي</span></button>\n                            <button type="button" class="sr-btn-checkout" onclick="openExecutiveCheckoutModal('${i.replace(/'/g,"'")}', 890)">\n                                <span>💳 اعتماد ودفع فوري (€890)</span>\n                            </button>\n                            <button type="button" class="sr-voice-btn-glass" onclick="bookBlueprintConsultation('${i.replace(/'/g,"'")}')">\n                                <span>👔 حجز استشارة VIP</span>\n                            </button>\n                        </div>\n                    </div>\n                `;n&&(n.innerHTML=r,n.style.display="block",n.scrollIntoView({behavior:"smooth",block:"nearest"})),t&&(t.innerHTML="✨ تم بناء وتوليد خطة عملك بنجاح تام! يمكنك الاستماع للملخص الصوتي أو تحميلها كـ PDF."),"undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("success")},700)}window.openAiVoicePlannerModal=openAiVoicePlannerModal,window.closeAiVoicePlannerModal=closeAiVoicePlannerModal;let isBlueprintSpeaking=!1,currentSpeechUtterance=null;function stopBlueprintAudioSynthesis(){if(window.speechSynthesis)try{window.speechSynthesis.cancel()}catch(e){console.warn(e)}isBlueprintSpeaking=!1,currentSpeechUtterance=null;const e=document.getElementById("blueprintAudioPlayer"),n=document.getElementById("blueprintPlayVoiceIcon"),t=document.getElementById("blueprintPlayVoiceLabel");e&&e.classList.remove("is-playing"),n&&(n.innerHTML="▶️"),t&&(t.textContent="استمع للخطة الآن")}function toggleBlueprintAudioSynthesis(){if(isBlueprintSpeaking)return void stopBlueprintAudioSynthesis();if(!("speechSynthesis"in window))return void alert("عذراً، المتصفح الحالي لا يدعم التوليف الصوتي المباشر. يمكنك قراءة الخطة أو تنزيلها بصيغة PDF.");stopBlueprintAudioSynthesis();const e=document.getElementById("blueprintAudioPlayer"),n=e?decodeURIComponent(e.getAttribute("data-project-name")||""):"مشروعك الذكي",t=e?decodeURIComponent(e.getAttribute("data-sys-rec")||""):"البنية السحابية الموصى بها",o=e?decodeURIComponent(e.getAttribute("data-roi-value")||""):"عائد استثماري نوعي",founderLead=e?decodeURIComponent(e.getAttribute("data-founder-lead")||""):"أهلاً بك في شركة إس آند آر.";const docLang = (document.documentElement.getAttribute("lang") || "ar").toLowerCase();
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
i.pitch = 0.88;const femaleKeywords = [
        "فاطمة", "ليلى", "أمينة", "سلمى", "رنا", "سناء", "نورا", "إيمان", "منى", "عائشة", "أمل", "زارية", "أماني", "ريم", "مريم", "هدى", "هدا", "زينب", "سارة", "أنثى",
        "laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman", "girl", "zira", "susan", "hazel", "linda", "eva", "katja", "hedda"
    ];
    const malePreferred = [
        "شاكر", "حامد", "ليث", "باسل", "علي", "إسماعيل", "تيم", "فهد", "رامي", "أحمد", "جمال", "عبدالله", "معاذ", "هادي", "صالح", "ماجد", "طارق", "نايف", "زيد", "رائد", "سليم",
        "shakir", "hamed", "laith", "basel", "ali", "ismail", "taim", "fahd", "rami", "ahmed", "jamal", "abdullah", "moath", "hadi", "saleh", "maged", "tarik", "naayf", "male",
        "david", "mark", "george", "guy", "james", "bart", "stefan", "frank", "bernd", "conrad"
    ];
    const allVoices = (window.speechSynthesis && window.speechSynthesis.getVoices) ? window.speechSynthesis.getVoices() : [];
    const targetVoices = allVoices.filter(v => (v.lang || "").toLowerCase().startsWith(targetLangPrefix));

    let s = targetVoices.find(v => {
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
    }const c=document.getElementById("blueprintPlayVoiceIcon"),a=document.getElementById("blueprintPlayVoiceLabel");i.onstart=function(){isBlueprintSpeaking=!0,e&&e.classList.add("is-playing"),c&&(c.innerHTML="⏸️"),a&&(a.textContent="إيقاف الملخص الصوتي"),"undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("hover")},i.onend=function(){stopBlueprintAudioSynthesis()},i.onerror=function(e){console.warn("Speech synthesis notice:",e),stopBlueprintAudioSynthesis()},window.speechSynthesis.speak(i)}function dispatchBlueprintToWhatsApp(){const e=document.getElementById("blueprintAudioPlayer"),n=e?decodeURIComponent(e.getAttribute("data-project-name")||""):"مشروع ذكي",t=e?decodeURIComponent(e.getAttribute("data-sys-rec")||""):"بنية سحابية متقدمة",o=e?decodeURIComponent(e.getAttribute("data-roi-value")||""):"+42% توفير تشغيلي",isRaed=e?("raed"===e.getAttribute("data-founder-type")):!1,targetFounder=isRaed?"الأستاذ رائد كعكة (مسؤول العمليات والـ ERP)":"المهندس محمد سليم عزيزة (المسؤول التقني والسحابي)",msg=`مرحباً فريق شركة إس آند آر، قمت بهندسة خطة مشروعي بإشراف ${targetFounder}:\n\n📋 *المشروع:* ${n}\n⚙️ *المنظومة المقترحة:* ${t}\n📈 *العائد الاستثماري:* ${o}\n\nأرغب باعتماد الخطة وحجز جلسة تنفيذ فورية.`;window.open(`https://wa.me/31618111116?text=${encodeURIComponent(msg)}`,"_blank"),"undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("success")}function dispatchBlueprintToTelegram(){const e=document.getElementById("blueprintAudioPlayer"),n=`خطة عمل تنفيذية معتمدة من S&R CoreSync AI Project Architect:\n🎯 ${e?decodeURIComponent(e.getAttribute("data-project-name")||""):"مشروع ذكي"}\n⚡ البنية: ${e?decodeURIComponent(e.getAttribute("data-sys-rec")||""):"بنية سحابية متقدمة"}\nللتواصل المباشر مع المؤسسين: https://t.me/SRCoreSync`,t=`https://t.me/share/url?url=${encodeURIComponent("https://sr-coresync.com")}&text=${encodeURIComponent(n)}`;window.open(t,"_blank"),"undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("success")}function openExecutiveCheckoutModal(e,n){const t=document.getElementById("srCheckoutModal");if(t){if(e){const n=document.getElementById("checkoutItemTitle");n&&(n.textContent=e)}if(n){const e=document.getElementById("checkoutAmountDisplay");e&&(e.innerHTML=`€${n}.00 <span style="font-size:12px; font-weight:normal; color:#94a3b8;">(BTW B2B Compliant)</span>`)}t.classList.add("active"),document.body.style.overflow="hidden","undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("open")}}function closeExecutiveCheckoutModal(){const e=document.getElementById("srCheckoutModal");e&&(e.classList.remove("active"),document.body.style.overflow="","undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("close"))}function selectPaymentMethod(e,n){document.querySelectorAll(".sr-checkout-method-btn").forEach(e=>e.classList.remove("active")),e.classList.add("active");const t=document.getElementById("checkoutBankSelect");t&&(t.style.display="ideal"===n?"block":"none"),"undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("click")}function processLiveCheckout(e){e.preventDefault();const n=document.getElementById("srLiveCheckoutSubmitBtn"),t=document.getElementById("checkoutSubmitBtnLabel"),o=document.getElementById("checkoutStatusMsg"),i=(document.getElementById("checkoutClientName").value,document.getElementById("checkoutClientEmail").value);n&&(n.disabled=!0),t&&(t.textContent="⏳ جاري الاتصال الآمن مع بوابة الدفع الأوروبية..."),o&&(o.style.display="block",o.style.background="rgba(197, 168, 128, 0.15)",o.style.color="#f3dfba",o.innerHTML="🔒 جاري تشفير المعاملة والتحقق من الحساب وتأكيد التسوية الفورية..."),setTimeout(()=>{const e="INV-2026-SR-"+Math.floor(1e3+9e3*Math.random());t&&(t.textContent="✓ تم تأكيد الدفع وإصدار الفاتورة!"),o&&(o.style.background="rgba(16, 185, 129, 0.2)",o.style.color="#4ade80",o.innerHTML=`🎉 <strong>تهانينا! تم تأكيد الدفع والتسوية بنجاح.</strong><br>رقم الفاتورة الرسمية: <strong>${e}</strong><br>تم إرسال إشعار التأكيد ووثائق الترخيص إلى ${i}. سيبدأ التنفيذ فوراً.`),"undefined"!=typeof LuxuryAudio&&LuxuryAudio.play("success"),setTimeout(()=>{closeExecutiveCheckoutModal(),n&&(n.disabled=!1),t&&(t.textContent="تأكيد الدفع والتسوية الفورية 🔒"),o&&(o.style.display="none")},4e3)},1600)}function exportBlueprintPdf(e){openBlueprintPreviewModal();setTimeout(()=>{window.print();},400);}function bookBlueprintConsultation(e){stopBlueprintAudioSynthesis(),closeAiVoicePlannerModal(),setTimeout(()=>{if("function"==typeof openExecutiveBookingModal){openExecutiveBookingModal("both");const n=document.getElementById("bookingClientNotes");n&&(n.value="أرغب بتنفيذ خطة العمل المتولدة بالصوت: "+e)}},300)}function notifyAiIdeaSubmitted(e){if(!e)return;try{localStorage.setItem("sr_last_ai_idea",e),localStorage.setItem("sr_last_ai_idea_time",(new Date).toISOString());const t=document.documentElement.getAttribute("lang")||"ar",n={event:"ai_idea_submitted",idea:e,lang:t,referrer:document.referrer||window.location.href,timestamp:(new Date).toISOString()};"function"==typeof window.dispatchLeadTelemetry?window.dispatchLeadTelemetry(n):navigator.sendBeacon&&navigator.sendBeacon("/api/lead-capture",JSON.stringify(n)),document.dispatchEvent(new CustomEvent("sr:ai-idea-submitted",{detail:n}))}catch(e){console.warn("[AI Idea Dispatch Notice]:",e)}}function fillHeroPromptSample(e){if(!e)return;const t=document.getElementById("heroAiIdeaInput");t&&(t.value=e);const n=document.getElementById("voicePlannerTranscript");n&&(n.value=e),notifyAiIdeaSubmitted(e),openAiVoicePlannerModal(),generateAiProjectBlueprint()}function submitHeroAiIdea(e){if(e&&e.preventDefault)e.preventDefault();const t=document.getElementById("heroAiIdeaInput"),n=t?t.value.trim():"",o=document.getElementById("voicePlannerTranscript");o&&n&&(o.value=n),n&&notifyAiIdeaSubmitted(n),openAiVoicePlannerModal(),n&&n.length>=3?generateAiProjectBlueprint():setTimeout((()=>{const e=document.getElementById("voicePlannerTranscript");e&&e.focus()}),300)}function openVoicePlannerFromHero(){openAiVoicePlannerModal(),setTimeout((()=>{startVoiceRecording()}),400)}window.submitHeroAiIdea=submitHeroAiIdea,window.openVoicePlannerFromHero=openVoicePlannerFromHero,window.fillHeroPromptSample=fillHeroPromptSample,window.notifyAiIdeaSubmitted=notifyAiIdeaSubmitted;

// =============================================================================
// S&R CoreSync - Multilingual Founder Speech & Sovereign A4 Preview Suite
// =============================================================================

const MULTILINGUAL_FOUNDER_SPEECH = {
    ar: {
        company: "شركة إس آند آر",
        salim: {
            name: "م. محمد سليم عزيزة",
            role: "كبير مهندسي السحابة والذكاء الاصطناعي",
            badge: "🎙️ صوت المهندس سليم الرقمي • AI Executive Audio",
            lead: "أهلاً بك، معك المهندس محمد سليم عزيزة، كبير مهندسي السحابة والذكاء الاصطناعي في شركة إس آند آر.",
            bookingGreeting: "أهلاً بك، معك المهندس محمد سليم عزيزة، كبير مهندسي السحابة والذكاء الاصطناعي في شركة إس آند آر. يسعدني مناقشة رؤيتكم الرقمية وهندسة البنية السحابية وتطبيقات الذكاء الاصطناعي الخاصة بكم في جلستنا القادمة. تفضل بتأكيد موعدك لنبدأ فوراً."
        },
        raed: {
            name: "أ. رائد كعكة",
            role: "المسؤول التنفيذي للعمليات وتطوير الأعمال",
            badge: "🎙️ صوت الأستاذ رائد الرقمي • AI Executive Audio",
            lead: "أهلاً بك، معك الأستاذ رائد كعكة، المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر.",
            bookingGreeting: "أهلاً بك، معك الأستاذ رائد كعكة، المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر. يسعدني مراجعة تحدياتكم المحاسبية، وتأسيس أنظمة الـ ERP والامتثال الضريبي الأوروبي لمؤسستكم في جلستنا القادمة. نحن هنا لضمان دقة ونمو أعمالكم."
        },
        both: {
            name: "الشركاء المؤسسون (سليم ورائد)",
            role: "جلسة استراتيجية مشتركة (هندسة برمجية + حوكمة مالية)",
            bookingGreeting: "أهلاً بكم في شركة إس آند آر. نتشرف بعقد جلسة استراتيجية مشتركة تجمع بين البنية الهندسية التقنية المتقدمة والحوكمة المالية وإدارة الأعمال لدفع مشروعكم نحو الريادة."
        },
        playAudio: "استمع للملخص الصوتي الذكي",
        stopAudio: "إيقاف الملخص الصوتي",
        blueprintPreview: "👁️ معاينة التقرير الرسمي A4 والختم السيادي",
        downloadPdf: "🖨️ طباعة وحفظ PDF فوري",
        whatsappConsult: "💬 استشارة فورية عبر WhatsApp",
        bookVip: "👔 حجز استشارة VIP"
    },
    nl: {
        company: "S&R",
        salim: {
            name: "Ir. Mohammad Salim Aziza",
            role: "Lead Cloud & AI Solutions Architect",
            badge: "🎙️ Digitale Stem Ir. Salim • AI Executive Audio",
            lead: "Welkom, ik ben Mohammad Salim Aziza, Lead Cloud en AI Architect bij S&R.",
            bookingGreeting: "Welkom, ik ben Mohammad Salim Aziza, Lead Cloud en AI Architect bij S&R. Ik kijk er naar uit om uw cloud-architectuur en AI-oplossingen te bespreken tijdens ons executive consult. Bevestig uw afspraak om direct te starten."
        },
        raed: {
            name: "Dhr. Raed Kaakeh",
            role: "Chief Operating Officer & Business Development",
            badge: "🎙️ Digitale Stem Dhr. Raed • AI Executive Audio",
            lead: "Welkom, ik ben Raed Kaakeh, Chief Operating Officer en Business Development bij S&R.",
            bookingGreeting: "Welkom, ik ben Raed Kaakeh, Chief Operating Officer en Business Development bij S&R. Ik help u graag bij het optimaliseren van uw ERP-systemen en Europese belasting- en BTW-compliance. Wij staan klaar voor uw groei."
        },
        both: {
            name: "Oprichters (Salim & Raed)",
            role: "Gezamenlijke Strategische Sessie (Cloud Architectuur + Bedrijfsvoering)",
            bookingGreeting: "Welkom bij S&R. Wij nodigen u van harte uit voor een gezamenlijke strategische sessie die geavanceerde cloud-engineering combineert met financiële en operationele governance."
        },
        playAudio: "Luister naar AI Executive Samenvatting",
        stopAudio: "Pauzeer Gesproken Samenvatting",
        blueprintPreview: "👁️ Bekijk A4 Rapport & Soeverein Zegel",
        downloadPdf: "🖨️ Print / Download Blueprint PDF",
        whatsappConsult: "💬 Direct WhatsApp Overleg",
        bookVip: "👔 Boek VIP Executive Consult"
    },
    de: {
        company: "S&R",
        salim: {
            name: "Ing. Mohammad Salim Aziza",
            role: "Leitender Cloud- & KI-Architekt",
            badge: "🎙️ Digitale Stimme Ing. Salim • AI Executive Audio",
            lead: "Herzlich willkommen, ich bin Mohammad Salim Aziza, Leitender Cloud- und KI-Architekt bei S&R.",
            bookingGreeting: "Herzlich willkommen, ich bin Mohammad Salim Aziza, Leitender Cloud- und KI-Architekt bei S&R. Gerne bespreche ich Ihre digitale Infrastruktur und maßgeschneiderte KI-Lösungen in unserem Beratungstermin."
        },
        raed: {
            name: "Hr. Raed Kaakeh",
            role: "Chief Operating Officer & Geschäftsentwicklung",
            badge: "🎙️ Digitale Stimme Hr. Raed • AI Executive Audio",
            lead: "Herzlich willkommen, ich bin Raed Kaakeh, Chief Operating Officer und Geschäftsentwicklung bei S&R.",
            bookingGreeting: "Herzlich willkommen, ich bin Raed Kaakeh, Chief Operating Officer und Geschäftsentwicklung bei S&R. Ich unterstütze Sie bei ERP-Integrationen und steuerlicher Compliance in Europa."
        },
        both: {
            name: "Gründer (Salim & Raed)",
            role: "Gemeinsame Strategiesitzung (Cloud-Engineering + Finanz-Governance)",
            bookingGreeting: "Herzlich willkommen bei S&R. Wir freuen uns auf eine gemeinsame Strategiesitzung zur Beschleunigung Ihrer digitalen und geschäftlichen Transformation."
        },
        playAudio: "Executive Audio-Zusammenfassung anhören",
        stopAudio: "Audio-Wiedergabe anhalten",
        blueprintPreview: "👁️ Offiziellen A4-Bericht & Siegel ansehen",
        downloadPdf: "🖨️ Blueprint als PDF drucken / speichern",
        whatsappConsult: "💬 Sofortberatung per WhatsApp",
        bookVip: "👔 VIP-Strategiesitzung buchen"
    },
    en: {
        company: "S&R",
        salim: {
            name: "Eng. Mohammad Salim Aziza",
            role: "Lead Cloud & AI Solutions Architect",
            badge: "🎙️ Digital Voice Eng. Salim • AI Executive Audio",
            lead: "Welcome, I am Eng. Mohammad Salim Aziza, Lead Cloud and AI Architect at S&R.",
            bookingGreeting: "Welcome, I am Eng. Mohammad Salim Aziza, Lead Cloud and AI Architect at S&R. I look forward to discussing your digital vision, sovereign cloud infrastructure, and custom AI agents during our executive session. Please confirm your booking to begin."
        },
        raed: {
            name: "Mr. Raed Kaakeh",
            role: "Chief Operating Officer & Head of Business Development",
            badge: "🎙️ Digital Voice Mr. Raed • AI Executive Audio",
            lead: "Welcome, I am Raed Kaakeh, Chief Operating Officer and Head of Business Development at S&R.",
            bookingGreeting: "Welcome, I am Raed Kaakeh, Chief Operating Officer and Head of Business Development at S&R. I look forward to reviewing your financial architecture, ERP systems, and European BTW/VAT compliance during our executive session. We are committed to your operational growth."
        },
        both: {
            name: "Founding Partners (Salim & Raed)",
            role: "Joint Strategic Consultation (Cloud Engineering + Financial Governance)",
            bookingGreeting: "Welcome to S&R. We look forward to hosting you in a joint executive session combining advanced enterprise cloud engineering with European financial and operational governance."
        },
        playAudio: "Listen to AI Executive Audio Summary",
        stopAudio: "Pause Audio Summary",
        blueprintPreview: "👁️ Preview Official A4 Dossier & Sovereign Seal",
        downloadPdf: "🖨️ Print / Download Executive Blueprint PDF",
        whatsappConsult: "💬 Instant WhatsApp Consultation",
        bookVip: "👔 Book VIP Executive Session"
    }
};

let isBookingGreetingSpeaking = false;
let currentBookingUtterance = null;

function stopBookingAudioGreeting() {
    isBookingGreetingSpeaking = false;
    if ("speechSynthesis" in window) {
        try { window.speechSynthesis.cancel(); } catch(e) {}
    }
    const strip = document.getElementById("bookingAudioGreetingStrip");
    if (strip) strip.classList.remove("is-playing");
    const btnText = document.getElementById("bookingAudioPlayBtnText");
    const btnIcon = document.getElementById("bookingAudioPlayBtnIcon");
    const docLang = (document.documentElement.getAttribute("lang") || "ar").toLowerCase();
    const isAr = docLang.startsWith("ar");
    if (btnText) btnText.textContent = isAr ? "استمع للرسالة الصوتية 🎙️" : "Listen to Audio Greeting 🎙️";
    if (btnIcon) btnIcon.textContent = "🎙️";
}

function toggleBookingAudioGreeting() {
    if (isBookingGreetingSpeaking) {
        stopBookingAudioGreeting();
        return;
    }
    if (!("speechSynthesis" in window)) {
        alert("Speech synthesis is not supported in this browser.");
        return;
    }
    stopBookingAudioGreeting();
    if (typeof stopBlueprintAudioSynthesis === "function") stopBlueprintAudioSynthesis();

    const docLang = (document.documentElement.getAttribute("lang") || "ar").toLowerCase();
    let lk = "en";
    if (docLang.startsWith("ar")) lk = "ar";
    else if (docLang.startsWith("nl")) lk = "nl";
    else if (docLang.startsWith("de")) lk = "de";

    const langData = MULTILINGUAL_FOUNDER_SPEECH[lk] || MULTILINGUAL_FOUNDER_SPEECH.en;
    const advisorField = document.getElementById("selectedAdvisorField");
    const advisor = advisorField ? advisorField.value : "salim";
    const advisorData = langData[advisor] || langData.salim;
    const greetingText = advisorData.bookingGreeting || advisorData.lead;

    const utt = new SpeechSynthesisUtterance(greetingText);
    currentBookingUtterance = utt;
    utt.rate = 0.95;
    utt.pitch = 0.88;

    let targetLangPrefix = "ar";
    let langCode = "ar-SA";
    if (lk === "nl") { targetLangPrefix = "nl"; langCode = "nl-NL"; }
    else if (lk === "de") { targetLangPrefix = "de"; langCode = "de-DE"; }
    else if (lk === "en") { targetLangPrefix = "en"; langCode = "en-US"; }
    utt.lang = langCode;

    const femaleKeywords = [
        "فاطمة", "ليلى", "أمينة", "سلمى", "رنا", "سناء", "نورا", "إيمان", "منى", "عائشة", "أمل", "زارية", "أماني", "ريم", "مريم", "هدى", "هدا", "زينب", "سارة", "أنثى",
        "laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman", "girl", "zira", "susan", "hazel", "linda", "eva", "katja", "hedda"
    ];
    const malePreferred = [
        "شاكر", "حامد", "ليث", "باسل", "علي", "إسماعيل", "تيم", "فهد", "رامي", "أحمد", "جمال", "عبدالله", "معاذ", "هادي", "صالح", "ماجد", "طارق", "نايف", "زيد", "رائد", "سليم",
        "shakir", "hamed", "laith", "basel", "ali", "ismail", "taim", "fahd", "rami", "ahmed", "jamal", "abdullah", "moath", "hadi", "saleh", "maged", "tarik", "naayf", "male",
        "david", "mark", "george", "guy", "james", "bart", "stefan", "frank", "bernd", "conrad"
    ];
    const allVoices = (window.speechSynthesis && window.speechSynthesis.getVoices) ? window.speechSynthesis.getVoices() : [];
    const targetVoices = allVoices.filter(v => (v.lang || "").toLowerCase().startsWith(targetLangPrefix));

    let matchedVoice = targetVoices.find(v => {
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

    window.speechSynthesis.speak(utt);
}

function openBlueprintPreviewModal() {
    let modal = document.getElementById("srBlueprintPreviewModal");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "srBlueprintPreviewModal";
        modal.className = "sr-a4-preview-modal";
        modal.setAttribute("role", "dialog");
        modal.setAttribute("aria-modal", "true");
        modal.innerHTML = `
            <div class="sr-exec-modal-backdrop" data-sr-call="closeBlueprintPreviewModal"></div>
            <div class="sr-a4-preview-wrapper">
                <div class="sr-a4-toolbar">
                    <div class="sr-a4-toolbar-title">
                        <span>🏛️ وثيقة دراسة الجدوى والمعمارية التنفيذية 2026 (A4 Sovereign Dossier)</span>
                    </div>
                    <div class="sr-a4-toolbar-actions">
                        <button type="button" class="sr-a4-btn-action sr-a4-btn-print" data-sr-call="exportBlueprintPdf">🖨️ طباعة / حفظ PDF فوري</button>
                        <button type="button" class="sr-a4-btn-action sr-a4-btn-close" data-sr-call="closeBlueprintPreviewModal">✖️ إغلاق</button>
                    </div>
                </div>
                <div class="sr-a4-sheet" id="srA4SheetContent"></div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    const player = document.getElementById("blueprintAudioPlayer");
    const projectName = player ? decodeURIComponent(player.getAttribute("data-project-name") || "") : "مشروع التحول الرقمي السحابي 2026";
    const sysRec = player ? decodeURIComponent(player.getAttribute("data-sys-rec") || "") : "بنية سحابية سيادية متكاملة";
    const roiVal = player ? decodeURIComponent(player.getAttribute("data-roi-value") || "") : "+42% توفير بالتكاليف التشغيلية و 3.8x سرعة في إنجاز العمليات";
    const founderType = player ? player.getAttribute("data-founder-type") : "salim";
    const isRaed = founderType === "raed";

    const docLang = (document.documentElement.getAttribute("lang") || "ar").toLowerCase();
    const isAr = docLang.startsWith("ar");
    const lk = isAr ? "ar" : (docLang.startsWith("nl") ? "nl" : (docLang.startsWith("de") ? "de" : "en"));
    const langData = MULTILINGUAL_FOUNDER_SPEECH[lk] || MULTILINGUAL_FOUNDER_SPEECH.en;
    const founder = isRaed ? langData.raed : langData.salim;
    
    const assetPrefix = window.location.pathname.includes("/en/") || window.location.pathname.includes("/nl/") || window.location.pathname.includes("/de/") || window.location.pathname.split("/").filter(Boolean).length > 1 ? "../assets/" : "./assets/";
    const founderImg = assetPrefix + (isRaed ? "founder-raed.webp" : "founder-salim.webp");
    const emblemImg = assetPrefix + "sr-emblem-gold-luxury-4k.jpg";
    const randomRef = "SR-DOC-2026-" + Math.floor(10000 + Math.random() * 90000);
    const currentDate = new Date().toLocaleDateString(isAr ? 'ar-EG' : 'en-GB', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    });

    const sheet = document.getElementById("srA4SheetContent");
    if (sheet) {
        sheet.innerHTML = `
            <div class="sr-a4-watermark">S&amp;R CORESYNC</div>
            <div class="sr-a4-sheet-header">
                <div class="sr-a4-brand-logo">
                    <img src="${emblemImg}" alt="S&amp;R Emblem" width="52" height="52">
                    <div class="sr-a4-brand-text">
                        <h2>S&amp;R CoreSync For Intelligent Solutions B.V.</h2>
                        <p>${isAr ? 'وثيقة الاعتماد الهندسي والدراسة التنفيذية للمشاريع الرقمية 2026' : 'Official Architectural Certification & Feasibility Blueprint 2026'}</p>
                        <p style="font-size:0.7rem; color:#64748b;">Keizersgracht 482, 1016 EG Amsterdam, The Netherlands • KvK &amp; BTW Registered</p>
                    </div>
                </div>
                <div class="sr-a4-doc-meta">
                    <div class="sr-a4-doc-ref">${randomRef}</div><br>
                    <span class="sr-a4-confidential-badge">SOVEREIGN CLASSIFICATION TIER-1</span>
                    <div style="margin-top:4px; font-size:0.72rem; color:#64748b;">${currentDate} • Amsterdam CET</div>
                </div>
            </div>

            <div class="sr-a4-sheet-body">
                <div class="sr-a4-section-title">${isAr ? 'ملخص المشروع ومواصفات المنظومة المقترحة' : 'Project Executive Summary & Architectural Blueprint'}</div>
                <div class="sr-a4-grid-2">
                    <div class="sr-a4-card-box">
                        <div class="sr-a4-card-label">${isAr ? 'اسم المنظومة المعتمدة' : 'Approved Solution Name'}</div>
                        <div class="sr-a4-card-val">${projectName}</div>
                    </div>
                    <div class="sr-a4-card-box">
                        <div class="sr-a4-card-label">${isAr ? 'القطاع الاستراتيجي' : 'Strategic Domain'}</div>
                        <div class="sr-a4-card-val">${isRaed ? (isAr ? 'الأنظمة المالية والـ ERP والضرائب وسلاسل التوريد' : 'Enterprise ERP, Finance, BTW & Supply Chain') : (isAr ? 'البنية السحابية وهندسة الذكاء الاصطناعي والتطبيقات' : 'Cloud Architecture, Custom AI & FinTech')}</div>
                    </div>
                </div>

                <div class="sr-a4-section-title">${isAr ? 'مكونات البنية التحتية والتقنيات الهندسية' : 'Technical Architecture & Infrastructure Stack'}</div>
                <table class="sr-a4-table">
                    <thead>
                        <tr>
                            <th>${isAr ? 'المستوى الهندسي' : 'Architecture Layer'}</th>
                            <th>${isAr ? 'المواصفات التقنية السيادية المعتمدة' : 'Approved Enterprise Specifications'}</th>
                            <th>${isAr ? 'مؤشر الأداء' : 'SLA & Performance'}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>${isAr ? 'البنية التحتية السحابية' : 'Cloud Infrastructure'}</strong></td>
                            <td>${sysRec}</td>
                            <td>99.99% Uptime • Zero-Trust</td>
                        </tr>
                        <tr>
                            <td><strong>${isAr ? 'الأمان والامتثال الأوروبي' : 'Security & EU Compliance'}</strong></td>
                            <td>${isAr ? 'تشفير متقدم AES-256-GCM مع الامتثال التام للـ GDPR والقوانين التجارية الهولندية' : 'Advanced AES-256-GCM encryption with strict GDPR & Dutch Dutch corporate compliance'}</td>
                            <td>ISO 27001 / GDPR Ready</td>
                        </tr>
                        <tr>
                            <td><strong>${isAr ? 'العائد الاستثماري المتوقع' : 'Projected ROI & Cost Reduction'}</strong></td>
                            <td>${roiVal}</td>
                            <td>3.8x Acceleration</td>
                        </tr>
                    </tbody>
                </table>

                <div class="sr-a4-endorsement-strip">
                    <div class="sr-a4-founder-sign-box">
                        <img src="${founderImg}" alt="${founder.name}" class="sr-a4-founder-sign-img">
                        <div>
                            <div class="sr-a4-founder-sign-name">${founder.name}</div>
                            <div class="sr-a4-founder-sign-role">${founder.role} • S&amp;R CoreSync Amsterdam</div>
                            <div style="font-size:0.72rem; color:#10b981; font-weight:700; margin-top:2px;">✓ ${isAr ? 'معتمد وموقع رقمياً (Cryptographically Verified Endorsement)' : 'Cryptographically Verified Executive Endorsement'}</div>
                        </div>
                    </div>
                    <div class="sr-a4-official-seal">
                        <span class="sr-a4-seal-title">S&amp;R CORESYNC</span>
                        <span class="sr-a4-seal-star">★ ★ ★</span>
                        <span class="sr-a4-seal-sub">AMSTERDAM SEAL 2026</span>
                    </div>
                </div>
            </div>

            <div class="sr-a4-sheet-footer">
                <div>© 2026 S&amp;R CoreSync For Intelligent Solutions B.V. All rights reserved. Proprietary &amp; Confidential.</div>
                <div style="font-weight:700; color:#0f172a;">https://sr-coresync.com</div>
            </div>
        `;
    }

    modal.classList.add("active");
    document.body.style.overflow = "hidden";
}

function closeBlueprintPreviewModal() {
    const modal = document.getElementById("srBlueprintPreviewModal");
    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "";
    }
}

// Attach functions to global window for Strict CSP
window.MULTILINGUAL_FOUNDER_SPEECH = MULTILINGUAL_FOUNDER_SPEECH;
window.toggleBookingAudioGreeting = toggleBookingAudioGreeting;
window.stopBookingAudioGreeting = stopBookingAudioGreeting;
window.openBlueprintPreviewModal = openBlueprintPreviewModal;
window.closeBlueprintPreviewModal = closeBlueprintPreviewModal;
