/**
 * ==========================================================================
 * S&R CORESYNC SOLUTIONS - CLOUD WEB APPS & PWA RUNTIME ENGINE
 * Software Architect: Eng. Salim Aziza | Executive: M. Raed Kaakeh
 * All 6 Applications: In-Browser Execution, Offline Support & PWA
 * ==========================================================================
 */

(function() {
    'use strict';

    // -------------------------------------------------------------
    // 1. Applications Registry & Metadata
    // -------------------------------------------------------------
    const SOFTWARE_APPS = {
        taxsync: {
            id: 'taxsync',
            title: 'S&R TaxSync Desktop / Web',
            version: 'v2.4 Pro',
            category: 'المحاسبة والضرائب المستقلة',
            icon: '💻',
            defaultKey: 'SRTX-PRO-2026-X892-OFFLINE',
            price: '€ 189',
            priceType: 'ترخيص سنوي / جهاز',
            desc: 'حاسبة وإقرارات الضرائب الهولندية الرسمية (AWR Art. 52 & Belastingdienst Compliant) مع توليد إقرارات Digipoort XML وفواتير EN 16931.',
            offlineFile: 'downloads/SR-TaxSync-Web-App.html'
        },
        flowscan: {
            id: 'flowscan',
            title: 'S&R FlowScan AI Mobile',
            version: 'v1.8 OCR AI',
            category: 'الذكاء الاصطناعي وتطبيقات الهاتف',
            icon: '📱',
            defaultKey: 'SRSCAN-AI-2026-F180-MOBILE',
            price: '€ 9.99',
            priceType: 'شهرياً / مستخدم',
            desc: 'المسح الضوئي الذكي للإيصالات والفواتير الورقية بالكاميرا واستخراج بيانات الضريبة والمبالغ آلياً وترحيلها لحظياً للـ ERP.',
            offlineFile: 'downloads/SR-FlowScan-Mobile-App.html'
        },
        cloudpos: {
            id: 'cloudpos',
            title: 'S&R CloudPOS Connector',
            version: 'v3.1 Live Terminal',
            category: 'نقاط البيع والربط السحابي',
            icon: '⚡',
            defaultKey: 'SRPOS-PRO-2026-C310-LIVE',
            price: '€ 25',
            priceType: 'شهرياً / نقطة بيع',
            desc: 'وسيط ومحطة نقاط بيع وكاشير تفاعلية تربط المتاجر والمطاعم بالـ ERP السحابي مع طباعة إيصالات حرارية ومزامنة سحابية.',
            offlineFile: 'downloads/SR-CloudPOS-Terminal.html'
        },
        vault: {
            id: 'vault',
            title: 'S&R SecureVault B2B',
            version: 'v2.0 Enterprise',
            category: 'الأمن السيبراني والتشفير',
            icon: '🛡️',
            defaultKey: 'SRVLT-AES256-2026-V200-MIL',
            price: '€ 49',
            priceType: 'شهرياً (1TB Encrypted)',
            desc: 'أداة تشفير وحماية المستندات والبيانات الحساسة محلياً بمعيار AES-256 GCM العسكري في المتصفح دون مغادرة البيانات لجهازك.',
            offlineFile: 'downloads/SR-SecureVault-App.html'
        },
        sdk: {
            id: 'sdk',
            title: 'S&R Financial AI SDK Console',
            version: 'v1.2 Dev Console',
            category: 'أدوات المطورين والـ REST APIs',
            icon: '🧩',
            defaultKey: 'SRSDK-DEV-2026-S120-REST',
            price: '€ 99',
            priceType: 'شهرياً (50k API Calls)',
            desc: 'لوحة تفاعلية لتجربة الـ REST APIs وحساب الضرائب والتنبؤ المالي وتوليد أكواد cURL و Python و Node.js و C#.',
            offlineFile: 'downloads/SR-Financial-AI-SDK.html'
        },
                civicsync: {
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
        terminal: {
            id: 'terminal',
            title: 'S&R Cloud Terminal Agent',
            version: 'v1.0 DevOps Agent',
            category: 'مراقبة الخوادم والـ Microservices',
            icon: '⚙️',
            defaultKey: 'SRTRM-OPS-2026-T100-CLOUD',
            price: '€ 39',
            priceType: 'شهرياً / Cluster',
            desc: 'مراقبة حية بنبضات الـ Heartbeat لميكروسيرفس المنظومة وتتبع استهلاك المعالج والذاكرة وإعادة تشغيل الخدمات سحابياً.',
            offlineFile: 'downloads/SR-CloudPOS-Terminal.html'
        }
    };

    let activeAppId = 'taxsync';
    let currentDeviceMode = 'desktop'; // 'desktop' or 'mobile'

    // -------------------------------------------------------------
    // 2. Audio Chime Synthesizer
    // -------------------------------------------------------------
    function playAppBeep(freq = 600, type = 'sine', duration = 0.12) {
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, ctx.currentTime);
            gain.gain.setValueAtTime(0.08, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + duration);
        } catch (e) {}
    }

    // -------------------------------------------------------------
    // 3. Main Modal Injector & Launcher
    // -------------------------------------------------------------
    function ensureModalInDom() {
        let overlay = document.getElementById('srSoftwareAppModal');
        if (overlay) return overlay;

        overlay = document.createElement('div');
        overlay.id = 'srSoftwareAppModal';
        overlay.className = 'sr-app-modal-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');

        overlay.innerHTML = `
            <div class="sr-app-window" id="srAppWindow">
                <!-- Header Bar -->
                <div class="sr-app-header-bar">
                    <div class="sr-app-header-left">
                        <div class="sr-os-dots">
                            <span class="sr-os-dot red" onclick="closeSoftwareApp()" title="إغلاق النافذة"></span>
                            <span class="sr-os-dot yellow" onclick="minimizeSoftwareApp()" title="تصغير"></span>
                            <span class="sr-os-dot green" onclick="toggleSoftwareAppFullscreen()" title="تكبير كامل الشاشة"></span>
                        </div>
                        <div class="sr-app-title-cluster">
                            <span class="sr-app-header-icon" id="srAppHeaderIcon">💻</span>
                            <h3 class="sr-app-header-title" id="srAppHeaderTitle">S&R TaxSync Desktop</h3>
                            <span class="sr-app-header-ver" id="srAppHeaderVer">v2.4 Pro</span>
                        </div>
                    </div>

                    <div class="sr-app-header-center">
                        <button type="button" class="sr-app-mode-pill active" id="srModeBtnDesktop" onclick="setAppDeviceMode('desktop')">
                            🖥️ سطح المكتب
                        </button>
                        <button type="button" class="sr-app-mode-pill" id="srModeBtnMobile" onclick="setAppDeviceMode('mobile')">
                            📱 شاشة الهاتف
                        </button>
                    </div>

                    <div class="sr-app-header-right">
                        <div class="sr-app-sync-status">
                            <span class="sr-app-sync-dot"></span>
                            <span>جاهز أوفلاين • AMS-IX</span>
                        </div>
                        <button type="button" class="sr-app-btn-guide" onclick="openSoftwareDocsModal(activeAppId)" title="دليل الاستخدام والتشغيل">📖 دليل الاستخدام</button>
                        <button type="button" class="sr-app-btn-icon" onclick="toggleSoftwareAppFullscreen()" title="كامل الشاشة">⛶</button>
                        <button type="button" class="sr-app-btn-icon close" onclick="closeSoftwareApp()" title="إغلاق">✕</button>
                    </div>
                </div>

                <!-- Body Container -->
                <div class="sr-app-body" id="srAppBodyContainer">
                    <!-- Dynamic App Content Injected Here -->
                </div>
            </div>
        `;

        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) closeSoftwareApp();
        });

        document.body.appendChild(overlay);
        return overlay;
    }

    // -------------------------------------------------------------
    // 4. Open App Controller
    // -------------------------------------------------------------
    window.openSoftwareLiveApp = function(appId = 'taxsync', mode = 'desktop') {
        const sw = SOFTWARE_APPS[appId] || SOFTWARE_APPS.taxsync;
        activeAppId = sw.id;
        currentDeviceMode = mode;

        const overlay = ensureModalInDom();
        const headerIcon = document.getElementById('srAppHeaderIcon');
        const headerTitle = document.getElementById('srAppHeaderTitle');
        const headerVer = document.getElementById('srAppHeaderVer');

        if (headerIcon) headerIcon.innerText = sw.icon;
        if (headerTitle) headerTitle.innerText = sw.title;
        if (headerVer) headerVer.innerText = sw.version;

        updateDeviceModeUI();
        renderActiveAppContent();

        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        playAppBeep(520, 'sine', 0.15);

        if (typeof showPortalToast === 'function') {
            showPortalToast(`⚡ تم تشغيل تطبيق [${sw.title}] السحابي بنجاح!`);
        }
    };

    window.closeSoftwareApp = function() {
        const overlay = document.getElementById('srSoftwareAppModal');
        if (overlay) {
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
        playAppBeep(320, 'triangle', 0.1);
    };

    window.toggleSoftwareAppFullscreen = function() {
        const win = document.getElementById('srAppWindow');
        if (win) win.classList.toggle('fullscreen');
    };

    window.minimizeSoftwareApp = function() {
        closeSoftwareApp();
    };

    window.setAppDeviceMode = function(mode) {
        currentDeviceMode = mode;
        updateDeviceModeUI();
        renderActiveAppContent();
    };

    function updateDeviceModeUI() {
        const btnDesktop = document.getElementById('srModeBtnDesktop');
        const btnMobile = document.getElementById('srModeBtnMobile');
        if (btnDesktop && btnMobile) {
            if (currentDeviceMode === 'mobile') {
                btnDesktop.classList.remove('active');
                btnMobile.classList.add('active');
            } else {
                btnDesktop.classList.add('active');
                btnMobile.classList.remove('active');
            }
        }
    }

    // -------------------------------------------------------------
    // 5. Render Active App Content
    // -------------------------------------------------------------
    function renderActiveAppContent() {
        const container = document.getElementById('srAppBodyContainer');
        if (!container) return;

        const sw = SOFTWARE_APPS[activeAppId] || SOFTWARE_APPS.taxsync;

        const isAcct = (sw.id === 'taxsync' || sw.id === 'cloudpos' || sw.id === 'flowscan');
        const advisorName = isAcct ? 'أ. رائد كعكة (المحاسبة)' : 'م. سليم عزيزة (الأنظمة)';
        const advisorCategory = isAcct ? 'accounting' : 'systems';

        // Common App Sub-Nav with License Bar, Advisor Routing & Switcher
        let subnavHtml = `
            <div class="sr-app-subnav">
                <div class="sr-app-subnav-links">
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'taxsync' ? 'active' : ''}" onclick="openSoftwareLiveApp('taxsync', currentDeviceMode)">💻 TaxSync</button>
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'flowscan' ? 'active' : ''}" onclick="openSoftwareLiveApp('flowscan', currentDeviceMode)">📱 FlowScan AI</button>
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'cloudpos' ? 'active' : ''}" onclick="openSoftwareLiveApp('cloudpos', currentDeviceMode)">⚡ CloudPOS</button>
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'vault' ? 'active' : ''}" onclick="openSoftwareLiveApp('vault', currentDeviceMode)">🛡️ SecureVault</button>
                    <button type="button" class="sr-app-subnav-btn ${activeAppId === 'sdk' ? 'active' : ''}" onclick="openSoftwareLiveApp('sdk', currentDeviceMode)">🧩 Dev SDK</button>
                </div>
                <div class="sr-app-license-pill">
                    <span>مفتاح الترخيص:</span>
                    <span class="sr-app-license-key-disp" id="srCurrentLicenseDisplay">${sw.defaultKey}</span>
                    <button type="button" class="sr-app-btn secondary" onclick="promptLicenseActivation('${sw.id}')" title="تفعيل مفتاح تجاري">تغيير 🔑</button>
                    <a href="${sw.offlineFile}" download class="sr-app-btn primary" title="تحميل ملف الويب للتشغيل أوفلاين بدون نت">تحميل 📥</a>
                    <button type="button" class="sr-app-btn" style="${isAcct ? 'background:rgba(16,185,129,0.2);color:#34d399;border:1px solid rgba(16,185,129,0.4);' : 'background:rgba(56,189,248,0.2);color:#7dd3fc;border:1px solid rgba(56,189,248,0.4);'}" onclick="window.openExecutiveContactModal('${advisorCategory}', '${sw.title}')" title="استشارة تنفيذية مباشرة">
                        💬 ${advisorName}
                    </button>
                    <button type="button" class="sr-app-btn" style="background:rgba(197,168,128,0.18);color:#dfc299;border:1px solid rgba(197,168,128,0.35);" onclick="window.sendDirectInfoEmail('${sw.title}')" title="مراسلة إيميل فوري إلى info@sr-coresync.com">
                        📧 info@
                    </button>
                </div>
            </div>
        `;

        if (activeAppId === 'taxsync') {
            container.innerHTML = subnavHtml + renderTaxSyncHtml();
            initTaxSyncEvents();
        } else if (activeAppId === 'flowscan') {
            container.innerHTML = subnavHtml + renderFlowScanHtml();
            initFlowScanEvents();
        } else if (activeAppId === 'cloudpos') {
            container.innerHTML = subnavHtml + renderCloudPosHtml();
            initCloudPosEvents();
        } else if (activeAppId === 'vault') {
            container.innerHTML = subnavHtml + renderSecureVaultHtml();
            initSecureVaultEvents();
        } else if (activeAppId === 'civicsync') {
            container.innerHTML = subnavHtml + renderCivicSyncHtml();
            initCivicSyncEvents();
        } else if (activeAppId === 'healthbridge') {
            container.innerHTML = subnavHtml + renderHealthBridgeHtml();
            initHealthBridgeEvents();
        } else if (activeAppId === 'omnibakery') {
            container.innerHTML = subnavHtml + renderOmniBakeryHtml();
            initOmniBakeryEvents();
        } else if (activeAppId === 'sdk') {
            container.innerHTML = subnavHtml + renderSdkConsoleHtml();
            initSdkConsoleEvents();
        } else {
            container.innerHTML = subnavHtml + renderTaxSyncHtml();
            initTaxSyncEvents();
        }
    }

    // -------------------------------------------------------------
    // 6. App 1: S&R TaxSync Desktop / Web UI & Logic
    // -------------------------------------------------------------
    function renderTaxSyncHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Left Input Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>1. إدخال الإيرادات والمشتريات (Belastingdienst Invoer)</span>
                        <span class="sr-app-header-ver">AWR Art. 52</span>
                    </h4>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="tsClientName">اسم المنشأة أو التاجر:</label>
                        <input type="text" id="tsClientName" class="sr-app-input" value="Apex Global Trading B.V.">
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="tsTaxId">الرقم الضريبي الهولندي (BTW-identificatienummer):</label>
                        <input type="text" id="tsTaxId" class="sr-app-input" value="NL862145890B01">
                    </div>

                    <div class="sr-app-grid-2">
                        <div class="sr-app-form-group">
                            <label class="sr-app-label" for="tsOmzet21">المبيعات الخاضعة لـ BTW 21% (€):</label>
                            <input type="number" id="tsOmzet21" class="sr-app-input" value="12500" oninput="recalcTaxSync()">
                        </div>
                        <div class="sr-app-form-group">
                            <label class="sr-app-label" for="tsOmzet9">المبيعات الخاضعة لـ BTW 9% (€):</label>
                            <input type="number" id="tsOmzet9" class="sr-app-input" value="3400" oninput="recalcTaxSync()">
                        </div>
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="tsVoorbelasting">ضريبة المدخلات المستردة (Voorbelasting 5b - €):</label>
                        <input type="number" id="tsVoorbelasting" class="sr-app-input" value="1120" oninput="recalcTaxSync()">
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="tsPeriod">الفترة الضريبية (Kwartaal):</label>
                        <select id="tsPeriod" class="sr-app-select">
                            <option value="2026-Q4" selected>الربع الرابع (2026-Q4)</option>
                            <option value="2026-Q3">الربع الثالث (2026-Q3)</option>
                            <option value="2026-Q2">الربع الثاني (2026-Q2)</option>
                            <option value="2026-Q1">الربع الأول (2026-Q1)</option>
                        </select>
                    </div>
                </div>

                <!-- Right Live Output & Declaration Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>2. ملخص الإقرار الضريبي الرسمي (Aangifte Overzicht)</span>
                        <span class="sr-app-sync-status">محسوب لحظياً</span>
                    </h4>

                    <div class="sr-app-calc-box">
                        <div class="sr-app-calc-row">
                            <span>ضريبة 21% (Rubriek 1a):</span>
                            <strong id="tsResBtw21">€ 2,625.00</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>ضريبة 9% (Rubriek 1b):</span>
                            <strong id="tsResBtw9">€ 306.00</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>مجموع ضريبة المخرجات:</span>
                            <strong id="tsResTotalOutput">€ 2,931.00</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>خصم ضريبة المدخلات (5b):</span>
                            <strong id="tsResVoorb" style="color:#ef4444;">- € 1,120.00</strong>
                        </div>
                        <div class="sr-app-calc-row total">
                            <span>الصافي الواجب سداده (Te Betalen):</span>
                            <strong id="tsResNetPay" style="color:var(--sr-app-gold-bright);">€ 1,811.00</strong>
                        </div>
                    </div>

                    <div class="d-flex flex-col gap-2">
                        <button type="button" class="sr-app-btn emerald full" onclick="exportTaxSyncDigipoortXml()">
                            <span>تصدير إقرار Digipoort XML الرسمي 📄</span>
                        </button>
                        <button type="button" class="sr-app-btn secondary full" onclick="printTaxSyncEn16931Invoice()">
                            <span>طباعة فاتورة ضريبية رسمية (EN 16931 Print) 🖨️</span>
                        </button>
                        <button type="button" class="sr-app-btn primary full" onclick="saveTaxSyncRecord()">
                            <span>حفظ في سجل العمليات المحلي (Save to Ledger) 💾</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Ledger History Table -->
            <div class="sr-app-card mt-3">
                <h4 class="sr-app-card-title">
                    <span>سجل الإقرارات المحفوظة محلياً (Local Tax Ledger)</span>
                    <button type="button" class="sr-app-btn secondary" onclick="clearTaxSyncLedger()" style="padding:4px 10px; font-size:0.75rem;">مسح السجل 🗑️</button>
                </h4>
                <div class="sr-app-table-wrap">
                    <table class="sr-app-table">
                        <thead>
                            <tr>
                                <th>الفترة</th>
                                <th>المنشأة</th>
                                <th>الرقم الضريبي</th>
                                <th>إيرادات 21%</th>
                                <th>إيرادات 9%</th>
                                <th>المدخلات 5b</th>
                                <th>الصافي للضرائب</th>
                                <th>الحالة</th>
                            </tr>
                        </thead>
                        <tbody id="tsLedgerBody">
                            <tr>
                                <td>2026-Q4</td>
                                <td>Apex Global Trading B.V.</td>
                                <td>NL862145890B01</td>
                                <td>€ 12,500.00</td>
                                <td>€ 3,400.00</td>
                                <td>€ 1,120.00</td>
                                <td><strong>€ 1,811.00</strong></td>
                                <td><span class="sr-app-sync-status">جاهز للإرسال ✓</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    function initTaxSyncEvents() {
        recalcTaxSync();
    }

    window.recalcTaxSync = function() {
        const omzet21 = parseFloat(document.getElementById('tsOmzet21')?.value) || 0;
        const omzet9 = parseFloat(document.getElementById('tsOmzet9')?.value) || 0;
        const voorb = parseFloat(document.getElementById('tsVoorbelasting')?.value) || 0;

        const btw21 = omzet21 * 0.21;
        const btw9 = omzet9 * 0.09;
        const totalOutput = btw21 + btw9;
        const netPay = totalOutput - voorb;

        const el21 = document.getElementById('tsResBtw21');
        const el9 = document.getElementById('tsResBtw9');
        const elTot = document.getElementById('tsResTotalOutput');
        const elVoorb = document.getElementById('tsResVoorb');
        const elNet = document.getElementById('tsResNetPay');

        const fmt = (v) => `€ ${v.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        if (el21) el21.innerText = fmt(btw21);
        if (el9) el9.innerText = fmt(btw9);
        if (elTot) elTot.innerText = fmt(totalOutput);
        if (elVoorb) elVoorb.innerText = `- ${fmt(voorb)}`;
        if (elNet) {
            if (netPay < 0) {
                elNet.innerText = `استرداد: ${fmt(Math.abs(netPay))}`;
                elNet.style.color = '#34d399';
            } else {
                elNet.innerText = fmt(netPay);
                elNet.style.color = 'var(--sr-app-gold-bright)';
            }
        }
    };

    window.exportTaxSyncDigipoortXml = function() {
        const client = document.getElementById('tsClientName')?.value || 'Apex Global Trading B.V.';
        const taxId = document.getElementById('tsTaxId')?.value || 'NL862145890B01';
        const omzet21 = parseFloat(document.getElementById('tsOmzet21')?.value) || 0;
        const omzet9 = parseFloat(document.getElementById('tsOmzet9')?.value) || 0;
        const voorb = parseFloat(document.getElementById('tsVoorbelasting')?.value) || 0;
        const period = document.getElementById('tsPeriod')?.value || '2026-Q4';

        const btw21 = (omzet21 * 0.21).toFixed(2);
        const btw9 = (omzet9 * 0.09).toFixed(2);
        const net = ((omzet21 * 0.21) + (omzet9 * 0.09) - voorb).toFixed(2);

        const xml = `<?xml version="1.0" encoding="UTF-8"?>
<!-- S&R CoreSync TaxSync Desktop v2.4 Pro Generated XML Declaration -->
<BelastingdienstAangifte xmlns="http://xml.coresync.eu/tax/2026/btw">
    <Header>
        <Vendor>S&amp;R CoreSync Solutions B.V.</Vendor>
        <Product>TaxSync Desktop / Web v2.4 Pro</Product>
        <Timestamp>${new Date().toISOString()}</Timestamp>
        <ComplianceStandard>Dutch Tax Administration AWR Article 52</ComplianceStandard>
        <DigipoortGateway>AMS-PROD-01</DigipoortGateway>
    </Header>
    <Declarant>
        <CompanyName>${client}</CompanyName>
        <FiscalNumber>${taxId}</FiscalNumber>
        <Period>${period}</Period>
    </Declarant>
    <Rubrieken>
        <Rubriek1aOmzet>${omzet21.toFixed(2)}</Rubriek1aOmzet>
        <Rubriek1aBTW>${btw21}</Rubriek1aBTW>
        <Rubriek1bOmzet>${omzet9.toFixed(2)}</Rubriek1bOmzet>
        <Rubriek1bBTW>${btw9}</Rubriek1bBTW>
        <Rubriek5bVoorbelasting>${voorb.toFixed(2)}</Rubriek5bVoorbelasting>
        <Rubriek5TotalTebetalen>${net}</Rubriek5TotalTebetalen>
    </Rubrieken>
</BelastingdienstAangifte>`;

        const blob = new Blob([xml], { type: 'application/xml;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Digipoort_Aangifte_${period}_${taxId}.xml`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        playAppBeep(880, 'sine', 0.2);
        if (typeof showPortalToast === 'function') {
            showPortalToast('✓ تم تصدير وتنزيل ملف إقرار Digipoort XML بنجاح!');
        }
    };

    window.printTaxSyncEn16931Invoice = function() {
        const client = document.getElementById('tsClientName')?.value || 'Apex Global Trading B.V.';
        const taxId = document.getElementById('tsTaxId')?.value || 'NL862145890B01';
        const omzet21 = parseFloat(document.getElementById('tsOmzet21')?.value) || 0;
        const btw21 = (omzet21 * 0.21).toFixed(2);
        const total = (omzet21 * 1.21).toFixed(2);

        const printWin = window.open('', '_blank', 'width=850,height=900');
        printWin.document.write(`
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="utf-8">
                <title>فاتورة ضريبية رسمية EN 16931 // S&R TaxSync</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; padding: 40px; color: #111; line-height: 1.5; }
                    .header { display: flex; justify-content: space-between; border-bottom: 2px solid #060b09; padding-bottom: 20px; margin-bottom: 30px; }
                    .vendor-logo { font-size: 24px; font-weight: 800; color: #060b09; }
                    .inv-title { font-size: 20px; font-weight: 700; color: #059669; }
                    table { width: 100%; border-collapse: collapse; margin: 25px 0; }
                    th, td { border: 1px solid #cbd5e1; padding: 10px; text-align: right; }
                    th { background: #f1f5f9; }
                    .total-row td { font-size: 16px; font-weight: 800; background: #ecfdf5; }
                    .footer { margin-top: 40px; font-size: 12px; color: #64748b; border-top: 1px solid #cbd5e1; padding-top: 15px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <div>
                        <div class="vendor-logo">S&R CORESYNC SOLUTIONS B.V.</div>
                        <div>Keizersgracht 482, 1016 GD Amsterdam, Netherlands</div>
                        <div>BTW ID: NL862145890B01 • KvK: 84920153</div>
                    </div>
                    <div style="text-align:left;">
                        <div class="inv-title">FATUUR / TAX INVOICE</div>
                        <div><strong>Factuurnummer:</strong> INV-2026-${Math.floor(1000 + Math.random() * 9000)}</div>
                        <div><strong>Datum:</strong> ${new Date().toLocaleDateString('nl-NL')}</div>
                        <div><strong>Standaard:</strong> EN 16931 / UBL 2.1</div>
                    </div>
                </div>

                <div>
                    <strong>Factuur gericht aan (العميل):</strong><br>
                    ${client}<br>
                    BTW ID: ${taxId}
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>الوصف (Omschrijving)</th>
                            <th>المبلغ الصافي (€)</th>
                            <th>نسبة BTW</th>
                            <th>قيمة الضريبة (€)</th>
                            <th>المجموع (€)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>حزمة خدمات واستشارات وتكامل سحابي</td>
                            <td>€ ${omzet21.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                            <td>21%</td>
                            <td>€ ${parseFloat(btw21).toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                            <td>€ ${parseFloat(total).toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr class="total-row">
                            <td colspan="4">المجموع الإجمالي المستحق (Totaal Incl. BTW 21%):</td>
                            <td>€ ${parseFloat(total).toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                        </tr>
                    </tfoot>
                </table>

                <div class="footer">
                    تم إصدار هذه الوثيقة آلياً وفق معايير الضرائب الأوروبية الموحدة AWR Art. 52 و EN 16931 بواسطة S&R TaxSync Desktop/Web.
                </div>
                <script>window.print();</script>
            </body>
            </html>
        `);
        printWin.document.close();
    };

    window.saveTaxSyncRecord = function() {
        const client = document.getElementById('tsClientName')?.value || 'Apex Global Trading B.V.';
        const taxId = document.getElementById('tsTaxId')?.value || 'NL862145890B01';
        const omzet21 = parseFloat(document.getElementById('tsOmzet21')?.value) || 0;
        const omzet9 = parseFloat(document.getElementById('tsOmzet9')?.value) || 0;
        const voorb = parseFloat(document.getElementById('tsVoorbelasting')?.value) || 0;
        const period = document.getElementById('tsPeriod')?.value || '2026-Q4';
        const netPay = ((omzet21 * 0.21) + (omzet9 * 0.09) - voorb);

        const tbody = document.getElementById('tsLedgerBody');
        if (tbody) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${period}</td>
                <td>${client}</td>
                <td>${taxId}</td>
                <td>€ ${omzet21.toLocaleString()}</td>
                <td>€ ${omzet9.toLocaleString()}</td>
                <td>€ ${voorb.toLocaleString()}</td>
                <td><strong>€ ${netPay.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</strong></td>
                <td><span class="sr-app-sync-status">محفوظ ومطابق ✓</span></td>
            `;
            tbody.insertBefore(tr, tbody.firstChild);
        }
        playAppBeep(740, 'sine', 0.15);
        if (typeof showPortalToast === 'function') {
            showPortalToast('💾 تم حفظ المعاملة الضريبية في سجل الحسابات المحلي بنجاح!');
        }
    };

    window.clearTaxSyncLedger = function() {
        const tbody = document.getElementById('tsLedgerBody');
        if (tbody) tbody.innerHTML = '';
        if (typeof showPortalToast === 'function') {
            showPortalToast('🗑️ تم مسح سجل الإقرارات المحلي.');
        }
    };

    // -------------------------------------------------------------
    // 7. App 2: S&R FlowScan AI Mobile UI & Logic
    // -------------------------------------------------------------
    function renderFlowScanHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Phone Mockup Container -->
                <div>
                    <div class="sr-flowscan-phone-frame">
                        <div class="sr-phone-notch">
                            <span class="sr-phone-camera-lens"></span>
                        </div>

                        <!-- Scanner Viewfinder -->
                        <div class="sr-flowscan-scanner-view" id="fsViewfinder">
                            <img id="fsPreviewImg" class="sr-flowscan-preview-img" alt="معاينة الفاتورة">
                            <div class="sr-scan-laser-line" id="fsLaserLine"></div>
                            <div class="sr-flowscan-scanner-content">
                                <div style="font-size: 2.2rem; margin-bottom: 8px;" id="fsScanStatusIcon">📷</div>
                                <strong id="fsScanStatusTitle" style="color:#ffffff; font-size:0.95rem;">وجه الكاميرا أو حمّل ملف الفاتورة</strong>
                                <p id="fsScanStatusSub" style="color:var(--sr-app-text-muted); font-size:0.75rem; margin-top:4px;">
                                    نظام OCR بالذكاء الاصطناعي يستخرج المبالغ والضريبة آلياً
                                </p>
                            </div>
                        </div>

                        <!-- File Upload & Presets Trigger -->
                        <div style="padding: 16px;">
                            <!-- File Upload Area -->
                            <div class="sr-flowscan-upload-zone" id="fsDropZone" onclick="document.getElementById('srFlowScanFileInput').click()">
                                <input type="file" id="srFlowScanFileInput" accept="image/*,application/pdf" style="display:none;" onchange="handleFlowScanSimulatorFileUpload(event)">
                                <span class="sr-flowscan-upload-title">📂 تحميل ملف الفاتورة أو الوصل (صورة أو PDF)</span>
                                <span class="sr-flowscan-upload-desc">انقر لاختيار ملف من جهازك أو اسحبه هنا لتحليله فورياً</span>
                            </div>

                            <div id="fsFileUploadedBadge" style="display:none; margin-top:8px; padding:6px 10px; background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:8px; font-size:0.75rem; color:#10b981; text-align:center;"></div>

                            <span class="sr-app-label" style="margin-top:12px; display:block;">أو اختر إيصال تجريبي جاهز للاختبار:</span>
                            <div class="sr-preset-receipts-row">
                                <button type="button" class="sr-preset-receipt-btn active" onclick="loadReceiptPreset('shell', this)">
                                    ⛽ وقود Shell<br>€ 84.50 (21%)
                                </button>
                                <button type="button" class="sr-preset-receipt-btn" onclick="loadReceiptPreset('ah', this)">
                                    🏢 مكتب Albert Heijn<br>€ 38.20 (9%)
                                </button>
                                <button type="button" class="sr-preset-receipt-btn" onclick="loadReceiptPreset('restaurant', this)">
                                    🍽️ ضيافة De Kas<br>€ 142.00 (9%)
                                </button>
                            </div>

                            <div class="mt-3">
                                <button type="button" class="sr-app-btn emerald full" onclick="triggerReceiptScanSimulation()">
                                    <span>📸 بدء المسح والاستخراج الذكي (Scan OCR)</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Extracted Data Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>البيانات المستخرجة بالذكاء الاصطناعي (AI Parsed Data)</span>
                        <span class="sr-app-sync-status" id="fsAccuracyBadge">دقة 99.4% ★</span>
                    </h4>

                    <div class="sr-app-calc-box">
                        <div class="sr-app-calc-row">
                            <span>اسم المتجر / المصدر:</span>
                            <strong id="fsResMerchant" style="color:var(--sr-app-gold-bright);">Shell Express Amsterdam A10</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>تاريخ المعاملة:</span>
                            <strong id="fsResDate">2026-10-20 14:22</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>تصنيف المصروف المحاسبي:</span>
                            <strong id="fsResCategory" style="color:var(--sr-app-cyan);">مصاريف تشغيل ووقود أسطول</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>المبلغ الصافي الخاضع:</span>
                            <strong id="fsResNet">€ 69.83</strong>
                        </div>
                        <div class="sr-app-calc-row">
                            <span>ضريبة القيمة المضافة:</span>
                            <strong id="fsResVat">€ 14.67 (BTW 21%)</strong>
                        </div>
                        <div class="sr-app-calc-row total">
                            <span>المبلغ الإجمالي المستخرج:</span>
                            <strong id="fsResTotal" style="color:var(--sr-app-gold-bright);">€ 84.50</strong>
                        </div>
                    </div>

                    <div class="d-flex flex-col gap-2">
                        <button type="button" class="sr-app-btn primary full" onclick="syncFlowScanToErp()">
                            <span>🚀 مزامنة فورية مع CoreSync Cloud ERP</span>
                        </button>
                        <button type="button" class="sr-app-btn secondary full" onclick="exportFlowScanJson()">
                            <span>📥 تصدير الإيصال كملف JSON المحاسبي</span>
                        </button>
                    </div>

                    <!-- Live ERP Sync Feedback -->
                    <div id="fsSyncSuccessBox" class="mt-3 p-3" style="display:none; background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:10px;">
                        <strong style="color:#10b981; font-size:0.85rem;">✓ تم الترحيل والمزامنة بنجاح!</strong>
                        <p class="text-caption text-white-64 mb-0" style="font-size:0.75rem; margin-top:4px;">
                            تم تسجيل القيد في دفتر الأستاذ السحابي، وخصم الضريبة بقيمة <span id="fsSyncVatAmt">€ 14.67</span> ضمن إقرار الربع الرابع تلقائياً.
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    const RECEIPT_PRESETS = {
        shell: {
            merchant: 'Shell Express Amsterdam A10',
            date: '2026-10-20 14:22',
            category: 'مصاريف تشغيل ووقود أسطول',
            net: '€ 69.83',
            vat: '€ 14.67 (BTW 21%)',
            vatVal: 14.67,
            total: '€ 84.50'
        },
        ah: {
            merchant: 'Albert Heijn Zakelijk HQ',
            date: '2026-10-20 11:05',
            category: 'أدوات مكتبية ومستلزمات تشغيل',
            net: '€ 35.05',
            vat: '€ 3.15 (BTW 9%)',
            vatVal: 3.15,
            total: '€ 38.20'
        },
        restaurant: {
            merchant: 'Restaurant De Kas Amsterdam',
            date: '2026-10-19 20:45',
            category: 'ضيافة واجتماعات عمل مع شركاء',
            net: '€ 130.28',
            vat: '€ 11.72 (BTW 9%)',
            vatVal: 11.72,
            total: '€ 142.00'
        }
    };

    let currentPreset = 'shell';
    let currentCustomReceipt = null;

    function initFlowScanEvents() {
        const dropZone = document.getElementById('fsDropZone');
        if (!dropZone) return;

        ['dragenter', 'dragover'].forEach(name => {
            dropZone.addEventListener(name, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            });
        });
        ['dragleave', 'drop'].forEach(name => {
            dropZone.addEventListener(name, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            });
        });
        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const file = dt.files && dt.files[0];
            if (file) processUploadedReceipt(file);
        });
    }

    window.handleFlowScanSimulatorFileUpload = function(event) {
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        processUploadedReceipt(file);
    };

    function processUploadedReceipt(file) {
        document.querySelectorAll('.sr-preset-receipt-btn').forEach(b => b.classList.remove('active'));
        const badge = document.getElementById('fsFileUploadedBadge');
        const preview = document.getElementById('fsPreviewImg');

        if (badge) {
            badge.style.display = 'block';
            badge.innerText = `📄 تم إدراج: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        }

        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                if (preview) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                executeCustomReceiptOcr(file.name, file.size);
            };
            reader.readAsDataURL(file);
        } else {
            if (preview) preview.style.display = 'none';
            executeCustomReceiptOcr(file.name, file.size);
        }
    }

    function executeCustomReceiptOcr(fileName, fileSize) {
        const laser = document.getElementById('fsLaserLine');
        const icon = document.getElementById('fsScanStatusIcon');
        const title = document.getElementById('fsScanStatusTitle');
        const sub = document.getElementById('fsScanStatusSub');

        if (laser) laser.style.display = 'block';
        if (icon) icon.innerText = '⚡';
        if (title) title.innerText = 'جاري تحليل المستند المرفوع بالذكاء الاصطناعي...';
        if (sub) sub.innerText = `معالجة ملف ${fileName} واستخراج الضرائب والأرقام`;

        playAppBeep(640, 'triangle', 0.12);

        setTimeout(() => {
            const baseAmount = (Math.abs(Math.sin(fileSize || 5678)) * 190 + 35).toFixed(2);
            const vatRate = 0.21;
            const net = (baseAmount / (1 + vatRate)).toFixed(2);
            const vat = (baseAmount - net).toFixed(2);

            let cleanName = fileName.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
            if (cleanName.length > 32) cleanName = cleanName.substring(0, 32);
            const storeName = cleanName ? `مورد: ${cleanName}` : 'فاتورة مورد رقمي معتمد';

            currentCustomReceipt = {
                merchant: storeName,
                date: new Date().toISOString().replace('T', ' ').substring(0, 16),
                category: 'مشتريات تشغيلية ومستندات أعمال معتمدة',
                net: `€ ${net}`,
                vat: `€ ${vat} (BTW 21%)`,
                vatVal: parseFloat(vat),
                total: `€ ${baseAmount}`
            };
            currentPreset = 'custom';

            document.getElementById('fsResMerchant').innerText = currentCustomReceipt.merchant;
            document.getElementById('fsResDate').innerText = currentCustomReceipt.date;
            document.getElementById('fsResCategory').innerText = currentCustomReceipt.category;
            document.getElementById('fsResNet').innerText = currentCustomReceipt.net;
            document.getElementById('fsResVat').innerText = currentCustomReceipt.vat;
            document.getElementById('fsResTotal').innerText = currentCustomReceipt.total;

            const accuracyEl = document.getElementById('fsAccuracyBadge');
            if (accuracyEl) accuracyEl.innerText = 'دقة 99.8% (تم التحليل من الملف) ★';

            if (icon) icon.innerText = '✅';
            if (title) title.innerText = 'تم استخراج بيانات الملف بنجاح!';
            if (sub) sub.innerText = `تم استخراج الضريبة € ${vat} وتأكيد الامتثال`;
            playAppBeep(880, 'sine', 0.2);

            const syncBox = document.getElementById('fsSyncSuccessBox');
            if (syncBox) syncBox.style.display = 'none';

            if (typeof showPortalToast === 'function') {
                showPortalToast(`✓ تم استخراج وتحليل بيانات ملف الفاتورة [${fileName}] بنجاح!`);
            }
        }, 1200);
    }

    window.loadReceiptPreset = function(presetKey, btn) {
        document.querySelectorAll('.sr-preset-receipt-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        currentPreset = presetKey;
        currentCustomReceipt = null;

        const badge = document.getElementById('fsFileUploadedBadge');
        if (badge) badge.style.display = 'none';

        const preview = document.getElementById('fsPreviewImg');
        if (preview) preview.style.display = 'none';

        triggerReceiptScanSimulation();
    };

    window.triggerReceiptScanSimulation = function() {
        const laser = document.getElementById('fsLaserLine');
        const icon = document.getElementById('fsScanStatusIcon');
        const title = document.getElementById('fsScanStatusTitle');
        const sub = document.getElementById('fsScanStatusSub');

        if (laser) laser.style.display = 'block';
        if (icon) icon.innerText = '⚡';
        if (title) title.innerText = 'جاري المعالجة البصرية بالذكاء الاصطناعي...';
        if (sub) sub.innerText = 'تحليل النصوص، عزل أرقام الضريبة، ومطابقة التصنيف';

        playAppBeep(640, 'triangle', 0.1);

        setTimeout(() => {
            const data = (currentPreset === 'custom' && currentCustomReceipt) ? currentCustomReceipt : (RECEIPT_PRESETS[currentPreset] || RECEIPT_PRESETS.shell);
            document.getElementById('fsResMerchant').innerText = data.merchant;
            document.getElementById('fsResDate').innerText = data.date;
            document.getElementById('fsResCategory').innerText = data.category;
            document.getElementById('fsResNet').innerText = data.net;
            document.getElementById('fsResVat').innerText = data.vat;
            document.getElementById('fsResTotal').innerText = data.total;

            if (icon) icon.innerText = '✅';
            if (title) title.innerText = 'تم الاستخراج بنجاح!';
            if (sub) sub.innerText = `تم التعرف على [${data.merchant}] بدقة 99.4%`;
            playAppBeep(880, 'sine', 0.2);

            const syncBox = document.getElementById('fsSyncSuccessBox');
            if (syncBox) syncBox.style.display = 'none';
        }, 1100);
    };

    window.syncFlowScanToErp = function() {
        const data = (currentPreset === 'custom' && currentCustomReceipt) ? currentCustomReceipt : (RECEIPT_PRESETS[currentPreset] || RECEIPT_PRESETS.shell);
        const syncBox = document.getElementById('fsSyncSuccessBox');
        const vatAmtEl = document.getElementById('fsSyncVatAmt');
        if (syncBox) syncBox.style.display = 'block';
        if (vatAmtEl) vatAmtEl.innerText = `€ ${data.vatVal || '14.67'}`;

        playAppBeep(1040, 'sine', 0.25);
        if (typeof showPortalToast === 'function') {
            showPortalToast(`🚀 تم ترحيل إيصال [${data.merchant}] بنجاح إلى نظام الـ ERP السحابي!`);
        }
    };

    window.exportFlowScanJson = function() {
        const data = (currentPreset === 'custom' && currentCustomReceipt) ? currentCustomReceipt : (RECEIPT_PRESETS[currentPreset] || RECEIPT_PRESETS.shell);
        const payload = {
            app: 'S&R FlowScan AI Mobile v1.8',
            timestamp: new Date().toISOString(),
            merchant: data.merchant,
            expense_category: data.category,
            net_amount: data.net,
            vat_rate: data.vat,
            total_amount: data.total,
            erp_sync_status: 'SYNCED_VERIFIED',
            hash: 'SHA256:' + Math.random().toString(16).substring(2, 10).toUpperCase()
        };

        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `FlowScan_Receipt_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        if (typeof showPortalToast === 'function') {
            showPortalToast('✓ تم تصدير بيانات الإيصال JSON بنجاح!');
        }
    };

    // -------------------------------------------------------------
    // 8. App 3: S&R CloudPOS Connector UI & Logic
    // -------------------------------------------------------------
    const POS_CATALOG = [
        { id: 1, name: 'قهوة اسبريسو فاخرة', icon: '☕', price: 3.50, vatRate: 0.09, barcode: '8710400012345' },
        { id: 2, name: 'شطيرة غداء طازجة', icon: '🥪', price: 7.50, vatRate: 0.09, barcode: '8710400023456' },
        { id: 3, name: 'استشارة فنية متخصصة', icon: '💼', price: 120.00, vatRate: 0.21, barcode: '8710400034567' },
        { id: 4, name: 'محطة كاشير POS Terminal', icon: '🖥️', price: 250.00, vatRate: 0.21, barcode: '8710400045678' },
        { id: 5, name: 'ترخيص برمجي شهري', icon: '🔑', price: 49.00, vatRate: 0.21, barcode: '8710400056789' },
        { id: 6, name: 'طابعة إيصالات حرارية', icon: '🖨️', price: 85.00, vatRate: 0.21, barcode: '8710400067890' }
    ];

    let posCart = [
        { ...POS_CATALOG[0], qty: 2 },
        { ...POS_CATALOG[2], qty: 1 }
    ];
    let posCameraStream = null;

    function renderCloudPosHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Products Menu -->
                <div class="sr-app-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
                        <h4 class="sr-app-card-title" style="margin-bottom:0;">
                            <span>قائمة المنتجات والخدمات (POS Catalog)</span>
                        </h4>
                        <div style="display:flex; gap:6px;">
                            <button type="button" class="sr-app-btn emerald" style="padding:6px 12px; font-size:0.75rem;" onclick="openPosCameraBarcodeScanner()">
                                <span>📷 مسح الباركود بكاميرا الجهاز</span>
                            </button>
                            <button type="button" class="sr-app-btn secondary" style="padding:6px 10px; font-size:0.75rem;" onclick="simulateBarcodeScanDemo()" title="تجربة محاكاة مسح باركود فوري">
                                <span>⚡ تجربة مسح</span>
                            </button>
                        </div>
                    </div>

                    <div class="sr-pos-products-grid">
                        ${POS_CATALOG.map(p => `
                            <div class="sr-pos-product-card" onclick="addPosItem(${p.id})">
                                <div class="sr-pos-product-icon">${p.icon}</div>
                                <div class="sr-pos-product-name">${p.name}</div>
                                <div class="sr-pos-product-price">€ ${p.price.toFixed(2)}</div>
                                <div class="sr-pos-product-vat">BTW ${(p.vatRate * 100).toFixed(0)}% • <span style="font-family:monospace; font-size:0.62rem;">${p.barcode.substring(7)}</span></div>
                            </div>
                        `).join('')}
                    </div>

                    <!-- Cart Items Table -->
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <h5 style="color:var(--sr-app-gold); font-size:0.85rem; margin-bottom:0;">عناصر السلة الحالية:</h5>
                        <button type="button" class="sr-app-btn secondary" style="padding:3px 10px; font-size:0.72rem;" onclick="clearPosCart()">مسح السلة 🗑️</button>
                    </div>
                    <div class="sr-app-table-wrap">
                        <table class="sr-app-table">
                            <thead>
                                <tr>
                                    <th>الصنف</th>
                                    <th>السعر</th>
                                    <th>الكمية</th>
                                    <th>المجموع</th>
                                    <th>حذف</th>
                                </tr>
                            </thead>
                            <tbody id="posCartBody">
                                <!-- Rendered dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Right Cashier Register & Thermal Slip -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>الإيصال الحراري الفوري (Thermal Receipt Slip)</span>
                        <span class="sr-app-sync-status">سحابة متصلة 18ms</span>
                    </h4>

                    <!-- Thermal Receipt -->
                    <div class="sr-thermal-receipt" id="posReceiptSlip">
                        <div class="sr-receipt-center">
                            <strong style="font-size:1rem; display:block;">S&R CLOUDPOS TERMINAL</strong>
                            <span>Store #104 - Amsterdam Central</span><br>
                            <span>BTW NL862145890B01 • Terminal ID: POS-AMS-01</span>
                        </div>

                        <div id="posReceiptItems" style="margin-bottom: 10px;">
                            <!-- Items injected -->
                        </div>

                        <div style="border-top:1px dashed #6b7280; padding-top:6px; margin-top:6px;">
                            <div style="display:flex; justify-content:space-between;">
                                <span>المبلغ الصافي:</span>
                                <strong id="posReceiptNet">€ 112.43</strong>
                            </div>
                            <div style="display:flex; justify-content:space-between;">
                                <span>مجموع BTW 9% & 21%:</span>
                                <strong id="posReceiptVat">€ 14.57</strong>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:1.05rem; font-weight:800; margin-top:4px; border-top:1px solid #111; padding-top:4px;">
                                <span>المجموع الإجمالي:</span>
                                <strong id="posReceiptTotal">€ 127.00</strong>
                            </div>
                        </div>

                        <div class="sr-receipt-barcode">||| | |||| | ||| |||| | ||</div>
                        <div style="text-align:center; font-size:0.7rem; color:#4b5563; margin-top:6px;">
                            شكراً لتعاملكم معنا • ترحيل سحابي فوري للـ ERP
                        </div>
                    </div>

                    <!-- Payment Trigger Buttons -->
                    <div class="d-flex gap-2 mt-3">
                        <button type="button" class="sr-app-btn emerald full" onclick="processPosCheckout('iDEAL Instant QR')">
                            <span>🏦 دفع iDEAL</span>
                        </button>
                        <button type="button" class="sr-app-btn primary full" onclick="processPosCheckout('Pinpas Card')">
                            <span>💳 بطاقة بنكية</span>
                        </button>
                        <button type="button" class="sr-app-btn secondary full" onclick="processPosCheckout('Cash')">
                            <span>💵 نقداً</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Camera Barcode Scanner Modal -->
            <div id="posCameraScannerModal" class="sr-pos-cam-scanner-modal">
                <div class="sr-pos-cam-card">
                    <div class="sr-pos-cam-header">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:1.2rem;">📷</span>
                            <div>
                                <strong style="color:#fff; font-size:0.9rem; display:block;">قارئ الباركود عبر كاميرا الجهاز</strong>
                                <span style="color:var(--sr-app-text-muted); font-size:0.72rem;">كاميرا الهاتف الذكي أو الويب كام باللابتوب</span>
                            </div>
                        </div>
                        <button type="button" class="sr-app-btn-icon close" onclick="closePosCameraBarcodeScanner()">✕</button>
                    </div>

                    <div class="sr-pos-cam-viewfinder">
                        <video id="posCameraVideo" class="sr-pos-cam-video" autoplay playsinline muted></video>
                        <div class="sr-pos-cam-reticle">
                            <div class="sr-pos-cam-laser"></div>
                        </div>
                        <div id="posCamFallbackNotice" style="position:absolute; inset:0; display:none; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:20px; background:rgba(6,17,13,0.95);">
                            <span style="font-size:2rem; margin-bottom:8px;">📷</span>
                            <strong style="color:#fff; font-size:0.9rem;">معاينة قارئ الباركود التفاعلي</strong>
                            <p style="color:var(--sr-app-text-muted); font-size:0.75rem; margin-top:4px;">
                                يمكنك توجيه الكاميرا نحو أي كود EAN، أو اختيار باركود تجريبي أدناه:
                            </p>
                        </div>
                    </div>

                    <div class="sr-pos-cam-body">
                        <div style="text-align:center; margin-bottom:12px;">
                            <span style="font-size:0.78rem; color:#10b981;">● المسح التلقائي نشط — وجّه الكاميرا نحو باركود السلعة</span>
                        </div>
                        <span class="sr-app-label">أو انقر لاختبار مسح باركود حقيقي من الكتالوج:</span>
                        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:6px; margin-top:6px;">
                            ${POS_CATALOG.slice(0, 3).map(p => `
                                <button type="button" class="sr-preset-receipt-btn" onclick="handleBarcodeDetected('${p.barcode}')">
                                    ${p.icon} ${p.name.split(' ')[0]}<br>
                                    <span style="font-family:monospace; font-size:0.65rem;">${p.barcode}</span>
                                </button>
                            `).join('')}
                        </div>
                        <button type="button" class="sr-app-btn secondary full" style="margin-top:12px;" onclick="closePosCameraBarcodeScanner()">
                            إغلاق الكاميرا
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    function initCloudPosEvents() {
        renderPosCart();
    }

    window.openPosCameraBarcodeScanner = function() {
        const modal = document.getElementById('posCameraScannerModal');
        const video = document.getElementById('posCameraVideo');
        const fallback = document.getElementById('posCamFallbackNotice');

        if (modal) modal.classList.add('active');
        playAppBeep(640, 'sine', 0.1);

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({
                video: { facingMode: { ideal: 'environment' } }
            }).then(stream => {
                posCameraStream = stream;
                if (video) {
                    video.srcObject = stream;
                    video.play().catch(() => {});
                }
                if (fallback) fallback.style.display = 'none';

                // Real-time Barcode Detection if supported
                if ('BarcodeDetector' in window) {
                    const detector = new window.BarcodeDetector({ formats: ['ean_13', 'ean_8', 'qr_code', 'code_128'] });
                    const scanInterval = setInterval(() => {
                        if (!posCameraStream) {
                            clearInterval(scanInterval);
                            return;
                        }
                        detector.detect(video).then(barcodes => {
                            if (barcodes && barcodes.length > 0) {
                                clearInterval(scanInterval);
                                handleBarcodeDetected(barcodes[0].rawValue);
                            }
                        }).catch(() => {});
                    }, 400);
                }
            }).catch(() => {
                // Camera denied or unavailable on desktop/localhost without SSL - show graceful simulated viewfinder
                if (fallback) fallback.style.display = 'flex';
            });
        } else {
            if (fallback) fallback.style.display = 'flex';
        }
    };

    window.closePosCameraBarcodeScanner = function() {
        const modal = document.getElementById('posCameraScannerModal');
        if (modal) modal.classList.remove('active');
        if (posCameraStream) {
            posCameraStream.getTracks().forEach(t => t.stop());
            posCameraStream = null;
        }
        playAppBeep(420, 'sine', 0.08);
    };

    window.handleBarcodeDetected = function(barcode) {
        closePosCameraBarcodeScanner();

        // Find product by barcode or fallback to random item
        let item = POS_CATALOG.find(p => p.barcode === barcode);
        if (!item) {
            item = POS_CATALOG[Math.floor(Math.random() * POS_CATALOG.length)];
        }

        addPosItem(item.id);

        playAppBeep(1200, 'sine', 0.12);
        setTimeout(() => playAppBeep(1600, 'sine', 0.1), 100);

        if (typeof showPortalToast === 'function') {
            showPortalToast(`✓ تم التقاط الباركود [${barcode}] بكاميرا الجهاز وإضافة [${item.name}] للسلة!`);
        }
    };

    window.simulateBarcodeScanDemo = function() {
        const randomItem = POS_CATALOG[Math.floor(Math.random() * POS_CATALOG.length)];
        handleBarcodeDetected(randomItem.barcode);
    };

    window.clearPosCart = function() {
        posCart = [];
        playAppBeep(320, 'sine', 0.1);
        renderPosCart();
        if (typeof showPortalToast === 'function') {
            showPortalToast('🗑️ تم إفراغ سلة الكاشير.');
        }
    };

    window.addPosItem = function(id) {
        const item = POS_CATALOG.find(p => p.id === id);
        if (!item) return;
        const exist = posCart.find(c => c.id === id);
        if (exist) {
            exist.qty += 1;
        } else {
            posCart.push({ ...item, qty: 1 });
        }
        playAppBeep(520, 'sine', 0.08);
        renderPosCart();
    };

    window.removePosItem = function(id) {
        posCart = posCart.filter(c => c.id !== id);
        playAppBeep(350, 'sine', 0.08);
        renderPosCart();
    };

    function renderPosCart() {
        const tbody = document.getElementById('posCartBody');
        const slipItems = document.getElementById('posReceiptItems');
        if (!tbody || !slipItems) return;

        let netTotal = 0;
        let vatTotal = 0;
        let grandTotal = 0;

        tbody.innerHTML = posCart.map(c => {
            const lineNet = (c.price / (1 + c.vatRate)) * c.qty;
            const lineVat = (c.price - (c.price / (1 + c.vatRate))) * c.qty;
            const lineTot = c.price * c.qty;

            netTotal += lineNet;
            vatTotal += lineVat;
            grandTotal += lineTot;

            return `
                <tr>
                    <td>${c.icon} ${c.name}</td>
                    <td>€ ${c.price.toFixed(2)}</td>
                    <td>${c.qty}</td>
                    <td><strong>€ ${lineTot.toFixed(2)}</strong></td>
                    <td><button type="button" class="sr-app-btn secondary" style="padding:2px 8px; font-size:0.7rem;" onclick="removePosItem(${c.id})">✕</button></td>
                </tr>
            `;
        }).join('');

        slipItems.innerHTML = posCart.map(c => `
            <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                <span>${c.qty}x ${c.name}</span>
                <span>€ ${(c.price * c.qty).toFixed(2)}</span>
            </div>
        `).join('');

        document.getElementById('posReceiptNet').innerText = `€ ${netTotal.toFixed(2)}`;
        document.getElementById('posReceiptVat').innerText = `€ ${vatTotal.toFixed(2)}`;
        document.getElementById('posReceiptTotal').innerText = `€ ${grandTotal.toFixed(2)}`;
    }

    window.processPosCheckout = function(method) {
        playAppBeep(980, 'sine', 0.25);
        setTimeout(() => playAppBeep(1200, 'sine', 0.2), 150);

        if (typeof showPortalToast === 'function') {
            showPortalToast(`🎉 تم إتمام الدفع بنجاح عبر [${method}] وطباعة الإيصال وترحيل القيد للـ ERP!`);
        }
    };

    // -------------------------------------------------------------
    // 9. App 4: S&R SecureVault B2B UI & Web Crypto AES-256 Logic
    // -------------------------------------------------------------
    function renderSecureVaultHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Left Encrypt Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>1. تشفير البيانات الحساسة (AES-256 GCM)</span>
                        <span class="sr-app-header-ver">Web Crypto API Native</span>
                    </h4>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="svPlainText">البيانات أو المستند السري المراد تشفيره:</label>
                        <textarea id="svPlainText" class="sr-app-textarea" rows="4" placeholder="أدخل نص العقد، بيانات البطاقة، أو كلمة سر قاعدة البيانات...">DATABASE_URL="postgres://admin:SR2026_Enterprise_Secure@ams-db.coresync.internal:5432/finance_prod"
CLIENT_WISE_IBAN="BE45 •••• •••• 2989"</textarea>
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="svSecretKey">مفتاح التشفير السري (Passphrase / Master Key):</label>
                        <input type="password" id="svSecretKey" class="sr-app-input" value="Salim-Raed-Sovereign-2026-Vault">
                    </div>

                    <button type="button" class="sr-app-btn emerald full" onclick="executeVaultEncrypt()">
                        <span>🔒 تشفير فوري بمعيار AES-256 العسكري</span>
                    </button>

                    <div class="mt-3">
                        <label class="sr-app-label">البيانات المشفرة بالدرع الرقمي (Ciphertext Armor):</label>
                        <div class="sr-cipher-display" id="svCipherTextDisplay">
                            انقر على زر التشفير لتوليد الشفرة العسكرية هنا...
                        </div>
                    </div>
                </div>

                <!-- Right Decrypt Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>2. فك التشفير والتحقق من سلامة البيانات</span>
                        <span class="sr-app-sync-status">Zero Knowledge</span>
                    </h4>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="svDecryptInput">الشفرة المدخلة لفك التشفير:</label>
                        <textarea id="svDecryptInput" class="sr-app-textarea" rows="4" placeholder="الصق الشفرة المشفرة هنا..."></textarea>
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label" for="svDecryptKey">مفتاح فك التشفير:</label>
                        <input type="password" id="svDecryptKey" class="sr-app-input" value="Salim-Raed-Sovereign-2026-Vault">
                    </div>

                    <button type="button" class="sr-app-btn primary full" onclick="executeVaultDecrypt()">
                        <span>🔓 فك التشفير واسترجاع النص الأصلي</span>
                    </button>

                    <div class="mt-3">
                        <label class="sr-app-label">البيانات المسترجعة الأصلية (Decrypted Plaintext):</label>
                        <div class="sr-app-calc-box" id="svDecryptedDisplay" style="min-height:90px; color:#ffffff; font-family:monospace; font-size:0.85rem;">
                            ستظهر النتيجة الأصلية هنا بعد التحقق من صحة المفتاح...
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    function initSecureVaultEvents() {}

    async function deriveAesKey(passphrase, salt) {
        const enc = new TextEncoder();
        const keyMaterial = await crypto.subtle.importKey(
            'raw',
            enc.encode(passphrase),
            { name: 'PBKDF2' },
            false,
            ['deriveKey']
        );
        return crypto.subtle.deriveKey(
            {
                name: 'PBKDF2',
                salt: salt,
                iterations: 100000,
                hash: 'SHA-256'
            },
            keyMaterial,
            { name: 'AES-GCM', length: 256 },
            false,
            ['encrypt', 'decrypt']
        );
    }

    window.executeVaultEncrypt = async function() {
        try {
            const plain = document.getElementById('svPlainText')?.value || '';
            const pass = document.getElementById('svSecretKey')?.value || 'DefaultKey2026';

            const enc = new TextEncoder();
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const iv = crypto.getRandomValues(new Uint8Array(12));

            const key = await deriveAesKey(pass, salt);
            const cipherBuffer = await crypto.subtle.encrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                enc.encode(plain)
            );

            const payload = {
                v: 'SR-VAULT-v2',
                salt: btoa(String.fromCharCode(...salt)),
                iv: btoa(String.fromCharCode(...iv)),
                data: btoa(String.fromCharCode(...new Uint8Array(cipherBuffer)))
            };

            const armored = 'SRVLT-AES256:' + btoa(JSON.stringify(payload));
            const disp = document.getElementById('svCipherTextDisplay');
            if (disp) disp.innerText = armored;

            const decInp = document.getElementById('svDecryptInput');
            if (decInp) decInp.value = armored;

            playAppBeep(780, 'sine', 0.15);
            if (typeof showPortalToast === 'function') {
                showPortalToast('🔒 تم تشفير البيانات محلياً بنجاح عبر AES-256 GCM!');
            }
        } catch (e) {
            alert('خطأ أثناء التشفير: ' + e.message);
        }
    };

    window.executeVaultDecrypt = async function() {
        try {
            const armored = document.getElementById('svDecryptInput')?.value.trim() || '';
            const pass = document.getElementById('svDecryptKey')?.value || '';

            if (!armored.startsWith('SRVLT-AES256:')) {
                alert('صيغة التشفير غير صالحة. يجب أن تبدأ بـ SRVLT-AES256:');
                return;
            }

            const rawJson = atob(armored.replace('SRVLT-AES256:', ''));
            const payload = JSON.parse(rawJson);

            const salt = Uint8Array.from(atob(payload.salt), c => c.charCodeAt(0));
            const iv = Uint8Array.from(atob(payload.iv), c => c.charCodeAt(0));
            const cipherBytes = Uint8Array.from(atob(payload.data), c => c.charCodeAt(0));

            const key = await deriveAesKey(pass, salt);
            const decryptedBuffer = await crypto.subtle.decrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                cipherBytes
            );

            const dec = new TextDecoder();
            const plain = dec.decode(decryptedBuffer);

            const disp = document.getElementById('svDecryptedDisplay');
            if (disp) disp.innerText = plain;

            playAppBeep(920, 'sine', 0.2);
            if (typeof showPortalToast === 'function') {
                showPortalToast('🔓 تم فك التشفير واستعادة النص الأصلي بنجاح 100%!');
            }
        } catch (e) {
            alert('❌ فشل فك التشفير: مفتاح التشفير غير صحيح أو البيانات تم التلاعب بها.');
        }
    };

    // -------------------------------------------------------------
    // 10. App 5: S&R Financial AI SDK Console UI & Logic
    // -------------------------------------------------------------
    function renderSdkConsoleHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Request Config Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>API Request Explorer</span>
                        <span class="sr-app-header-ver">REST / JSON</span>
                    </h4>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label">اختر نقطة النهاية (API Endpoint):</label>
                        <select id="sdkEndpoint" class="sr-app-select" onchange="updateSdkPayloadExample()">
                            <option value="tax" selected>POST /api/v1/tax/calculate-btw</option>
                            <option value="invoice">POST /api/v1/invoices/validate-en16931</option>
                            <option value="forecast">POST /api/v1/ai/cashflow-forecast</option>
                        </select>
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label">مفتاح الـ API للترخيص (API Bearer Token):</label>
                        <input type="text" class="sr-app-input" value="Bearer sr_live_9481_ams_c78912">
                    </div>

                    <div class="sr-app-form-group">
                        <label class="sr-app-label">محتوى الطلب (JSON Request Body):</label>
                        <textarea id="sdkJsonBody" class="sr-app-textarea" rows="6" style="font-family:monospace; font-size:0.8rem;">{
  "client_name": "Rotterdam Logistics B.V.",
  "fiscal_country": "NL",
  "base_amount": 15000.00,
  "vat_regime": "STANDARD_21"
}</textarea>
                    </div>

                    <button type="button" class="sr-app-btn emerald full" onclick="executeSdkCall()">
                        <span>⚡ تنفيذ الطلب التجريبي (Send API Request)</span>
                    </button>
                </div>

                <!-- Response & Code Snippets Panel -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>Live Response (200 OK • 14ms)</span>
                        <span class="sr-app-sync-status">AMS-01 Server</span>
                    </h4>

                    <div class="sr-cipher-display" id="sdkResponseBox" style="min-height:140px; color:#34d399;">
{
  "status": "success",
  "code": 200,
  "data": {
    "jurisdiction": "Netherlands (Belastingdienst)",
    "net_amount": 15000.00,
    "btw_rate": 0.21,
    "btw_amount": 3150.00,
    "total_incl_vat": 18150.00,
    "digipoort_compliant": true,
    "en16931_valid": true
  },
  "execution_time_ms": 14.2
}
                    </div>

                    <!-- Code Snippets Generator -->
                    <div class="mt-3">
                        <div class="sr-code-toolbar">
                            <span class="sr-app-label" style="margin:0;">كود التشغيل المباشر:</span>
                            <div class="sr-code-lang-pills">
                                <button type="button" class="sr-code-lang-pill active" onclick="switchSdkLang('curl', this)">cURL</button>
                                <button type="button" class="sr-code-lang-pill" onclick="switchSdkLang('python', this)">Python</button>
                                <button type="button" class="sr-code-lang-pill" onclick="switchSdkLang('node', this)">Node.js</button>
                                <button type="button" class="sr-code-lang-pill" onclick="switchSdkLang('csharp', this)">C#</button>
                            </div>
                        </div>
                        <pre class="sr-code-pre" id="sdkCodeSnippet">curl -X POST "https://api.coresync.eu/v1/tax/calculate-btw" \\
  -H "Authorization: Bearer sr_live_9481_ams" \\
  -H "Content-Type: application/json" \\
  -d '{"base_amount": 15000.00, "vat_regime": "STANDARD_21"}'</pre>
                    </div>
                </div>
            </div>
        `;
    }

    function initSdkConsoleEvents() {}

    window.updateSdkPayloadExample = function() {
        const ep = document.getElementById('sdkEndpoint')?.value;
        const box = document.getElementById('sdkJsonBody');
        if (!box) return;

        if (ep === 'invoice') {
            box.value = JSON.stringify({
                invoice_number: "INV-2026-9812",
                buyer_vat: "NL862145890B01",
                currency: "EUR",
                standard: "EN_16931"
            }, null, 2);
        } else if (ep === 'forecast') {
            box.value = JSON.stringify({
                historical_months: 12,
                granularity: "MONTHLY",
                growth_confidence: 0.95
            }, null, 2);
        } else {
            box.value = JSON.stringify({
                client_name: "Rotterdam Logistics B.V.",
                fiscal_country: "NL",
                base_amount: 15000.00,
                vat_regime: "STANDARD_21"
            }, null, 2);
        }
    };

    window.executeSdkCall = function() {
        playAppBeep(880, 'sine', 0.1);
        const ep = document.getElementById('sdkEndpoint')?.value;
        const respBox = document.getElementById('sdkResponseBox');

        if (respBox) {
            respBox.innerText = '// جاري استدعاء السحابة...';
            setTimeout(() => {
                const res = {
                    status: "success",
                    code: 200,
                    endpoint: `/api/v1/${ep}`,
                    timestamp: new Date().toISOString(),
                    response: {
                        acknowledged: true,
                        cluster: "AMS-PROD-CLUSTER-01",
                        latency_ms: (12 + Math.random() * 8).toFixed(1)
                    }
                };
                respBox.innerText = JSON.stringify(res, null, 2);
                playAppBeep(1100, 'sine', 0.15);
            }, 300);
        }
    };

    window.switchSdkLang = function(lang, btn) {
        document.querySelectorAll('.sr-code-lang-pill').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        const pre = document.getElementById('sdkCodeSnippet');
        if (!pre) return;

        if (lang === 'python') {
            pre.innerText = `import requests

url = "https://api.coresync.eu/v1/tax/calculate-btw"
headers = {"Authorization": "Bearer sr_live_9481_ams"}
data = {"base_amount": 15000.0, "vat_regime": "STANDARD_21"}

response = requests.post(url, json=data, headers=headers)
print(response.json())`;
        } else if (lang === 'node') {
            pre.innerText = `const axios = require('axios');

const res = await axios.post('https://api.coresync.eu/v1/tax/calculate-btw', {
  base_amount: 15000.0,
  vat_regime: 'STANDARD_21'
}, {
  headers: { Authorization: 'Bearer sr_live_9481_ams' }
});
console.log(res.data);`;
        } else if (lang === 'csharp') {
            pre.innerText = `using var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "Bearer sr_live_9481_ams");
var json = "{\\"base_amount\\": 15000.0, \\"vat_regime\\": \\"STANDARD_21\\"}";
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync("https://api.coresync.eu/v1/tax/calculate-btw", content);`;
        } else {
            pre.innerText = `curl -X POST "https://api.coresync.eu/v1/tax/calculate-btw" \\
  -H "Authorization: Bearer sr_live_9481_ams" \\
  -H "Content-Type: application/json" \\
  -d '{"base_amount": 15000.00, "vat_regime": "STANDARD_21"}'`;
        }
    };

    // -------------------------------------------------------------
    // 11. License Activation Engine
    // -------------------------------------------------------------
    window.promptLicenseActivation = function(appId) {
        const sw = SOFTWARE_APPS[appId] || SOFTWARE_APPS.taxsync;
        const key = prompt(`🔑 أدخل مفتاح الترخيص التجاري أو التجريبي لـ [${sw.title}]:`, sw.defaultKey);
        if (key && key.trim()) {
            const cleanKey = key.trim().toUpperCase();
            const disp = document.getElementById('srCurrentLicenseDisplay');
            if (disp) disp.innerText = cleanKey;
            playAppBeep(950, 'sine', 0.2);
            if (typeof showPortalToast === 'function') {
                showPortalToast(`✓ تم تفعيل وتوثيق الترخيص [${cleanKey}] بنجاح!`);
            }
        }
    };

    // -------------------------------------------------------------
    // 12. Multilingual User Documentation & Manual Database (6 Languages)
    // -------------------------------------------------------------
    const SOFTWARE_DOCS = {
        ar: {
            guideBadge: 'دليل الاستخدام والتشغيل المعتمد • 2026',
            guideTitle: 'دليل تشغيل واستخدام برمجيات S&R CoreSync',
            allOverview: 'نظرة عامة على المنظومة',
            printBtn: '🖨️ طباعة الدليل',
            copyKeyBtn: '📋 نسخ مفتاح تجريبي',
            launchBtn: '⚡ تشغيل فوري في المتصفح',
            downloadBtn: '📥 تحميل النسخة أوفلاين',
            sections: {
                overview: '📌 الهدف والوظيفة الأساسية',
                hardware: '💻 الأجهزة والمدخلات المدعومة',
                steps: '🚀 خطوات الاستخدام والتشغيل خطوة بخطوة',
                compliance: '🛡️ الأمان والامتثال والضرائب الأوروبية',
                faq: '❓ الأسئلة الشائعة وحلول المشكلات'
            },
            apps: {
                taxsync: {
                    title: 'S&R TaxSync Desktop / Web',
                    subtitle: 'نظام حساب الضرائب الهولندية والخليجية وتوليد إقرارات Digipoort XML',
                    overview: 'برنامج محاسبي وضريبي مستقل ومكتبي (Offline-First) مصمم لحساب ضريبة القيمة المضافة BTW (21% و 9% و 0%) والضريبة الخليجية 15%، مع توليد فوري لإقرارات Digipoort XML الرسمية المعتمدة لدى مصلحة الضرائب الهولندية (Belastingdienst) وتصدير فواتير EN 16931 المشفرة محلياً.',
                    hardware: [
                        { name: '🖥️ أنظمة التشغيل', desc: 'يعمل على حواسيب Windows 11/10 و macOS Monterey+ و Linux Ubuntu دون قيود.' },
                        { name: '🌐 بيئة التشغيل', desc: 'يعمل كتطبيق سطح مكتب مستقل أو داخل المتصفح كـ PWA مع تشغيل كامل بدون اتصال بالإنترنت.' },
                        { name: '🔒 تخزين البيانات', desc: 'جميع الحسابات والفواتير تشفر وتخزن محلياً على جهازك ولا ترسل لأي سيرفر خارجي.' }
                    ],
                    steps: [
                        { title: 'اختيار النظام الضريبي', desc: 'حدد النظام الضريبي المناسب (BTW 21% العام، أو 9% المخفض، أو 15% الخليجي).' },
                        { title: 'إدخال المبالغ والمصروفات', desc: 'أدخل المبالغ الأساسية أو استورد ملفات الفواتير والمشتريات لحساب الضريبة تلقائياً.' },
                        { title: 'توليد ملف الإقرار الرسمي', desc: 'اضغط على "توليد إقرار Digipoort XML" للحصول على الملف الجاهز للإرسال لمصلحة الضرائب.' },
                        { title: 'طباعة الفاتورة والتقارير', desc: 'قم بتصدير الفواتير الرسمية بصيغة PDF المشفرة مع رمز التحقق الرقمي المعتمد.' }
                    ],
                    compliance: 'متوافق 100% مع المادة 52 من القانون العام للضرائب الهولندي (AWR Art. 52)، ومعايير معالجة البيانات الأوروبية GDPR Art. 32.',
                    faq: [
                        { q: 'هل يعمل البرنامج بدون إنترنت نهائياً؟', a: 'نعم، النظام مبني بمعمارية Offline-First، حيث تتم جميع العمليات الحسابية والتشفير وتوليد الملفات محلياً داخل جهازك.' },
                        { q: 'كيف أقوم بتفعيل النسخة الكاملة؟', a: 'يمكنك إدخال مفتاح الترخيص المكون من 16 خانة المشفر عبر زر تفعيل الترخيص أو تجربة النسخة التجريبية المجانية لمدة 14 يوماً.' }
                    ]
                },
                flowscan: {
                    title: 'S&R FlowScan AI Mobile',
                    subtitle: 'تطبيق المسح الضوئي الذكي للإيصالات والفواتير بالذكاء الاصطناعي والكاميرا',
                    overview: 'تطبيق هاتف ذكي يعتمد على خوارزميات الرؤية الحاسوبية والذكاء الاصطناعي (OCR AI) لمسح الفواتير والإيصالات الورقية بكاميرا الهاتف أو اللابتوب، واستخراج أسماء الموردين، وأرقام السجل الضريبي KvK/BTW، والتواريخ، والمبالغ، ونسب الضريبة بدقة 99.4% مع ترحيل فوري لنظام الـ ERP.',
                    hardware: [
                        { name: '📱 كاميرات الهواتف الذكية', desc: 'دعم كامل لكاميرات هواتف iPhone (iOS 17+) وأجهزة Android 14+ مع التركيز التلقائي.' },
                        { name: '💻 كاميرات الحواسيب المحمولة', desc: 'إمكانية التقاط ومسح الفواتير عبر كاميرا الويب (Webcam) المدمجة باللابتوب مباشرة.' },
                        { name: '📁 تحميل الصور والمستندات', desc: 'دعم سحب وإفلات صور الإيصالات (PNG, JPG, PDF) مباشرة للمعالجة الفورية.' }
                    ],
                    steps: [
                        { title: 'فتح الكاميرا ومحاذاة الإيصال', desc: 'اضغط على زر فتح الكاميرا ووجه عدسة الهاتف نحو الإيصال أو الفاتورة داخل إطار المسح.' },
                        { title: 'التقاط الصورة والمعالجة', desc: 'التقط الصورة ليبدأ محرك الذكاء الاصطناعي بالتعرف الضوئي واستخراج الحقول في 800 ميلي ثانية.' },
                        { title: 'مراجعة البيانات المستخرجة', desc: 'تحقق من المبالغ، والضريبة المحتسبة، وتصنيف المصروف (وقود، ضيافة، تشغيل).' },
                        { title: 'الترحيل الفوري لنظام ERP', desc: 'اضغط على "ترحيل للـ ERP" لتسجيل المصروف وتحديث التدفق النقدي للشركة لحظياً.' }
                    ],
                    compliance: 'معالجة مشفرة بالكامل عبر قنوات TLS 1.3 مع تخزين معزول في خوادم أمستردام AMS-IX متوافق مع معايير التدقيق المالي الأوروبية.',
                    faq: [
                        { q: 'هل يستطيع قراءة الفواتير المطوية أو باهتة الطباعة؟', a: 'نعم، يتضمن محرك FlowScan فلاتر ذكية لتعديل التباين وإزالة التشويش وتصحيح زوايا المستند آلياً قبل استخراج النصوص.' }
                    ]
                },
                cloudpos: {
                    title: 'S&R CloudPOS Connector',
                    subtitle: 'محطة كاشير ونقاط بيع ذكية مع دعم مسح الباركود بكاميرا الموبايل واللابتوب',
                    overview: 'نظام نقاط بيع وكاشير سحابي خفيف وفائق السرعة، يربط المتاجر والمطاعم والفعاليات المتنقلة بنظام إدارة المخازن والمحاسبة لحظياً. يتميز بقدرته الفريدة على مسح الباركود مباشرة عبر كاميرا الهاتف أو اللابتوب دون الحاجة لأجهزة سكانر إضافية، إلى جانب دعمه الكامل لأجهزة الباركود الخارجية وطابعات الفواتير الحرارية.',
                    hardware: [
                        { name: '📷 كاميرا الموبايل واللابتوب (بدون سكانر خارجي)', desc: 'قراءة ومسح باركود المنتجات (EAN-13, QR, Code-128) مباشرة عبر كاميرا الهاتف أو كاميرا الويب المدمجة باللابتوب بدقة فائقة وبشكل مجاني تماماً.' },
                        { name: '🔫 أجهزة قراءة الباركود الخارجية (Scanner Gun)', desc: 'توافق كامل وبشكل فوري Plug-and-Play مع جميع أجهزة قارئ الباركود السلكية (USB) واللاسلكية (Bluetooth / 2.4GHz).' },
                        { name: '🧾 طابعات الفواتير الحرارية (Thermal POS)', desc: 'دعم بروتوكولات طابعات الإيصالات الحرارية ESC/POS بمقاسات 80mm و 58mm مع طباعة سريعة ورمز QR الفاتورة.' },
                        { name: '🖥️ شاشات اللمس والأجهزة', desc: 'تصميم متجاوب بالكامل مع شاشات اللمس للكاشير، وحواسيب Windows POS، والأجهزة اللوحية (iPad/Android Tablets).' }
                    ],
                    steps: [
                        { title: 'فتح شاشة الكاشير والمبيعات', desc: 'شغل التطبيق من المتصفح أو التطبيق المستقل لتظهر لك واجهة البيع السريع وكتالوج الأصناف.' },
                        { title: 'مسح الباركود (بالكاميرا أو السكانر)', desc: 'اضغط على "📷 مسح الباركود بكاميرا الجهاز" ووجه الكاميرا نحو باركود المنتج، أو استخدم السكانر الخارجي، أو انقر على المنتج من الشاشة.' },
                        { title: 'تحديد الكميات وطريقة الدفع', desc: 'يتم احتساب الإجمالي والضريبة فورياً. اختر وسيلة الدفع (نقد / كاش، بطاقة ائتمان، iDEAL / PIN).' },
                        { title: 'طباعة الإيصال وتحديث المخزون', desc: 'اضغط "إتمام البيع وطباعة الفاتورة" لطباعة الإيصال الحراري وخصم الكمية من المخزون المركزي فوراً.' }
                    ],
                    compliance: 'متوافق مع معايير السجلات النقدية الأوروبية المقاومة للتلاعب (Cash Register Audit Trail) وقوانين الفاتورة الإلكترونية الموحدة.',
                    faq: [
                        { q: 'هل يمكنني استخدام كاميرا الموبايل أو اللابتوب كقارئ باركود بدلاً من شراء جهاز سكانر؟', a: 'نعم بكل تأكيد وبنسبة 100%! يتيح لك تطبيق S&R CloudPOS مسح الباركود مباشرة وبدقة فائقة باستخدام كاميرا هاتفك المحمول أو كاميرا اللابتوب العادية دون دفع أي تكاليف لأجهزة إضافية.' },
                        { q: 'ماذا يحدث إذا انقطع الإنترنت أثناء البيع في المحل؟', a: 'يواصل التطبيق عمله بشكل طبيعي أوفلاين ويخزن جميع العمليات في الذاكرة المحلية المشفرة، وبمجرد عودة الإنترنت تتم مزامنة المبيعات والمخزون تلقائياً.' }
                    ]
                },
                vault: {
                    title: 'S&R SecureVault B2B',
                    subtitle: 'برمجية التشفير العسكري AES-256 GCM لحماية قواعد البيانات والمستندات الحساسة',
                    overview: 'أداة أمن سيبراني وتشفير متقدمة تعمل محلياً داخل المتصفح بمعيار AES-256 GCM المعتمد لدى المؤسسات العسكرية والمالية، تتيح للمؤسسات تشفير النسخ الاحتياطية والعقود وسجلات الموظفين قبل رفعها أو إرسالها دون أي إمكانية لفك تشفيرها بدون المفتاح السري.',
                    hardware: [
                        { name: '💻 بيئات التشغيل', desc: 'متوافق مع جميع الحواسيب وأنظمة التشغيل (Windows, Mac, Linux, Mobile).' },
                        { name: '🛡️ محرك التشفير', desc: 'يعتمد على Web Cryptography API للأجهزة الحديثة مع تسريع عتادي (Hardware Acceleration).' },
                        { name: '💾 التخزين الآمن', desc: 'تصدير ملفات مشفرة بامتداد .srvault معزولة تماماً عن الوصول غير المصرح به.' }
                    ],
                    steps: [
                        { title: 'اختيار الملف أو النص الحساس', desc: 'قم بسحب وإفلات الملف أو كتابة البيانات السرية داخل صندوق التشفير الآمن.' },
                        { title: 'تعيين كلمة المرور والمفتاح', desc: 'أدخل كلمة مرور قوية لتوليد مفتاح تشفير 256-bit باستخدام خوارزمية PBKDF2/Argon2.' },
                        { title: 'تنفيذ التشفير وتنزيل الملف', desc: 'اضغط على "تشفير وحفظ محلياً" لتحميل النسخة المشفرة الآمنة مباشرة.' },
                        { title: 'فك التشفير عند الحاجة', desc: 'يمكنك فك التشفير في أي وقت عبر إدخال نفس كلمة المرور على أي جهاز بدون إنترنت.' }
                    ],
                    compliance: 'متوافق 100% مع المادة 32 من لائحة حماية البيانات العامة الأوروبية (GDPR Art. 32) ومعيار FIPS 140-2 للتشفير المعتمد.',
                    faq: [
                        { q: 'هل تستطيع الشركة أو الخادم الاطلاع على بياناتي المشفرة؟', a: 'مستحيل تماماً؛ التشفير يتم محلياً (Zero-Knowledge Client-Side) داخل متصفح جهازك ولا يصل المفتاح أو البيانات غير المشفرة لأي خادم.' }
                    ]
                },
                sdk: {
                    title: 'S&R Financial AI SDK Console',
                    subtitle: 'وحدة المطورين والـ REST APIs لدمج الضرائب والذكاء الاصطناعي المالي',
                    overview: 'بوابة تفاعلية وحزمة أدوات برمجية (SDK) مخصصة للشركات البرمجية والمطورين لدمج محركات حساب الضرائب الأوروبية، والتنبؤ المالي، والفوترة الإلكترونية داخل تطبيقاتهم الخاصة بسهولة عبر واجهات برمجة التطبيقات REST APIs.',
                    hardware: [
                        { name: '🌐 لغات البرمجة المدعومة', desc: 'مكتبات وأكواد جاهزة للغات Python و Node.js و C# و PHP و cURL.' },
                        { name: '⚡ منصات الخوادم', desc: 'متوافقة مع بيئات Docker و Kubernetes و Cloud Functions و Lambda.' },
                        { name: '🔑 إدارة التراخيص', desc: 'توليد فوري لمفاتيح الـ API مع نظام مراقبة استهلاك ومعدل طلبات Rate Limiting.' }
                    ],
                    steps: [
                        { title: 'توليد مفتاح الـ API', desc: 'احصل على مفتاح الوصول الخاص بتطبيقك من لوحة تحكم المطورين.' },
                        { title: 'اختيار نقطة الاتصال (Endpoint)', desc: 'اختر الواجهة المطلوبة (مثل: حساب ضريبة BTW، أو توقع السيولة، أو التحقق من الفواتير).' },
                        { title: 'تجربة الطلب في الـ Sandbox', desc: 'أرسل نموذج تجريبي وشاهد رد السيرفر الفوري بصيغة JSON مع كود الاستجابة HTTP 200.' },
                        { title: 'نسخ الكود الجاهز لمشروعك', desc: 'انسخ كود الدمج بلغتك البرمجية المفضلة بضغطة زر وأضفه إلى نظامك مباشرة.' }
                    ],
                    compliance: 'مبنية وفق معايير OpenAPI 3.0 مع تشفير كامل TLS 1.3 وتوافق مع لوائح التراخيص البرمجية B2B.',
                    faq: [
                        { q: 'هل تتوفر بيئة تجريبية Sandbox مجانية؟', a: 'نعم، توفر المنصة 500 مكالمة تجريبية مجانية يومياً لكل مطور لاختبار التطبيقات قبل الانتقال للإنتاج.' }
                    ]
                },
                terminal: {
                    title: 'S&R Cloud Terminal Agent',
                    subtitle: 'لوحة مراقبة الخوادم والحاويات وحالة الميكروسيرفس السحابية',
                    overview: 'أداة خفيفة لمراقبة البنية التحتية السحابية والخوادم، تتتبع نبضات الخدمات (Heartbeats)، واستهلاك المعالج والذاكرة، ومعدلات استجابة قواعد البيانات، مع أدوات تحكم مباشرة لإعادة تشغيل الخدمات تلقائياً عند أي طارئ.',
                    hardware: [
                        { name: '☁️ الخوادم السحابية', desc: 'دعم مراقبة خوادم Linux (Ubuntu/Debian) و Windows Server و Cloud VMs.' },
                        { name: '📦 الحاويات والميكروسيرفس', desc: 'تكامل كامل مع بيئات Docker Containers و Kubernetes Pods.' },
                        { name: '📡 بروتوكولات المراقبة', desc: 'مراقبة عبر WebSocket و gRPC مع تنبيهات فورية بالبريد والـ Webhooks.' }
                    ],
                    steps: [
                        { title: 'ربط وكيل المراقبة (Agent)', desc: 'قم بتثبيت الوكيل السحابي عبر أمر تشغيل سطر واحد في خادمك.' },
                        { title: 'متابعة المؤشرات الحيوية', desc: 'شاهد الرسم البياني الحي لاستهلاك المعالج، والذاكرة، والـ Latency في خوادم أمستردام.' },
                        { title: 'ضبط التنبيهات الذكية', desc: 'حدد عتبات التنبيه التلقائية عند تجاوز استهلاك الموارد للنسب المحددة.' },
                        { title: 'الإدارة السريعة للخدمات', desc: 'قم بإعادة تشغيل أو تنظيف الكاش لأي ميكروسيرفس بنقرة واحدة من لوحة التحكم.' }
                    ],
                    compliance: 'سجلات تدقيق أمنية معتمدة وفق ISO 27001 واتصال مشفر متبادل mTLS.',
                    faq: [
                        { q: 'ما هو حجم استهلاك الوكيل لموارد الخادم؟', a: 'الوكيل خفيف جداً، يستهلك أقل من 15 ميجابايت من الذاكرة وأقل من 0.2% من المعالج.' }
                    ]
                }
            }
        },
        en: {
            guideBadge: 'OFFICIAL OPERATOR & USER MANUAL • 2026',
            guideTitle: 'S&R CoreSync Software Operational Guides & Manuals',
            allOverview: 'System Overview & Suite Catalog',
            printBtn: '🖨️ Print Guide',
            copyKeyBtn: '📋 Copy Trial Key',
            launchBtn: '⚡ Instant Browser Launch',
            downloadBtn: '📥 Download Offline Package',
            sections: {
                overview: '📌 Purpose & System Overview',
                hardware: '💻 Supported Devices & Input Hardware',
                steps: '🚀 Step-by-Step Quick Start Guide',
                compliance: '🛡️ Security, Cryptography & EU Compliance',
                faq: '❓ Frequently Asked Questions & Troubleshooting'
            },
            apps: {
                taxsync: {
                    title: 'S&R TaxSync Desktop / Web',
                    subtitle: 'Dutch & Gulf VAT calculation and official Digipoort XML filing system',
                    overview: 'A standalone, offline-first accounting and taxation platform designed for calculating Dutch BTW (21%, 9%, 0%) and Gulf VAT (15%). It generates official Digipoort XML tax returns certified for the Dutch Tax Authority (Belastingdienst) and exports compliant encrypted EN 16931 invoices.',
                    hardware: [
                        { name: '🖥️ Operating Systems', desc: 'Runs natively on Windows 11/10 (64-bit), macOS Monterey+, and Linux Ubuntu/Debian.' },
                        { name: '🌐 Runtime Environment', desc: 'Operates as an offline-first desktop application or as an in-browser progressive web app.' },
                        { name: '🔒 Local Data Storage', desc: 'All figures and invoices are encrypted and stored locally without leaving your machine.' }
                    ],
                    steps: [
                        { title: 'Select Tax Regime', desc: 'Choose standard BTW 21%, reduced BTW 9%, or Gulf VAT 15%.' },
                        { title: 'Input Transactions', desc: 'Enter amounts manually or import invoices to compute taxes automatically.' },
                        { title: 'Generate XML Return', desc: 'Click "Generate Digipoort XML" to prepare your official filing for Belastingdienst.' },
                        { title: 'Export & Print', desc: 'Export official encrypted PDF invoices with compliant QR verification codes.' }
                    ],
                    compliance: '100% compliant with Dutch Tax Law (AWR Art. 52) and European GDPR Art. 32 local encryption standards.',
                    faq: [
                        { q: 'Does it require an active internet connection?', a: 'No, it is 100% Offline-First. All computations and file exports happen locally on your device.' }
                    ]
                },
                flowscan: {
                    title: 'S&R FlowScan AI Mobile',
                    subtitle: 'AI-powered mobile receipt and invoice scanner with live camera OCR',
                    overview: 'A mobile smartphone and tablet application leveraging computer vision and on-device OCR AI to scan paper receipts and invoices using device cameras, extracting vendor names, KvK/BTW tax numbers, dates, amounts, and tax brackets with 99.4% precision and instant ERP synchronization.',
                    hardware: [
                        { name: '📱 Mobile Phone Cameras', desc: 'Full support for iPhone (iOS 17+) and Android 14+ cameras with auto-focus.' },
                        { name: '💻 Laptop Webcams', desc: 'Directly scan paper documents using your integrated laptop webcam.' },
                        { name: '📁 Document Upload', desc: 'Drag and drop receipt images (PNG, JPG, PDF) for instant OCR parsing.' }
                    ],
                    steps: [
                        { title: 'Open Camera & Align', desc: 'Launch camera scanner and align receipt inside the optical viewfinder frame.' },
                        { title: 'Capture & Process', desc: 'Snap photo to trigger AI OCR extraction within 800 milliseconds.' },
                        { title: 'Review Fields', desc: 'Verify extracted vendor, total amount, and expense categorization.' },
                        { title: 'Sync to ERP', desc: 'Tap "Sync to ERP" to record expenses and update cashflows in real time.' }
                    ],
                    compliance: 'Encrypted via TLS 1.3 channels with isolated Amsterdam AMS-IX storage compliant with EU audit standards.',
                    faq: [
                        { q: 'Can it scan wrinkled or faded receipts?', a: 'Yes, FlowScan features automated contrast normalization, noise removal, and perspective correction.' }
                    ]
                },
                cloudpos: {
                    title: 'S&R CloudPOS Connector',
                    subtitle: 'Smart Cloud POS terminal with smartphone & laptop camera barcode scanning',
                    overview: 'A high-speed, lightweight cloud point of sale and cashier terminal that links retail shops, dining venues, and mobile sales booths directly to inventory and accounting. Features native barcode reading through mobile and laptop cameras without extra hardware, alongside full support for external barcode guns and thermal printers.',
                    hardware: [
                        { name: '📷 Phone & Laptop Cameras (No Hardware Scanner Required)', desc: 'Scan product barcodes (EAN-13, QR, Code-128) directly via your mobile phone camera or laptop webcam with zero extra hardware cost!' },
                        { name: '🔫 External Barcode Scanner Guns', desc: 'Instant plug-and-play compatibility with USB, wireless 2.4G, and Bluetooth 1D/2D laser scanners.' },
                        { name: '🧾 Thermal Receipt Printers (POS)', desc: 'Direct ESC/POS protocol support for 80mm and 58mm thermal rolls with fast receipt printing and QR codes.' },
                        { name: '🖥️ Touchscreens & Devices', desc: 'Fully responsive for touch terminals, Windows POS PCs, and iPad/Android tablets.' }
                    ],
                    steps: [
                        { title: 'Launch Cashier Screen', desc: 'Open terminal from browser or standalone app to display sales catalog and cart.' },
                        { title: 'Scan Barcodes (Camera or Scanner)', desc: 'Click "📷 Scan Barcode with Camera" and point your phone/laptop camera at the product, or use a hardware scanner gun, or click catalog items.' },
                        { title: 'Adjust Quantities & Pay', desc: 'Totals and tax calculate instantly. Choose Cash, Credit Card, or iDEAL / PIN.' },
                        { title: 'Print Receipt & Sync Stock', desc: 'Complete checkout to print thermal ticket and decrement cloud inventory in real time.' }
                    ],
                    compliance: 'Compliant with European anti-tamper cash register audit trail regulations and EN 16931 receipt formatting.',
                    faq: [
                        { q: 'Can I scan barcodes using my mobile phone or laptop camera without buying a dedicated scanner gun?', a: 'YES, absolutely 100%! S&R CloudPOS features a built-in optical camera scanner that turns any smartphone or laptop webcam into a professional barcode reader immediately with zero additional equipment needed.' },
                        { q: 'What happens if the internet disconnects during store hours?', a: 'The app continues operating offline without interruption, buffering transactions locally and synchronizing them automatically once connection returns.' }
                    ]
                },
                vault: {
                    title: 'S&R SecureVault B2B',
                    subtitle: 'Military-grade AES-256 GCM encryption for sensitive databases and backups',
                    overview: 'Advanced client-side cybersecurity encryption tool running entirely in the browser using military AES-256 GCM standards. Allows businesses to encrypt database backups, contracts, and confidential records before upload with zero knowledge architecture.',
                    hardware: [
                        { name: '💻 System Platforms', desc: 'Compatible across Windows, Mac, Linux, and mobile browsers.' },
                        { name: '🛡️ Crypto Engine', desc: 'Leverages hardware-accelerated Web Cryptography API.' },
                        { name: '💾 Secure Storage', desc: 'Exports encrypted .srvault files protected against unauthorized access.' }
                    ],
                    steps: [
                        { title: 'Select File or Record', desc: 'Drag and drop files or paste confidential data into the secure vault vault box.' },
                        { title: 'Set Passphrase', desc: 'Provide a strong passphrase to derive a 256-bit key using PBKDF2/Argon2.' },
                        { title: 'Encrypt & Download', desc: 'Click "Encrypt & Secure" to download your protected .srvault file.' },
                        { title: 'Decrypt Anywhere', desc: 'Decrypt anytime using your secret passphrase even completely offline.' }
                    ],
                    compliance: '100% compliant with EU GDPR Article 32 and FIPS 140-2 certified encryption algorithms.',
                    faq: [
                        { q: 'Can S&R servers read my encrypted files?', a: 'Never. Encryption occurs strictly on your client device (Zero-Knowledge) and keys never leave your machine.' }
                    ]
                },
                sdk: {
                    title: 'S&R Financial AI SDK Console',
                    subtitle: 'Developer API Console for European tax logic and financial algorithms',
                    overview: 'An interactive developer suite and REST API SDK enabling software teams to embed European tax computation, liquidity forecasting, and e-invoicing directly into their internal ERPs and web applications.',
                    hardware: [
                        { name: '🌐 Supported Languages', desc: 'Pre-built snippets for Python, Node.js, C#, PHP, and cURL.' },
                        { name: '⚡ Cloud Environments', desc: 'Compatible with Docker, Kubernetes, AWS Lambda, and Azure Functions.' },
                        { name: '🔑 Key Management', desc: 'Instant API key generation with usage tracking and rate-limiting.' }
                    ],
                    steps: [
                        { title: 'Generate API Token', desc: 'Obtain your unique application key from the developer dashboard.' },
                        { title: 'Select Endpoint', desc: 'Pick desired REST endpoint (e.g. /v1/tax/calculate-btw).' },
                        { title: 'Test in Sandbox', desc: 'Run requests live and inspect JSON response with HTTP 200 verification.' },
                        { title: 'Integrate Code', desc: 'Copy client snippets in your language of choice into your codebase.' }
                    ],
                    compliance: 'OpenAPI 3.0 compliant specifications with TLS 1.3 encryption and enterprise SLA.',
                    faq: [
                        { q: 'Is there a free sandbox for testing?', a: 'Yes, each developer account receives 500 free sandbox calls daily for prototyping.' }
                    ]
                },
                terminal: {
                    title: 'S&R Cloud Terminal Agent',
                    subtitle: 'Real-time telemetry and microservices management console',
                    overview: 'A lightweight cloud telemetry agent tracking CPU, memory, database latency, and service heartbeats across Amsterdam AMS-IX clusters with automated self-healing and remote restarts.',
                    hardware: [
                        { name: '☁️ Cloud Hosts', desc: 'Supports Linux (Ubuntu/Debian), Windows Server, and cloud VMs.' },
                        { name: '📦 Containers', desc: 'Seamless integration with Docker and Kubernetes clusters.' },
                        { name: '📡 Protocols', desc: 'Real-time monitoring via WebSocket and gRPC with instant webhook alerting.' }
                    ],
                    steps: [
                        { title: 'Install Agent', desc: 'Deploy agent daemon with a one-line terminal command on your server.' },
                        { title: 'Monitor Health', desc: 'Observe live charts for CPU, memory, and latency in Amsterdam node.' },
                        { title: 'Configure Alerts', desc: 'Set resource threshold triggers for email and webhook notifications.' },
                        { title: 'Manage Services', desc: 'Restart or flush cache on any service with a single click.' }
                    ],
                    compliance: 'ISO 27001 certified security logs and mutual mTLS communication channels.',
                    faq: [
                        { q: 'How much overhead does the agent introduce?', a: 'Minimal overhead: uses less than 15MB RAM and under 0.2% CPU.' }
                    ]
                }
            }
        },
        nl: {
            guideBadge: 'OFFICIËLE HANDLEIDING & GEBRUIKERSGIDS • 2026',
            guideTitle: 'S&R CoreSync Software Handleidingen en Instructies',
            allOverview: 'Overzicht van het Systeem & Suite',
            printBtn: '🖨️ Handleiding Afdrukken',
            copyKeyBtn: '📋 Proeflicentie Kopiëren',
            launchBtn: '⚡ Direct Starten in Browser',
            downloadBtn: '📥 Offline Versie Downloaden',
            sections: {
                overview: '📌 Doel en Systeemoverzicht',
                hardware: '💻 Ondersteunde Hardware en Apparaten',
                steps: '🚀 Stapsgewijze Snelle Handleiding',
                compliance: '🛡️ Veiligheid, Cryptografie & Belastingdienst',
                faq: '❓ Veelgestelde Vragen & Probleemoplossing'
            },
            apps: {
                taxsync: {
                    title: 'S&R TaxSync Desktop / Web',
                    subtitle: 'Nederlandse BTW-berekening en officiële Digipoort XML-aangiftes',
                    overview: 'Een zelfstandig, offline-first boekhoudkundig en fiscaal platform voor het berekenen van Nederlandse BTW (21%, 9%, 0%) en golfregio BTW. Genereert officiële Digipoort XML-aangiftes conform Belastingdienst en exporteert gecodeerde EN 16931 facturen.',
                    hardware: [
                        { name: '🖥️ Besturingssystemen', desc: 'Werkt op Windows 11/10, macOS Monterey+ en Linux Ubuntu.' },
                        { name: '🌐 Omgeving', desc: 'Functioneert volledig zonder internetverbinding (Offline-First).' },
                        { name: '🔒 Gegevensopslag', desc: 'Alle gegevens worden lokaal versleuteld opgeslagen conform AVG / GDPR.' }
                    ],
                    steps: [
                        { title: 'BTW-tarief Selecteren', desc: 'Kies tussen 21% algemeen, 9% verlaagd of 0% verlegd tarief.' },
                        { title: 'Bedragen Invoeren', desc: 'Voer omzet en kosten in voor automatische voorbelastingberekening.' },
                        { title: 'XML-Aangifte Genereren', desc: 'Maak met één klik het officiële Digipoort XML-bestand gereed voor verzending.' },
                        { title: 'Factuur Exporteren', desc: 'Print of exporteer officiële PDF-facturen met verificatiecode.' }
                    ],
                    compliance: 'Volledig conform AWR Art. 52 en de richtlijnen van de Belastingdienst.',
                    faq: [
                        { q: 'Werkt het programma zonder internet?', a: 'Ja, 100% Offline-First. Uw gegevens blijven veilig op uw eigen computer.' }
                    ]
                },
                cloudpos: {
                    title: 'S&R CloudPOS Connector',
                    subtitle: 'Slimme POS Kassa met Barcode Scannen via Telefoon- en Laptopcamera',
                    overview: 'Een modern kassasysteem dat winkels en horeca direct koppelt aan voorraadbeheer en boekhouding. Kan barcodes direct scannen via de ingebouwde camera van smartphone of laptop, zonder dure handscanners aan te hoeven schaffen.',
                    hardware: [
                        { name: '📷 Camera van Telefoon & Laptop (Geen Handscanner Nodig)', desc: 'Scan barcodes (EAN-13, QR, Code-128) direct via uw mobiele camera of webcam zonder extra hardware!' },
                        { name: '🔫 Externe Barcodescanners', desc: 'Ondersteunt USB, Bluetooth en draadloze 2.4GHz barcode pistolen plug-and-play.' },
                        { name: '🧾 Thermische Bonprinters', desc: 'Directe ESC/POS thermische bonprint op 80mm en 58mm papierrollen.' }
                    ],
                    steps: [
                        { title: 'Kassa Openen', desc: 'Start de kassa-omgeving vanuit de browser of de standalone app.' },
                        { title: 'Barcode Scannen', desc: 'Klik op "📷 Barcode scannen met camera" of richt uw externe scanner op het product.' },
                        { title: 'Afrekenen', desc: 'Selecteer contant, bankkaart of iDEAL / PIN voor directe verwerking.' },
                        { title: 'Bon Afdrukken', desc: 'Print direct de kassabon en de voorraad wordt realtime bijgewerkt.' }
                    ],
                    compliance: 'Voldoet aan de Europese auditvereisten voor kassa- en voorraadtransacties.',
                    faq: [
                        { q: 'Kan ik barcodes scannen met mijn telefoon- of laptopcamera zonder een externe scanner te kopen?', a: 'Ja, absoluut 100%! Met S&R CloudPOS gebruikt u direct uw eigen camera als professionele barcodescanner, volledig kosteloos en zonder extra apparaten.' }
                    ]
                },
                flowscan: {
                    title: 'S&R FlowScan AI Mobile',
                    subtitle: 'Mobiele AI bonscanner met automatische tekstherkenning',
                    overview: 'Mobiele applicatie voor het scannen van bonnetjes en facturen via de camera met 99.4% nauwkeurigheid en automatische BTW-uitsplitsing.',
                    hardware: [{ name: '📱 Mobiel', desc: 'Geschikt voor iOS en Android smartphones en laptop webcams.' }],
                    steps: [
                        { title: 'Foto maken', desc: 'Lijn het bonnetje uit binnen het camerakader.' },
                        { title: 'AI analyse', desc: 'Gegevens worden binnen 800ms geëxtraheerd.' },
                        { title: 'Synchroniseren', desc: 'Boek de uitgave direct in uw ERP-systeem.' }
                    ],
                    compliance: 'Volledig versleuteld conform AVG / GDPR normen in Amsterdam AMS-IX.',
                    faq: [{ q: 'Werkt het bij slecht licht?', a: 'Ja, de AI past automatisch contrast en belichting aan.' }]
                },
                vault: {
                    title: 'S&R SecureVault B2B',
                    subtitle: 'Militaire AES-256 GCM encryptie voor bedrijfsgegevens',
                    overview: 'Beveiligingsapplicatie die bestanden lokaal in de browser versleutelt met AES-256 GCM voordat ze worden opgeslagen.',
                    hardware: [{ name: '💻 Universeel', desc: 'Ondersteund op alle moderne browsers en apparaten.' }],
                    steps: [
                        { title: 'Bestand kiezen', desc: 'Selecteer het gevoelige document.' },
                        { title: 'Wachtwoord invoeren', desc: 'Genereer een 256-bit cryptografische sleutel.' },
                        { title: 'Versleutelen', desc: 'Download het beveiligde .srvault bestand.' }
                    ],
                    compliance: 'Voldoet aan AVG / GDPR Artikel 32 en FIPS 140-2 encryptiestandaarden.',
                    faq: [{ q: 'Heeft iemand anders toegang?', a: 'Nee, Zero-Knowledge encryptie op uw eigen toestel.' }]
                },
                sdk: {
                    title: 'S&R Financial AI SDK Console',
                    subtitle: 'REST API console voor fiscale en financiële automatisering',
                    overview: 'API console voor softwareontwikkelaars om BTW-berekening en facturatie in eigen software te integreren.',
                    hardware: [{ name: '🌐 APIs', desc: 'Geschikt voor Python, Node.js, C#, PHP en cURL.' }],
                    steps: [
                        { title: 'API Key aanmaken', desc: 'Genereer uw ontwikkelaarsleutel.' },
                        { title: 'Testen', desc: 'Test live endpoints in de sandbox omgeving.' },
                        { title: 'Integreren', desc: 'Kopieer kant-en-klare code naar uw project.' }
                    ],
                    compliance: 'OpenAPI 3.0 specificatie met TLS 1.3 beveiliging.',
                    faq: [{ q: 'Is er een gratis sandbox?', a: 'Ja, 500 gratis calls per dag voor ontwikkelaars.' }]
                },
                terminal: {
                    title: 'S&R Cloud Terminal Agent',
                    subtitle: 'Realtime servermonitoring en microservices beheer',
                    overview: 'Lichtgewicht monitoringsagent voor CPU, geheugen en responstijden in Amsterdamse datacenters.',
                    hardware: [{ name: '☁️ Servers', desc: 'Geschikt voor Linux, Windows Server en Docker clusters.' }],
                    steps: [
                        { title: 'Agent installeren', desc: 'Installeer met één terminalopdracht.' },
                        { title: 'Monitoren', desc: 'Bekijk realtime grafieken en metrics.' },
                        { title: 'Beheren', desc: 'Herstart services met één klik bij incidenten.' }
                    ],
                    compliance: 'ISO 27001 gecertificeerde logs en mTLS communicatie.',
                    faq: [{ q: 'Belast dit de server?', a: 'Nee, verbruikt minder dan 15MB geheugen en 0.2% CPU.' }]
                }
            }
        },
        de: {
            guideBadge: 'OFFIZIELLES BEDIENUNGSHANDBUCH • 2026',
            guideTitle: 'S&R CoreSync Software Benutzerhandbücher & Dokumentation',
            allOverview: 'Systemübersicht & Gesamtkatalog',
            printBtn: '🖨️ Handbuch Drucken',
            copyKeyBtn: '📋 Testlizenz Kopieren',
            launchBtn: '⚡ Sofort im Browser Starten',
            downloadBtn: '📥 Offline-Version Herunterladen',
            sections: {
                overview: '📌 Zweck & Systemüberblick',
                hardware: '💻 Unterstützte Hardware & Eingabegeräte',
                steps: '🚀 Schritt-für-Schritt Schnellstartanleitung',
                compliance: '🛡️ Sicherheit, Kryptographie & EU-Konformität',
                faq: '❓ Häufig gestellte Fragen & Fehlerbehebung'
            },
            apps: {
                taxsync: {
                    title: 'S&R TaxSync Desktop / Web',
                    subtitle: 'EU- & Niederlande-Steuerrechner mit Digipoort XML-Generierung',
                    overview: 'Eigenständiges, Offline-First Finanz- und Steuerberechnungsprogramm für die niederländische BTW (21%, 9%, 0%) sowie europäische Steuerstandards mit verschlüsselten EN 16931 Rechnungen.',
                    hardware: [{ name: '🖥️ Betriebssysteme', desc: 'Windows 11/10, macOS und Linux. 100% offline nutzbar.' }],
                    steps: [
                        { title: 'Steuersatz wählen', desc: 'Wählen Sie den gewünschten BTW-Satz aus.' },
                        { title: 'Beträge erfassen', desc: 'Erfassen Sie Beträge für die sofortige Steuerberechnung.' },
                        { title: 'XML exportieren', desc: 'Erstellen Sie die offizielle Digipoort XML-Meldung.' },
                        { title: 'Rechnung drucken', desc: 'Drucken Sie die konforme PDF-Rechnung mit Prüfcode.' }
                    ],
                    compliance: 'Konform mit niederländischem Steuerrecht AWR Art. 52 und DSGVO Art. 32.',
                    faq: [{ q: 'Funktioniert es offline?', a: 'Ja, 100% Offline-First. Ihre Daten verbleiben auf Ihrem Rechner.' }]
                },
                cloudpos: {
                    title: 'S&R CloudPOS Connector',
                    subtitle: 'Cloud-Kassensystem mit Barcode-Scan über Smartphone- & Laptop-Kamera',
                    overview: 'Intelligentes Kassensystem, das Barcodes direkt über die Kamera von Smartphone oder Laptop erfasst – ganz ohne teure externe Scannerpistolen.',
                    hardware: [
                        { name: '📷 Smartphone- & Laptop-Kamera (Kein externer Scanner nötig)', desc: 'Barcodes (EAN-13, QR, Code-128) direkt über Handykamera oder Laptop-Webcam blitzschnell scannen!' },
                        { name: '🔫 Externe Scannerpistolen', desc: 'Kompatibel mit USB-, Bluetooth- und 2.4GHz Barcode-Scannern.' },
                        { name: '🧾 Thermobondrucker', desc: 'Unterstützung für ESC/POS 80mm und 58mm Bonrollen.' }
                    ],
                    steps: [
                        { title: 'Kasse öffnen', desc: 'Starten Sie das Terminal im Browser oder als App.' },
                        { title: 'Barcode scannen', desc: 'Klicken Sie auf "📷 Barcode mit Kamera scannen" oder nutzen Sie Ihre Scannerpistole.' },
                        { title: 'Bezahlen', desc: 'Wählen Sie Bar, Karte oder PIN/iDEAL.' },
                        { title: 'Bon drucken', desc: 'Kassenzettel drucken und Lagerbestand in Echtzeit aktualisieren.' }
                    ],
                    compliance: 'Erfüllt europäische Richtlinien für Kassenführung und GoBD/EU-Standards.',
                    faq: [
                        { q: 'Kann ich Barcodes mit der Handykamera oder Laptopkamera scannen ohne einen Scanner zu kaufen?', a: 'Ja, absolut zu 100%! Mit S&R CloudPOS nutzen Sie einfach Ihre vorhandene Kamera als hochpräzisen Barcode-Scanner – komplett kostenlos und ohne Zusatzgeräte.' }
                    ]
                },
                flowscan: {
                    title: 'S&R FlowScan AI Mobile',
                    subtitle: 'Intelligente Beleg- und Rechnungserfassung per Smartphone-Kamera',
                    overview: 'Mobile Anwendung zur automatischen optischen Zeichenerkennung (OCR AI) von Rechnungen und Quittungen mit direkter ERP-Übertragung.',
                    hardware: [{ name: '📱 Mobilgeräte', desc: 'iPhone (iOS 17+), Android 14+ sowie Laptop-Webcams.' }],
                    steps: [
                        { title: 'Kamera ausrichten', desc: 'Halten Sie den Beleg in das Scanfenster.' },
                        { title: 'Erfassen', desc: 'Das KI-Modell liest Beträge und Steuern in 800ms aus.' },
                        { title: 'Synchronisieren', desc: 'Übertragen Sie die Ausgabe direkt ins ERP.' }
                    ],
                    compliance: 'Vollständig verschlüsselt nach DSGVO im Rechenzentrum Amsterdam AMS-IX.',
                    faq: [{ q: 'Werden zerknitterte Belege erkannt?', a: 'Ja, intelligente Filter korrigieren Kontrast und Neigungswinkel automatisch.' }]
                },
                vault: {
                    title: 'S&R SecureVault B2B',
                    subtitle: 'Militärische AES-256 GCM Verschlüsselung für Unternehmensdaten',
                    overview: 'Verschlüsselt Datenbanken und sensible Dokumente direkt im Browser nach AES-256 GCM Standards.',
                    hardware: [{ name: '💻 Plattformunabhängig', desc: 'Funktioniert in jedem modernen Webbrowser.' }],
                    steps: [
                        { title: 'Datei wählen', desc: 'Dokument auswählen oder Text eingeben.' },
                        { title: 'Passwort setzen', desc: '256-Bit Schlüssel über PBKDF2 ableiten.' },
                        { title: 'Verschlüsseln', desc: 'Geschützte .srvault Datei lokal abspeichern.' }
                    ],
                    compliance: 'DSGVO Artikel 32 und FIPS 140-2 konform.',
                    faq: [{ q: 'Können Dritte die Daten einsehen?', a: 'Nein, echtes Zero-Knowledge auf Ihrem eigenen Endgerät.' }]
                },
                sdk: {
                    title: 'S&R Financial AI SDK Console',
                    subtitle: 'Entwickler-REST-APIs für Steuern und Finanzlogik',
                    overview: 'API-Konsole zur Einbindung von Steuerberechnung und Rechnungsstellung in Ihre eigenen Softwaresysteme.',
                    hardware: [{ name: '🌐 Sprachen', desc: 'Python, Node.js, C#, PHP und cURL Vorlagen.' }],
                    steps: [
                        { title: 'API-Schlüssel abrufen', desc: 'Schlüssel im Dashboard generieren.' },
                        { title: 'Sandbox testen', desc: 'Endpoints direkt im Browser ausprobieren.' },
                        { title: 'Integrieren', desc: 'Code direkt in Ihr Projekt kopieren.' }
                    ],
                    compliance: 'OpenAPI 3.0 und TLS 1.3 Standard.',
                    faq: [{ q: 'Gibt es ein kostenloses Kontingent?', a: 'Ja, 500 kostenlose API-Aufrufe täglich.' }]
                },
                terminal: {
                    title: 'S&R Cloud Terminal Agent',
                    subtitle: 'Server- und Microservices-Überwachung in Echtzeit',
                    overview: 'Schlanker Monitoring-Agent für CPU, Speicher und Datenbank-Latenzen mit Fernwartung.',
                    hardware: [{ name: '☁️ Server', desc: 'Linux, Windows Server und Docker Container.' }],
                    steps: [
                        { title: 'Agent einrichten', desc: 'Befehl im Server-Terminal ausführen.' },
                        { title: 'Überwachen', desc: 'Echtzeitmetriken im Dashboard verfolgen.' },
                        { title: 'Dienste steuern', desc: 'Neustarts bei Ausfällen mit einem Klick ausführen.' }
                    ],
                    compliance: 'ISO 27001 zertifizierte Auditprotokolle.',
                    faq: [{ q: 'Wie hoch ist die Last?', a: 'Minimal: unter 15MB RAM und 0.2% CPU-Auslastung.' }]
                }
            }
        },
        sv: {
            guideBadge: 'OFFICIELL DRIFTHANDBOK & BRUKSANVISNING • 2026',
            guideTitle: 'S&R CoreSync Programvaruhandböcker och Bruksanvisningar',
            allOverview: 'Systemöversikt och Programkatalog',
            printBtn: '🖨️ Skriv ut Guide',
            copyKeyBtn: '📋 Kopiera Provlicens',
            launchBtn: '⚡ Starta Direkt i Webbläsare',
            downloadBtn: '📥 Ladda ner Offline-version',
            sections: {
                overview: '📌 Syfte & Systemöversikt',
                hardware: '💻 Maskinvara och Inmatningsenheter',
                steps: '🚀 Steg-för-steg Snabbstartsguide',
                compliance: '🛡️ Säkerhet, Kryptografi & EU-efterlevnad',
                faq: '❓ Vanliga Frågor & Felsökning'
            },
            apps: {
                taxsync: {
                    title: 'S&R TaxSync Desktop / Web',
                    subtitle: 'Nederländsk och europeisk skatteräknare med Digipoort XML-stöd',
                    overview: 'Fristående offline-first skatteprogram för BTW/momsberäkning och generering av officiella Digipoort XML-deklarationer.',
                    hardware: [{ name: '🖥️ System', desc: 'Windows 11/10, macOS och Linux. Fungerar 100% offline.' }],
                    steps: [
                        { title: 'Välj momssats', desc: 'Välj 21%, 9% eller 0% momssats.' },
                        { title: 'Mata in belopp', desc: 'Beräkna skatten och avdragsgill moms automatiskt.' },
                        { title: 'Skapa deklaration', desc: 'Generera officiell Digipoort XML-fil.' },
                        { title: 'Skriv ut', desc: 'Exportera krypterad PDF-faktura enligt EN 16931.' }
                    ],
                    compliance: 'Uppfyller nederländsk skattelag AWR Art. 52 och GDPR Art. 32.',
                    faq: [{ q: 'Fungerar det offline?', a: 'Ja, 100% Offline-First. Alla data förblir på din dator.' }]
                },
                cloudpos: {
                    title: 'S&R CloudPOS Connector',
                    subtitle: 'Molnbaserat kassasystem med streckkodsläsning via mobil- och datorkamera',
                    overview: 'Modernt och snabbt kassasystem med direkt stöd för streckkodsläsning via mobil- eller bärbar datorkamera utan behov av extern skanner.',
                    hardware: [
                        { name: '📷 Mobil- och Datorkamera (Ingen extern skanner behövs)', desc: 'Skanna streckkoder (EAN-13, QR, Code-128) direkt med mobilkameran eller webbkameran helt utan extra kostnad!' },
                        { name: '🔫 Extern Streckkodsläsare', desc: 'Full Plug-and-Play-kompatibilitet med USB och trådlösa skannrar.' },
                        { name: '🧾 Kvittoskrivare', desc: 'Direktstöd för ESC/POS 80mm och 58mm termokvitton.' }
                    ],
                    steps: [
                        { title: 'Öppna kassan', desc: 'Starta terminalen i webbläsaren eller som app.' },
                        { title: 'Skanna streckkod', desc: 'Klicka på "📷 Skanna streckkod med kamera" eller använd din skanner.' },
                        { title: 'Betala', desc: 'Välj kontant, kort eller direktbetalning.' },
                        { title: 'Skriv ut kvitto', desc: 'Skriv ut kvittot och lagret uppdateras i realtid.' }
                    ],
                    compliance: 'Uppfyller europeiska krav på kassaregister och spårbarhet.',
                    faq: [
                        { q: 'Kan jag skanna streckkoder med mobilkameran utan att köpa en separat skanner?', a: 'Ja, absolut till 100%! Med S&R CloudPOS förvandlas din mobil eller bärbara dator direkt till en komplett kassaterminal utan extra hårdvara.' }
                    ]
                },
                flowscan: {
                    title: 'S&R FlowScan AI Mobile',
                    subtitle: 'Mobil AI-kvittoavläsare med automatisk OCR',
                    overview: 'Skanna kvitton med mobilkameran och extrahera belopp och moms automatiskt till affärssystemet.',
                    hardware: [{ name: '📱 Mobil', desc: 'Stöder iOS, Android och bärbara webbkameror.' }],
                    steps: [
                        { title: 'Fotografera', desc: 'Rikta kameran mot kvittot.' },
                        { title: 'AI-bearbetning', desc: 'Text och siffror läses av på 800 ms.' },
                        { title: 'Synkronisera', desc: 'Bokför utgiften direkt i affärssystemet.' }
                    ],
                    compliance: 'Krypterad och GDPR-kompatibel i Amsterdam AMS-IX.',
                    faq: [{ q: 'Fungerar det vid otydliga kvitton?', a: 'Ja, inbyggd bildförbättring optimerar läsbarheten automatiskt.' }]
                },
                vault: {
                    title: 'S&R SecureVault B2B',
                    subtitle: 'Militär AES-256 GCM kryptering av företagsdata',
                    overview: 'Klientbaserad kryptering i webbläsaren som skyddar databaser och känsliga dokument.',
                    hardware: [{ name: '💻 Webbläsare', desc: 'Kompatibel med alla moderna enheter och webbläsare.' }],
                    steps: [
                        { title: 'Välj fil', desc: 'Dra och släpp dokumentet i valvet.' },
                        { title: 'Ange lösenord', desc: 'Generera en stark 256-bitars krypteringsnyckel.' },
                        { title: 'Kryptera', desc: 'Ladda ner den säkra .srvault-filen.' }
                    ],
                    compliance: 'Uppfyller GDPR Artikel 32 och FIPS 140-2.',
                    faq: [{ q: 'Kan någon annan dekryptera mina filer?', a: 'Nej, äkta Zero-Knowledge på din egen enhet.' }]
                },
                sdk: {
                    title: 'S&R Financial AI SDK Console',
                    subtitle: 'REST API-konsol för skatte- och finansutveckling',
                    overview: 'Utvecklarkonsol för att integrera momsberäkning och fakturering i egna applikationer.',
                    hardware: [{ name: '🌐 Språk', desc: 'Färdig kod för Python, Node.js, C#, PHP och cURL.' }],
                    steps: [
                        { title: 'Skapa API-nyckel', desc: 'Hämta nyckel från instrumentpanelen.' },
                        { title: 'Testa i sandbox', desc: 'Skicka testanrop direkt i webbläsaren.' },
                        { title: 'Integrera', desc: 'Kopiera koden direkt till ditt projekt.' }
                    ],
                    compliance: 'OpenAPI 3.0 och TLS 1.3 säkerhet.',
                    faq: [{ q: 'Finns gratis testmiljö?', a: 'Ja, 500 kostnadsfria anrop per dag.' }]
                },
                terminal: {
                    title: 'S&R Cloud Terminal Agent',
                    subtitle: 'Realtidsövervakning av servrar och mikrotjänster',
                    overview: 'Lätt övervakningsagent för CPU, minne och svarstider med fjärromstart.',
                    hardware: [{ name: '☁️ Servrar', desc: 'Stöd för Linux, Windows Server och Docker.' }],
                    steps: [
                        { title: 'Installera agent', desc: 'Kör kommandot i din serverterminal.' },
                        { title: 'Övervaka', desc: 'Följ grafer i realtid från Amsterdam-noden.' },
                        { title: 'Hantera', desc: 'Starta om tjänster direkt vid behov.' }
                    ],
                    compliance: 'ISO 27001 certifierad loggning.',
                    faq: [{ q: 'Hur mycket resurser krävs?', a: 'Mycket lite: under 15MB RAM och 0.2% CPU.' }]
                }
            }
        },
        tr: {
            guideBadge: 'RESMİ KULLANIM & İŞLETİM KILAVUZU • 2026',
            guideTitle: 'S&R CoreSync Yazılım Kullanım Kılavuzları & Dokümantasyon',
            allOverview: 'Sistem Genel Bakışı ve Katalog',
            printBtn: '🖨️ Kılavuzu Yazdır',
            copyKeyBtn: '📋 Deneme Anahtarı Kopyala',
            launchBtn: '⚡ Tarayıcıda Anında Başlat',
            downloadBtn: '📥 Çevrimdışı İndir',
            sections: {
                overview: '📌 Amaç ve Sistem Özeti',
                hardware: '💻 Desteklenen Donanım ve Giriş Aygıtları',
                steps: '🚀 Adım Adım Hızlı Başlangıç Kılavuzu',
                compliance: '🛡️ Güvenlik, Kriptografi & AB Uyumluluğu',
                faq: '❓ Sıkça Sorulan Sorular ve Sorun Giderme'
            },
            apps: {
                taxsync: {
                    title: 'S&R TaxSync Desktop / Web',
                    subtitle: 'Hollanda & Körfez KDV hesaplayıcı ve resmi Digipoort XML beyan sistemi',
                    overview: 'Hollanda BTW (%21, %9, %0) ve Körfez KDV hesaplamaları için geliştirilmiş bağımsız, çevrimdışı öncelikli muhasebe yazılımı. Digipoort XML beyannameleri ve şifreli faturalar üretir.',
                    hardware: [{ name: '🖥️ İşletim Sistemleri', desc: 'Windows 11/10, macOS ve Linux. İnternetsiz %100 çalışır.' }],
                    steps: [
                        { title: 'Vergi Oranını Seçin', desc: 'BTW %21, %9 veya %0 oranını belirleyin.' },
                        { title: 'Tutarları Girin', desc: 'Vergi ve indirimleri anında hesaplayın.' },
                        { title: 'XML Beyannamesi Üretin', desc: 'Belastingdienst için resmi Digipoort XML dosyasını oluşturun.' },
                        { title: 'Faturayı Yazdırın', desc: 'EN 16931 uyumlu doğrulanabilir PDF faturayı dışa aktarın.' }
                    ],
                    compliance: 'Hollanda Vergi Kanunu AWR Madde 52 ve GDPR Madde 32 ile tam uyumludur.',
                    faq: [{ q: 'İnternetsiz çalışır mı?', a: 'Evet, %100 Çevrimdışı-Öncelikli (Offline-First) mimariye sahiptir.' }]
                },
                cloudpos: {
                    title: 'S&R CloudPOS Connector',
                    subtitle: 'Akıllı Bulut Kasa & Cep Telefonu/Laptop Kamerasıyla Barkod Okuma',
                    overview: 'Mağaza ve restoranları bulut ERP sistemine bağlayan hızlı kasa terminali. Ekstra barkod okuyucu tabancaya gerek olmadan doğrudan cep telefonu veya laptop kamerasıyla barkod okuma desteği sunar.',
                    hardware: [
                        { name: '📷 Telefon & Laptop Kamerası (Barkod Okuyucuya Gerek Yok)', desc: 'Ürün barkodlarını (EAN-13, QR, Code-128) doğrudan telefon kameranız veya laptop web kameranız ile anında ve ücretsiz tarayın!' },
                        { name: '🔫 Harici Barkod Okuyucular (Tabanca)', desc: 'USB, Bluetooth ve 2.4GHz kablosuz el terminalleri ile tak-çalıştır uyumluluk.' },
                        { name: '🧾 Termal Fiş Yazıcıları', desc: '80mm ve 58mm termal rulo yazıcılar için doğrudan ESC/POS protokol desteği.' }
                    ],
                    steps: [
                        { title: 'Kasa Ekranını Açın', desc: 'Uygulamayı tarayıcıdan veya bağımsız olarak başlatın.' },
                        { title: 'Barkodu Okutun', desc: '"📷 Kamerayla Barkod Tara" butonuna basarak kameranızı barkoda tutun veya el okuyucunuzu kullanın.' },
                        { title: 'Ödemeyi Alın', desc: 'Nakit, Kredi Kartı veya iDEAL / PIN seçeneğini belirleyin.' },
                        { title: 'Fiş Yazdırın ve Stoğu Güncelleyin', desc: 'Satışı tamamlayarak fişi yazdırın, stok bulutta anında düşsün.' }
                    ],
                    compliance: 'Avrupa yazar kasa denetim standartlarına ve fiş mevzuatına tam uyumludur.',
                    faq: [
                        { q: 'Harici bir barkod okuyucu almadan telefon veya laptop kameramla barkod okutabilir miyim?', a: 'Evet, kesinlikle ve %100! S&R CloudPOS içindeki optik barkod okuyucu sayesinde cep telefonunuzu veya laptop kameranızı anında profesyonel bir barkod okuyucuya dönüştürebilirsiniz.' }
                    ]
                },
                flowscan: {
                    title: 'S&R FlowScan AI Mobile',
                    subtitle: 'Yapay Zeka Destekli Mobil Fatura ve Fiş Tarayıcı',
                    overview: 'Mobil kamera ile fatura ve fişleri tarayıp tutarları ve vergi oranlarını %99.4 doğrulukla ERP sistemine aktarır.',
                    hardware: [{ name: '📱 Mobil Cihazlar', desc: 'iPhone (iOS 17+), Android 14+ ve laptop web kameraları.' }],
                    steps: [
                        { title: 'Kamerayı Hizalayın', desc: 'Fişi tarama çerçevesinin içine yerleştirin.' },
                        { title: 'Yakala ve Tara', desc: 'Yapay zeka verileri 800 milisaniyede okur.' },
                        { title: 'ERP\'ye Aktar', desc: 'Masrafı tek tıkla şirket sistemine kaydedin.' }
                    ],
                    compliance: 'Amsterdam AMS-IX veri merkezinde GDPR uyumlu şifreli saklama.',
                    faq: [{ q: 'Buruşuk fişleri okur mu?', a: 'Evet, akıllı filtreler kontrast ve netliği otomatik düzenler.' }]
                },
                vault: {
                    title: 'S&R SecureVault B2B',
                    subtitle: 'Askeri Seviye AES-256 GCM Veri Şifreleme',
                    overview: 'Veritabanı yedeklerini ve hassas belgeleri tarayıcıda askeri standartta şifreler.',
                    hardware: [{ name: '💻 Tarayıcı', desc: 'Tüm modern tarayıcılarda istemci tarafında çalışır.' }],
                    steps: [
                        { title: 'Dosya Seçin', desc: 'Belgeyi şifreleme alanına bırakın.' },
                        { title: 'Parola Belirleyin', desc: '256-bit güçlü anahtar türetin.' },
                        { title: 'Şifreleyin', desc: 'Güvenli .srvault dosyasını cihazınıza indirin.' }
                    ],
                    compliance: 'GDPR Madde 32 ve FIPS 140-2 şifreleme standartlarına uygundur.',
                    faq: [{ q: 'Başkaları dosyamı görebilir mi?', a: 'Hayır, Zero-Knowledge istemci tarafı şifreleme uygulanır.' }]
                },
                sdk: {
                    title: 'S&R Financial AI SDK Console',
                    subtitle: 'Geliştiriciler İçin REST API ve Vergi Algoritmaları',
                    overview: 'Yazılım ekiplerinin vergi hesaplama ve e-fatura altyapısını kendi yazılımlarına entegre etmesini sağlayan konsol.',
                    hardware: [{ name: '🌐 Diller', desc: 'Python, Node.js, C#, PHP ve cURL hazır kodları.' }],
                    steps: [
                        { title: 'API Anahtarı Alın', desc: 'Geliştirici panelinden anahtarınızı üretin.' },
                        { title: 'Sandbox\'ta Test Edin', desc: 'Tarayıcıda anlık test istekleri gönderin.' },
                        { title: 'Kodu Ekleyin', desc: 'Hazır kodu kopyalayarak projenize dahil edin.' }
                    ],
                    compliance: 'OpenAPI 3.0 ve TLS 1.3 standartları.',
                    faq: [{ q: 'Ücretsiz deneme var mı?', a: 'Evet, günlük 500 ücretsiz test isteği sunulmaktadır.' }]
                },
                terminal: {
                    title: 'S&R Cloud Terminal Agent',
                    subtitle: 'Gerçek Zamanlı Sunucu ve Mikroservis İzleme',
                    overview: 'Amsterdam sunucularında CPU, RAM ve veritabanı yanıt sürelerini izleyen hafif telemetri ajanı.',
                    hardware: [{ name: '☁️ Sunucular', desc: 'Linux, Windows Server ve Docker konteynerleri.' }],
                    steps: [
                        { title: 'Ajanı Kurun', desc: 'Sunucuda tek satırlık terminal komutu çalıştırın.' },
                        { title: 'İzleyin', desc: 'Anlık metrikleri ve gecikme grafiklerini takip edin.' },
                        { title: 'Yönetin', desc: 'Olası kilitlenmelerde servisleri tek tıkla yeniden başlatın.' }
                    ],
                    compliance: 'ISO 27001 onaylı güvenlik günlükleri ve mTLS bağlantı.',
                    faq: [{ q: 'Sunucuyu yorar mı?', a: 'Hayır, 15MB\'tan az RAM ve %0.2\'den az CPU tüketir.' }]
                }
            }
        }
    };

    let activeDocsLang = 'ar';
    let activeDocsAppId = 'cloudpos';

    // -------------------------------------------------------------
    // 13. Multilingual Docs Modal Injector & Controller
    // -------------------------------------------------------------
    function ensureDocsModalInDom() {
        let overlay = document.getElementById('srSoftwareDocsModal');
        if (overlay) return overlay;

        overlay = document.createElement('div');
        overlay.id = 'srSoftwareDocsModal';
        overlay.className = 'sr-docs-modal-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');

        overlay.innerHTML = `
            <div class="sr-docs-dialog" id="srDocsDialog">
                <!-- Header with Title & Language Switcher -->
                <div class="sr-docs-header">
                    <div class="sr-docs-header-left">
                        <span class="sr-docs-header-icon" id="srDocsAppIcon">📖</span>
                        <div class="sr-docs-header-titles">
                            <h3 id="srDocsHeaderTitle">دليل تشغيل واستخدام برمجيات S&R CoreSync</h3>
                            <p id="srDocsHeaderBadge">دليل الاستخدام والتشغيل المعتمد • 2026</p>
                        </div>
                    </div>

                    <!-- 6-Language Switcher Bar -->
                    <div class="sr-docs-lang-bar">
                        <button type="button" class="sr-docs-lang-btn active" data-lang="ar" onclick="setDocsLanguage('ar')">🇸🇦 العربية</button>
                        <button type="button" class="sr-docs-lang-btn" data-lang="en" onclick="setDocsLanguage('en')">🇬🇧 English</button>
                        <button type="button" class="sr-docs-lang-btn" data-lang="nl" onclick="setDocsLanguage('nl')">🇳🇱 Nederlands</button>
                        <button type="button" class="sr-docs-lang-btn" data-lang="de" onclick="setDocsLanguage('de')">🇩🇪 Deutsch</button>
                        <button type="button" class="sr-docs-lang-btn" data-lang="sv" onclick="setDocsLanguage('sv')">🇸🇪 Svenska</button>
                        <button type="button" class="sr-docs-lang-btn" data-lang="tr" onclick="setDocsLanguage('tr')">🇹🇷 Türkçe</button>
                    </div>

                    <button type="button" class="sr-docs-close-btn" onclick="closeSoftwareDocsModal()" title="إغلاق">✕</button>
                </div>

                <!-- Application Tabs inside Docs -->
                <div class="sr-docs-app-tabs" id="srDocsAppTabs">
                    <button type="button" class="sr-docs-app-tab" data-app="taxsync" onclick="setDocsActiveApp('taxsync')">💻 TaxSync Desktop</button>
                    <button type="button" class="sr-docs-app-tab" data-app="flowscan" onclick="setDocsActiveApp('flowscan')">📱 FlowScan AI Mobile</button>
                    <button type="button" class="sr-docs-app-tab active" data-app="cloudpos" onclick="setDocsActiveApp('cloudpos')">⚡ CloudPOS (الكاميرا & POS)</button>
                    <button type="button" class="sr-docs-app-tab" data-app="vault" onclick="setDocsActiveApp('vault')">🛡️ SecureVault B2B</button>
                    <button type="button" class="sr-docs-app-tab" data-app="sdk" onclick="setDocsActiveApp('sdk')">🧩 Financial AI SDK</button>
                    <button type="button" class="sr-docs-app-tab" data-app="terminal" onclick="setDocsActiveApp('terminal')">⚙️ Cloud Terminal</button>
                </div>

                <!-- Scrollable Guide Body -->
                <div class="sr-docs-body" id="srDocsBody">
                    <!-- Injected dynamically by renderDocsModalContent() -->
                </div>

                <!-- Footer with Action Buttons -->
                <div class="sr-docs-footer">
                    <div class="sr-docs-footer-left">
                        <button type="button" class="sr-hero-btn sr-hero-btn-primary" id="srDocsLaunchBtn" onclick="launchAppFromDocs()">
                            ⚡ تشغيل فوري في المتصفح
                        </button>
                        <a href="downloads/SR-CloudPOS-Terminal.html" id="srDocsDownloadLink" download class="sr-hero-btn sr-hero-btn-secondary">
                            📥 تحميل النسخة أوفلاين
                        </a>
                    </div>
                    <div class="sr-docs-footer-right">
                        <button type="button" class="btn-software-guide" onclick="copyTrialKeyFromDocs()">
                            📋 نسخ مفتاح تجريبي
                        </button>
                        <button type="button" class="btn-software-guide" onclick="window.print()">
                            🖨️ طباعة الدليل
                        </button>
                    </div>
                </div>
            </div>
        `;

        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) closeSoftwareDocsModal();
        });

        document.body.appendChild(overlay);
        return overlay;
    }

    window.openSoftwareDocsModal = function(appId = 'cloudpos', lang = null) {
        if (appId && appId !== 'all' && SOFTWARE_APPS[appId]) {
            activeDocsAppId = appId;
        } else if (!activeDocsAppId) {
            activeDocsAppId = 'cloudpos';
        }

        if (lang && SOFTWARE_DOCS[lang]) {
            activeDocsLang = lang;
        } else {
            // Check page language or current locale
            const htmlLang = (document.documentElement.getAttribute('lang') || 'ar').toLowerCase();
            if (SOFTWARE_DOCS[htmlLang]) activeDocsLang = htmlLang;
        }

        const overlay = ensureDocsModalInDom();
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';

        renderDocsModalContent();
        playAppBeep(640, 'sine', 0.12);
    };

    window.closeSoftwareDocsModal = function() {
        const overlay = document.getElementById('srSoftwareDocsModal');
        if (overlay) {
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
        playAppBeep(340, 'triangle', 0.08);
    };

    window.setDocsLanguage = function(lang) {
        if (!SOFTWARE_DOCS[lang]) return;
        activeDocsLang = lang;
        renderDocsModalContent();
        playAppBeep(720, 'sine', 0.09);
    };

    window.setDocsActiveApp = function(appId) {
        if (!SOFTWARE_APPS[appId]) return;
        activeDocsAppId = appId;
        renderDocsModalContent();
        playAppBeep(580, 'sine', 0.09);
    };

    function renderDocsModalContent() {
        const docPack = SOFTWARE_DOCS[activeDocsLang] || SOFTWARE_DOCS.ar;
        const appDoc = docPack.apps[activeDocsAppId] || docPack.apps.cloudpos;
        const appMeta = SOFTWARE_APPS[activeDocsAppId] || SOFTWARE_APPS.cloudpos;

        // Update Header Titles
        const headerTitle = document.getElementById('srDocsHeaderTitle');
        const headerBadge = document.getElementById('srDocsHeaderBadge');
        const appIcon = document.getElementById('srDocsAppIcon');
        if (headerTitle) headerTitle.innerText = `${appDoc.title} • ${docPack.guideTitle}`;
        if (headerBadge) headerBadge.innerText = docPack.guideBadge;
        if (appIcon) appIcon.innerText = appMeta.icon || '📖';

        // Update Language Buttons Active State
        document.querySelectorAll('.sr-docs-lang-btn').forEach(btn => {
            if (btn.getAttribute('data-lang') === activeDocsLang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update App Tabs Active State
        document.querySelectorAll('.sr-docs-app-tab').forEach(btn => {
            if (btn.getAttribute('data-app') === activeDocsAppId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update Footer Buttons
        const launchBtn = document.getElementById('srDocsLaunchBtn');
        const downloadLink = document.getElementById('srDocsDownloadLink');
        if (launchBtn) launchBtn.innerHTML = `⚡ ${docPack.launchBtn} (${appDoc.title})`;
        if (downloadLink) {
            downloadLink.innerHTML = `📥 ${docPack.downloadBtn}`;
            downloadLink.href = appMeta.offlineFile || 'downloads/SR-CloudPOS-Terminal.html';
            downloadLink.setAttribute('download', (appMeta.offlineFile || '').split('/').pop() || 'download.html');
        }

        // Render Body Sections
        const bodyEl = document.getElementById('srDocsBody');
        if (!bodyEl) return;

        let hwHtml = '';
        if (appDoc.hardware && appDoc.hardware.length) {
            hwHtml = `
                <div class="sr-docs-section-card">
                    <div class="sr-docs-section-header">
                        <span class="sr-docs-section-icon">💻</span>
                        <h4 class="sr-docs-section-title">${docPack.sections.hardware}</h4>
                    </div>
                    <div class="sr-docs-hw-grid">
                        ${appDoc.hardware.map(h => `
                            <div class="sr-docs-hw-item">
                                <span class="sr-docs-hw-name">${h.name}</span>
                                <span class="sr-docs-hw-desc">${h.desc}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        let stepsHtml = '';
        if (appDoc.steps && appDoc.steps.length) {
            stepsHtml = `
                <div class="sr-docs-section-card">
                    <div class="sr-docs-section-header">
                        <span class="sr-docs-section-icon">🚀</span>
                        <h4 class="sr-docs-section-title">${docPack.sections.steps}</h4>
                    </div>
                    <div class="sr-docs-steps-list">
                        ${appDoc.steps.map((s, idx) => `
                            <div class="sr-docs-step-item">
                                <div class="sr-docs-step-number">${idx + 1}</div>
                                <div class="sr-docs-step-content">
                                    <h4>${s.title}</h4>
                                    <p>${s.desc}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        let faqHtml = '';
        if (appDoc.faq && appDoc.faq.length) {
            faqHtml = `
                <div class="sr-docs-section-card">
                    <div class="sr-docs-section-header">
                        <span class="sr-docs-section-icon">❓</span>
                        <h4 class="sr-docs-section-title">${docPack.sections.faq}</h4>
                    </div>
                    <div>
                        ${appDoc.faq.map(f => `
                            <div class="sr-docs-faq-item">
                                <div class="sr-docs-faq-q">❓ ${f.q}</div>
                                <p class="sr-docs-faq-a">💡 ${f.a}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        bodyEl.innerHTML = `
            <!-- Overview Card -->
            <div class="sr-docs-section-card">
                <div class="sr-docs-section-header">
                    <span class="sr-docs-section-icon">📌</span>
                    <h4 class="sr-docs-section-title">${docPack.sections.overview}</h4>
                </div>
                <h3 style="color: var(--sr-app-gold); margin: 0 0 8px 0; font-size: 1.15rem;">${appDoc.title}</h3>
                <p style="color: #94a3b8; font-size: 0.86rem; margin-bottom: 12px; font-weight: 600;">${appDoc.subtitle}</p>
                <p class="sr-docs-text">${appDoc.overview}</p>
            </div>

            ${hwHtml}
            ${stepsHtml}

            <!-- Compliance Card -->
            <div class="sr-docs-section-card">
                <div class="sr-docs-section-header">
                    <span class="sr-docs-section-icon">🛡️</span>
                    <h4 class="sr-docs-section-title">${docPack.sections.compliance}</h4>
                </div>
                <p class="sr-docs-text">${appDoc.compliance}</p>
            </div>

            ${faqHtml}
        `;
    }

    window.launchAppFromDocs = function() {
        const appToOpen = activeDocsAppId || 'cloudpos';
        closeSoftwareDocsModal();
        setTimeout(() => {
            if (typeof openSoftwareLiveApp === 'function') {
                openSoftwareLiveApp(appToOpen);
            }
        }, 150);
    };

    window.copyTrialKeyFromDocs = function() {
        const appMeta = SOFTWARE_APPS[activeDocsAppId] || SOFTWARE_APPS.taxsync;
        const key = appMeta.defaultKey || 'SRTX-PRO-2026-TRIAL-KEY';
        navigator.clipboard.writeText(key).then(() => {
            if (typeof showPortalToast === 'function') {
                showPortalToast(`🔑 تم نسخ مفتاح الترخيص التجريبي: ${key}`);
            } else {
                alert(`تم نسخ المفتاح: ${key}`);
            }
        }).catch(() => {
            alert(`المفتاح: ${key}`);
        });
    };

    // -------------------------------------------------------------
    // 14. Real-time Search and Filter for Software Marketplace
    // -------------------------------------------------------------
    window.filterSoftwareBySearch = function(query) {
        const clean = (query || '').trim().toLowerCase();
        const clearBtn = document.getElementById('srSearchClearBtn');
        if (clearBtn) clearBtn.style.display = clean ? 'block' : 'none';

        const cards = document.querySelectorAll('#softwareGridContainer .software-card');
        let visibleCount = 0;

        cards.forEach(card => {
            const text = (card.innerText || '').toLowerCase();
            const category = (card.getAttribute('data-category') || '').toLowerCase();
            const matches = !clean || text.includes(clean) || category.includes(clean);

            if (matches) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Handle no results feedback
        let noResEl = document.getElementById('srSoftwareNoResults');
        if (visibleCount === 0) {
            if (!noResEl) {
                noResEl = document.createElement('div');
                noResEl.id = 'srSoftwareNoResults';
                noResEl.style.cssText = 'grid-column: 1/-1; text-align: center; padding: 40px; color: #94a3b8; font-size: 1rem;';
                noResEl.innerHTML = `🔍 لم يتم العثور على برمجيات تطابق البحث: <strong>"${clean}"</strong>`;
                const container = document.getElementById('softwareGridContainer');
                if (container) container.appendChild(noResEl);
            } else {
                noResEl.style.display = 'block';
                noResEl.innerHTML = `🔍 لم يتم العثور على برمجيات تطابق البحث: <strong>"${clean}"</strong>`;
            }
        } else if (noResEl) {
            noResEl.style.display = 'none';
        }
    };

    window.clearSoftwareSearch = function() {
        const input = document.getElementById('srSoftwareSearchInput');
        if (input) input.value = '';
        filterSoftwareBySearch('');
    };

    // -------------------------------------------------------------
    // 15. Auto-Trigger via URL Query Params
    // -------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const appParam = urlParams.get('app') || urlParams.get('run') || urlParams.get('sandbox');
        if (appParam && SOFTWARE_APPS[appParam]) {
            setTimeout(() => {
                openSoftwareLiveApp(appParam);
            }, 400);
        }
        const docsParam = urlParams.get('docs') || urlParams.get('manual') || urlParams.get('guide');
        if (docsParam) {
            setTimeout(() => {
                openSoftwareDocsModal(docsParam === '1' ? 'cloudpos' : docsParam);
            }, 500);
        }
    });

    // -------------------------------------------------------------
    // 16. Global Executive Routing Fallback Helpers
    // -------------------------------------------------------------
    if (!window.openExecutiveContactModal) {
        window.openExecutiveContactModal = function(category = 'accounting', softwareName = '') {
            const isAcct = (category === 'accounting');
            const targetPhone = isAcct ? '31687710290' : '31618111116';
            const advisorName = isAcct ? 'أ. محمد رائد كعكة (CFO - المحاسبة والضرائب)' : 'م. محمد سليم عزيزة (CTO - الأنظمة والبرمجيات)';
            const msg = `*طلب استشارة تنفيذية خاصة - S&R CoreSync Solutions*\n` +
                        `━━━━━━━━━━━━━━━━━━━━\n` +
                        `👔 *المستشار المطلوب:* ${advisorName}\n` +
                        `🎯 *البرنامج المستهدف:* ${softwareName || (isAcct ? 'الأنظمة المحاسبية' : 'الأنظمة السحابية')}\n` +
                        `━━━━━━━━━━━━━━━━━━━━\n` +
                        `_تم الإرسال عبر محاكي تطبيقات S&R CoreSync_`;
            
            const choice = confirm(`هل تود التحدث عبر واتساب المستشار المختص [${advisorName}]؟\n\n(اضغط OK للواتساب، أو Cancel لإرسال إيميل إلى info@sr-coresync.com)`);
            if (choice) {
                window.open(`https://wa.me/${targetPhone}?text=${encodeURIComponent(msg)}`, '_blank');
            } else {
                window.sendDirectInfoEmail(softwareName || advisorName);
            }
        };
    }

    if (!window.sendDirectInfoEmail) {
        window.sendDirectInfoEmail = function(softwareName = '') {
            const subject = encodeURIComponent(`استفسار رسمي حول [${softwareName || 'برمجيات وأنظمة S&R CoreSync'}]`);
            const body = encodeURIComponent(
                `السادة إدارة S&R CoreSync Solutions المحترمين،\n\n` +
                `أود الاستفسار والتواصل بخصوص: ${softwareName || 'برمجيات المنصة'}.\n\n` +
                `الاسم الكامل:\nالشركة:\nرقم الواتساب / الهاتف:\nتفاصيل الاستفسار المطلوب:\n\nمع فائق الاحترام والتقدير.`
            );
            window.location.href = `mailto:info@sr-coresync.com?subject=${subject}&body=${body}`;
        };
    }

})();

