# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
Integrate Interactive Live Simulators for S&R CivicSync, S&R HealthBridge, and S&R OmniBakery
into js/sr-software-apps.js and update cards across all portals.
"""

def read_file(p):
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(p, c):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

js_path = 'js/sr-software-apps.js'
js = read_file(js_path)

# 1. Add platform app definitions to SOFTWARE_APPS
platforms_apps_def = """        civicsync: {
            id: 'civicsync',
            title: 'S&R CivicSync™ Community OS',
            version: 'v2.6 White-Label',
            category: 'منصات White-Label السيادية',
            icon: '🌐',
            defaultKey: 'SR-CIVIC-SYNC-2026-WL-PRO',
            price: 'عرض سعر مخصص',
            priceType: 'ترخيص مؤسسي / جهة',
            desc: 'منظومة عامة لإدارة الجاليات والمنظمات: مساعد قانوني ذكي RAG، بطاقات عضوية رقمية QR، خزانة مستندات آمنة، ودليل فعاليات.',
            offlineFile: 'preview-work.html#platforms-civicsync'
        },
        healthbridge: {
            id: 'healthbridge',
            title: 'S&R HealthBridge™ Telehealth Suite',
            version: 'v3.2 Clinical Suite',
            category: 'منصات White-Label السيادية',
            icon: '🏥',
            defaultKey: 'SR-HLTH-BRIDGE-2026-WL-PRO',
            price: 'عرض سعر مخصص',
            priceType: 'ترخيص عيادات وشبكات طبية',
            desc: 'منظومة العيادات والطب الاتصالي: استشارات فيديو WebRTC مشفرة، فحص تداخلات الأدوية، وحجز مواعيد وامتثال GDPR.',
            offlineFile: 'preview-work.html#platforms-healthbridge'
        },
        omnibakery: {
            id: 'omnibakery',
            title: 'S&R OmniBakery™ Fleet ERP',
            version: 'v4.0 POS & Fleet',
            category: 'منصات White-Label السيادية',
            icon: '🥖',
            defaultKey: 'SR-OMNI-BAKE-2026-WL-PRO',
            price: 'عرض سعر مخصص',
            priceType: 'ترخيص مخابز وتوزيع غذائي',
            desc: 'نظام كاشير لمسي سحابي أونلاين/أوفلاين، تتبع أسطول السائقين، وفواتير ضريبية BTW 9% و 21% متوافقة مع Belastingdienst.',
            offlineFile: 'preview-work.html#platforms-omnibakery'
        },
