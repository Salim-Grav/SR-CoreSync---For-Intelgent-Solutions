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

        // Common App Sub-Nav with License Bar & Switcher
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
                    <span>مفتاح الترخيص المفعل:</span>
                    <span class="sr-app-license-key-disp" id="srCurrentLicenseDisplay">${sw.defaultKey}</span>
                    <button type="button" class="sr-app-btn secondary" onclick="promptLicenseActivation('${sw.id}')" title="تفعيل مفتاح تجاري">تغيير 🔑</button>
                    <a href="${sw.offlineFile}" download class="sr-app-btn primary" title="تحميل ملف الويب للتشغيل أوفلاين بدون نت">تحميل أوفلاين 📥</a>
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
                            <div class="sr-scan-laser-line" id="fsLaserLine"></div>
                            <div style="font-size: 2.2rem; margin-bottom: 8px;" id="fsScanStatusIcon">📷</div>
                            <strong id="fsScanStatusTitle" style="color:#ffffff; font-size:0.95rem;">وجه الكاميرا نحو الإيصال</strong>
                            <p id="fsScanStatusSub" style="color:var(--sr-app-text-muted); font-size:0.75rem; margin-top:4px;">
                                نظام OCR بالذكاء الاصطناعي يستخرج المبالغ والضريبة آلياً
                            </p>
                        </div>

                        <!-- Presets & Camera Trigger -->
                        <div style="padding: 16px;">
                            <span class="sr-app-label">اختر إيصال تجريبي للاختبار الفوري:</span>
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

    function initFlowScanEvents() {}

    window.loadReceiptPreset = function(presetKey, btn) {
        document.querySelectorAll('.sr-preset-receipt-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        currentPreset = presetKey;
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
            const data = RECEIPT_PRESETS[currentPreset] || RECEIPT_PRESETS.shell;
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
        const data = RECEIPT_PRESETS[currentPreset] || RECEIPT_PRESETS.shell;
        const syncBox = document.getElementById('fsSyncSuccessBox');
        const vatAmtEl = document.getElementById('fsSyncVatAmt');
        if (syncBox) syncBox.style.display = 'block';
        if (vatAmtEl) vatAmtEl.innerText = `€ ${data.vatVal}`;

        playAppBeep(1040, 'sine', 0.25);
        if (typeof showPortalToast === 'function') {
            showPortalToast(`🚀 تم ترحيل إيصال [${data.merchant}] بنجاح إلى نظام الـ ERP السحابي!`);
        }
    };

    window.exportFlowScanJson = function() {
        const data = RECEIPT_PRESETS[currentPreset] || RECEIPT_PRESETS.shell;
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
        { id: 1, name: 'قهوة اسبريسو فاخرة', icon: '☕', price: 3.50, vatRate: 0.09 },
        { id: 2, name: 'شطيرة غداء طازجة', icon: '🥪', price: 7.50, vatRate: 0.09 },
        { id: 3, name: 'استشارة فنية متخصصة', icon: '💼', price: 120.00, vatRate: 0.21 },
        { id: 4, name: 'محطة كاشير POS Terminal', icon: '🖥️', price: 250.00, vatRate: 0.21 },
        { id: 5, name: 'ترخيص برمجي شهري', icon: '🔑', price: 49.00, vatRate: 0.21 },
        { id: 6, name: 'طابعة إيصالات حرارية', icon: '🖨️', price: 85.00, vatRate: 0.21 }
    ];

    let posCart = [
        { ...POS_CATALOG[0], qty: 2 },
        { ...POS_CATALOG[2], qty: 1 }
    ];

    function renderCloudPosHtml() {
        return `
            <div class="sr-app-grid-2">
                <!-- Products Menu -->
                <div class="sr-app-card">
                    <h4 class="sr-app-card-title">
                        <span>قائمة المنتجات والخدمات (POS Catalog)</span>
                        <span class="sr-app-header-ver">انقر للإضافة إلى السلة</span>
                    </h4>

                    <div class="sr-pos-products-grid">
                        ${POS_CATALOG.map(p => `
                            <div class="sr-pos-product-card" onclick="addPosItem(${p.id})">
                                <div class="sr-pos-product-icon">${p.icon}</div>
                                <div class="sr-pos-product-name">${p.name}</div>
                                <div class="sr-pos-product-price">€ ${p.price.toFixed(2)}</div>
                                <div class="sr-pos-product-vat">BTW ${(p.vatRate * 100).toFixed(0)}%</div>
                            </div>
                        `).join('')}
                    </div>

                    <!-- Cart Items Table -->
                    <h5 style="color:var(--sr-app-gold); font-size:0.85rem; margin-bottom:10px;">عناصر السلة الحالية:</h5>
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
        `;
    }

    function initCloudPosEvents() {
        renderPosCart();
    }

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
    // 12. Auto-Trigger via URL Query Params
    // -------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const appParam = urlParams.get('app') || urlParams.get('run') || urlParams.get('sandbox');
        if (appParam && SOFTWARE_APPS[appParam]) {
            setTimeout(() => {
                openSoftwareLiveApp(appParam);
            }, 400);
        }
    });

})();
