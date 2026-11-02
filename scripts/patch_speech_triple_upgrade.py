"""
Script to patch js/sr-inline-13eaa28e.js with:
- Multilingual founder speech (AR, NL, DE, EN)
- Booking modal audio greeting (toggleBookingAudioGreeting & stopBookingAudioGreeting)
- Sovereign A4 Blueprint Preview Modal (openBlueprintPreviewModal & closeBlueprintPreviewModal)
- Export PDF linking to A4 modal
- Strict-CSP compliance (all functions exposed on window)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, 'js', 'sr-inline-13eaa28e.js')

with open(TARGET, 'r', encoding='utf-8') as f:
    code = f.read()

triple_upgrade_js = """
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
            name: "أ. رائد عزيزة",
            role: "المسؤول التنفيذي للعمليات وتطوير الأعمال",
            badge: "🎙️ صوت الأستاذ رائد الرقمي • AI Executive Audio",
            lead: "أهلاً بك، معك الأستاذ رائد عزيزة، المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر.",
            bookingGreeting: "أهلاً بك، معك الأستاذ رائد عزيزة، المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر. يسعدني مراجعة تحدياتكم المحاسبية، وتأسيس أنظمة الـ ERP والامتثال الضريبي الأوروبي لمؤسستكم في جلستنا القادمة. نحن هنا لضمان دقة ونمو أعمالكم."
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
            name: "Dhr. Raed Aziza",
            role: "Chief Operating Officer & Business Development",
            badge: "🎙️ Digitale Stem Dhr. Raed • AI Executive Audio",
            lead: "Welkom, ik ben Raed Aziza, Chief Operating Officer en Business Development bij S&R.",
            bookingGreeting: "Welkom, ik ben Raed Aziza, Chief Operating Officer en Business Development bij S&R. Ik help u graag bij het optimaliseren van uw ERP-systemen en Europese belasting- en BTW-compliance. Wij staan klaar voor uw groei."
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
            name: "Hr. Raed Aziza",
            role: "Chief Operating Officer & Geschäftsentwicklung",
            badge: "🎙️ Digitale Stimme Hr. Raed • AI Executive Audio",
            lead: "Herzlich willkommen, ich bin Raed Aziza, Chief Operating Officer und Geschäftsentwicklung bei S&R.",
            bookingGreeting: "Herzlich willkommen, ich bin Raed Aziza, Chief Operating Officer und Geschäftsentwicklung bei S&R. Ich unterstütze Sie bei ERP-Integrationen und steuerlicher Compliance in Europa."
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
            name: "Mr. Raed Aziza",
            role: "Chief Operating Officer & Head of Business Development",
            badge: "🎙️ Digital Voice Mr. Raed • AI Executive Audio",
            lead: "Welcome, I am Raed Aziza, Chief Operating Officer and Head of Business Development at S&R.",
            bookingGreeting: "Welcome, I am Raed Aziza, Chief Operating Officer and Head of Business Development at S&R. I look forward to reviewing your financial architecture, ERP systems, and European BTW/VAT compliance during our executive session. We are committed to your operational growth."
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

    const femaleKeywords = ["laila", "zeina", "salma", "hoda", "maryam", "fatima", "yasmin", "zari", "sara", "noor", "female", "woman", "zira", "susan", "hazel", "linda", "eva", "katja", "hedda"];
    const malePreferred = ["maged", "tarik", "naayf", "shakir", "zayd", "hamed", "bassam", "male", "david", "mark", "george", "guy", "james", "bart", "stefan", "frank", "bernd", "conrad"];
    const allVoices = window.speechSynthesis.getVoices ? window.speechSynthesis.getVoices() : [];

    let matchedVoice = allVoices.find(v => {
        const n = (v.name || "").toLowerCase();
        const l = (v.lang || "").toLowerCase();
        return l.startsWith(targetLangPrefix) && malePreferred.some(m => n.includes(m)) && !femaleKeywords.some(f => n.includes(f));
    });
    if (!matchedVoice) {
        matchedVoice = allVoices.find(v => {
            const n = (v.name || "").toLowerCase();
            const l = (v.lang || "").toLowerCase();
            return l.startsWith(targetLangPrefix) && !femaleKeywords.some(f => n.includes(f));
        });
    }
    if (!matchedVoice) {
        matchedVoice = allVoices.find(v => (v.lang || "").toLowerCase().startsWith(targetLangPrefix));
    }
    if (matchedVoice) utt.voice = matchedVoice;

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
"""

# Now replace exportBlueprintPdf to ensure A4 sheet is open before printing
code = code.replace(
    'function exportBlueprintPdf(e){window.print()}',
    'function exportBlueprintPdf(e){openBlueprintPreviewModal();setTimeout(()=>{window.print();},400);}'
)

# Append the suite if not present
if 'MULTILINGUAL_FOUNDER_SPEECH' not in code:
    code += "\n" + triple_upgrade_js
    print("Appended MULTILINGUAL_FOUNDER_SPEECH and A4 Preview Suite to js/sr-inline-13eaa28e.js")
else:
    print("MULTILINGUAL_FOUNDER_SPEECH already in js/sr-inline-13eaa28e.js")

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated js/sr-inline-13eaa28e.js")