"""

if 'civicsync:' not in js:
    # Insert right before terminal definition
    term_marker = "terminal: {"
    js = js.replace(term_marker, platforms_apps_def + "        " + term_marker, 1)
    print("Added platforms to SOFTWARE_APPS in js/sr-software-apps.js")

# 2. Add platform buttons to subnavHtml
platform_subnav_buttons = """                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'civicsync' ? 'active' : ''}" onclick="openSoftwareLiveApp('civicsync', currentDeviceMode)">🌐 CivicSync™</button>
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'healthbridge' ? 'active' : ''}" onclick="openSoftwareLiveApp('healthbridge', currentDeviceMode)">🏥 HealthBridge™</button>
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'omnibakery' ? 'active' : ''}" onclick="openSoftwareLiveApp('omnibakery', currentDeviceMode)">🥖 OmniBakery™</button>
"""

subnav_marker = '<button type="button" class="sr-app-subnav-btn ${activeAppId === \'taxsync\' ? \'active\' : \'\'}" onclick="openSoftwareLiveApp(\'taxsync\', currentDeviceMode)">💻 TaxSync</button>'
if 'CivicSync™' not in js and subnav_marker in js:
    js = js.replace(subnav_marker, platform_subnav_buttons + '                    ' + subnav_marker, 1)
    print("Added platform buttons to subnavHtml")

# 3. Add platform rendering branches in renderActiveAppContent
branch_marker = "} else if (activeAppId === 'sdk') {"
platform_branches = """} else if (activeAppId === 'civicsync') {
            container.innerHTML = subnavHtml + renderCivicSyncHtml();
            initCivicSyncEvents();
        } else if (activeAppId === 'healthbridge') {
            container.innerHTML = subnavHtml + renderHealthBridgeHtml();
            initHealthBridgeEvents();
        } else if (activeAppId === 'omnibakery') {
            container.innerHTML = subnavHtml + renderOmniBakeryHtml();
            initOmniBakeryEvents();
        """

if 'activeAppId === \'civicsync\'' not in js and branch_marker in js:
    js = js.replace(branch_marker, platform_branches + branch_marker, 1)
    print("Added platform branches to renderActiveAppContent")

# 4. Append the HTML renderers and event handlers for the 3 platforms
platform_simulator_code = """
    // =============================================================
    // PLATFORM 1: S&R CivicSync™ Simulator (AI Legal RAG + Digital ID)
    // =============================================================
    function renderCivicSyncHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Left: RAG AI Legal Assistant -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>🤖 المساعد القانوني والإداري الذكي (Civic AI RAG)</span>
                        <span class="sr-app-header-ver">Ollama • Multilingual</span>
                    </h4>
                    <p style="font-size:0.8rem;color:#94a3b8;margin-bottom:12px;">
                        مساعد مدرب على القوانين واللوائح الإدارية (قوانين الإقامة، لم الشمل، والتجنيس في هولندا والاتحاد الأوروبي).
                    </p>
                    
                    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;">
                        <button type="button" class="sr-code-lang-pill" onclick="setCivicPrompt('ما هي شروط التقدم للجنسية الهولندية بعد 5 سنوات؟')">🇳🇱 شروط الجنسية</button>
                        <button type="button" class="sr-code-lang-pill" onclick="setCivicPrompt('كيف يتم توثيق عقود السكن والبلدية BSN؟')">📋 تسجيل BSN</button>
                        <button type="button" class="sr-code-lang-pill" onclick="setCivicPrompt('ما هي إجراءات لم شمل العائلة وفق IND؟')">👨‍👩‍👧 لم شمل الأسرة</button>
                    </div>

                    <div id="civicChatBox" style="background:#020604;border:1px solid rgba(197,168,128,0.2);border-radius:10px;padding:12px;height:220px;overflow-y:auto;display:flex;flex-direction:column;gap:8px;font-size:0.82rem;">
                        <div style="background:rgba(197,168,128,0.12);padding:8px 12px;border-radius:8px;border-inline-start:3px solid #c5a880;align-self:flex-start;max-width:90%;">
                            <strong>المساعد الذكي (CivicSync):</strong> مرحباً بكم! أنا مساعدكم القانوني الذكي في هولندا. كيف يمكنني خدمتكم اليوم بشأن الإجراءات أو الأوراق الرسمية؟
                        </div>
                    </div>

                    <div style="display:flex;gap:8px;margin-top:12px;">
                        <input type="text" id="civicChatInput" class="sr-app-input" placeholder="اكتب استفسارك القانوني أو الإداري هنا..." onkeypress="if(event.key==='Enter') sendCivicMessage()">
                        <button type="button" class="sr-hero-btn sr-hero-btn-primary" style="padding:8px 16px;font-size:0.85rem;" onclick="sendCivicMessage()">إرسال 🚀</button>
                    </div>
                </div>

                <!-- Right: Digital Membership Card Simulator -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>🪪 بطاقة العضوية الرقمية الذكية (Dynamic NFC & QR)</span>
                        <span class="sr-app-header-ver">Live Verify</span>
                    </h4>
                    
                    <div style="background:linear-gradient(135deg, #0a1f18 0%, #030806 100%);border:1px solid rgba(197,168,128,0.4);border-radius:16px;padding:18px;box-shadow:0 12px 30px rgba(0,0,0,0.6);position:relative;overflow:hidden;margin-bottom:14px;">
                        <div style="position:absolute;top:-20px;right:-20px;width:100px;height:100px;background:radial-gradient(circle,rgba(197,168,128,0.2),transparent 70%);pointer-events:none;"></div>
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <img src="./assets/sr-core-emblem.svg" width="24" height="24" alt="CivicSync">
                                <span style="font-size:0.85rem;font-weight:800;color:#dfc299;">S&R CivicSync™ Member</span>
                            </div>
                            <span style="font-size:0.7rem;font-weight:700;background:rgba(16,185,129,0.2);color:#34d399;border:1px solid rgba(16,185,129,0.4);padding:2px 8px;border-radius:99px;">عضوية نشطة ✓</span>
                        </div>
                        <div style="display:flex;gap:14px;align-items:center;">
                            <div style="width:58px;height:58px;border-radius:50%;background:rgba(197,168,128,0.2);border:2px solid #c5a880;display:flex;align-items:center;justify-content:center;font-size:1.8rem;">
                                👤
                            </div>
                            <div style="flex:1;">
                                <div id="cardMemberName" style="font-size:1rem;font-weight:800;color:#ffffff;">م. محمد الأحمد</div>
                                <div style="font-size:0.76rem;color:#cbd5e1;">الرقم التعريفي: <span style="font-family:monospace;color:#dfc299;" id="cardMemberId">NL-2026-8841</span></div>
                                <div style="font-size:0.74rem;color:#94a3b8;">المدينة: أمستردام • الصلاحية: 2026-2027</div>
                            </div>
                            <div style="text-align:center;background:#ffffff;padding:6px;border-radius:8px;">
                                <div style="font-size:1.8rem;line-height:1;">🏁</div>
                                <span style="font-size:0.6rem;color:#000;font-weight:700;display:block;">QR التحقق</span>
                            </div>
                        </div>
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label">تعديل اسم العضو لتجربة الإصدار الحي:</label>
                        <input type="text" id="inputMemberName" class="sr-app-input" value="م. محمد الأحمد" oninput="updateMemberCard(this.value)">
                    </div>

                    <div style="display:flex;gap:8px;">
                        <button type="button" class="btn-consult-advisor btn-advisor-salim" style="flex:1;" onclick="alert('✓ تم مسح رمز QR بنجاح: العضوية صالحة ومسجلة في قاعدة بيانات الجالية!')">
                            <span>🔍 تجربة مسح الـ QR</span>
                        </button>
                        <button type="button" class="btn-consult-email" onclick="alert('✓ تم تصدير بطاقة العضوية الرقمية بنجاح إلى محفظة Apple/Google Wallet!')">
                            <span>📲 حفظ في Wallet</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    function initCivicSyncEvents() {}

    window.setCivicPrompt = function(txt) {
        const inp = document.getElementById('civicChatInput');
        if (inp) inp.value = txt;
        window.sendCivicMessage();
    };

    window.sendCivicMessage = function() {
        const inp = document.getElementById('civicChatInput');
        const box = document.getElementById('civicChatBox');
        if (!inp || !box) return;
        const q = inp.value.trim();
        if (!q) return;

        box.innerHTML += `
            <div style="background:rgba(56,189,248,0.15);padding:8px 12px;border-radius:8px;border-inline-end:3px solid #38bdf8;align-self:flex-end;max-width:90%;color:#fff;">
                <strong>أنت:</strong> ${q}
            </div>
        `;
        inp.value = '';
        box.scrollTop = box.scrollHeight;

        let ans = "وفقاً للوائح الإقامة والاندماج الهولندية (IND)، فإن هذا الإجراء يتطلب استيفاء الشروط الأساسية واجتياز اختبارات الاندماج المدني (Inburgeringsexamen). في منظومة CivicSync، تتيح المنصة إرفاق المستندات مباشرة وتدقيقها آلياً قبل الرفع للجهات الرسمية.";
        if (q.includes('جنسية')) {
            ans = "شروط التقدم للجنسية الهولندية تشمل: إقامة قانونية لمدة 5 سنوات متواصلة مع تصريح ساري، اجتياز اختبار الاندماج المدني بمستوى B1 أو A2 حسب سنة البدء، وعدم وجود سجل جنائي خلال السنوات الأربع الماضية. تتيح لك المنصة متابعة ملفك خطوة بخطوة.";
        } else if (q.includes('BSN') || q.includes('سكن')) {
            ans = "تسجيل الـ BSN يتطلب حجز موعد لدى بلدية مقر إقامتك (Gemeente) وتقديم عقد إيجار موثق وجواز سفر ساري المفعول وشهادة الميلاد المترجمة والمصدقة. توفر منصة CivicSync دليلاً تفاعلياً لربطك فورياً بمستشاري الجالية المعتمدين.";
        }

        setTimeout(() => {
            box.innerHTML += `
                <div style="background:rgba(197,168,128,0.12);padding:8px 12px;border-radius:8px;border-inline-start:3px solid #c5a880;align-self:flex-start;max-width:90%;">
                    <strong>المساعد الذكي (CivicSync):</strong> ${ans}
                </div>
            `;
            box.scrollTop = box.scrollHeight;
            playAppBeep(680, 'sine', 0.1);
        }, 500);
    };

    window.updateMemberCard = function(val) {
        const el = document.getElementById('cardMemberName');
        if (el) el.innerText = val || 'اسم العضو';
    };


    // =============================================================
    // PLATFORM 2: S&R HealthBridge™ Simulator (Telehealth WebRTC + Drugs)
    // =============================================================
    function renderHealthBridgeHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Left: Telehealth Call Simulation -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>🩺 عيادة الاستشارة الافتراضية (Live WebRTC Video)</span>
                        <span class="sr-app-header-ver" style="color:#10b981;">● متصل الآن</span>
                    </h4>
                    
                    <div style="background:#020705;border:1px solid rgba(16,185,129,0.3);border-radius:14px;position:relative;height:240px;overflow:hidden;display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                        <div style="position:absolute;inset:0;background:radial-gradient(circle at center, rgba(16,185,129,0.15), transparent 70%);"></div>
                        <div style="text-align:center;z-index:2;">
                            <div style="width:70px;height:70px;border-radius:50%;background:rgba(16,185,129,0.2);border:2px solid #10b981;display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 10px auto;box-shadow:0 0 20px rgba(16,185,129,0.4);">
                                👨‍⚕️
                            </div>
                            <h5 style="color:#ffffff;margin:0 0 4px 0;font-size:1rem;font-weight:800;">د. يان دي يونغ (Dr. Jan de Jong)</h5>
                            <span style="color:#7dd3fc;font-size:0.78rem;">استشاري أمراض الباطنة والقلب • BIG-register: 490281</span>
                            <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(0,0,0,0.6);padding:3px 10px;border-radius:99px;margin-top:8px;font-family:monospace;color:#34d399;font-size:0.75rem;">
                                ⏱️ مدة الجلسة: <span id="telehealthTimer">04:18</span>
                            </div>
                        </div>

                        <!-- Mini PIP patient camera -->
                        <div style="position:absolute;bottom:12px;right:12px;width:75px;height:55px;background:#06140e;border:1px solid rgba(255,255,255,0.3);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;box-shadow:0 4px 12px rgba(0,0,0,0.8);">
                            🤳
                        </div>
                    </div>

                    <!-- Call HUD controls -->
                    <div style="display:flex;justify-content:center;gap:12px;margin-bottom:12px;">
                        <button type="button" class="sr-app-btn" style="background:rgba(255,255,255,0.1);color:#fff;border-radius:50%;width:38px;height:38px;padding:0;display:flex;align-items:center;justify-content:center;" title="كتم الميكروفون">🎙️</button>
                        <button type="button" class="sr-app-btn" style="background:rgba(255,255,255,0.1);color:#fff;border-radius:50%;width:38px;height:38px;padding:0;display:flex;align-items:center;justify-content:center;" title="تبديل الكاميرا">📹</button>
                        <button type="button" class="sr-app-btn" style="background:rgba(16,185,129,0.25);color:#34d399;border:1px solid #10b981;border-radius:20px;padding:6px 14px;font-size:0.8rem;font-weight:700;" onclick="alert('✓ تم إصدار الوصفة الطبية المشفرة وإرسالها للصيدلية المركزية!')">
                            📝 إصدار وصفة إلكترونية
                        </button>
                    </div>

                    <div style="display:flex;justify-content:space-between;background:rgba(255,255,255,0.03);padding:8px 12px;border-radius:8px;font-size:0.76rem;color:#cbd5e1;">
                        <span>تشفير المكالمة: <strong>AES-256 WebRTC</strong></span>
                        <span>الامتثال: <strong style="color:#10b981;">EU GDPR & NEN 7510</strong></span>
                    </div>
                </div>

                <!-- Right: Drug Interaction Safety Checker -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>💊 فحص أمان التداخلات الدوائية (Drug Safety)</span>
                        <span class="sr-app-header-ver">AI Check</span>
                    </h4>
                    <p style="font-size:0.8rem;color:#94a3b8;margin-bottom:12px;">
                        تحليل تلقائي فوري قبل صرف الدواء لمنع أي تداخلات خطيرة بين الأدوية المزمنة والموصوفة.
                    </p>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label">الدواء الأول (العلاج الحالي):</label>
                        <select id="drug1" class="sr-app-input" onchange="checkDrugSafety()">
                            <option value="warfarin">وارفارين (Warfarin - مضاد تخثر)</option>
                            <option value="metformin">ميتفورمين (Metformin - سكري)</option>
                            <option value="lisinopril">ليزينوبريل (Lisinopril - ضغط دم)</option>
                        </select>
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label">الدواء الثاني (المراد وصفه):</label>
                        <select id="drug2" class="sr-app-input" onchange="checkDrugSafety()">
                            <option value="aspirin">أسبرين (Aspirin - مسكن)</option>
                            <option value="ibuprofen">إيبوبروفين (Ibuprofen - مضاد التهاب)</option>
                            <option value="paracetamol" selected>باراسيتامول (Paracetamol)</option>
                        </select>
                    </div>

                    <div id="drugSafetyResult" style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.4);border-radius:10px;padding:12px;margin-top:14px;">
                        <div style="display:flex;align-items:center;gap:8px;color:#34d399;font-weight:700;font-size:0.88rem;margin-bottom:4px;">
                            <span>✓ آمن ومسموح بالصرف</span>
                        </div>
                        <p style="font-size:0.78rem;color:#cbd5e1;margin:0;">لا يوجد تعارض حرج مسجل بين الدوائين المحددين بالجرعات العلاجية القياسية.</p>
                    </div>

                    <div style="margin-top:16px;">
                        <button type="button" class="sr-hero-btn sr-hero-btn-primary" style="width:100%;justify-content:center;" onclick="alert('✓ تم اعتماد صرف الدواء وتسجيله في سجل المريض الطبي NEN-7510!')">
                            صرف الدواء وتأكيد الحجز 📋
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    function initHealthBridgeEvents() {}

    window.checkDrugSafety = function() {
        const d1 = document.getElementById('drug1')?.value;
        const d2 = document.getElementById('drug2')?.value;
        const res = document.getElementById('drugSafetyResult');
        if (!res) return;

        if ((d1 === 'warfarin' && d2 === 'aspirin') || (d1 === 'warfarin' && d2 === 'ibuprofen')) {
            res.style.background = 'rgba(239,68,68,0.15)';
            res.style.borderColor = 'rgba(239,68,68,0.5)';
            res.innerHTML = `
                <div style="display:flex;align-items:center;gap:8px;color:#f87171;font-weight:800;font-size:0.88rem;margin-bottom:4px;">
                    <span>⚠️ تحذير: تداخل عالي الخطورة!</span>
                </div>
                <p style="font-size:0.78rem;color:#fecaca;margin:0;">الجمع بين مضاد التخثر ومضاد الالتهاب غير الستيرويدي يرفع خطر النزيف بشكل حرج. يُوصى باستبداله بالباراسيتامول أو مراجعة الطبيب المعالج.</p>
            `;
            playAppBeep(350, 'sawtooth', 0.2);
        } else {
            res.style.background = 'rgba(16,185,129,0.12)';
            res.style.borderColor = 'rgba(16,185,129,0.4)';
            res.innerHTML = `
                <div style="display:flex;align-items:center;gap:8px;color:#34d399;font-weight:700;font-size:0.88rem;margin-bottom:4px;">
                    <span>✓ آمن ومسموح بالصرف</span>
                </div>
                <p style="font-size:0.78rem;color:#cbd5e1;margin:0;">لا يوجد تعارض حرج مسجل بين الدوائين المحددين بالجرعات العلاجية القياسية وفق المعايير السريرية الأوروبية.</p>
            `;
            playAppBeep(620, 'sine', 0.1);
        }
    };


    // =============================================================
    // PLATFORM 3: S&R OmniBakery™ Simulator (Touch POS & BTW Thermal Receipt)
    // =============================================================
    let bakeryCart = [
        { name: 'مناقيش زعتر وجبنة', price: 3.50, qty: 2, btw: 9 },
        { name: 'خبز سوري تنور (5 ربطات)', price: 6.00, qty: 1, btw: 9 }
    ];

    function renderOmniBakeryHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Left: Touch POS Terminal Menu -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>🥖 نقطة البيع السحابية اللمسية (Bakery Touch POS)</span>
                        <span class="sr-app-header-ver">BTW 9% & 21%</span>
                    </h4>
                    <p style="font-size:0.8rem;color:#94a3b8;margin-bottom:12px;">انقر على المنتجات لإضافتها لسلة الكاشير وتوليد الفاتورة الضريبية فوراً:</p>

                    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(125px,1fr));gap:10px;margin-bottom:14px;">
                        <div class="sr-pos-product-card" onclick="addBakeryItem('مناقيش زعتر وجبنة', 3.50, 9)">
                            <div class="sr-pos-product-icon">🍕</div>
                            <div class="sr-pos-product-name">مناقيش زعتر وجبنة</div>
                            <div class="sr-pos-product-price">€ 3.50</div>
                            <div class="sr-pos-product-vat">BTW 9%</div>
                        </div>
                        <div class="sr-pos-product-card" onclick="addBakeryItem('فطائر سبانخ (دزينة)', 4.50, 9)">
                            <div class="sr-pos-product-icon">🥟</div>
                            <div class="sr-pos-product-name">فطائر سبانخ (12)</div>
                            <div class="sr-pos-product-price">€ 4.50</div>
                            <div class="sr-pos-product-vat">BTW 9%</div>
                        </div>
                        <div class="sr-pos-product-card" onclick="addBakeryItem('خبز سوري تنور (5 ربطات)', 6.00, 9)">
                            <div class="sr-pos-product-icon">🫓</div>
                            <div class="sr-pos-product-name">خبز تنور (5 ربطات)</div>
                            <div class="sr-pos-product-price">€ 6.00</div>
                            <div class="sr-pos-product-vat">BTW 9%</div>
                        </div>
                        <div class="sr-pos-product-card" onclick="addBakeryItem('بقلاوة مشكلة 1 كغ', 18.50, 9)">
                            <div class="sr-pos-product-icon">🍯</div>
                            <div class="sr-pos-product-name">بقلاوة مشكلة (1كغ)</div>
                            <div class="sr-pos-product-price">€ 18.50</div>
                            <div class="sr-pos-product-vat">BTW 9%</div>
                        </div>
                        <div class="sr-pos-product-card" onclick="addBakeryItem('مشروبات غازية / شاي', 2.00, 21)">
                            <div class="sr-pos-product-icon">🥤</div>
                            <div class="sr-pos-product-name">مشروبات ومياه</div>
                            <div class="sr-pos-product-price">€ 2.00</div>
                            <div class="sr-pos-product-vat">BTW 21%</div>
                        </div>
                    </div>

                    <!-- Cart table -->
                    <div style="background:#020604;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:10px;max-height:160px;overflow-y:auto;font-size:0.8rem;margin-bottom:12px;">
                        <table style="width:100%;border-collapse:collapse;color:#cbd5e1;" id="bakeryCartTable">
                            <!-- Populated dynamically -->
                        </table>
                    </div>

                    <div style="display:flex;gap:8px;">
                        <button type="button" class="sr-hero-btn sr-hero-btn-primary" style="flex:1;justify-content:center;" onclick="printBakeryThermalReceipt()">
                            🖨️ طباعة فاتورة كاشير حرارية
                        </button>
                        <button type="button" class="btn-consult-email" onclick="clearBakeryCart()">
                            🗑️ تفريغ
                        </button>
                    </div>
                </div>

                <!-- Right: Realistic Thermal Receipt Preview -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>🧾 الفاتورة الضريبية الفورية (Belastingdienst Receipt)</span>
                        <span class="sr-app-header-ver">Kassabon</span>
                    </h4>

                    <div class="sr-thermal-receipt" id="bakeryThermalReceipt">
                        <div class="sr-receipt-center">
                            <strong style="font-size:0.95rem;display:block;">S&R OMNIBAKERY B.V.</strong>
                            <span style="font-size:0.74rem;">Bakkerij & Distributie Nederland</span><br>
                            <span style="font-size:0.72rem;">KvK: 89201948 • BTW: NL89201948B01</span><br>
                            <span style="font-size:0.7rem;color:#4b5563;">Datum: 21-10-2026 • Kassa #01</span>
                        </div>

                        <div id="thermalReceiptLines" style="margin:10px 0;border-bottom:1px dashed #6b7280;padding-bottom:8px;">
                            <!-- Lines rendered dynamically -->
                        </div>

                        <div style="display:flex;justify-content:space-between;font-weight:800;font-size:0.95rem;margin:8px 0;">
                            <span>TOTAAL (شامل الضريبة):</span>
                            <span id="thermalTotalAmount">€ 13.00</span>
                        </div>

                        <div style="font-size:0.72rem;color:#4b5563;border-top:1px dashed #9ca3af;padding-top:6px;margin-top:6px;">
                            <div style="display:flex;justify-content:space-between;">
                                <span>BTW 9% (Voeding):</span>
                                <span id="thermalBtw9">€ 1.07</span>
                            </div>
                            <div style="display:flex;justify-content:space-between;">
                                <span>BTW 21% (Overig):</span>
                                <span id="thermalBtw21">€ 0.00</span>
                            </div>
                        </div>

                        <div class="sr-receipt-barcode">
                            ||| | |||| | ||| |||| |
                        </div>
                        <div style="text-align:center;font-size:0.68rem;color:#6b7280;margin-top:4px;">
                            Bedankt voor uw bezoek! • شكراً لزيارتكم
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    function initOmniBakeryEvents() {
        updateBakeryCartUI();
    }

    window.addBakeryItem = function(name, price, btw) {
        const item = bakeryCart.find(i => i.name === name);
        if (item) {
            item.qty++;
        } else {
            bakeryCart.push({ name, price, qty: 1, btw });
        }
        updateBakeryCartUI();
        playAppBeep(750, 'sine', 0.08);
    };

    window.clearBakeryCart = function() {
        bakeryCart = [];
        updateBakeryCartUI();
    };

    function updateBakeryCartUI() {
        const tbl = document.getElementById('bakeryCartTable');
        const lines = document.getElementById('thermalReceiptLines');
        const totalEl = document.getElementById('thermalTotalAmount');
        const btw9El = document.getElementById('thermalBtw9');
        const btw21El = document.getElementById('thermalBtw21');

        if (!tbl || !lines) return;

        let total = 0;
        let base9 = 0;
        let base21 = 0;

        let tableHtml = '<tr><th style=\"text-align:right;padding:4px;\">الصنف</th><th style=\"text-align:center;\">الكمية</th><th style=\"text-align:left;\">السعر</th></tr>';
        let receiptHtml = '';

        bakeryCart.forEach(item => {
            const itemTotal = item.price * item.qty;
            total += itemTotal;
            if (item.btw === 9) base9 += itemTotal;
            if (item.btw === 21) base21 += itemTotal;

            tableHtml += `
                <tr style=\"border-top:1px solid rgba(255,255,255,0.05);\">
                    <td style=\"padding:4px;\">${item.name}</td>
                    <td style=\"text-align:center;\">${item.qty}x</td>
                    <td style=\"text-align:left;color:#c5a880;\">€ ${itemTotal.toFixed(2)}</td>
                </tr>
            `;

            receiptHtml += `
                <div style=\"display:flex;justify-content:space-between;font-size:0.78rem;\">
                    <span>${item.qty}x ${item.name}</span>
                    <span>€ ${itemTotal.toFixed(2)}</span>
                </div>
            `;
        });

        if (bakeryCart.length === 0) {
            tableHtml += '<tr><td colspan=\"3\" style=\"text-align:center;padding:12px;color:#64748b;\">السلة فارغة. انقر على منتج لإضافته.</td></tr>';
            receiptHtml = '<div style=\"text-align:center;color:#6b7280;font-size:0.75rem;\">لا توجد عناصر مضافة</div>';
        }

        tbl.innerHTML = tableHtml;
        lines.innerHTML = receiptHtml;

        const vat9 = base9 - (base9 / 1.09);
        const vat21 = base21 - (base21 / 1.21);

        if (totalEl) totalEl.innerText = '€ ' + total.toFixed(2);
        if (btw9El) btw9El.innerText = '€ ' + vat9.toFixed(2);
        if (btw21El) btw21El.innerText = '€ ' + vat21.toFixed(2);
    }

    window.printBakeryThermalReceipt = function() {
        playAppBeep(880, 'sine', 0.15);
        if (typeof showPortalToast === 'function') {
            showPortalToast('🖨️ جاري إرسال أمر الطباعة لطابعة الإيصالات الحرارية عبر شبكة الـ ESC/POS...');
        } else {
            alert('🖨️ تم إرسال أمر الطباعة بنجاح لطابعة الكاشير الحرارية المتوافقة مع معايير الضرائب الهولندية!');
        }
    };
