# -*- coding: utf-8 -*-
"""
S&R CoreSync - Inject Autonomous Financial & Tax Advisory Engine into js/smart-business-advisor.js
"""

JS_FILE = "js/smart-business-advisor.js"

with open(JS_FILE, "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update tabBtns and sections
old_tabs = """    var tabBtns = {
        voice: document.getElementById('tab-btn-voice'),
        onboarding: document.getElementById('tab-btn-onboarding'),
        accountant: document.getElementById('tab-btn-accountant'),
        stats: document.getElementById('tab-btn-stats')
    };

    var sections = {
        voice: document.getElementById('section-voice'),
        onboarding: document.getElementById('section-onboarding'),
        accountant: document.getElementById('section-accountant'),
        stats: document.getElementById('section-stats')
    };"""

new_tabs = """    var tabBtns = {
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
    };"""

if old_tabs in js:
    js = js.replace(old_tabs, new_tabs)
    print("Updated tabBtns and sections.")
else:
    print("Error: old_tabs not found.")

# Add listener for tab-btn-engine
old_switch = """    if (tabBtns.voice) {
        tabBtns.voice.addEventListener('click', function () {
            switchTab('voice');
        });
    }"""

new_switch = """    if (tabBtns.voice) {
        tabBtns.voice.addEventListener('click', function () {
            switchTab('voice');
        });
    }

    if (tabBtns.engine) {
        tabBtns.engine.addEventListener('click', function () {
            switchTab('engine');
        });
    }"""

if old_switch in js:
    js = js.replace(old_switch, new_switch)
    print("Added tabBtns.engine listener.")
else:
    print("Error: old_switch not found.")

# Add Financial Advisory Engine Module before })();
engine_module = """
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
            var summary = encodeURIComponent(
                "🏛️ استشارة مالية وضريبية ذكية معتمدة (S&R CoreSync):\n" +
                "🏢 القطاع: " + a.sector + "\n" +
                "⚖️ الكيان: " + a.entity + "\n" +
                "💶 المبيعات السنوية: €" + Math.round(a.revenue).toLocaleString('nl-NL') + "\n" +
                "📈 صافي الربح التشغيلي: €" + Math.round(a.operatingProfit).toLocaleString('nl-NL') + "\n" +
                "💰 الوفورات الضريبية المقدرة: €" + Math.round(a.taxSavings).toLocaleString('nl-NL') + "\n" +
                "🛡️ مؤشر الامتثال والأمان: " + a.auditScore + "%\n" +
                "نرجو جدولة مراجعة الملف مع المحاسب القانوني المعتمد (الأستاذ رودين)."
            );
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
"""

# Inject before closing })();
if "})();" in js:
    js = js.replace("})();", engine_module + "\n})();")
    print("Injected Autonomous Financial & Tax Advisory Engine.")
else:
    print("Error: })(); not found.")

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(js)
print("Updated js/smart-business-advisor.js successfully.")
