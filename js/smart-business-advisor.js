/*
 * S&R CoreSync For Intelligent Solutions - Sovereign Smart Business Advisor
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 *
 * External script compliant with strict CSP (No inline script hashes needed)
 */

(function () {
    'use strict';

    // Initial Case Data
    var casesDatabase = [
        {
            id: 'SR-CASE-2026-081',
            clientName: 'أبو جميل (مطعم دمشق الأصيل)',
            type: 'غرامة تأخير إقرار BTW مصلحة الضرائب',
            amount: '€4,500',
            deadline: '18 نوفمبر 2026',
            status: 'قيد الاعتراض والتخفيض',
            statusClass: 'pending',
            assignedTo: 'أ. رودين (المحاسب المعتمد)',
            notes: 'إهمال المحاسب السابق لموعد الربع الثاني. تم إعداد مذكرة Bezwaarschrift لطلب الإعفاء استناداً لمبدأ حسن النية وحداثة العهد بنظام KVK.'
        },
        {
            id: 'SR-CASE-2026-082',
            clientName: 'كافيه الياسمين (أمستردام وست)',
            type: 'مخالفة ترخيص إشغال رصيف البلدية (Gemeente)',
            amount: '€1,850',
            deadline: '24 نوفمبر 2026',
            status: 'تم التخفيض بنسبة 70%',
            statusClass: 'resolved',
            assignedTo: 'أ. رودين (المحاسب المعتمد)',
            notes: 'تم تقديم اعتراض رسمي بعدم استلام الإخطار التمهيدي، وتخفيض المخالفة إلى €550.'
        },
        {
            id: 'SR-CASE-2026-083',
            clientName: 'سوبرماركت البركة للتموين الغذائي',
            type: 'تسوية ضرائب رواتب وأجور موظفين (Loonheffing)',
            amount: '€8,200',
            deadline: '02 ديسمبر 2026',
            status: 'جدولة معتمدة من الضرائب',
            statusClass: 'resolved',
            assignedTo: 'فريق المحاسبة القانونية',
            notes: 'تمت الموافقة على خطة دفع مقسطة على 12 شهراً بدون فوائد تأخير جزائية.'
        }
    ];

    // DOM Elements
    var tabBtns = {
        voice: document.getElementById('tab-btn-voice'),
        engine: document.getElementById('tab-btn-engine'),
        onboarding: document.getElementById('tab-btn-onboarding'),
        accountant: document.getElementById('tab-btn-accountant'),
        stats: document.getElementById('tab-btn-stats')
    };

    var sections = {
        voice: document.getElementById('section-voice'),
        engine: document.getElementById('section-engine'),
        onboarding: document.getElementById('section-onboarding'),
        accountant: document.getElementById('section-accountant'),
        stats: document.getElementById('section-stats')
    };

    // Tab Switching
    function switchTab(activeKey) {
        Object.keys(tabBtns).forEach(function (key) {
            if (key === activeKey) {
                tabBtns[key].style.background = 'var(--gold-primary)';
                tabBtns[key].style.color = '#04070d';
                sections[key].style.display = 'block';
            } else {
                tabBtns[key].style.background = 'rgba(255,255,255,0.06)';
                tabBtns[key].style.color = '#cbd5e1';
                sections[key].style.display = 'none';
            }
        });
    }

    if (tabBtns.voice) { tabBtns.voice.addEventListener('click', function () { switchTab('voice'); }); }
    if (tabBtns.engine) { tabBtns.engine.addEventListener('click', function () { switchTab('engine'); }); }
    if (tabBtns.onboarding) { tabBtns.onboarding.addEventListener('click', function () { switchTab('onboarding'); }); }
    if (tabBtns.accountant) { tabBtns.accountant.addEventListener('click', function () { switchTab('accountant'); }); }
    if (tabBtns.stats) { tabBtns.stats.addEventListener('click', function () { switchTab('stats'); }); }

    // Speech Recognition
    var micBtn = document.getElementById('mic-trigger');
    var micLabel = document.getElementById('mic-status-label');
    var caseInput = document.getElementById('case-input-text');
    var recognition = null;
    var isRecording = false;

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRec();
        recognition.lang = 'ar-SA';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function () {
            isRecording = true;
            if (micBtn) { micBtn.classList.add('recording'); }
            if (micLabel) { micLabel.textContent = '🎙️ جاري الاستماع إلى صوتك الآن... تحدث بحرية'; micLabel.style.color = '#ef4444'; }
        };

        recognition.onresult = function (event) {
            var transcript = event.results[0][0].transcript;
            if (caseInput) {
                caseInput.value = caseInput.value ? caseInput.value + ' ' + transcript : transcript;
            }
        };

        recognition.onerror = function (e) {
            if (micLabel) { micLabel.textContent = 'تعذر التعرف الصوتي: ' + e.error + '. يمكنك الكتابة مباشرة.'; micLabel.style.color = '#f59e0b'; }
            if (micBtn) { micBtn.classList.remove('recording'); }
            isRecording = false;
        };

        recognition.onend = function () {
            isRecording = false;
            if (micBtn) { micBtn.classList.remove('recording'); }
            if (micLabel) { micLabel.textContent = 'تم تسجيل الصوت بنجاح! انقر للحديث مرة أخرى أو انقر "تشخيص المشكلة".'; micLabel.style.color = '#10b981'; }
        };
    }

    if (micBtn) {
        micBtn.addEventListener('click', function () {
            if (!recognition) {
                alert('المتصفح الحالي لا يدعم Web Speech API. يمكنك الكتابة مباشرة في الصندوق أدناه.');
                return;
            }
            if (isRecording) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (err) {
                    recognition.stop();
                }
            }
        });
    }

    // Quick tag injection
    var tags = document.querySelectorAll('.quick-tag');
    tags.forEach(function (tag) {
        tag.addEventListener('click', function () {
            var caseText = this.getAttribute('data-case');
            if (caseInput && caseText) {
                caseInput.value = caseText;
            }
        });
    });

    // Clear input
    var clearBtn = document.getElementById('btn-clear-input');
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            if (caseInput) { caseInput.value = ''; }
        });
    }

    // AI Analysis & Legal Draft Generator
    var analyzeBtn = document.getElementById('btn-analyze-case');
    var outputContainer = document.getElementById('analysis-output-container');
    var statusPill = document.getElementById('analysis-status-pill');

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function () {
            var text = caseInput ? caseInput.value.trim() : '';
            if (!text) {
                alert('يرجى التحدث بالصوت أو كتابة تفاصيل المشكلة أو اختيار أحد القوالب الشائعة أولاً.');
                return;
            }

            if (statusPill) {
                statusPill.textContent = 'جاري التحليل القانوني...';
                statusPill.className = 'status-badge-live pending';
            }

            setTimeout(function () {
                var isAbuJameel = text.indexOf('جميل') !== -1 || text.indexOf('BTW') !== -1 || text.indexOf('ضرائب') !== -1;
                var fineAmount = isAbuJameel ? '€4,500' : '€1,850 - €3,000';
                var penaltyType = isAbuJameel ? 'Verzuimboete / النكول أو التأخير غير المتعمد في إقرار BTW' : 'مخالفة إدارية / ترخيص بلدي';

                var html = `
                    <div style="background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.3); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                            <span style="color: #10b981; font-weight: 800; font-size: 1rem;">✅ التكييف القانوني الأولي للحالة:</span>
                            <span class="status-badge-live resolved">نسبة التخفيض أو الإسقاط المتوقعة: 70% - 100%</span>
                        </div>
                        <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; padding-right: 1.2rem;">
                            <li><strong>تصنيف الغرامة:</strong> ${penaltyType}</li>
                            <li><strong>المبلغ المقدر:</strong> ${fineAmount}</li>
                            <li><strong>المهلة القانونية (Bezwaartermijn):</strong> 6 أسابيع من تاريخ الإشعار (موجب المادة 6:7 من قانون الإدارة العامة الهولندي Awb).</li>
                            <li><strong>السند القانوني للاعتراض:</strong> انعدام القصد الجنائي (Afwezigheid van alle schuld - AVAS)، وإثبات إهمال المحاسب السابق، مع تقديم الإقرار فوراً وإثبات حسن النية.</li>
                        </ul>
                    </div>

                    <div style="background: #060b13; border: 1px solid var(--border-gold); border-radius: 12px; padding: 1.2rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; flex-wrap: wrap; gap: 0.5rem;">
                            <span style="color: var(--gold-primary); font-weight: 800; font-size: 0.95rem;">
                                📜 مسودة خطاب الاعتراض الرسمي بالهولندية (Bezwaarschrift Concept):
                            </span>
                            <button id="btn-copy-draft" class="btn" style="background: rgba(212,175,55,0.2); color: var(--gold-primary); border: 1px solid var(--border-gold); padding: 0.35rem 0.8rem; border-radius: 6px; font-size: 0.78rem; cursor: pointer;">
                                📋 نسخ المسودة
                            </button>
                        </div>
                        <pre style="background: #04070d; border: 1px solid var(--border-dim); border-radius: 8px; padding: 0.9rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; line-height: 1.5; white-space: pre-wrap; direction: ltr; text-align: left;" id="draft-text-content">
Aan: Belastingdienst / Afdeling Bezwaren
Onderwerp: Bezwaarschrift tegen boetebeschikking aanslagnummer [NUMMER]
Betreft: Verzoek tot matiging / kwijtschelding van de verzuimboete

Geachte inspecteur,

Hierbij maak ik namens belanghebbende tijdig bezwaar tegen bovengenoemde verzuimboete.
Belanghebbende heeft altijd te goeder trouw gehandeld. De geconstateerde vertraging 
is uitsluitend veroorzaakt door ernstige nalatigheid van de voormalige administratieve 
dienstverlener, hetgeen belanghebbende niet kan worden toegerekend (pleitbaar standpunt 
/ afwezigheid van opzet).

Het juiste BTW-overzicht is inmiddels volledig ingediend. Gelet op het beleid van de 
Belastingdienst en het evenredigheidsbeginsel, verzoeken wij u de opgelegde boete te 
vernietigen dan wel ambtshalve substantieel te matigen.

Hoogachtend,
S&R CoreSync Business Advisory Services & Partner (Rodin Accounting)</pre>
                        <div style="margin-top: 1rem; display: flex; gap: 0.8rem;">
                            <button id="btn-assign-rodin" class="btn" style="flex: 1; background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; padding: 0.6rem; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 0.9rem;">
                                ⚖️ إرسال وتخصيص الملف للأستاذ رودين (المحاسب المعتمد)
                            </button>
                        </div>
                    </div>
                `;

                if (outputContainer) { outputContainer.innerHTML = html; }
                if (statusPill) {
                    statusPill.textContent = 'تم إعداد المسودة والتكييف بنجاح';
                    statusPill.className = 'status-badge-live resolved';
                }

                // Copy draft button listener
                var copyBtn = document.getElementById('btn-copy-draft');
                if (copyBtn) {
                    copyBtn.addEventListener('click', function () {
                        var pre = document.getElementById('draft-text-content');
                        if (pre) {
                            navigator.clipboard.writeText(pre.textContent).then(function () {
                                copyBtn.textContent = '✓ تم النسخ!';
                                setTimeout(function () { copyBtn.textContent = '📋 نسخ المسودة'; }, 2000);
                            });
                        }
                    });
                }

                // Assign to Rodin button
                var assignBtn = document.getElementById('btn-assign-rodin');
                if (assignBtn) {
                    assignBtn.addEventListener('click', function () {
                        alert('تم تسجيل القضية بنجاح وتخصيصها في لوحة تحكم المحاسب القانوني (الأستاذ رودين) وتجهيز إشعار المتابعة.');
                        switchTab('accountant');
                    });
                }

            }, 600);
        });
    }

    // Populate Cases in Accountant Table
    function renderAccountantTable() {
        var tbody = document.getElementById('accountant-cases-table-body');
        if (!tbody) return;

        tbody.innerHTML = '';
        casesDatabase.forEach(function (item) {
            var tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid rgba(255,255,255,0.06)';
            tr.innerHTML = `
                <td style="padding: 0.8rem; font-family: monospace; color: var(--gold-primary);">${item.id}</td>
                <td style="padding: 0.8rem; font-weight: 700; color: #fff;">${item.clientName}</td>
                <td style="padding: 0.8rem; color: #cbd5e1;">${item.type}</td>
                <td style="padding: 0.8rem; font-weight: 800; color: #f43f5e;">${item.amount}</td>
                <td style="padding: 0.8rem; color: #f59e0b;">${item.deadline}</td>
                <td style="padding: 0.8rem;"><span class="status-badge-live ${item.statusClass}">${item.status}</span></td>
                <td style="padding: 0.8rem;">
                    <button class="btn btn-view-case" data-id="${item.id}" style="background: rgba(56,189,248,0.15); color: var(--cyan); border: 1px solid var(--border-dim); padding: 0.3rem 0.6rem; border-radius: 6px; cursor: pointer; font-size: 0.8rem;">
                        عرض المسودة
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Add view button listeners
        var viewBtns = tbody.querySelectorAll('.btn-view-case');
        viewBtns.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var caseId = this.getAttribute('data-id');
                var found = casesDatabase.find(function (c) { return c.id === caseId; });
                if (found) {
                    alert(`تفاصيل القضية [${found.id}]:\nالعميل: ${found.clientName}\nالمسؤول: ${found.assignedTo}\nملاحظات: ${found.notes}`);
                }
            });
        });
    }

    renderAccountantTable();

    // Onboarding Form Submission
    var onboardingForm = document.getElementById('onboarding-form');
    var onboardingResult = document.getElementById('onboarding-result');

    if (onboardingForm) {
        onboardingForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var bName = document.getElementById('business-name').value;
            var oName = document.getElementById('owner-name').value;
            var phone = document.getElementById('contact-phone').value;
            var city = document.getElementById('business-city').value;
            var need = document.getElementById('primary-need').value;

            var newCaseId = 'SR-CASE-2026-0' + (casesDatabase.length + 81);

            casesDatabase.push({
                id: newCaseId,
                clientName: `${oName} (${bName})`,
                type: need,
                amount: 'قيد التقدير',
                deadline: '6 أسابيع',
                status: 'ملف جديد قيد التدقيق',
                statusClass: 'pending',
                assignedTo: 'أ. رودين (المحاسب المعتمد)',
                notes: `تم تسجيل العميل عبر بوابة الانضمام السريع من مدينة ${city}. الهاتف: ${phone}.`
            });

            renderAccountantTable();

            if (onboardingResult) {
                onboardingResult.style.display = 'block';
                onboardingResult.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span style="color: #10b981; font-weight: 800; font-size: 1.1rem;">🎉 تم تسجيل النشاط بنجاح وإنشاء الملف الرقمي!</span>
                        <span style="font-family: monospace; color: var(--gold-primary); font-weight: 700;">${newCaseId}</span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6;">
                        تم ربط ملف <strong>${bName}</strong> بإدارة المحاسب القانوني المعتمد <strong>(الأستاذ رودين)</strong>. تم إنشاء مذكرة ترحيبية وتجهيز قناة تواصل مباشرة لحل كافة الغرامات والالتزامات الضريبية فوراً.
                    </p>
                    <div style="margin-top: 1rem; display: flex; gap: 0.6rem;">
                        <button id="btn-goto-accountant" class="btn" style="background: var(--gold-primary); color: #04070d; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 700; cursor: pointer;">
                            الانتقال إلى لوحة المحاسب لمشاهدة الملف
                        </button>
                    </div>
                `;

                var gotoBtn = document.getElementById('btn-goto-accountant');
                if (gotoBtn) {
                    gotoBtn.addEventListener('click', function () {
                        switchTab('accountant');
                    });
                }
            }

            onboardingForm.reset();
        });
    }

    // Export all cases JSON
    var exportBtn = document.getElementById('btn-export-all-cases');
    if (exportBtn) {
        exportBtn.addEventListener('click', function () {
            var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(casesDatabase, null, 2));
            var downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", "SR_CoreSync_Community_Cases_2026.json");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        });
    }

    // WhatsApp Dispatch Button
    var waBtn = document.getElementById('btn-whatsapp-dispatch');
    if (waBtn) {
        waBtn.addEventListener('click', function () {
            var msg = encodeURIComponent(
                "مرحباً S&R CoreSync - المستشار القانوني والمحاسبي الذكي للأعمال:\n" +
                "أود استشارة عاجلة بخصوص مخالفة/غرامة ضريبية مع مصلحة الضرائب الهولندية (Belastingdienst) وتنسيق موعد مع المحاسب القانوني المعتمد (الأستاذ رودين)."
            );
            window.open(`https://wa.me/31618111116?text=${msg}`, '_blank');
        });
    }


    // =========================================================================
    // 🧠 Autonomous Financial & Tax Advisory Engine (2026 Sovereign Edition)
    // Compliant with IFRS, Awb, Wet IB 2001 & Dutch Tax Law Regulations
    // =========================================================================

    var engineElements = {
        sector: document.getElementById('engine-sector'),
        entity: document.getElementById('engine-entity'),
        revenue: document.getElementById('engine-revenue'),
        cogsPct: document.getElementById('engine-cogs-pct'),
        payroll: document.getElementById('engine-payroll'),
        opex: document.getElementById('engine-opex'),
        investments: document.getElementById('engine-investments'),
        btnRun: document.getElementById('btn-run-engine'),
        btnReset: document.getElementById('btn-reset-engine'),
        btnSample: document.getElementById('btn-engine-quick-sample'),
        btnWhatsapp: document.getElementById('btn-engine-whatsapp'),
        btnPrint: document.getElementById('btn-engine-print'),
        btnJson: document.getElementById('btn-engine-json'),
        scoreBadge: document.getElementById('engine-score-badge'),
        metricNetProfit: document.getElementById('metric-net-profit'),
        metricTaxSavings: document.getElementById('metric-tax-savings'),
        metricFinalTax: document.getElementById('metric-final-tax'),
        metricBvStatus: document.getElementById('metric-bv-status'),
        recommendationsBox: document.getElementById('engine-recommendations-box')
    };

    var latestEngineAnalysis = null;

    function formatCurrency(val) {
        return '€' + Math.round(val).toLocaleString('nl-NL');
    }

    function runFinancialAdvisoryEngine() {
        if (!engineElements.revenue) return;

        var sector = engineElements.sector ? engineElements.sector.value : 'horeca';
        var entity = engineElements.entity ? engineElements.entity.value : 'eenmanszaak';
        var revenue = Math.max(0, parseFloat(engineElements.revenue.value) || 0);
        var cogsPct = Math.max(0, Math.min(95, parseFloat(engineElements.cogsPct.value) || 0));
        var payroll = Math.max(0, parseFloat(engineElements.payroll.value) || 0);
        var opex = Math.max(0, parseFloat(engineElements.opex.value) || 0);
        var investments = Math.max(0, parseFloat(engineElements.investments.value) || 0);

        var cogsAmount = revenue * (cogsPct / 100);
        var grossProfit = revenue - cogsAmount;
        var totalExpenses = cogsAmount + payroll + opex;
        var operatingProfit = revenue - totalExpenses;

        // 1. Kleinschaligheidsinvesteringsaftrek (KIA 2026: 28% for investments between €2,800 and €69,765)
        var kiaDeduction = 0;
        if (investments >= 2800) {
            kiaDeduction = Math.min(investments * 0.28, 19534);
        }

        // 2. Entrepreneur deductions (Zelfstandigenaftrek 2026: €2,460)
        var zelfstandigenaftrek = 0;
        if (entity === 'eenmanszaak' || entity === 'vof' || entity === 'zzp') {
            zelfstandigenaftrek = 2460;
        }

        // 3. MKB-winstvrijstelling 2026: 13.31%
        var taxableBeforeMkb = Math.max(0, operatingProfit - kiaDeduction - zelfstandigenaftrek);
        var mkbVrijstelling = (entity !== 'bv') ? (taxableBeforeMkb * 0.1331) : 0;
        var taxableProfit = Math.max(0, taxableBeforeMkb - mkbVrijstelling);

        // 4. Tax Calculation & BV Comparison
        var finalTax = 0;
        var standardTaxWithoutOptim = Math.max(0, operatingProfit * 0.45);
        var isBvRecommended = operatingProfit >= 85000;
        var bvStatusText = isBvRecommended ? 'موصى به بقوة (توفير ضرائب وحماية أصول)' : 'الكيان الفردي أوفر حالياً (استفادة من MKB)';

        if (entity === 'bv') {
            // Corporate Tax (VPB 2026: 19% up to €200k, 25.8% above)
            var dgaSalary = Math.min(56000, Math.max(0, operatingProfit * 0.6));
            var bvProfit = Math.max(0, operatingProfit - dgaSalary - kiaDeduction);
            var vpbTax = (bvProfit <= 200000) ? (bvProfit * 0.19) : (200000 * 0.19 + (bvProfit - 200000) * 0.258);
            var dgaIncomeTax = dgaSalary * 0.3697;
            finalTax = vpbTax + dgaIncomeTax;
        } else {
            // Box 1 Progressive: 36.97% up to €75,518, 49.50% above
            if (taxableProfit <= 75518) {
                finalTax = taxableProfit * 0.3697;
            } else {
                finalTax = (75518 * 0.3697) + ((taxableProfit - 75518) * 0.4950);
            }
        }

        var taxSavings = Math.max(0, standardTaxWithoutOptim - finalTax);

        // 5. Compliance & Audit Risk Score (0 - 100%)
        var auditScore = 95;
        var riskNotes = [];

        if (sector === 'horeca') {
            if (cogsPct < 25 || cogsPct > 40) {
                auditScore -= 12;
                riskNotes.push('نسبة المشتريات والمواد الخام خارج النطاق المعياري لقطاع المطاعم (المعيار: 28% - 35%).');
            }
            if (payroll / revenue > 0.40) {
                auditScore -= 8;
                riskNotes.push('نسبة الرواتب والعمالة مرتفعة مقارنة برقم المبيعات (تتجاوز 40%).');
            }
        } else if (sector === 'retail') {
            if (cogsPct < 45 || cogsPct > 75) {
                auditScore -= 10;
                riskNotes.push('نسبة تكلفة البضائع للمتاجر تسترعي تدقيق مصلحة الضرائب.');
            }
        }

        if (investments > 0 && kiaDeduction === 0) {
            riskNotes.push('استثمارات الأصول أقل من عتبة €2,800 المطلوبة لتفعيل خصم KIA الضريبي.');
        }

        auditScore = Math.max(65, Math.min(98, auditScore));

        // Update UI Metrics
        if (engineElements.metricNetProfit) engineElements.metricNetProfit.textContent = formatCurrency(operatingProfit);
        if (engineElements.metricTaxSavings) engineElements.metricTaxSavings.textContent = formatCurrency(taxSavings);
        if (engineElements.metricFinalTax) engineElements.metricFinalTax.textContent = formatCurrency(finalTax);
        if (engineElements.metricBvStatus) {
            engineElements.metricBvStatus.textContent = isBvRecommended ? 'موصى به بقوة ✓' : 'الكيان الحالي كافٍ';
            engineElements.metricBvStatus.style.color = isBvRecommended ? '#10b981' : 'var(--cyan)';
        }

        if (engineElements.scoreBadge) {
            var scoreClass = auditScore >= 85 ? 'resolved' : (auditScore >= 75 ? 'pending' : 'failed');
            engineElements.scoreBadge.className = 'status-badge-live ' + scoreClass;
            engineElements.scoreBadge.textContent = 'مؤشر الامتثال: ' + auditScore + '% (' + (auditScore >= 85 ? 'آمن ومحصّن' : 'يتطلب معالجة محاسبية') + ')';
        }

        // Sector Arabic Labels
        var sectorNames = {
            horeca: 'المطاعم والمقاهي والضيافة',
            retail: 'التجارة والتجزئة والمتاجر الإلكترونية',
            services: 'الخدمات المهنية والاستشارات وتقنية المعلومات',
            construction: 'المقاولات والإنشاءات والصيانة العامة',
            logistics: 'الشحن والخدمات اللوجستية والنقل'
        };

        var entityNames = {
            eenmanszaak: 'منشأة فردية (Eenmanszaak)',
            vof: 'شركة تضامن وشراكة (VOF)',
            bv: 'شركة ذات مسؤولية محدودة (BV)',
            zzp: 'عمل حر مستقل (ZZP)'
        };

        // 5 Strategic Recommendations
        var recs = [
            {
                title: '1. الهيكل القانوني وحماية الأصول (Legal Entity & Asset Protection)',
                desc: isBvRecommended
                    ? `بما أن الأرباح التشغيلية بلغت ${formatCurrency(operatingProfit)}، يُنصح بالتحول الاستراتيجي إلى شركة BV لعزل الذمة المالية الشخصية وتفادي الشريحة الضريبية العليا Box 1 (49.5%).`
                    : `الكيان الحالي (${entityNames[entity] || entity}) يحقق الاستفادة القصوى من حوافز ريادة الأعمال وإعفاء MKB بنسبة 13.31%، ولا حاجة ملحة لتحمل تكاليف تأسيس BV حالياً.`
            },
            {
                title: '2. كفاءة ضريبة القيمة المضافة واسترداد الفواتير (BTW Optimization)',
                desc: `يتم تفعيل استرداد ضريبة القيمة المضافة بنسبة 21% على كافة الأجهزة والمشتريات الاستثمارية (${formatCurrency(investments)})، مما يوفر استرداداً نقدياً فورياً بقيمة ${formatCurrency(investments * 0.21)} من مصلحة الضرائب.`
            },
            {
                title: '3. حافز الاستثمار للشركات الصغيرة (KIA Investment Allowance)',
                desc: kiaDeduction > 0
                    ? `تم اعتماد خصم استثمار الأجهزة والتجهيزات (KIA) بقيمة ${formatCurrency(kiaDeduction)} يخصم مباشرة من الوعاء الضريبي، مما يقلل الالتزام الضريبي السنوي فورياً.`
                    : `للاستفادة من خصم KIA السنوي، احرص على أن تتجاوز استثمارات الأجهزة والتجهيزات عتبة €2,800 سنوياً مع الاحتفاظ بالفواتير الرسمية باسم المنشأة.`
            },
            {
                title: '4. ضبط سجلات الرواتب وعقود العمالة (Payroll & Inspectie SZW)',
                desc: `تم رصد ميزانية رواتب سنوية بقيمة ${formatCurrency(payroll)}. نوصي بتطبيق عقود العمل المرنة وتوثيق نظام البصمة وسجلات الدوام لحماية المنشأة من غرامات التفتيش العمالي الهولندي.`
            },
            {
                title: '5. التحصين الاستباقي ومطابقة مصلحة الضرائب (Audit Safeguard)',
                desc: riskNotes.length > 0
                    ? `تنبيه تدقيق: ${riskNotes.join(' ')} ينصح بجدولة مراجعة دورية مع الشريك المحاسبي القانوني المعتمد (الأستاذ رودين) لضبط قيود الإدخال وإرسال الإقرارات بانتظام.`
                    : `المنشأة تقع ضمن النطاقات المعيارية المعتمدة لقطاع ${sectorNames[sector]}. يُنصح بالمحافظة على إرسال إقرارات BTW الشهرية/الربعية دون تأخير لتجنب غرامات النكول (Verzuimboete).`
            }
        ];

        // Render Recommendations
        if (engineElements.recommendationsBox) {
            var recsHtml = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; border-bottom: 1px solid rgba(212,175,55,0.2); padding-bottom: 0.5rem;">
                    <span style="color: var(--gold-primary); font-weight: 800; font-size: 0.95rem;">
                        📋 التوصيات الاستراتيجية الخمس للمنشأة (${sectorNames[sector]}):
                    </span>
                    <span style="font-size: 0.78rem; color: #94a3b8;">معايير IFRS والضرائب 2026</span>
                </div>
                <div style="display: flex; flex-col; gap: 0.7rem; font-size: 0.86rem; color: #cbd5e1; line-height: 1.6;">
            `;

            recs.forEach(function (r) {
                recsHtml += `
                    <div style="background: rgba(255,255,255,0.02); border-right: 3px solid var(--gold-primary); padding: 0.5rem 0.8rem; margin-bottom: 0.5rem; border-radius: 0 6px 6px 0;">
                        <strong style="color: #fff; display: block; margin-bottom: 0.2rem;">${r.title}</strong>
                        <span style="color: #94a3b8;">${r.desc}</span>
                    </div>
                `;
            });

            recsHtml += '</div>';
            engineElements.recommendationsBox.innerHTML = recsHtml;
        }

        // Cache latest analysis
        latestEngineAnalysis = {
            sector: sectorNames[sector],
            entity: entityNames[entity],
            revenue: revenue,
            grossProfit: grossProfit,
            operatingProfit: operatingProfit,
            taxSavings: taxSavings,
            finalTax: finalTax,
            bvRecommended: isBvRecommended,
            auditScore: auditScore,
            recommendations: recs,
            timestamp: new Date().toISOString()
        };
    }

    // Attach Engine Event Listeners
    if (engineElements.btnRun) {
        engineElements.btnRun.addEventListener('click', function () {
            runFinancialAdvisoryEngine();
        });
    }

    if (engineElements.btnReset) {
        engineElements.btnReset.addEventListener('click', function () {
            if (engineElements.sector) engineElements.sector.value = 'horeca';
            if (engineElements.entity) engineElements.entity.value = 'eenmanszaak';
            if (engineElements.revenue) engineElements.revenue.value = '350000';
            if (engineElements.cogsPct) engineElements.cogsPct.value = '32';
            if (engineElements.payroll) engineElements.payroll.value = '85000';
            if (engineElements.opex) engineElements.opex.value = '48000';
            if (engineElements.investments) engineElements.investments.value = '18000';
            runFinancialAdvisoryEngine();
        });
    }

    if (engineElements.btnSample) {
        engineElements.btnSample.addEventListener('click', function () {
            if (engineElements.sector) engineElements.sector.value = 'horeca';
            if (engineElements.entity) engineElements.entity.value = 'eenmanszaak';
            if (engineElements.revenue) engineElements.revenue.value = '380000';
            if (engineElements.cogsPct) engineElements.cogsPct.value = '31';
            if (engineElements.payroll) engineElements.payroll.value = '92000';
            if (engineElements.opex) engineElements.opex.value = '52000';
            if (engineElements.investments) engineElements.investments.value = '22000';
            runFinancialAdvisoryEngine();
        });
    }

    if (engineElements.btnWhatsapp) {
        engineElements.btnWhatsapp.addEventListener('click', function () {
            if (!latestEngineAnalysis) runFinancialAdvisoryEngine();
            var a = latestEngineAnalysis;
            var lines = [
                '🏛️ استشارة مالية وضريبية ذكية معتمدة (S&R CoreSync):',
                '🏢 القطاع: ' + a.sector,
                '⚖️ الكيان: ' + a.entity,
                '💶 المبيعات السنوية: €' + Math.round(a.revenue).toLocaleString('nl-NL'),
                '📈 صافي الربح التشغيلي: €' + Math.round(a.operatingProfit).toLocaleString('nl-NL'),
                '💰 الوفورات الضريبية المقدرة: €' + Math.round(a.taxSavings).toLocaleString('nl-NL'),
                '🛡️ مؤشر الامتثال والأمان: ' + a.auditScore + '%',
                'نرجو جدولة مراجعة الملف مع المحاسب القانوني المعتمد (الأستاذ رودين).'
            ];
            var summary = encodeURIComponent(lines.join('\n'));
            window.open(`https://wa.me/31618111116?text=${summary}`, '_blank');
        });
    }

    if (engineElements.btnPrint) {
        engineElements.btnPrint.addEventListener('click', function () {
            if (!latestEngineAnalysis) runFinancialAdvisoryEngine();
            window.print();
        });
    }

    if (engineElements.btnJson) {
        engineElements.btnJson.addEventListener('click', function () {
            if (!latestEngineAnalysis) runFinancialAdvisoryEngine();
            var jsonStr = JSON.stringify(latestEngineAnalysis, null, 2);
            var blob = new Blob([jsonStr], { type: 'application/json' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'SR-CoreSync-Financial-Advisory-Report-2026.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }

    // Auto-run once to initialize the dashboard with baseline values
    runFinancialAdvisoryEngine();

})();