"""

if 'renderCivicSyncHtml' not in js:
    js += platform_simulator_code
    print("Appended platform simulator renderers to js/sr-software-apps.js")

write_file(js_path, js)
print("Updated js/sr-software-apps.js successfully!")


# 5. Now update platform cards in preview-software.html and index.html
# Add `⚡ تشغيل فوري` button to CivicSync, HealthBridge, and OmniBakery cards!

def update_platform_card_buttons(filepath):
    c = read_file(filepath)
    modified = False

    # CivicSync button update
    old_civi_actions = """                                <div class="software-card-actions">
                                    <a href="#work" onclick="navigateToPlatformWork('civicsync'); return false;" class="software-btn-download" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>
                                </div>"""
    new_civi_actions = """                                <div class="software-card-actions">
                                    <button type="button" class="software-btn-download" onclick="openSoftwareLiveApp('civicsync')" title="تشغيل فوري تفاعلي في المتصفح">
                                        <span>⚡ تشغيل فوري</span>
                                    </button>
                                    <a href="#work" onclick="navigateToPlatformWork('civicsync'); return false;" class="btn-live-preview software-btn-sim" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>
                                </div>"""

    if old_civi_actions in c:
        c = c.replace(old_civi_actions, new_civi_actions)
        modified = True

    # HealthBridge button update
    old_hb_actions = """                                <div class="software-card-actions">
                                    <a href="#work" onclick="navigateToPlatformWork('healthbridge'); return false;" class="software-btn-download" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>
                                </div>"""
    new_hb_actions = """                                <div class="software-card-actions">
                                    <button type="button" class="software-btn-download" onclick="openSoftwareLiveApp('healthbridge')" title="تشغيل فوري تفاعلي في المتصفح">
                                        <span>⚡ تشغيل فوري</span>
                                    </button>
                                    <a href="#work" onclick="navigateToPlatformWork('healthbridge'); return false;" class="btn-live-preview software-btn-sim" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>
                                </div>"""

    if old_hb_actions in c:
        c = c.replace(old_hb_actions, new_hb_actions)
        modified = True

    # OmniBakery button update
    old_ob_actions = """                                <div class="software-card-actions">
                                    <a href="#work" onclick="navigateToPlatformWork('omnibakery'); return false;" class="software-btn-download" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>
                                </div>"""
    new_ob_actions = """                                <div class="software-card-actions">
                                    <button type="button" class="software-btn-download" onclick="openSoftwareLiveApp('omnibakery')" title="تشغيل فوري تفاعلي في المتصفح">
                                        <span>⚡ تشغيل فوري</span>
                                    </button>
                                    <a href="#work" onclick="navigateToPlatformWork('omnibakery'); return false;" class="btn-live-preview software-btn-sim" title="استعراض دراسة الحالة الكاملة">
                                        <span>📄 دراسة الحالة</span>
                                    </a>
                                </div>"""

    if old_ob_actions in c:
        c = c.replace(old_ob_actions, new_ob_actions)
        modified = True

    if modified:
        write_file(filepath, c)
        print(f"Updated platform card buttons in {filepath}")
    else:
        print(f"No button changes needed in {filepath}")

for path in ['preview-software.html', 'index.html', 'nl/index.html', 'en/index.html', 'de/index.html']:
    update_platform_card_buttons(path)

print("ALL PLATFORM SIMULATOR INTEGRATIONS COMPLETED!")
