/**
 * S&R CoreSync Solutions - Enterprise Suite Engine v2.0
 * 1. Instant Official PDF Quotation Generator
 * 2. Client Visual Feedback Hub
 * 3. EU GDPR Cookie Consent System
 * 4. Executive Meeting Scheduler (Auto-Timezone & Calendar .ICS)
 * 5. AI & ERP Digital Readiness Assessment Engine
 * 6. Enterprise Case Studies & Measurable ROI Hub
 * 7. Live Cloud ERP Demo Sandbox Quick Access
 */

(function () {
    'use strict';

    const WHATSAPP_NUM = '31687764998';

    // State for Assessment Quiz
    let currentQuizStep = 0;
    const quizAnswers = {};

    const QUIZ_QUESTIONS = [
        {
            title: 'ما هو حجم منشأتكم وعدد الموظفين الحالي؟',
            options: [
                { text: 'مؤسسة ناشئة / متنامية (1 - 10 موظفين)', score: 15, saving: 800 },
                { text: 'شركة متوسطة الحجم (11 - 50 موظفاً)', score: 25, saving: 1800 },
                { text: 'مؤسسة متعددة الأقسام (51 - 200 موظف)', score: 35, saving: 3500 },
                { text: 'مجموعة كبرى / سلاسل فروع (+200 موظف)', score: 45, saving: 6500 }
            ]
        },
        {
            title: 'كيف تدار العمليات المحاسبية وسلاسل الإمداد حالياً؟',
            options: [
                { text: 'ملفات Excel يدوية وتقارير مبعثرة', score: 10, saving: 1200 },
                { text: 'برنامج محاسبي قديم غير متصل بالسحابة', score: 20, saving: 900 },
                { text: 'نظام سحابي منفصل يفتقر للتكامل الكامل', score: 30, saving: 600 },
                { text: 'نظام ERP متقدم ولكن يحتاج أتمتة وذكاء اصطناعي', score: 40, saving: 400 }
            ]
        },
        {
            title: 'ما هو مستوى الأتمتة بالذكاء الاصطناعي لديكم؟',
            options: [
                { text: 'لا يوجد أي استخدام للذكاء الاصطناعي حتى الآن', score: 5, saving: 1500 },
                { text: 'استخدامات فردية وبدائية (ChatGPT فقط)', score: 15, saving: 1000 },
                { text: 'أتمتة جزئية لبعض المهام المكررة', score: 25, saving: 700 },
                { text: 'منظومة سحابية ذكية تبحث عن حلول RAG مخصصة', score: 35, saving: 500 }
            ]
        },
        {
            title: 'ما هو الهدف الأهم لمنشأتكم في المرحلة المقبلة؟',
            options: [
                { text: 'الامتثال الضريبي الأوروبي وتوحيد حسابات الفروع', score: 25, saving: 1100 },
                { text: 'تقليل الهدر المالي وتسريع دورة إصدار الفواتير', score: 30, saving: 1400 },
                { text: 'ربط الفروع بنظام سحابي مركزي فوري المزامنة', score: 35, saving: 1600 },
                { text: 'بناء تطبيق سحابي ومنصة مخصصة لعملاء VIP', score: 40, saving: 1200 }
            ]
        }
    ];

    // Enterprise Case Studies Data
    const CASE_STUDIES = {
        almarai: {
            client: 'سلاسل الإمداد الأوروبية – قطاع المواد الغذائية',
            title: 'مزامنة لوجستية فورية وأنظمة ERP عالية التوافر عبر 4 دول أوروبية',
            tag: 'Cloud ERP & Microservices',
            kpis: [
                { val: '94%', lbl: 'تسريع مزامنة البيانات' },
                { val: '18 ساعة', lbl: 'وفر أسبوعي لفرق المحاسبة' },
                { val: '99.99%', lbl: 'توافر سحابي High Availability' }
            ],
            challenge: 'كانت المستودعات في هولندا وألمانيا وبلجيكا تعاني من تأخر مزامنة المخزون وتكرار الفواتير اليدوية بسبب استخدام أنظمة محلية متفرقة، مما أدى لاختناقات في التوزيع وتأخر التسويات المالية الشهرية.',
            solution: 'قام م. سليم عزيزة بتصميم بنية سحابية موزعة بنظام Microservices فائقة السرعة على خوادم أوروبية آمنة، بينما أشرف أ. رائد كعكة على توحيد شجرة الحسابات والامتثال لضريبة القيمة المضافة الأوروبية (VAT & IFRS).',
            roi: 'تم خفض وقت إصدار التقارير المجمعة من 8 أيام إلى نقرة واحدة فورية، وتحقيق وفر سنوي تجاوز 45,000 يورو في تكاليف العمليات والفاقد المخزني.'
        },
        schoon365: {
            client: '365 SCHOON B.V. – هولندا',
            title: 'أتمتة الفواتير والامتثال الضريبي الهولندي (Belastingdienst)',
            tag: 'Dutch Tax & Financial Automation',
            kpis: [
                { val: '100%', lbl: 'امتثال ضريبي هولندي خالٍ من الأخطاء' },
                { val: '45%', lbl: 'تسريع تحصيل الفواتير (iDEAL)' },
                { val: '0 دقيقة', lbl: 'جهد يدوي في حساب الـ BTW' }
            ],
            challenge: 'التعامل مع آلاف الفواتير الشهرية وعقود الصيانة المتكررة وفق اللوائح الضريبية الهولندية الصارمة للـ Belastingdienst، مع صعوبة متابعة التحصيل اليدوي للشركات المتعاقدة.',
            solution: 'تطوير محرك مالي مخصص يربط مباشرة مع بوابات الدفع الهولندية (iDEAL / SEPA Direct Debit)، ويقوم بتوليد الإقرارات الضريبية تلقائياً بصيغة موحدة متوافقة مع مكاتب المحاسبة والتدقيق الهولندية.',
            roi: 'تحول دورة الفوترة إلى دورة آلية بالكامل تعمل في الخلفية دون أي تدخل بشري، مما مكن الإدارة من مضاعفة عدد العملاء دون الحاجة لتوظيف محاسبين إضافيين.'
        },
        buraq: {
            client: 'براق للخدمات اللوجستية والشحن الذكي',
            title: 'نظام ذكاء اصطناعي للتنبؤ بالمسارات وإدارة الأساطيل اللحظية',
            tag: 'Predictive AI & Logistics Ops',
            kpis: [
                { val: '22%', lbl: 'توفير في تكاليف استهلاك الوقود' },
                { val: '99.2%', lbl: 'التزام دقيق بمواعيد التسليم' },
                { val: '< 2 ثانية', lbl: 'استجابة التوجيه اللحظي للمركبات' }
            ],
            challenge: 'تذبذب أوقات التوصيل وارتفاع تكاليف الوقود بسبب عدم وجود رؤية تنبؤية للازدحامات وتوزيع الشحنات غير المتوازن بين السائقين.',
            solution: 'بناء خوارزمية ذكاء اصطناعي تنبؤية تقوم بتحليل بيانات المسارات والطقس وحجم الشحنات لحظياً، وإعادة توجيه الأسطول ديناميكياً مع لوحة تحكم فورية للإدارة.',
            roi: 'تقليص وقت الرحلات بنسبة 28% وزيادة رضا العملاء بنسبة 40%، مما أتاح للشركة توسيع أسطولها وزيادة عقود النقل B2B الكبرى.'
        }
    };

    // 1. Initialize DOM Elements
    function initEnterpriseSuite() {
        injectPDFModal();
        injectFloatingHub();
        injectGDPRBanner();
        injectSchedulerModal();
        injectReadinessModal();
        injectCaseStudyModal();
        attachEstimatorButton();
        injectHeaderDemoPill();
        injectHeaderCurrencyWidget();
        bindCaseStudiesOnCards();
        checkURLParams();
    }

    // Attach PDF Button to Cost Estimator
    function attachEstimatorButton() {
        const actionsContainer = document.querySelector('.summary-actions');
        if (actionsContainer && !document.getElementById('estimatorPdfBtn')) {
            const pdfBtn = document.createElement('button');
            pdfBtn.type = 'button';
            pdfBtn.id = 'estimatorPdfBtn';
            pdfBtn.className = 'estimator-btn-pdf';
            pdfBtn.title = 'تصدير عرض سعر رسمي بصيغة PDF';
            pdfBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <span>تصدير عرض سعر رسمي (PDF)</span>
            `;
            pdfBtn.onclick = window.exportEstimatorPDF;
            actionsContainer.appendChild(pdfBtn);
        }
    }

    // Inject Live Demo Button in Header
    function injectHeaderDemoPill() {
        const actions = document.querySelector('.header-col-actions');
        if (actions && !document.getElementById('headerLiveDemoPill')) {
            const demoBtn = document.createElement('a');
            demoBtn.id = 'headerLiveDemoPill';
            demoBtn.href = window.location.pathname.includes('/en/') || window.location.pathname.includes('/nl/') ? '../demo.html' : 'demo.html';
            demoBtn.className = 'btn-live-sandbox-header';
            const isEn = window.location.pathname.includes('/en/');
            const isNl = window.location.pathname.includes('/nl/');
            const label = isEn ? 'Live ERP Demo ⚡' : (isNl ? 'Live ERP Demo ⚡' : 'تجربة ERP السحابي ⚡');
            demoBtn.title = isEn ? 'Test Live Cloud ERP Dashboard' : (isNl ? 'Test Live Cloud ERP Dashboard' : 'تجربة لوحة تحكم ERP السحابية الحية');
            demoBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                <span>${label}</span>
            `;
            const mobileBtn = actions.querySelector('.btn-mobile-menu');
            if (mobileBtn) {
                actions.insertBefore(demoBtn, mobileBtn);
            } else {
                actions.appendChild(demoBtn);
            }
        }
    }

    // 2. Inject PDF Quotation Modal
    function injectPDFModal() {
        if (document.getElementById('esQuoteModalOverlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'esQuoteModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-quote-modal" role="dialog" aria-modal="true" aria-labelledby="esQuoteTitle">
                <div class="es-quote-toolbar">
                    <div class="es-quote-toolbar-title" id="esQuoteTitle">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        <span>عرض السعر المؤسسي الرسمي // S&R CoreSync B.V.</span>
                    </div>
                    <div class="es-toolbar-actions">
                        <button type="button" class="es-btn-tool es-btn-tool-print" onclick="window.printOfficialQuote()">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                            <span>طباعة / حفظ كـ PDF</span>
                        </button>
                        <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeQuoteModal()">إغلاق ✕</button>
                    </div>
                </div>

                <div class="es-quote-paper" id="esQuotePrintableArea">
                    <div class="es-quote-header">
                        <div class="es-quote-brand">
                            <h2>S&R CORESYNC SOLUTIONS</h2>
                            <p>Enterprise Cloud Architecture & Intelligent AI Systems</p>
                            <p style="font-size: 0.78rem; color: #a0aec0; margin-top: 2px;">Amsterdam HQ, The Netherlands | Global Enterprise Delivery</p>
                        </div>
                        <div class="es-quote-meta">
                            <span class="es-quote-ref" id="quoteRefNumber">REF-SR-2026-8941</span>
                            <div><strong>تاريخ الإصدار:</strong> <span id="quoteIssueDate"></span></div>
                            <div><strong>صلاحية العرض:</strong> 14 يوماً من تاريخه</div>
                        </div>
                    </div>

                    <div class="es-quote-section-title">
                        <span>تفاصيل عرض العمل والمواصفات المحددة</span>
                    </div>

                    <table class="es-quote-table">
                        <thead>
                            <tr>
                                <th>البند / المكون البرمجي</th>
                                <th>المواصفات الفنية</th>
                                <th>الجدول الزمني</th>
                                <th>التقدير المالي</th>
                            </tr>
                        </thead>
                        <tbody id="quoteTableBody"></tbody>
                    </table>

                    <div class="es-quote-total-box">
                        <div class="es-quote-total-card">
                            <div class="es-quote-total-row">
                                <span>المجموع الصافي:</span>
                                <span id="quoteSubtotal">€0</span>
                            </div>
                            <div class="es-quote-total-row">
                                <span>ضريبة القيمة المضافة (0% B2B EU):</span>
                                <span>€0.00</span>
                            </div>
                            <div class="es-quote-total-row grand-total">
                                <span>الإجمالي المقدر:</span>
                                <span id="quoteGrandTotal" style="color: #c5a880;">€0</span>
                            </div>
                        </div>
                    </div>

                    <div style="font-size: 0.78rem; color: #718096; line-height: 1.6; margin-bottom: 24px;">
                        * ملاحظة: هذا التقدير معتمد بموجب بروتوكول S&R للهندسة السحابية وأنظمة الـ ERP والذكاء الاصطناعي، ويخضع لاتفاقية مستوى الخدمة المؤسسية (SLA). يشمل العرض كافة اختبارات الحماية وتوافق معايير GDPR الأوروبية.
                    </div>

                    <div class="es-quote-signatures">
                        <div class="es-sig-block">
                            <div class="es-sig-title">الاعتماد التقني والهندسة السحابية</div>
                            <div class="es-sig-name">Eng. Mohammad Salim Aziza</div>
                            <div class="es-sig-role">Co-Founder & CTO // Lead Cloud Systems Architect</div>
                        </div>
                        <div class="es-sig-block">
                            <div class="es-sig-title">الإشراف المالي والأنظمة المؤسسية</div>
                            <div class="es-sig-name">Mr. Mohammad Raed Kaakeh</div>
                            <div class="es-sig-role">Co-Founder & CFO // Financial ERP Architect</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) window.closeQuoteModal();
        });
    }

    // 3. Inject Floating Hub (Feedback, Quiz, Scheduler)
    function injectFloatingHub() {
        if (document.getElementById('esFloatingSuite')) return;

        const hub = document.createElement('div');
        hub.id = 'esFloatingSuite';
        hub.className = 'es-floating-suite';
        hub.innerHTML = `
            <button type="button" class="es-feedback-fab" onclick="window.openReadinessModal()" title="قياس الجاهزية الرقمية لشركتكم">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                <span>قياس الجاهزية الرقمية 📊</span>
            </button>
            <button type="button" class="es-feedback-fab" onclick="window.openSchedulerModal()" title="حجز جلسة استشارية تنفيذية">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <span>حجز استشارة تنفيذية 📅</span>
            </button>
            <button type="button" class="es-feedback-fab" onclick="window.openFeedbackModal()" title="إرسال ملاحظة أو طلب تعديل مباشر">
                <span class="es-feedback-dot"></span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                <span>ملاحظات الزبون | Feedback</span>
            </button>
        `;
        document.body.appendChild(hub);

        // Feedback Modal
        const overlay = document.createElement('div');
        overlay.id = 'esFeedbackModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-feedback-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <span class="es-feedback-dot"></span>
                        <span>بوابة ملاحظات الزبون المباشرة</span>
                    </h3>
                    <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeFeedbackModal()">✕</button>
                </div>
                <div class="es-feedback-body">
                    <p style="font-size: 0.82rem; color: rgba(255,255,255,0.7); margin: 0 0 10px;">
                        شارك ملاحظاتك أو طلبات التعديل مباشرة مع م. سليم ليتم تنفيذها في النسخة التجريبية الحية.
                    </p>

                    <div class="es-input-group">
                        <label>الاسم أو المؤسسة:</label>
                        <input type="text" id="fbClientName" class="es-input-field" placeholder="مثال: شركة الأفق للتجارة">
                    </div>

                    <div class="es-input-group">
                        <label>القسم المستهدف بالملاحظة:</label>
                        <select id="fbTargetSection" class="es-select-field">
                            <option value="الواجهة الرئيسية (Hero Section)">الواجهة الرئيسية (Hero Section)</option>
                            <option value="كروت الخدمات وباقات دانا">كروت الخدمات وباقات دانا</option>
                            <option value="حاسبة التكلفة والأسعار">حاسبة التكلفة والأسعار</option>
                            <option value="المشاريع السابقة (Portfolio)">المشاريع السابقة (Portfolio)</option>
                            <option value="قسم الشركاء والمؤسسين">قسم الشركاء والمؤسسين</option>
                            <option value="أخرى / فكرة عامة">أخرى / فكرة عامة</option>
                        </select>
                    </div>

                    <div class="es-input-group">
                        <label>نوع الملاحظة:</label>
                        <select id="fbCategory" class="es-select-field">
                            <option value="🎨 تعديل تصميم وألوان">🎨 تعديل تصميم وألوان</option>
                            <option value="✍️ تعديل نصوص وصياغة">✍️ تعديل نصوص وصياغة</option>
                            <option value="⚡ طلب ميزة إضافية">⚡ طلب ميزة إضافية</option>
                            <option value="🐞 ملاحظة فنية / استجابة">🐞 ملاحظة فنية / استجابة</option>
                        </select>
                    </div>

                    <div class="es-input-group">
                        <label>نص الملاحظة بالتفصيل:</label>
                        <textarea id="fbDetails" class="es-textarea-field" rows="3" placeholder="اكتب تفاصيل التعديل المطلوب هنا..."></textarea>
                    </div>

                    <div class="es-feedback-actions">
                        <button type="button" class="es-btn-send-wa" onclick="window.sendFeedbackViaWhatsApp()">
                            <svg viewBox="0 0 32 32" width="18" height="18" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                            <span>إرسال فوراً عبر واتساب</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) window.closeFeedbackModal();
        });
    }

    // 4. Inject Executive Meeting Scheduler Modal
    function injectSchedulerModal() {
        if (document.getElementById('esSchedulerModalOverlay')) return;

        const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/Amsterdam';

        const overlay = document.createElement('div');
        overlay.id = 'esSchedulerModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-scheduler-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        <span>مجدول الاستشارات التنفيذية // S&R Executive Advisory</span>
                    </h3>
                    <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeSchedulerModal()">✕</button>
                </div>
                <div class="es-feedback-body">
                    <p style="font-size: 0.82rem; color: rgba(255,255,255,0.7); margin: 0;">
                        احجز جلسة استشارية أولية مجانية مدتها 30 دقيقة عبر Zoom لمناقشة بنيتكم السحابية أو متطلبات الـ ERP.
                    </p>

                    <div class="es-input-group">
                        <label>اختر المستشار التنفيذي:</label>
                        <div class="es-consultant-grid">
                            <div class="es-consultant-card active" onclick="window.selectConsultant('salim', this)">
                                <div class="es-consultant-name">م. سليم عزيزة</div>
                                <div class="es-consultant-role">CTO • الأنظمة والذكاء الاصطناعي</div>
                            </div>
                            <div class="es-consultant-card" onclick="window.selectConsultant('raed', this)">
                                <div class="es-consultant-name">أ. رائد كعكة</div>
                                <div class="es-consultant-role">CFO • الحلول المالية وERP</div>
                            </div>
                            <div class="es-consultant-card" onclick="window.selectConsultant('both', this)">
                                <div class="es-consultant-name">جلسة مشتركة</div>
                                <div class="es-consultant-role">استشارة تقنية ومالية شاملة</div>
                            </div>
                        </div>
                    </div>

                    <div style="font-size: 0.75rem; color: var(--es-cyan); display: flex; align-items: center; gap: 6px;">
                        <span>🌐 منطقتك الزمنية المكتشفة تلقائياً:</span>
                        <strong>${tz}</strong>
                    </div>

                    <div class="es-input-group">
                        <label>اختر اليوم والوقت المفضل (بتوقيتك المحلي):</label>
                        <div class="es-slots-grid">
                            <button type="button" class="es-slot-btn active" onclick="window.selectSlot('غداً - 11:00 صباحاً', this)">غداً 11:00 ص</button>
                            <button type="button" class="es-slot-btn" onclick="window.selectSlot('غداً - 03:00 مساءً', this)">غداً 03:00 م</button>
                            <button type="button" class="es-slot-btn" onclick="window.selectSlot('بعد غد - 01:00 ظهراً', this)">بعد غد 01:00 م</button>
                            <button type="button" class="es-slot-btn" onclick="window.selectSlot('بعد غد - 05:00 مساءً', this)">بعد غد 05:00 م</button>
                            <button type="button" class="es-slot-btn" onclick="window.selectSlot('الأسبوع القادم - صباحاً', this)">الأسبوع القادم (ص)</button>
                            <button type="button" class="es-slot-btn" onclick="window.selectSlot('الأسبوع القادم - مساءً', this)">الأسبوع القادم (م)</button>
                        </div>
                    </div>

                    <div class="es-input-group">
                        <label>الاسم والشركة:</label>
                        <input type="text" id="schClientName" class="es-input-field" placeholder="مثال: م. أحمد - المدير العام لشركة ...">
                    </div>

                    <div class="es-input-group">
                        <label>موضوع الاستشارة الأساسي:</label>
                        <input type="text" id="schTopic" class="es-input-field" placeholder="مثال: ترقية نظام الـ ERP السحابي وربط الفروع">
                    </div>

                    <div class="es-feedback-actions">
                        <button type="button" class="es-btn-send-wa" onclick="window.confirmScheduler()">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                            <span>تأكيد الحجز وجدولة الموعد فوراً</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) window.closeSchedulerModal();
        });
    }

    // 5. Inject AI & ERP Digital Readiness Assessment Modal
    function injectReadinessModal() {
        if (document.getElementById('esReadinessModalOverlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'esReadinessModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-readiness-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                        <span>مقياس الجاهزية الرقمية والوفر المالي // CoreSync AI Assessment</span>
                    </h3>
                    <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeReadinessModal()">✕</button>
                </div>
                <div class="es-feedback-body" id="quizContainer">
                    <div class="es-quiz-progress-bar">
                        <div class="es-quiz-progress-fill" id="quizProgressFill"></div>
                    </div>
                    <div id="quizQuestionArea">
                        <!-- Questions injected dynamically -->
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) window.closeReadinessModal();
        });
    }

    // 6. Inject Enterprise Case Studies Modal
    function injectCaseStudyModal() {
        if (document.getElementById('esCaseStudyModalOverlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'esCaseStudyModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-casestudy-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        <span>دراسة حالة موثقة وعائد الاستثمار // Enterprise Case Study</span>
                    </h3>
                    <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeCaseStudyModal()">✕</button>
                </div>
                <div class="es-feedback-body" id="caseStudyBody">
                    <!-- Populated dynamically -->
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) window.closeCaseStudyModal();
        });
    }

    // 7. Inject EU GDPR Cookie Banner
    function injectGDPRBanner() {
        if (localStorage.getItem('coresync_gdpr_status')) return;
        if (document.getElementById('esGdprBanner')) return;

        const banner = document.createElement('div');
        banner.id = 'esGdprBanner';
        banner.className = 'es-gdpr-banner active';
        banner.innerHTML = `
            <div class="es-gdpr-content">
                <div class="es-gdpr-title">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    <span>الامتثال للائحة حماية البيانات الأوروبية (EU GDPR)</span>
                </div>
                <p class="es-gdpr-text">
                    نحن نستخدم ملفات تعريف الارتباط والتقنيات السحابية الأساسية في منصة S&R CoreSync لضمان سرعة التحميل وتجربة تصفح آمنة ومطابقة للقوانين الهولندية والأوروبية.
                </p>
            </div>
            <div class="es-gdpr-actions">
                <button type="button" class="es-btn-gdpr-accept" onclick="window.acceptGDPR()">قبول الكل (Accept All)</button>
                <button type="button" class="es-btn-gdpr-decline" onclick="window.declineGDPR()">الأساسية فقط</button>
            </div>
        `;
        document.body.appendChild(banner);
    }

    // Bind Case Studies on existing portfolio buttons
    function bindCaseStudiesOnCards() {
        document.querySelectorAll('.work-explore-btn').forEach((btn, idx) => {
            const keys = ['almarai', 'schoon365', 'buraq'];
            const key = keys[idx % keys.length];
            btn.onclick = function (e) {
                e.preventDefault();
                window.openCaseStudy(key);
            };
        });
    }

    function checkURLParams() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('feedback') || urlParams.get('preview') === 'client') {
            setTimeout(() => window.openFeedbackModal(), 800);
        }
        if (urlParams.has('scheduler')) {
            setTimeout(() => window.openSchedulerModal(), 800);
        }
        if (urlParams.has('assessment')) {
            setTimeout(() => window.openReadinessModal(), 800);
        }
    }

    // ==========================================
    // Window Global Functions
    // ==========================================

    window.exportEstimatorPDF = function () {
        const state = window._estimatorState || {
            type: { title: 'هوية بصرية وتطوير متكامل', price: 950, days: '7 - 10 أيام عمل' },
            pages: { title: '1 - 5 صفحات رئيسية', price: 0 },
            lang: { title: 'لغة واحدة', price: 0 },
            pay: { title: 'بدون دفع إلكتروني', price: 0 },
            speed: { title: 'تسليم قياسي', price: 0 }
        };

        const total = Object.values(state).reduce((sum, g) => sum + (g.price || 0), 0);
        const now = new Date();
        const issueDate = now.toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' });
        const ref = 'CSR-' + now.getFullYear() + '-' + Math.floor(1000 + Math.random() * 9000);

        document.getElementById('quoteRefNumber').textContent = ref;
        document.getElementById('quoteIssueDate').textContent = issueDate;

        const tbody = document.getElementById('quoteTableBody');
        tbody.innerHTML = `
            <tr>
                <td><strong>نوع الحزمة والمشروع</strong></td>
                <td>${state.type.title}</td>
                <td>${state.type.days || 'حسب الاتفاق'}</td>
                <td>€${(state.type.price || total).toLocaleString('en')}</td>
            </tr>
            <tr>
                <td><strong>نطاق الصفحات والتنفيذ</strong></td>
                <td>${state.pages.title}</td>
                <td>مشمول</td>
                <td>€${(state.pages.price || 0).toLocaleString('en')}</td>
            </tr>
            <tr>
                <td><strong>منظومة اللغات والترجمة</strong></td>
                <td>${state.lang.title}</td>
                <td>مشمول</td>
                <td>€${(state.lang.price || 0).toLocaleString('en')}</td>
            </tr>
            <tr>
                <td><strong>بوابات الدفع والربط البنكي</strong></td>
                <td>${state.pay.title}</td>
                <td>مشمول</td>
                <td>€${(state.pay.price || 0).toLocaleString('en')}</td>
            </tr>
            <tr>
                <td><strong>معيار وسرعة التسليم</strong></td>
                <td>${state.speed.title}</td>
                <td>مشمول</td>
                <td>€${(state.speed.price || 0).toLocaleString('en')}</td>
            </tr>
        `;

        document.getElementById('quoteSubtotal').textContent = `€${total.toLocaleString('en')}`;
        document.getElementById('quoteGrandTotal').textContent = `€${total.toLocaleString('en')}`;

        const overlay = document.getElementById('esQuoteModalOverlay');
        overlay.classList.add('active');
    };

    window.closeQuoteModal = () => document.getElementById('esQuoteModalOverlay')?.classList.remove('active');
    window.printOfficialQuote = () => window.print();

    window.openFeedbackModal = () => document.getElementById('esFeedbackModalOverlay')?.classList.add('active');
    window.closeFeedbackModal = () => document.getElementById('esFeedbackModalOverlay')?.classList.remove('active');

    window.sendFeedbackViaWhatsApp = function () {
        const clientName = document.getElementById('fbClientName').value.trim() || 'عميل تجريبي';
        const targetSection = document.getElementById('fbTargetSection').value;
        const category = document.getElementById('fbCategory').value;
        const details = document.getElementById('fbDetails').value.trim();

        if (!details) {
            alert('يرجى كتابة نص الملاحظة قبل الإرسال.');
            return;
        }

        const msg = [
            `*💡 ملاحظة جديدة على النسخة التجريبية – S&R CoreSync*`,
            `👤 *من:* ${clientName}`,
            `📍 *القسم:* ${targetSection}`,
            `🏷️ *النوع:* ${category}`,
            `📝 *الملاحظة:* ${details}`,
            `🔗 *الرابط:* ${window.location.href}`
        ].join('\n');

        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeFeedbackModal();
    };

    // Scheduler Handlers
    let selectedConsultant = 'salim';
    let selectedSlot = 'غداً - 11:00 صباحاً';

    window.openSchedulerModal = () => document.getElementById('esSchedulerModalOverlay')?.classList.add('active');
    window.closeSchedulerModal = () => document.getElementById('esSchedulerModalOverlay')?.classList.remove('active');

    window.selectConsultant = function (type, el) {
        selectedConsultant = type;
        document.querySelectorAll('.es-consultant-card').forEach(c => c.classList.remove('active'));
        el.classList.add('active');
    };

    window.selectSlot = function (slot, el) {
        selectedSlot = slot;
        document.querySelectorAll('.es-slot-btn').forEach(b => b.classList.remove('active'));
        el.classList.add('active');
    };

    window.confirmScheduler = function () {
        const name = document.getElementById('schClientName').value.trim() || 'شخصية قيادية';
        const topic = document.getElementById('schTopic').value.trim() || 'استشارة سحابية وERP';
        const consultantNames = {
            salim: 'م. سليم عزيزة (CTO السحابي والذكاء الاصطناعي)',
            raed: 'أ. رائد كعكة (CFO الأنظمة المالية وERP)',
            both: 'جلسة استشارية مشتركة (م. سليم + أ. رائد)'
        };

        const msg = [
            `*📅 طلب حجز جلسة استشارية تنفيذية – S&R CoreSync*`,
            `👤 *الاسم / المنشأة:* ${name}`,
            `💼 *المستشار المطلوب:* ${consultantNames[selectedConsultant]}`,
            `⏰ *الموعد المقترح:* ${selectedSlot}`,
            `🎯 *موضوع الاستشارة:* ${topic}`,
            `🌐 *المنطقة الزمنية:* ${Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/Amsterdam'}`
        ].join('\n');

        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeSchedulerModal();
    };

    // Assessment Quiz Handlers
    window.openReadinessModal = function () {
        currentQuizStep = 0;
        renderQuizStep();
        document.getElementById('esReadinessModalOverlay')?.classList.add('active');
    };

    window.closeReadinessModal = () => document.getElementById('esReadinessModalOverlay')?.classList.remove('active');

    function renderQuizStep() {
        const fill = document.getElementById('quizProgressFill');
        const area = document.getElementById('quizQuestionArea');
        if (!area || !fill) return;

        if (currentQuizStep >= QUIZ_QUESTIONS.length) {
            renderQuizResults();
            return;
        }

        const q = QUIZ_QUESTIONS[currentQuizStep];
        fill.style.width = `${((currentQuizStep + 1) / QUIZ_QUESTIONS.length) * 100}%`;

        area.innerHTML = `
            <div style="font-size: 0.75rem; color: var(--es-cyan); font-weight: 700; margin-bottom: 6px;">
                السؤال ${currentQuizStep + 1} من ${QUIZ_QUESTIONS.length}
            </div>
            <h4 style="color: #fff; font-size: 1.05rem; font-weight: 800; margin-bottom: 16px;">
                ${q.title}
            </h4>
            <div class="es-quiz-options">
                ${q.options.map((opt, i) => `
                    <div class="es-quiz-option" onclick="window.chooseQuizOption(${opt.score}, ${opt.saving})">
                        <span>${opt.text}</span>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="9 18 15 12 9 6"/></svg>
                    </div>
                `).join('')}
            </div>
        `;
    }

    window.chooseQuizOption = function (score, saving) {
        quizAnswers[currentQuizStep] = { score, saving };
        currentQuizStep++;
        renderQuizStep();
    };

    function renderQuizResults() {
        const area = document.getElementById('quizQuestionArea');
        const totalScore = Object.values(quizAnswers).reduce((sum, a) => sum + a.score, 0);
        const monthlySaving = Object.values(quizAnswers).reduce((sum, a) => sum + a.saving, 0);
        const scorePercentage = Math.min(95, Math.max(35, totalScore));

        area.innerHTML = `
            <div style="text-align: center; padding: 10px 0;">
                <div class="es-quiz-score-circle">
                    <span class="es-quiz-score-val">${scorePercentage}%</span>
                    <span class="es-quiz-score-lbl">الجاهزية الرقمية</span>
                </div>
                <h3 style="color: #fff; font-size: 1.2rem; font-weight: 800; margin-bottom: 8px;">
                    تقرير الجدوى والتحول الرقمي لمنشأتكم
                </h3>
                <p style="color: rgba(255,255,255,0.78); font-size: 0.85rem; line-height: 1.6; max-width: 480px; margin: 0 auto 16px;">
                    بناءً على إجاباتكم، تمتلك منشأتكم أرضية ممتازة للتطوير، مع وجود <strong>فرصة مؤكدة لوفر تشغيلي يقدر بـ €${monthlySaving.toLocaleString('en')} شهرياً</strong> عبر أتمتة الـ ERP ودمج الذكاء الاصطناعي مع CoreSync.
                </p>
                <div class="es-casestudy-kpi-grid" style="margin-bottom: 20px;">
                    <div class="es-casestudy-kpi">
                        <div class="val">€${monthlySaving.toLocaleString('en')}</div>
                        <div class="lbl">وفر شهري مقدر</div>
                    </div>
                    <div class="es-casestudy-kpi">
                        <div class="val">4.5x</div>
                        <div class="lbl">تسريع التقارير المالية</div>
                    </div>
                    <div class="es-casestudy-kpi">
                        <div class="val">100%</div>
                        <div class="lbl">أتمتة سحابية موثوقة</div>
                    </div>
                </div>
                <button type="button" class="es-btn-send-wa" style="width: 100%;" onclick="window.bookAssessmentConsultation(${scorePercentage}, ${monthlySaving})">
                    <span>حجز جلسة لمناقشة خطة التحول المقترحة 🚀</span>
                </button>
            </div>
        `;
    }

    window.bookAssessmentConsultation = function (score, saving) {
        const msg = [
            `*📊 نتيجة تقييم الجاهزية الرقمية – S&R CoreSync*`,
            `🎯 *نسبة الجاهزية الحالية:* ${score}%`,
            `💰 *الوفر الشهري المقدر:* €${saving.toLocaleString('en')}`,
            `🤝 نرغب في مناقشة خطة العمل وأتمتة المنظومة معكم.`
        ].join('\n');
        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeReadinessModal();
    };

    // Case Study Modal Handlers
    window.openCaseStudy = function (key) {
        const data = CASE_STUDIES[key] || CASE_STUDIES.almarai;
        const body = document.getElementById('caseStudyBody');
        if (!body) return;

        body.innerHTML = `
            <div class="es-casestudy-hero">
                <span class="es-casestudy-tag">${data.tag}</span>
                <h3 style="color: #fff; font-size: 1.15rem; font-weight: 800; margin: 4px 0 6px;">${data.title}</h3>
                <p style="font-size: 0.8rem; color: var(--es-gold-light); margin: 0;">العميل / القطاع: ${data.client}</p>
            </div>
            <div style="padding: 16px 20px;">
                <div class="es-casestudy-kpi-grid">
                    ${data.kpis.map(k => `
                        <div class="es-casestudy-kpi">
                            <div class="val">${k.val}</div>
                            <div class="lbl">${k.lbl}</div>
                        </div>
                    `).join('')}
                </div>

                <div style="margin-bottom: 14px;">
                    <h5 style="color: #f87171; font-size: 0.82rem; font-weight: 800; margin-bottom: 4px;">⚠️ التحدي التشغيلي والمالي:</h5>
                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.75); line-height: 1.5; margin: 0;">${data.challenge}</p>
                </div>

                <div style="margin-bottom: 14px;">
                    <h5 style="color: var(--es-cyan); font-size: 0.82rem; font-weight: 800; margin-bottom: 4px;">⚡ الحل الهندسي من CoreSync:</h5>
                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.75); line-height: 1.5; margin: 0;">${data.solution}</p>
                </div>

                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
                    <h5 style="color: #34d399; font-size: 0.82rem; font-weight: 800; margin-bottom: 4px;">📈 الأثر المالي وعائد الاستثمار (ROI):</h5>
                    <p style="font-size: 0.8rem; color: #ecfdf5; line-height: 1.5; margin: 0;">${data.roi}</p>
                </div>

                <button type="button" class="es-btn-send-wa" style="width: 100%;" onclick="window.discussProjectWithTeam('${data.client}')">
                    <span>طلب دراسة حل مماثل لمشروعي عبر WhatsApp</span>
                </button>
            </div>
        `;

        document.getElementById('esCaseStudyModalOverlay')?.classList.add('active');
    };

    window.closeCaseStudyModal = () => document.getElementById('esCaseStudyModalOverlay')?.classList.remove('active');

    window.discussProjectWithTeam = function (projectName) {
        const msg = `مرحباً S&R CoreSync، اطلعت على دراسة الحالة الخاصة بـ (${projectName}) وأرغب في مناقشة حل سحابي/مالي مماثل لشركتنا.`;
        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeCaseStudyModal();
    };

    window.acceptGDPR = function () {
        localStorage.setItem('coresync_gdpr_status', 'accepted');
        document.getElementById('esGdprBanner')?.classList.remove('active');
    };

    window.declineGDPR = function () {
        localStorage.setItem('coresync_gdpr_status', 'essential_only');
        document.getElementById('esGdprBanner')?.classList.remove('active');
    };

/* =====================================================================
       FEATURE 1: CoreSync AI Concierge Widget with Purchase Intent & WhatsApp Human Expert
       ===================================================================== */
    const AI_KB = {
        cloud: {
            keywords: ['cloud', 'سحاب', 'aws', 'azure', 'gcp', 'microservices', 'kubernetes', 'devops', 'بنية', 'خوادم', 'hosting'],
            ar: 'نصمم بنى سحابية Hybrid/Multi-Cloud ذات توافر عالٍ (99.99%) على أفضل مزودي الخدمة العالميين. م. سليم عزيزة يقود هذا المجال بخبرة 10+ سنوات على AWS, Azure وGCP.',
            en: 'We architect Hybrid/Multi-Cloud solutions with 99.99% SLA on AWS, Azure & GCP. Led by Eng. Salim Aziza with 10+ years of enterprise cloud expertise.',
            nl: 'Wij ontwerpen Hybrid/Multi-Cloud-architecturen met 99,99% SLA op AWS, Azure en GCP, geleid door Ir. Salim Aziza.'
        },
        erp: {
            keywords: ['erp', 'odoo', 'oracle', 'sap', 'محاسبة', 'accounting', 'مالية', 'finance', 'invoic', 'فاتورة', 'belastingdienst', 'btw', 'vat', 'ضريبة'],
            ar: 'نقدم حلول ERP متكاملة تشمل Odoo وOracle وحلولاً مخصصة، مع خبرة في الامتثال الضريبي الأوروبي (BTW/VAT) والـ IFRS. أ. رائد كعكة هو معماري ERP الرئيسي.',
            en: 'We deliver ERP solutions including Odoo, Oracle, and custom systems. Expert in EU tax compliance (BTW/VAT), IFRS, and multi-currency financials.',
            nl: 'Wij leveren ERP-oplossingen waaronder Odoo en Oracle, inclusief BTW-compliance en IFRS-standaarden onder leiding van dhr. Raed Kaakeh.'
        },
        ai: {
            keywords: ['ai', 'ذكاء', 'artificial', 'machine learning', 'تعلم', 'nlp', 'automation', 'أتمتة', 'predict', 'تنبؤ'],
            ar: 'نبني نماذج ذكاء اصطناعي مخصصة (RAG, NLP, Predictive Analytics) مدمجة في أنظمة ERP السحابية لدعم القرار وأتمتة العمليات.',
            en: 'We build custom AI solutions (RAG pipelines, NLP, Predictive Analytics) integrated directly into cloud ERP systems for intelligent decision support.',
            nl: 'Wij ontwikkelen AI-oplossingen (RAG, NLP, Predictive Analytics) geïntegreerd in cloud-ERP-systemen voor geautomatiseerde besluitvorming.'
        },
        pricing: {
            keywords: ['price', 'cost', 'سعر', 'تكلفة', 'quote', 'عرض', 'prijs', 'kosten', 'offer', 'budget', 'اسعار', 'أسعار', 'باقة', 'باقات'],
            ar: 'تبدأ باقاتنا من €490 وحتى الحلول المؤسسية المتقدمة. يمكنك استخدام محول العملات والضرائب (EUR/SAR/AED/USD) وتوليد عرض سعر رسمي PDF فوراً.',
            en: 'Our enterprise packages range from €490 to custom enterprise cloud suites. You can switch currencies live and generate an official PDF quote instantly.',
            nl: 'Onze pakketten beginnen bij €490. U kunt live valuta en BTW bekijken en direct een officiële offerte downloaden.'
        },
        contact: {
            keywords: ['contact', 'تواصل', 'whatsapp', 'email', 'phone', 'هاتف', 'بريد', 'reach', 'meeting', 'اجتماع', 'schedule', 'afspraak', 'خبير', 'بشري', 'مهندس', 'سليم', 'رائد'],
            ar: 'فريق الإدارة التنفيذية متاح لمناقشة مشروعك:\n📱 WhatsApp: +31 6 87764998\n📧 info@coresync.solutions\n🏢 المقر: هولندا (EU) وعمليات الشرق الأوسط',
            en: 'Our executive leadership is available:\n📱 WhatsApp: +31 6 87764998\n📧 info@coresync.solutions\n🏢 HQ: Netherlands (EU) & Middle East operations',
            nl: 'Ons managementteam staat voor u klaar:\n📱 WhatsApp: +31 6 87764998\n📧 info@coresync.solutions\n🏢 Hoofdkantoor: Nederland (EU) & Midden-Oosten'
        },
        default: {
            ar: 'شكراً لتواصلك مع CoreSync AI. يسعدني مساعدتك في كل ما يخص الحلول السحابية وأنظمة ERP والذكاء الاصطناعي. اكتب سؤالك أو اختر أحد الخيارات السريعة.',
            en: 'Thank you for contacting CoreSync AI. I\'m here to help with cloud solutions, ERP systems, AI integration, and more. Type your question or choose a quick option.',
            nl: 'Bedankt voor uw contact met CoreSync AI. Ik help u graag met cloudoplossingen, ERP-systemen en AI-integratie. Typ uw vraag of kies een snelle optie.'
        }
    };

    function detectLang() {
        const lang = document.documentElement.lang || 'ar';
        if (lang.startsWith('en')) return 'en';
        if (lang.startsWith('nl')) return 'nl';
        return 'ar';
    }

    function isPurchaseOrConsultIntent(input) {
        const q = input.toLowerCase();
        const purchaseKeywords = [
            'سعر', 'اسعار', 'أسعار', 'تكلفة', 'تكاليف', 'عرض', 'عرض سعر', 'شراء', 'طلب', 'حجز', 'احجز',
            'استشارة', 'استشاره', 'اجتماع', 'خبير', 'بشري', 'انسان', 'شخص', 'سليم', 'رائد', 'باقة', 'باقات',
            'عقد', 'اتفاق', 'تعاقد', 'فاتورة', 'اريد', 'أريد', 'محتاج', 'مشروع',
            'buy', 'purchase', 'hire', 'quote', 'pricing', 'price', 'cost', 'book', 'schedule', 'consultation',
            'talk to human', 'human', 'expert', 'sales', 'proposal', 'contract', 'project', 'order', 'demo', 'person', 'salim', 'raed',
            'kopen', 'offerte', 'prijs', 'prijzen', 'kosten', 'afspraak', 'boeken', 'consultatie', 'mens', 'expert', 'voorstel', 'bestellen'
        ];
        return purchaseKeywords.some(kw => q.includes(kw));
    }

    function aiGetResponse(input) {
        const lang = detectLang();
        const q = input.toLowerCase();
        for (const key in AI_KB) {
            if (key === 'default') continue;
            if (AI_KB[key].keywords.some(kw => q.includes(kw))) {
                return { text: AI_KB[key][lang] || AI_KB[key].ar, category: key };
            }
        }
        return { text: AI_KB.default[lang] || AI_KB.default.ar, category: 'default' };
    }

    window.toggleAiChat = function () {
        const win = document.getElementById('esAiChatWindow');
        if (win) {
            win.classList.toggle('active');
            if (win.classList.contains('active')) {
                const input = document.getElementById('esAiInput');
                input && input.focus();
            }
        }
    };

    function injectAIConcierge() {
        if (document.getElementById('esAiChatWindow')) return;
        const lang = detectLang();
        const labels = {
            ar: { name: 'CoreSync AI Concierge', status: 'متاح الآن', humanBtn: '👤 خبير بشري', placeholder: 'اكتب سؤالك...', send: 'إرسال', quick: ['☁️ الحلول السحابية', '💼 أنظمة ERP', '🤖 الذكاء الاصطناعي', '💰 طلب عرض سعر', '📞 تواصل معنا'] },
            en: { name: 'CoreSync AI Concierge', status: 'Online now', humanBtn: '👤 Human Expert', placeholder: 'Ask me anything...', send: 'Send', quick: ['☁️ Cloud Solutions', '💼 ERP Systems', '🤖 AI Integration', '💰 Request a Quote', '📞 Contact Us'] },
            nl: { name: 'CoreSync AI Concierge', status: 'Nu online', humanBtn: '👤 Expert WhatsApp', placeholder: 'Stel uw vraag...', send: 'Versturen', quick: ['☁️ Cloudoplossingen', '💼 ERP-systemen', '🤖 AI-integratie', '💰 Offerte aanvragen', '📞 Neem contact op'] }
        };
        const lbl = labels[lang] || labels.ar;
        const welcomeMsg = AI_KB.default[lang] || AI_KB.default.ar;

        const humanWhatsAppMsg = encodeURIComponent('مرحباً فريق S&R CoreSync، أود التحدث مع خبير بشري (م. سليم عزيزة أو أ. رائد كعكة) لمناقشة متطلبات مشروعنا.');

        const win = document.createElement('div');
        win.id = 'esAiChatWindow';
        win.className = 'es-ai-chat-window';
        win.innerHTML = `
            <div class="es-ai-chat-header">
                <div class="es-ai-avatar">🤖</div>
                <div class="es-ai-chat-info">
                    <h4>${lbl.name}</h4>
                    <span>${lbl.status}</span>
                </div>
                <div class="es-ai-header-actions">
                    <a href="https://wa.me/${WHATSAPP_NUM}?text=${humanWhatsAppMsg}" target="_blank" rel="noopener" class="es-ai-header-human-btn" title="تحدث مع خبير بشري عبر واتساب">
                        ${lbl.humanBtn}
                    </a>
                </div>
                <button onclick="document.getElementById('esAiChatWindow').classList.remove('active')" style="background:none;border:none;color:rgba(255,255,255,0.5);cursor:pointer;font-size:1.2rem;line-height:1;" aria-label="Close">✕</button>
            </div>
            <div class="es-ai-messages" id="esAiMessages">
                <div class="es-ai-msg es-ai-msg-bot">${welcomeMsg}</div>
            </div>
            <div class="es-ai-quick-replies" id="esAiQuickReplies">
                ${lbl.quick.map(q => `<button class="es-ai-quick-btn" onclick="window.aiSendMessage('${q}')">${q}</button>`).join('')}
            </div>
            <div class="es-ai-input-row">
                <input class="es-ai-input" id="esAiInput" type="text" placeholder="${lbl.placeholder}" />
                <button class="es-ai-send-btn" onclick="window.aiSendFromInput()" title="${lbl.send}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                </button>
            </div>
        `;

        document.body.appendChild(win);

        // Bind chat toggle to the floating follow chat button
        const followChatBtn = document.getElementById('floatingFollowChatBtn');
        if (followChatBtn) {
            followChatBtn.onclick = window.toggleAiChat;
        }

        // Auto open if URL has #chat hash
        if (window.location.hash === '#chat') {
            win.classList.add('active');
        }

        const input = document.getElementById('esAiInput');
        if (input) {
            input.addEventListener('keydown', (e) => { if (e.key === 'Enter') window.aiSendFromInput(); });
        }
    }

    window.aiSendMessage = function(text) {
        const msgs = document.getElementById('esAiMessages');
        if (!msgs) return;
        const userEl = document.createElement('div');
        userEl.className = 'es-ai-msg es-ai-msg-user';
        userEl.textContent = text;
        msgs.appendChild(userEl);
        msgs.scrollTop = msgs.scrollHeight;

        const hasIntent = isPurchaseOrConsultIntent(text);

        // Typing indicator
        const typingEl = document.createElement('div');
        typingEl.className = 'es-ai-msg es-ai-msg-bot';
        typingEl.id = 'esAiTyping';
        typingEl.innerHTML = '⋯';
        msgs.appendChild(typingEl);
        msgs.scrollTop = msgs.scrollHeight;

        setTimeout(() => {
            const typing = document.getElementById('esAiTyping');
            if (typing) {
                typing.removeAttribute('id');
                const resp = aiGetResponse(text);
                let content = resp.text.replace(/\n/g, '<br>');

                // If purchase / booking / expert intent is detected, inject Human Expert WhatsApp CTA
                if (hasIntent || resp.category === 'pricing' || resp.category === 'contact') {
                    const waMsg = encodeURIComponent('مرحباً م. سليم عزيزة و أ. رائد كعكة (S&R CoreSync)، أود استشارة خبير بشري بخصوص: ' + text);
                    content += `
                        <div class="es-ai-intent-cta">
                            <div class="es-ai-intent-header">
                                <span class="es-ai-live-dot"></span>
                                <span>الخبراء متاحون الآن للتواصل المباشر</span>
                            </div>
                            <p>اكتشفنا اهتمامك بتنفيذ مشروع أو الاستفسار عن الأسعار. يمكنك التحدث فوراً مع مهندسينا ومستشارينا المعتمدين عبر واتساب:</p>
                            <a href="https://wa.me/${WHATSAPP_NUM}?text=${waMsg}" target="_blank" rel="noopener" class="es-ai-whatsapp-btn">
                                <svg viewBox="0 0 32 32" width="16" height="16" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                                <span>التحدث مع خبير بشري فوراً عبر WhatsApp</span>
                            </a>
                        </div>
                    `;
                }

                typing.innerHTML = content;
                msgs.scrollTop = msgs.scrollHeight;
            }
        }, 600 + Math.random() * 300);

        const quickReplies = document.getElementById('esAiQuickReplies');
        if (quickReplies) quickReplies.style.display = 'none';
    };

    window.aiSendFromInput = function() {
        const input = document.getElementById('esAiInput');
        if (!input || !input.value.trim()) return;
        window.aiSendMessage(input.value.trim());
        input.value = '';
    };

    /* =====================================================================
       FEATURE 2 & 3: Live Client Project DB (Supabase/Firebase Ready) & Secure Client Portal Session
       ===================================================================== */
    const DEFAULT_PROJECT_DB = {
        'CSN-2024-001': {
            client: '365 SCHOON B.V.',
            executive: 'Mr. Jan van den Berg',
            pin: '2024',
            location: 'Amsterdam, Netherlands',
            service: 'Dutch Cloud ERP & Automated Belastingdienst (BTW) Engine',
            completion: 100,
            status: 'Delivered / Live Production SLA',
            budget: '€48,500',
            currency: 'EUR',
            nda: 'DocuSign Ref: #NL-9942-S (Active)',
            assignedLead: 'Mr. Mohammad Raed Kaakeh (CFO) & Eng. Salim Aziza (CTO)',
            phases: [
                { title: 'Discovery & Requirements', sub: 'مكتمل – 15 يناير 2024', status: 'done', pct: 100 },
                { title: 'ERP Configuration & BTW Engine', sub: 'مكتمل – 28 فبراير 2024', status: 'done', pct: 100 },
                { title: 'iDEAL Payment Integration', sub: 'مكتمل – 15 مارس 2024', status: 'done', pct: 100 },
                { title: 'UAT & Go-Live', sub: 'مكتمل – 01 أبريل 2024', status: 'done', pct: 100 }
            ],
            deliverables: [
                { name: 'Architecture_Design_Doc_v2.4.pdf', size: '4.2 MB', date: '2024-03-20', type: 'PDF Spec' },
                { name: 'BTW_Audit_Compliance_Certification.pdf', size: '1.8 MB', date: '2024-04-01', type: 'Tax Certificate' },
                { name: 'Production_Credentials_Vault.enc', size: '12 KB', date: '2024-04-05', type: 'Encrypted Vault' }
            ],
            invoices: [
                { invNo: 'INV-2024-041', amount: '€18,500', status: 'paid', statusText: 'مدفوعة (iDEAL)', date: '2024-01-15' },
                { invNo: 'INV-2024-078', amount: '€20,000', status: 'paid', statusText: 'مدفوعة (SEPA)', date: '2024-03-01' },
                { invNo: 'INV-2024-112', amount: '€10,000', status: 'paid', statusText: 'مدفوعة (Mollie)', date: '2024-04-01' }
            ]
        },
        'CSN-2024-087': {
            client: 'شركة براق للخدمات اللوجستية',
            executive: 'المهندس فهد التميمي',
            pin: '8776',
            location: 'الرياض - دبي',
            service: 'Predictive AI Routing & Hybrid Cloud Fleet Infrastructure',
            completion: 78,
            status: 'Sprint 4: تجارب الأسطول الميدانية اللحظية',
            budget: 'SAR 285,000',
            currency: 'SAR',
            nda: 'NDA-KSA-2024-B (موقعة ومعتمدة)',
            assignedLead: 'Eng. Mohammad Salim Aziza (CTO & Cloud Lead)',
            phases: [
                { title: 'AI Model Training & Data Pipeline', sub: 'مكتمل – 10 أغسطس 2024', status: 'done', pct: 100 },
                { title: 'Real-time Routing Engine', sub: 'مكتمل – 01 سبتمبر 2024', status: 'done', pct: 100 },
                { title: 'Fleet Dashboard & Mobile App', sub: 'جارٍ الآن – التسليم الميداني 20 أكتوبر 2024', status: 'active', pct: 78 },
                { title: 'Training & Handover', sub: 'مجدول – نوفمبر 2024', status: 'pending', pct: 0 }
            ],
            deliverables: [
                { name: 'Fleet_AI_Model_Benchmark_Report.pdf', size: '5.1 MB', date: '2024-08-15', type: 'AI Benchmark' },
                { name: 'Microservices_API_Specs_v1.9.pdf', size: '2.6 MB', date: '2024-09-02', type: 'API Spec' },
                { name: 'Staging_Cluster_Access_Token.txt', size: '2 KB', date: '2024-09-28', type: 'Staging Token' }
            ],
            invoices: [
                { invNo: 'INV-KSA-0087-1', amount: 'SAR 120,000', status: 'paid', statusText: 'مدفوعة (حوالة مصرفية)', date: '2024-08-01' },
                { invNo: 'INV-KSA-0087-2', amount: 'SAR 100,000', status: 'paid', statusText: 'مدفوعة (تحويل سويفت)', date: '2024-09-10' },
                { invNo: 'INV-KSA-0087-3', amount: 'SAR 65,000', status: 'pending', statusText: 'بانتظار التسليم النهائي (أكتوبر)', date: 'Due 2024-10-25' }
            ]
        },
        'CSN-2025-014': {
            client: 'European Logistics Chain B.V.',
            executive: 'Marcus Lindqvist',
            pin: '2025',
            location: 'Rotterdam, Netherlands',
            service: 'Multi-Country Cloud ERP & High-Throughput Microservices',
            completion: 45,
            status: 'Phase 2: Microservices Build & Multi-Tenant Setup',
            budget: '€112,000',
            currency: 'EUR',
            nda: 'NDA-EU-2025-C (Active)',
            assignedLead: 'Eng. Salim Aziza & Mr. Raed Kaakeh',
            phases: [
                { title: 'Cloud Architecture Design', sub: 'مكتمل – 12 مارس 2025', status: 'done', pct: 100 },
                { title: 'Microservices Development', sub: 'جارٍ الآن – الاكتمال 60%', status: 'active', pct: 60 },
                { title: 'Data Migration & Sync', sub: 'مجدول – ديسمبر 2025', status: 'pending', pct: 0 },
                { title: 'Multi-Country Go-Live', sub: 'مجدول – يناير 2026', status: 'pending', pct: 0 }
            ],
            deliverables: [
                { name: 'MultiTenant_Architecture_Blueprint.pdf', size: '6.4 MB', date: '2025-03-12', type: 'Blueprint' }
            ],
            invoices: [
                { invNo: 'INV-2025-014-1', amount: '€45,000', status: 'paid', statusText: 'مدفوعة (SEPA B2B)', date: '2025-03-15' },
                { invNo: 'INV-2025-014-2', amount: '€35,000', status: 'pending', statusText: 'مستحقة المرحلة 2', date: '2025-11-01' }
            ]
        },
        'CSN-2026-099': {
            client: 'مجموعة الرواد للاستثمار والتقنية',
            executive: 'د. طارق المنصوري',
            pin: '2026',
            location: 'دبي - أمستردام',
            service: 'Enterprise AI Agent Hub & Multi-Currency Treasury Management',
            completion: 28,
            status: 'Phase 1: Architecture Blueprint & Security Auditing',
            budget: 'AED 380,000',
            currency: 'AED',
            nda: 'NDA-UAE-2026-A (موقعة ومعتمدة)',
            assignedLead: 'Eng. Mohammad Salim Aziza & Mr. Mohammad Raed Kaakeh',
            phases: [
                { title: 'Requirements & Multi-Currency Schema', sub: 'مكتمل – سبتمبر 2026', status: 'done', pct: 100 },
                { title: 'AI Agent Workflows & RAG Pipeline', sub: 'جارٍ الآن – الإنجاز 50%', status: 'active', pct: 50 },
                { title: 'Treasury ERP Integration', sub: 'مجدول – نوفمبر 2026', status: 'pending', pct: 0 },
                { title: 'Security Audit & Compliance Sign-off', sub: 'مجدول – ديسمبر 2026', status: 'pending', pct: 0 }
            ],
            deliverables: [
                { name: 'AI_Agent_Architecture_Spec_v1.0.pdf', size: '3.8 MB', date: '2026-09-18', type: 'Specification' }
            ],
            invoices: [
                { invNo: 'INV-UAE-099-1', amount: 'AED 150,000', status: 'paid', statusText: 'مدفوعة (تحويل بنكي دبي)', date: '2026-09-20' },
                { invNo: 'INV-UAE-099-2', amount: 'AED 120,000', status: 'pending', statusText: 'مستحقة قريباً', date: '2026-11-15' }
            ]
        }
    };

    // Live Project DB Connector with Supabase / Firebase / Local sync
    window.CoreSyncProjectDB = {
        config: {
            supabaseUrl: window.CORESYNC_SUPABASE_URL || 'https://api.coresync.solutions/supabase/v1',
            supabaseKey: window.CORESYNC_SUPABASE_KEY || '',
            storageKey: 'coresync_live_client_db'
        },
        getAll() {
            try {
                const stored = localStorage.getItem(this.config.storageKey);
                if (stored) return JSON.parse(stored);
            } catch (e) { console.warn(e); }
            return DEFAULT_PROJECT_DB;
        },
        save(code, data) {
            const all = this.getAll();
            all[code] = data;
            try {
                localStorage.setItem(this.config.storageKey, JSON.stringify(all));
            } catch (e) { console.warn(e); }
        },
        async getProject(code) {
            // Check remote Supabase/Firebase if configured with live credentials
            if (this.config.supabaseKey && this.config.supabaseUrl) {
                try {
                    const res = await fetch(`${this.config.supabaseUrl}/projects?code=eq.${code}`, {
                        headers: { 'apikey': this.config.supabaseKey, 'Authorization': `Bearer ${this.config.supabaseKey}` }
                    });
                    if (res.ok) {
                        const json = await res.json();
                        if (json && json.length > 0) return json[0];
                    }
                } catch (e) {
                    console.info('Supabase cloud fetch fallback to live local DB:', e.message);
                }
            }
            const all = this.getAll();
            return all[code] || null;
        },
        login(code, pin) {
            const all = this.getAll();
            const proj = all[code];
            if (!proj) return { success: false, msg: 'لم يتم العثور على رمز المشروع.' };
            if (proj.pin && proj.pin !== pin) return { success: false, msg: 'رمز الأمان (PIN) غير صحيح.' };
            const session = { code, client: proj.client, executive: proj.executive, loginTime: new Date().toISOString() };
            sessionStorage.setItem('coresync_client_session', JSON.stringify(session));
            return { success: true, project: proj };
        },
        logout() {
            sessionStorage.removeItem('coresync_client_session');
        },
        getSession() {
            try {
                const s = sessionStorage.getItem('coresync_client_session');
                return s ? JSON.parse(s) : null;
            } catch (e) { return null; }
        }
    };

    function injectTrackerModal() {
        if (document.getElementById('esTrackerModal')) return;
        const overlay = document.createElement('div');
        overlay.id = 'esTrackerModal';
        overlay.className = 'es-modal-overlay';
        overlay.style.display = 'none';
        overlay.innerHTML = `
            <div class="es-modal-inner" style="max-width:720px;" role="dialog" aria-label="Client Portal & Project Tracker">
                <div class="es-modal-header">
                    <div class="es-modal-header-left">
                        <div class="es-modal-icon" style="background:linear-gradient(135deg,rgba(56,189,248,0.2),rgba(56,189,248,0.05));border-color:rgba(56,189,248,0.3);">📡</div>
                        <div>
                            <h2 class="es-modal-title">بوابة العملاء وتتبع المشاريع الحية</h2>
                            <p class="es-modal-subtitle">CoreSync Client Portal & Live Project DB</p>
                        </div>
                    </div>
                    <button class="es-modal-close" onclick="window.closeTrackerModal()" aria-label="Close">✕</button>
                </div>
                <div class="es-modal-body">
                    <div class="es-portal-nav">
                        <button class="es-portal-nav-tab active" id="tabClientPortal" onclick="window.switchTrackerTab('portal')">🔐 بوابة العميل الآمنة (Client Portal)</button>
                        <button class="es-portal-nav-tab" id="tabPublicLookup" onclick="window.switchTrackerTab('lookup')">🔍 استعلام عام سريع</button>
                    </div>

                    <!-- Client Portal View -->
                    <div id="esPortalContainer"></div>

                    <!-- Public Lookup View -->
                    <div id="esLookupContainer" style="display:none;">
                        <div class="es-currency-switcher-widget" style="margin-bottom:14px;">
                            <span class="es-currency-switcher-label">أدخل رمز المشروع الخاص بك للاطلاع على تقدم الإنجاز العام</span>
                            <span class="es-vat-badge">PUBLIC</span>
                        </div>
                        <div class="es-tracker-search">
                            <input type="text" id="esTrackerCodeInput" placeholder="CSN-2024-087" />
                            <button onclick="window.lookupProjectPublic()">بحث</button>
                        </div>
                        <div id="esTrackerPublicResult"></div>
                    </div>
                </div>
            </div>
        `;
        overlay.addEventListener('click', (e) => { if (e.target === overlay) window.closeTrackerModal(); });
        document.body.appendChild(overlay);
    }

    window.openTrackerModal = function() {
        const el = document.getElementById('esTrackerModal');
        if (el) {
            el.style.display = 'flex';
            el.classList.add('active');
            window.renderClientPortalView();
        }
    };

    window.closeTrackerModal = function() {
        const el = document.getElementById('esTrackerModal');
        if (el) { el.style.display = 'none'; el.classList.remove('active'); }
    };

    window.switchTrackerTab = function(tab) {
        const tabP = document.getElementById('tabClientPortal');
        const tabL = document.getElementById('tabPublicLookup');
        const cP = document.getElementById('esPortalContainer');
        const cL = document.getElementById('esLookupContainer');
        if (tab === 'portal') {
            tabP.classList.add('active');
            tabL.classList.remove('active');
            cP.style.display = 'block';
            cL.style.display = 'none';
            window.renderClientPortalView();
        } else {
            tabL.classList.add('active');
            tabP.classList.remove('active');
            cL.style.display = 'block';
            cP.style.display = 'none';
        }
    };

    window.renderClientPortalView = function() {
        const container = document.getElementById('esPortalContainer');
        if (!container) return;
        const session = window.CoreSyncProjectDB.getSession();
        if (session) {
            const proj = window.CoreSyncProjectDB.getAll()[session.code];
            if (proj) {
                window.renderClientDashboard(container, session.code, proj);
                return;
            }
        }
        window.renderClientLoginForm(container);
    };

    window.renderClientLoginForm = function(container) {
        container.innerHTML = `
            <div class="es-portal-login-card">
                <div class="es-portal-session-badge">🛡️ اتصال مشفر آمن ببروتوكول 256-Bit SSL</div>
                <h3 style="font-size:1.05rem;color:var(--es-gold-light);margin-bottom:6px;">تسجيل الدخول إلى بوابة العميل الخاصة</h3>
                <p style="font-size:0.78rem;color:rgba(255,255,255,0.6);margin-bottom:16px;">أدخل رمز المشروع ورمز الأمان الخاص بك للوصول إلى المستندات السرية ومراحل التنفيذ والفواتير المعتمدة:</p>
                
                <div style="display:flex;flex-direction:column;gap:10px;max-width:380px;margin:0 auto 16px auto;">
                    <input type="text" id="esLoginCode" class="es-ai-input" placeholder="رمز المشروع (مثال: CSN-2024-087)" style="text-transform:uppercase;text-align:center;font-weight:700;" />
                    <input type="password" id="esLoginPin" class="es-ai-input" placeholder="رمز الأمان PIN (مثال: 8776)" style="text-align:center;" />
                    <button class="es-btn-primary" onclick="window.doClientLogin()" style="width:100%;padding:10px;">
                        🔐 الدخول الآمن للبوابة
                    </button>
                </div>
                <div id="esLoginError" style="font-size:0.78rem;color:#f87171;min-height:20px;margin-bottom:8px;"></div>
                
                <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:14px;margin-top:10px;">
                    <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-bottom:8px;">حسابات تجريبية سريعة للفحص والمعاينة (One-Click Demo):</div>
                    <div class="es-demo-logins">
                        <button class="es-demo-btn" onclick="window.quickDemoLogin('CSN-2024-087', '8776')">⚡ براق للخدمات اللوجستية</button>
                        <button class="es-demo-btn" onclick="window.quickDemoLogin('CSN-2024-001', '2024')">⚡ 365 SCHOON B.V.</button>
                        <button class="es-demo-btn" onclick="window.quickDemoLogin('CSN-2025-014', '2025')">⚡ European Logistics</button>
                        <button class="es-demo-btn" onclick="window.quickDemoLogin('CSN-2026-099', '2026')">⚡ مجموعة الرواد</button>
                    </div>
                </div>
            </div>
        `;
    };

    window.quickDemoLogin = function(code, pin) {
        const inpC = document.getElementById('esLoginCode');
        const inpP = document.getElementById('esLoginPin');
        if (inpC && inpP) {
            inpC.value = code;
            inpP.value = pin;
            window.doClientLogin();
        }
    };

    /* =====================================================================
       WEBHOOK NOTIFICATION ENGINE — Supabase Edge / Zapier / Telegram
       Fires instant notifications to executive team on client events.
       To activate live Telegram: set window.CORESYNC_TG_BOT_TOKEN & CORESYNC_TG_CHAT_ID
       To activate Zapier:        set window.CORESYNC_ZAPIER_WEBHOOK_URL
       To activate Supabase Edge: set window.CORESYNC_SUPABASE_WEBHOOK_URL
       ===================================================================== */
    window.CoreSyncWebhook = {
        async fire(eventType, payload) {
            const body = { eventType, timestamp: new Date().toISOString(), platform: 'S&R CoreSync Client Portal', ...payload };

            // 1. Zapier multi-step webhook
            const zapierUrl = window.CORESYNC_ZAPIER_WEBHOOK_URL || '';
            if (zapierUrl) {
                fetch(zapierUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
                    .catch(e => console.warn('[CoreSync Zapier Webhook]', e.message));
            }

            // 2. Supabase Edge Function
            const supaUrl = window.CORESYNC_SUPABASE_WEBHOOK_URL || '';
            const supaKey = window.CORESYNC_SUPABASE_KEY || '';
            if (supaUrl && supaKey) {
                fetch(supaUrl, { method: 'POST', headers: { 'Content-Type': 'application/json', 'apikey': supaKey, 'Authorization': `Bearer ${supaKey}` }, body: JSON.stringify(body) })
                    .catch(e => console.warn('[CoreSync Supabase Webhook]', e.message));
            }

            // 3. Telegram Bot notification
            const tgToken = window.CORESYNC_TG_BOT_TOKEN || '';
            const tgChat  = window.CORESYNC_TG_CHAT_ID  || '';
            if (tgToken && tgChat) {
                const text = `🔔 *S\&R CoreSync Portal Alert*\n\n` +
                    `📌 *Event:* ${eventType}\n` +
                    `🏢 *Client:* ${payload.client || 'N/A'}\n` +
                    `📁 *Project:* ${payload.projectCode || 'N/A'}\n` +
                    (payload.detail ? `📝 *Detail:* ${payload.detail}\n` : '') +
                    `⏰ *Time:* ${new Date().toLocaleString('ar')}\n` +
                    `\n_— Sent automatically by CoreSync Client Portal_`;
                fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: tgChat, text, parse_mode: 'Markdown' })
                }).catch(e => console.warn('[CoreSync Telegram Webhook]', e.message));
            }

            // 4. Always log for audit trail in localStorage
            try {
                const log = JSON.parse(localStorage.getItem('coresync_event_log') || '[]');
                log.unshift({ ...body });
                if (log.length > 100) log.length = 100;
                localStorage.setItem('coresync_event_log', JSON.stringify(log));
            } catch (_) {}

            console.info(`[CoreSync Webhook] ${eventType}`, payload);
        }
    };

    window.doClientLogin = function() {
        const code = (document.getElementById('esLoginCode')?.value || '').trim().toUpperCase();
        const pin = (document.getElementById('esLoginPin')?.value || '').trim();
        const err = document.getElementById('esLoginError');
        if (!code || !pin) {
            if (err) err.textContent = 'يرجى إدخال رمز المشروع ورمز الأمان PIN.';
            return;
        }
        const res = window.CoreSyncProjectDB.login(code, pin);
        if (!res.success) {
            if (err) err.textContent = res.msg;
            return;
        }

        // 🔔 Fire instant notification webhook to executive team
        window.CoreSyncWebhook.fire('CLIENT_LOGIN', {
            projectCode: code,
            client: res.project?.client || code,
            executive: res.project?.executive || 'Unknown',
            detail: `تسجيل دخول إلى بوابة المشروع ${code} بواسطة ${res.project?.executive || 'العميل'}`
        });

        window.renderClientPortalView();
    };

    window.doClientLogout = function() {
        window.CoreSyncProjectDB.logout();
        window.renderClientPortalView();
    };

    window.renderClientDashboard = function(container, code, proj) {
        const dotIcon = { done: '✓', active: '◉', pending: '○' };

        // Milestone Approval: render phases with approve button on active/done phases
        const phases = proj.phases.map((p, i) => {
            const isApprovable = (p.status === 'active' || p.status === 'done') && !p.approved;
            const isApproved = !!p.approved;
            return `
            <div class="es-timeline-item">
                <div class="es-timeline-track">
                    <div class="es-timeline-dot ${p.status}">${dotIcon[p.status]}</div>
                    ${i < proj.phases.length - 1 ? '<div class="es-timeline-line"></div>' : ''}
                </div>
                <div class="es-timeline-content">
                    <div class="es-timeline-title">${p.title}</div>
                    <div class="es-timeline-sub">${p.sub}</div>
                    ${p.status === 'active' ? `<div class="es-progress-bar-mini"><div class="es-progress-bar-fill" style="width:0%" data-target="${p.pct}%"></div></div>` : ''}
                    ${isApproved
                        ? `<div class="es-milestone-approved-badge">✅ معتمدة رقمياً من العميل — ${p.approvedAt || ''}</div>`
                        : isApprovable
                            ? `<button class="es-milestone-approve-btn" onclick="window.approveMilestone('${code}', ${i})">✔ اعتماد هذه المرحلة رقمياً</button>`
                            : ''
                    }
                </div>
            </div>`;
        }).join('');

        // Deliverables with webhook-tracked download
        const deliverables = (proj.deliverables || []).map((d, di) => `
            <div class="es-deliverable-item">
                <div>
                    <div style="font-weight:700;color:#ffffff;">📄 ${d.name}</div>
                    <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);">${d.type} · ${d.size} · ${d.date}</div>
                </div>
                <button class="es-deliverable-btn" onclick="window.downloadDeliverable('${code}', ${di}, '${d.name}')">
                    تحميل ⬇
                </button>
            </div>
        `).join('');

        // Invoices — pending ones get Stripe & iDEAL pay buttons
        const invoices = (proj.invoices || []).map((inv, ii) => {
            const isPending = inv.status !== 'paid';
            const waPayMsg = encodeURIComponent(`طلب دفع فاتورة: ${inv.invNo} بمبلغ ${inv.amount} للمشروع ${code}`);
            const stripeUrl = inv.stripeUrl || `https://wa.me/${WHATSAPP_NUM}?text=${waPayMsg}`;
            const idealUrl  = inv.idealUrl  || `https://wa.me/${WHATSAPP_NUM}?text=${waPayMsg}`;
            return `
            <tr>
                <td style="font-weight:700;">${inv.invNo}</td>
                <td>${inv.date}</td>
                <td style="font-weight:700;color:var(--es-gold-light);">${inv.amount}</td>
                <td>
                    <span class="es-inv-status ${isPending ? 'es-inv-pending' : 'es-inv-paid'}">${inv.statusText}</span>
                    ${isPending ? `
                    <div class="es-inv-pay-actions">
                        <a href="${stripeUrl}" target="_blank" rel="noopener" class="es-pay-btn es-pay-stripe" onclick="window.trackInvoicePayment('${code}', '${inv.invNo}', 'Stripe')">
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M13.976 9.15c-2.172-.806-3.356-1.426-3.356-2.409 0-.831.683-1.305 1.901-1.305 2.227 0 4.515.858 6.09 1.631l.89-5.494C18.252.975 15.697 0 12.165 0 9.667 0 7.589.654 6.104 1.872 4.56 3.147 3.757 4.992 3.757 7.218c0 4.039 2.467 5.76 6.476 7.219 2.585.92 3.445 1.574 3.445 2.583 0 .98-.84 1.545-2.354 1.545-1.875 0-4.965-.921-6.99-2.109l-.9 5.555C4.661 23.211 7.499 24 10.08 24c2.64 0 4.687-.642 6.116-1.865 1.594-1.34 2.418-3.368 2.418-5.824 0-4.103-2.529-5.813-4.638-7.161z"/></svg>
                            Stripe
                        </a>
                        <a href="${idealUrl}" target="_blank" rel="noopener" class="es-pay-btn es-pay-ideal" onclick="window.trackInvoicePayment('${code}', '${inv.invNo}', 'iDEAL')">
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M1 0h22C23.55 0 24 .45 24 1v22c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1V1C0 .45.45 0 1 0zm5.5 6C4.57 6 3 7.57 3 9.5v5C3 16.43 4.57 18 6.5 18H11v-2.5H6.5A1.5 1.5 0 0 1 5 14v-5A1.5 1.5 0 0 1 6.5 7.5H11V6H6.5zM13 6v2.5h4.5A1.5 1.5 0 0 1 19 10v4a1.5 1.5 0 0 1-1.5 1.5H13V18h4.5C19.43 18 21 16.43 21 14.5v-4C21 8.57 19.43 7 17.5 7L13 6z"/></svg>
                            iDEAL
                        </a>
                    </div>` : ''}
                </td>
            </tr>`;
        }).join('');

        const directMsg = encodeURIComponent(`مرحباً فريق S&R CoreSync، أنا العميل ${proj.executive} من شركة ${proj.client} (مشروع ${code})، أود الاستفسار حول تقدم المشروع.`);

        container.innerHTML = `
            <div class="es-portal-auth-header">
                <div>
                    <div class="es-portal-session-badge" style="margin-bottom:2px;">🔒 جلسة موثقة 256-Bit SSL</div>
                    <div style="font-size:0.85rem;font-weight:800;color:#ffffff;">${proj.client} — <span style="color:var(--es-gold-light);">${proj.executive}</span></div>
                    <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">المقر: ${proj.location} · العقد: ${proj.nda}</div>
                </div>
                <button class="es-portal-logout-btn" onclick="window.doClientLogout()">تسجيل خروج ✕</button>
            </div>

            <!-- Project KPI Header -->
            <div style="background:rgba(197,168,128,0.06);border:1px solid rgba(197,168,128,0.25);border-radius:12px;padding:14px;margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
                    <div>
                        <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">رقم المشروع السحابي</div>
                        <div style="font-size:1.1rem;font-weight:900;color:var(--es-gold);">${code}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);">المعمارية السحابية والحل</div>
                        <div style="font-size:0.82rem;font-weight:700;color:#e0f2fe;">${proj.service}</div>
                    </div>
                </div>
                <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);margin-bottom:4px;">
                    حالة الإنجاز الكلي: <strong style="color:var(--es-gold-light);">${proj.completion}%</strong> — ${proj.status}
                </div>
                <div class="es-progress-bar-mini"><div class="es-progress-bar-fill" style="width:0%" data-target="${proj.completion}%"></div></div>
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);margin-top:6px;">
                    المهندس المشرف: <span style="color:#ffffff;">${proj.assignedLead}</span>
                </div>
            </div>

            <!-- Phases Timeline with Milestone Approvals -->
            <h4 style="font-size:0.85rem;color:var(--es-gold);margin-bottom:4px;">مراحل التنفيذ والجدول الزمني</h4>
            <p style="font-size:0.72rem;color:rgba(255,255,255,0.45);margin-bottom:10px;">يمكنك اعتماد المراحل المنجزة رقمياً بتوقيع إلكتروني تلقائي محمي ومؤرخ.</p>
            <div class="es-project-timeline">${phases}</div>

            <!-- Deliverables Vault -->
            <h4 style="font-size:0.85rem;color:var(--es-gold);margin:14px 0 8px 0;">المستندات والملفات المعتمدة (Deliverables Vault)</h4>
            <div class="es-deliverables-list">${deliverables}</div>

            <!-- Invoices Ledger with Payment Buttons -->
            <h4 style="font-size:0.85rem;color:var(--es-gold);margin:14px 0 4px 0;">سجل الفواتير والدفعات المالية</h4>
            <p style="font-size:0.72rem;color:rgba(255,255,255,0.45);margin-bottom:8px;">الفواتير المعلقة مفعّل عليها الدفع الفوري عبر Stripe (بطاقات دولية) و iDEAL (الدفع الهولندي المباشر).</p>
            <table class="es-invoices-table">
                <thead>
                    <tr>
                        <th>رقم الفاتورة</th>
                        <th>التاريخ</th>
                        <th>المبلغ</th>
                        <th>الحالة / الدفع</th>
                    </tr>
                </thead>
                <tbody>${invoices}</tbody>
            </table>

            <!-- Support & Lead Contact -->
            <div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap;">
                <a href="https://wa.me/${WHATSAPP_NUM}?text=${directMsg}" target="_blank" rel="noopener" class="es-btn-primary" style="flex:1;text-align:center;text-decoration:none !important;padding:9px;">
                    💬 محادثة مباشرة مع المهندس المشرف
                </a>
            </div>
        `;

        setTimeout(() => {
            container.querySelectorAll('.es-progress-bar-fill').forEach(bar => {
                bar.style.width = bar.dataset.target;
            });
        }, 100);
    };

    /* =====================================================================
       CLIENT MILESTONE APPROVAL — Digital sign-off with webhook notification
       ===================================================================== */
    window.approveMilestone = function(projectCode, phaseIndex) {
        const all = window.CoreSyncProjectDB.getAll();
        const proj = all[projectCode];
        if (!proj || !proj.phases[phaseIndex]) return;

        const phase = proj.phases[phaseIndex];
        const approvedAt = new Date().toLocaleString('ar');
        const session = window.CoreSyncProjectDB.getSession();

        // Show confirmation dialog
        const confirmMsg = `هل تؤكد الموافقة الرقمية المعتمدة على المرحلة:\n"${phase.title}"؟\n\nسيتم توثيق توقيعك الإلكتروني وإشعار فريق S&R CoreSync فوراً.`;
        if (!confirm(confirmMsg)) return;

        // Mark phase as approved
        proj.phases[phaseIndex].approved = true;
        proj.phases[phaseIndex].approvedBy = session?.client || 'العميل';
        proj.phases[phaseIndex].approvedAt = approvedAt;
        window.CoreSyncProjectDB.save(projectCode, proj);

        // 🔔 Fire Webhook notification to executive team
        window.CoreSyncWebhook.fire('MILESTONE_APPROVED', {
            projectCode,
            client: proj.client,
            executive: proj.executive,
            detail: `اعتماد المرحلة "${phase.title}" (مرحلة ${phaseIndex + 1}) بتاريخ ${approvedAt}`,
            approvedBy: session?.client || proj.executive,
            phaseName: phase.title,
            phaseIndex
        });

        // Show approval receipt notification in portal
        const receipt = document.createElement('div');
        receipt.className = 'es-approval-receipt';
        receipt.innerHTML = `
            <div class="es-approval-receipt-icon">✅</div>
            <div>
                <div class="es-approval-receipt-title">تمت الموافقة الرقمية بنجاح!</div>
                <div class="es-approval-receipt-sub">المرحلة: <strong>${phase.title}</strong> · التوقيع بتاريخ: ${approvedAt}</div>
                <div class="es-approval-receipt-sub">🔔 تم إشعار فريق S&R CoreSync المختص فوراً. شكراً لثقتكم.</div>
            </div>
        `;
        document.querySelector('#esPortalContainer')?.prepend(receipt);
        setTimeout(() => receipt.style.opacity = '0', 5000);
        setTimeout(() => receipt.remove(), 5600);

        // Re-render dashboard to reflect new approval state
        setTimeout(() => window.renderClientPortalView(), 400);
    };

    /* =====================================================================
       DELIVERABLE DOWNLOAD — Webhook-tracked secure download event
       ===================================================================== */
    window.downloadDeliverable = function(projectCode, deliverableIndex, fileName) {
        const all = window.CoreSyncProjectDB.getAll();
        const proj = all[projectCode];
        const session = window.CoreSyncProjectDB.getSession();

        // 🔔 Fire Webhook notification on file download
        window.CoreSyncWebhook.fire('DELIVERABLE_DOWNLOADED', {
            projectCode,
            client: proj?.client || projectCode,
            executive: session?.executive || 'Unknown',
            detail: `تنزيل ملف: "${fileName}" من مخزن المستندات للمشروع ${projectCode}`,
            fileName,
            deliverableIndex
        });

        // Simulate download (in production, replace with signed URL from Supabase Storage or Firebase)
        alert(`⬇ جاري تنزيل الملف المشفر:\n${fileName}\n\n✅ تم توثيق عملية التنزيل وإشعار الفريق التنفيذي.`);
    };

    /* =====================================================================
       INVOICE PAYMENT TRACKING — webhook on pay button click
       ===================================================================== */
    window.trackInvoicePayment = function(projectCode, invoiceNo, gateway) {
        const all = window.CoreSyncProjectDB.getAll();
        const proj = all[projectCode];
        window.CoreSyncWebhook.fire('INVOICE_PAYMENT_INITIATED', {
            projectCode,
            client: proj?.client || projectCode,
            invoiceNo,
            gateway,
            detail: `بدء عملية دفع الفاتورة ${invoiceNo} عبر ${gateway} للمشروع ${projectCode}`
        });
    };

    window.lookupProjectPublic = function() {
        const code = (document.getElementById('esTrackerCodeInput')?.value || '').trim().toUpperCase();
        const result = document.getElementById('esTrackerPublicResult');
        if (!result) return;
        const all = window.CoreSyncProjectDB.getAll();
        const proj = all[code];
        if (!proj) {
            result.innerHTML = `<div style="text-align:center;padding:20px;color:#f87171;font-size:0.84rem;">❌ لم يُعثر على مشروع بهذا الرمز. يرجى التحقق وإعادة المحاولة.</div>`;
            return;
        }

        const dotIcon = { done: '✓', active: '◉', pending: '○' };
        const phases = proj.phases.map((p, i) => `
            <div class="es-timeline-item">
                <div class="es-timeline-track">
                    <div class="es-timeline-dot ${p.status}">${dotIcon[p.status]}</div>
                    ${i < proj.phases.length - 1 ? '<div class="es-timeline-line"></div>' : ''}
                </div>
                <div class="es-timeline-content">
                    <div class="es-timeline-title">${p.title}</div>
                    <div class="es-timeline-sub">${p.sub}</div>
                </div>
            </div>
        `).join('');

        result.innerHTML = `
            <div style="background:rgba(197,168,128,0.06);border:1px solid rgba(197,168,128,0.2);border-radius:12px;padding:14px;margin-top:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <div style="font-weight:900;color:var(--es-gold);">${code}</div>
                    <div style="font-weight:700;color:#ffffff;">${proj.client}</div>
                </div>
                <div style="font-size:0.78rem;color:rgba(255,255,255,0.6);margin-bottom:6px;">نسبة الإنجاز: ${proj.completion}%</div>
                <div class="es-progress-bar-mini"><div class="es-progress-bar-fill" style="width:${proj.completion}%"></div></div>
                <div class="es-project-timeline" style="margin-top:12px;">${phases}</div>
                <p style="font-size:0.7rem;color:rgba(255,255,255,0.4);text-align:center;margin-top:10px;">للوصول إلى الفواتير والمستندات السرية، يرجى الانتقال إلى تبويب "بوابة العميل الآمنة".</p>
            </div>
        `;
    };

    /* =====================================================================
       FEATURE 4: Multi-Currency & VAT Live Switcher Across All Prices
       ===================================================================== */
    const CURRENCIES = {
        EUR: { symbol: '€', flag: '🇪🇺', name: 'Euro', rate: 1, vat: 21, vatName: '🇳🇱 BTW 21% (NL/EU Tax Compliant)' },
        USD: { symbol: '$', flag: '🇺🇸', name: 'US Dollar', rate: 1.08, vat: 0, vatName: '🌐 0% VAT (Non-EU / Export)' },
        AED: { symbol: 'د.إ', flag: '🇦🇪', name: 'UAE Dirham', rate: 3.97, vat: 5, vatName: '🇦🇪 5% ضريبة القيمة المضافة UAE' },
        SAR: { symbol: '﷼', flag: '🇸🇦', name: 'Saudi Riyal', rate: 4.05, vat: 15, vatName: '🇸🇦 15% ضريبة القيمة المضافة KSA' },
        GBP: { symbol: '£', flag: '🇬🇧', name: 'British Pound', rate: 0.86, vat: 20, vatName: '🇬🇧 20% VAT (UK Compliant)' }
    };

    let activeCurrency = 'EUR';
    try {
        const savedCur = localStorage.getItem('coresync_currency');
        if (savedCur && CURRENCIES[savedCur]) {
            activeCurrency = savedCur;
        }
    } catch(e){}

    window.switchCurrency = function(code) {
        if (!CURRENCIES[code]) return;
        activeCurrency = code;
        const cur = CURRENCIES[code];

        // Persist preference
        try {
            localStorage.setItem('coresync_currency', code);
        } catch(e) {}

        // Update all currency buttons across document (pills, modal buttons, and header dropdown options)
        document.querySelectorAll('.es-currency-btn, .dana-cur-pill, .header-cur-option').forEach(btn => {
            const isMatch = btn.dataset.currency === code;
            btn.classList.toggle('active', isMatch);
            btn.classList.toggle('is-active', isMatch);
        });

        // Update Header Currency Display badge
        document.querySelectorAll('.header-currency').forEach(hc => {
            const currentBadge = hc.querySelector('.header-currency__current') || document.getElementById('headerCurCurrent');
            if (currentBadge) {
                currentBadge.innerHTML = `
                    <span class="header-cur-flag">${cur.flag}</span>
                    <span class="header-cur-code">${code} (${cur.symbol})</span>
                `;
            }
        });

        // Update all price displays tagged with data-eur-price
        document.querySelectorAll('[data-eur-price]').forEach(el => {
            const baseEur = parseFloat(el.dataset.eurPrice);
            if (isNaN(baseEur)) return;
            const converted = Math.round(baseEur * cur.rate);
            const formatted = converted.toLocaleString('en-US');

            // Handle preceding currency symbol sibling (e.g. in pricing cards)
            const prev = el.previousElementSibling;
            if (prev && (prev.classList.contains('gold-accent') || prev.dataset.currencySymbolMarker === 'true')) {
                prev.dataset.currencySymbolMarker = 'true';
                if (code === 'SAR' || code === 'AED') {
                    prev.style.display = 'none';
                    el.textContent = `${formatted} ${cur.symbol}`;
                } else {
                    prev.style.display = '';
                    prev.textContent = cur.symbol;
                    el.textContent = formatted;
                }
                return;
            }

            if (code === 'SAR' || code === 'AED') {
                el.textContent = `${formatted} ${cur.symbol}`;
            } else {
                el.textContent = `${cur.symbol}${formatted}`;
            }
        });

        // Update VAT live badges
        document.querySelectorAll('.es-vat-live-badge, .es-pricing-vat-notice span').forEach(el => {
            el.textContent = cur.vatName;
        });

        // Sync with ROI modal if open
        if (window.switchROICurrency) {
            window.switchROICurrency(code);
        }

        // Recalculate comparison addons if table is open
        if (window.recalcComparisonAddons) {
            window.recalcComparisonAddons();
        }
    };

    // Auto-inject header currency widget if not already in DOM
    function injectHeaderCurrencyWidget() {
        if (document.getElementById('headerCurrencyDropdown')) return;
        const actions = document.querySelector('.header-col-actions');
        if (!actions) return;

        const cur = CURRENCIES[activeCurrency] || CURRENCIES.EUR;
        const isAr = document.documentElement.lang === 'ar' || !document.documentElement.lang;
        const isNl = document.documentElement.lang === 'nl';
        
        const curWidget = document.createElement('details');
        curWidget.id = 'headerCurrencyDropdown';
        curWidget.className = 'header-currency notranslate';
        curWidget.setAttribute('translate', 'no');
        
        const optLabels = {
            EUR: isAr ? 'اليورو (EUR)' : (isNl ? 'EUR (Euro)' : 'EUR (Euro)'),
            USD: isAr ? 'الدولار (USD)' : (isNl ? 'USD (Dollar)' : 'USD (Dollar)'),
            SAR: isAr ? 'الريال السعودي (SAR)' : (isNl ? 'SAR (Riyal)' : 'SAR (Riyal)'),
            AED: isAr ? 'الدرهم الإماراتي (AED)' : (isNl ? 'AED (Dirham)' : 'AED (Dirham)'),
            GBP: isAr ? 'الجنيه الإسترليني (GBP)' : (isNl ? 'GBP (Pound)' : 'GBP (Pound)')
        };

        curWidget.innerHTML = `
            <summary aria-label="${isAr ? 'اختيار العملة' : (isNl ? 'Selecteer Valuta' : 'Select Currency')}">
                <span class="header-currency__current" id="headerCurCurrent">
                    <span class="header-cur-flag">${cur.flag}</span>
                    <span class="header-cur-code">${activeCurrency} (${cur.symbol})</span>
                </span>
                <span class="header-currency__chevron" aria-hidden="true">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                </span>
            </summary>
            <div class="header-currency__options">
                ${Object.entries(CURRENCIES).map(([code, c]) => `
                    <button type="button" class="header-cur-option${code === activeCurrency ? ' is-active' : ''}" data-currency="${code}" onclick="window.switchCurrency('${code}'); this.closest('details').removeAttribute('open');">
                        <span class="opt-left"><span class="header-cur-flag">${c.flag}</span><span>${optLabels[code] || code}</span></span>
                        <span class="opt-symbol">${c.symbol}</span>
                    </button>
                `).join('')}
            </div>
        `;

        const langSwitcher = actions.querySelector('.header-language');
        if (langSwitcher && langSwitcher.nextSibling) {
            actions.insertBefore(curWidget, langSwitcher.nextSibling);
        } else {
            actions.prepend(curWidget);
        }
    }

    // Close header currency on click outside
    document.addEventListener('click', function(e) {
        document.querySelectorAll('.header-currency').forEach(function(el) {
            if (el.hasAttribute('open') && !el.contains(e.target)) {
                el.removeAttribute('open');
            }
        });
    });

    /* =====================================================================
       FEATURE 5: Cloud Architecture ROI & Cost Optimizer
       ===================================================================== */
    function injectROIOptimizer() {
        if (document.getElementById('esROIModal')) return;
        const overlay = document.createElement('div');
        overlay.id = 'esROIModal';
        overlay.className = 'es-modal-overlay';
        overlay.style.display = 'none';
        overlay.innerHTML = `
            <div class="es-modal-inner" style="max-width:680px;" role="dialog" aria-label="Cloud ROI Optimizer">
                <div class="es-modal-header">
                    <div class="es-modal-header-left">
                        <div class="es-modal-icon" style="background:linear-gradient(135deg,rgba(16,185,129,0.2),rgba(16,185,129,0.05));border-color:rgba(16,185,129,0.3);">🚀</div>
                        <div>
                            <h2 class="es-modal-title">محسّن التكلفة السحابية</h2>
                            <p class="es-modal-subtitle">Cloud Architecture ROI Optimizer</p>
                        </div>
                    </div>
                    <button class="es-modal-close" onclick="window.closeROIModal()" aria-label="Close">✕</button>
                </div>
                <div class="es-modal-body">
                    <div class="es-currency-switcher-widget">
                        <span class="es-currency-switcher-label">حرّك الأشرطة لمحاكاة البنية التحتية الحالية وقارن مع الحل السحابي المُحسَّن</span>
                        <div class="es-currency-bar">
                            ${Object.entries(CURRENCIES).map(([code, c]) =>
                                `<button class="es-currency-btn${code === activeCurrency ? ' active' : ''}" data-currency="${code}" onclick="window.switchCurrency('${code}')">${c.flag} ${code}</button>`
                            ).join('')}
                        </div>
                    </div>

                    <div class="es-roi-slider-group">
                        <div class="es-roi-slider-label">
                            <span>عدد المستخدمين / المقاعد الشهرية</span>
                            <span class="es-roi-slider-val" id="roiUsersVal">25</span>
                        </div>
                        <input type="range" class="es-slider" id="roiUsers" min="5" max="500" value="25" oninput="window.calcROI()">
                    </div>

                    <div class="es-roi-slider-group">
                        <div class="es-roi-slider-label">
                            <span>تكلفة الخوادم الحالية (شهرياً)</span>
                            <span class="es-roi-slider-val" id="roiServerVal">€1,200</span>
                        </div>
                        <input type="range" class="es-slider" id="roiServer" min="200" max="20000" step="100" value="1200" oninput="window.calcROI()">
                    </div>

                    <div class="es-roi-slider-group">
                        <div class="es-roi-slider-label">
                            <span>ساعات العمل اليدوي أسبوعياً</span>
                            <span class="es-roi-slider-val" id="roiHoursVal">20 ساعة</span>
                        </div>
                        <input type="range" class="es-slider" id="roiHours" min="2" max="160" value="20" oninput="window.calcROI()">
                    </div>

                    <div class="es-roi-compare-grid">
                        <div class="es-roi-compare-card current">
                            <div class="es-roi-card-label">التكلفة الحالية</div>
                            <div class="es-roi-card-amount" id="roiCurrentCost">€2,900</div>
                            <div class="es-roi-card-period">شهرياً / monthly</div>
                        </div>
                        <div class="es-roi-compare-card optimized">
                            <div class="es-roi-card-label">مع CoreSync Cloud</div>
                            <div class="es-roi-card-amount" id="roiOptCost">€1,160</div>
                            <div class="es-roi-card-period">شهرياً / monthly</div>
                        </div>
                    </div>

                    <div class="es-roi-saving-banner">
                        <div class="es-roi-saving-title">الوفر المحقق سنوياً</div>
                        <div class="es-roi-saving-amount" id="roiAnnualSaving">€21,000</div>
                        <div class="es-roi-saving-period">estimated annual savings · توفير تقديري سنوي</div>
                    </div>

                    <div style="display:flex;gap:10px;flex-wrap:wrap;">
                        <button class="es-btn-primary" onclick="window.openModal('esQuoteModalOverlay')" style="flex:1;">
                            احصل على عرض سعر مخصص
                        </button>
                        <button class="es-btn-secondary" onclick="window.closeROIModal()" style="flex:1;">
                            إغلاق
                        </button>
                    </div>
                </div>
            </div>
        `;
        overlay.addEventListener('click', (e) => { if (e.target === overlay) window.closeROIModal(); });
        document.body.appendChild(overlay);
    }

    let roiCurrencyCode = 'EUR';

    window.switchROICurrency = function(code) {
        roiCurrencyCode = code;
        document.querySelectorAll('#esROIModal .es-currency-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.currency === code);
        });
        window.calcROI();
    };

    window.calcROI = function() {
        const users = parseInt(document.getElementById('roiUsers')?.value || 25);
        const server = parseInt(document.getElementById('roiServer')?.value || 1200);
        const hours = parseInt(document.getElementById('roiHours')?.value || 20);

        const cur = CURRENCIES[roiCurrencyCode] || CURRENCIES.EUR;
        const ratePerHour = 35 * cur.rate;

        const currentMonthlyEur = server + (hours * 4 * 35) + (users * 8);
        const optimizedEur = currentMonthlyEur * 0.40;
        const optimized = optimizedEur * cur.rate;
        const current = currentMonthlyEur * cur.rate;
        const annualSaving = (currentMonthlyEur - optimizedEur) * 12 * cur.rate;

        const fmt = (n) => cur.symbol + Math.round(n).toLocaleString('en-US');

        if (document.getElementById('roiUsersVal')) document.getElementById('roiUsersVal').textContent = users;
        if (document.getElementById('roiServerVal')) document.getElementById('roiServerVal').textContent = cur.symbol + Math.round(server * cur.rate).toLocaleString('en-US');
        if (document.getElementById('roiHoursVal')) document.getElementById('roiHoursVal').textContent = hours + ' ساعة';
        if (document.getElementById('roiCurrentCost')) document.getElementById('roiCurrentCost').textContent = fmt(current);
        if (document.getElementById('roiOptCost')) document.getElementById('roiOptCost').textContent = fmt(optimized);
        if (document.getElementById('roiAnnualSaving')) document.getElementById('roiAnnualSaving').textContent = fmt(annualSaving);
    };

    window.openROIModal = function() {
        const el = document.getElementById('esROIModal');
        if (el) { el.style.display = 'flex'; el.classList.add('active'); }
        window.calcROI();
    };

    window.closeROIModal = function() {
        const el = document.getElementById('esROIModal');
        if (el) { el.style.display = 'none'; el.classList.remove('active'); }
    };

    window.openModal = function(id) {
        const el = document.getElementById(id);
        if (el) { el.style.display = 'flex'; el.classList.add('active'); }
    };

    /* =====================================================================
       FEATURE 6: Executive Capability Deck with Live Chart.js Charts & Visual KPIs
       ===================================================================== */
    window.downloadCapabilityDeck = function() {
        const lang = detectLang();
        const titleMap = {
            ar: 'ملف القدرات التنفيذي ولوحة الـ KPIs – S&R CoreSync Solutions',
            en: 'Executive Capability Deck & Visual KPIs – S&R CoreSync Solutions',
            nl: 'Executive Capability Deck & KPI Dashboard – S&R CoreSync Solutions'
        };

        const deck = `<!DOCTYPE html>
<html lang="${lang}" dir="${lang === 'ar' ? 'rtl' : 'ltr'}">
<head>
<meta charset="UTF-8">
<title>${titleMap[lang]}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"><\/script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;900&family=Cairo:wght@400;600;700;900&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: ${lang === 'ar' ? "'Cairo', sans-serif" : "'Plus Jakarta Sans', sans-serif"};
    background: #010907;
    color: #ffffff;
    line-height: 1.6;
  }
  .deck-page { width: 210mm; min-height: 297mm; padding: 14mm 16mm; page-break-after: always; position: relative; margin: 0 auto; background: #010907; }
  .deck-cover { background: linear-gradient(135deg, #010907 0%, #021a12 50%, #010907 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
  .deck-logo-text { font-size: 2.8rem; font-weight: 900; background: linear-gradient(135deg, #c5a880, #f3dfba); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 8px; }
  .deck-tagline { color: rgba(255,255,255,0.7); font-size: 1rem; margin-bottom: 30px; }
  .deck-gold-line { width: 120px; height: 3px; background: linear-gradient(90deg, transparent, #c5a880, transparent); margin: 0 auto 30px; }
  .deck-title { font-size: 1.5rem; font-weight: 900; color: #ffffff; margin-bottom: 12px; }
  .deck-date { font-size: 0.85rem; color: rgba(255,255,255,0.45); }
  
  .deck-section { background: #0a1a12; border-radius: 14px; padding: 18px 20px; margin-bottom: 16px; border: 1px solid rgba(197,168,128,0.22); }
  .deck-section h2 { color: #c5a880; font-size: 1.05rem; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid rgba(197,168,128,0.2); display: flex; align-items: center; gap: 8px; }
  
  .deck-kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 12px; }
  .deck-kpi { background: rgba(197,168,128,0.08); border: 1px solid rgba(197,168,128,0.2); border-radius: 10px; padding: 12px; text-align: center; }
  .deck-kpi-val { font-size: 1.5rem; font-weight: 900; color: #f3dfba; }
  .deck-kpi-lbl { font-size: 0.72rem; color: rgba(255,255,255,0.65); margin-top: 2px; }

  .deck-charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 10px; }
  .deck-chart-box { background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px; text-align: center; }
  .deck-chart-box h3 { font-size: 0.78rem; color: #6ee7b7; margin-bottom: 8px; font-weight: 700; }
  .deck-chart-box canvas { width: 100% !important; max-height: 180px !important; }

  .deck-service { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 10px; }
  .deck-service-icon { width: 34px; height: 34px; border-radius: 8px; background: rgba(197,168,128,0.12); border: 1px solid rgba(197,168,128,0.25); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
  .deck-service-title { font-size: 0.85rem; font-weight: 800; color: #ffffff; margin-bottom: 2px; }
  .deck-service-desc { font-size: 0.74rem; color: rgba(255,255,255,0.65); line-height: 1.45; }

  .deck-leaders { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .deck-leader { background: rgba(197,168,128,0.06); border: 1px solid rgba(197,168,128,0.2); border-radius: 12px; padding: 14px; }
  .deck-leader-name { font-size: 0.95rem; font-weight: 900; color: #f3dfba; margin-bottom: 2px; }
  .deck-leader-role { font-size: 0.74rem; color: #6ee7b7; font-weight: 700; }

  .deck-contact { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 8px; }
  .deck-contact-item { background: rgba(6,182,212,0.08); border: 1px solid rgba(56,189,248,0.2); border-radius: 8px; padding: 10px; text-align: center; font-size: 0.76rem; color: #e0f2fe; }

  .deck-print-bar { position: fixed; top: 12px; right: 12px; z-index: 9999; display: flex; gap: 8px; }
  .deck-print-btn { background: #c5a880; color: #010907; border: none; padding: 8px 16px; border-radius: 999px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
  @media print {
    .deck-print-bar { display: none !important; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; background: #010907 !important; }
    .deck-page { margin: 0; box-shadow: none; }
  }
</style>
</head>
<body>
<div class="deck-print-bar">
  <button class="deck-print-btn" onclick="window.print()">🖨️ حفظ كـ PDF / طباعة</button>
  <button class="deck-print-btn" style="background:rgba(255,255,255,0.2);color:#fff;" onclick="window.close()">✕ إغلاق</button>
</div>

<!-- Page 1: Cover Page -->
<div class="deck-page deck-cover">
  <div class="deck-logo-text">S&R CoreSync</div>
  <div class="deck-tagline">Cloud Engineering · Financial ERP Architecture · Custom AI Solutions</div>
  <div class="deck-gold-line"></div>
  <div class="deck-title">${titleMap[lang]}</div>
  <div class="deck-date">Q4 2026 · Confidential & Proprietary Document · Amsterdam & Middle East</div>
</div>

<!-- Page 2: Analytical KPIs & Chart.js Visuals -->
<div class="deck-page">
  <div class="deck-section">
    <h2>🏆 Enterprise Performance KPIs</h2>
    <div class="deck-kpi-grid">
      <div class="deck-kpi"><div class="deck-kpi-val">99.99%</div><div class="deck-kpi-lbl">Cloud High-Availability SLA</div></div>
      <div class="deck-kpi"><div class="deck-kpi-val">€45,000+</div><div class="deck-kpi-lbl">Avg Annual Client Net Savings</div></div>
      <div class="deck-kpi"><div class="deck-kpi-val">60%</div><div class="deck-kpi-lbl">Hosting & Infra Cost Reduction</div></div>
      <div class="deck-kpi"><div class="deck-kpi-val">100%</div><div class="deck-kpi-lbl">EU Tax Compliance (BTW/VAT)</div></div>
      <div class="deck-kpi"><div class="deck-kpi-val">4.8x</div><div class="deck-kpi-lbl">3-Year Average Client ROI</div></div>
      <div class="deck-kpi"><div class="deck-kpi-val">0 Dwt</div><div class="deck-kpi-lbl">Zero Planned Maintenance Downtime</div></div>
    </div>
  </div>

  <div class="deck-section">
    <h2>📊 Financial Impact & Architecture Benchmarks (Live Visuals)</h2>
    <div class="deck-charts-grid">
      <div class="deck-chart-box">
        <h3>مقارنة التكلفة التشغيلية السنوية (€ TCO Reduction)</h3>
        <canvas id="chartTCO"></canvas>
      </div>
      <div class="deck-chart-box">
        <h3>مؤشر الجاهزية الرقمية والمعمارية (Readiness Radar)</h3>
        <canvas id="chartRadar"></canvas>
      </div>
    </div>
    <div class="deck-chart-box" style="margin-top:12px;">
      <h3>العائد المالي التراكمي على الاستثمار خلال 36 شهراً (€ Cumulative ROI)</h3>
      <canvas id="chartROI"></canvas>
    </div>
  </div>
</div>

<!-- Page 3: Core Services, Founders & Contact -->
<div class="deck-page">
  <div class="deck-section">
    <h2>⚙️ Enterprise Solutions & Capability Pillars</h2>
    <div class="deck-service">
      <div class="deck-service-icon">☁️</div>
      <div>
        <div class="deck-service-title">Cloud Architecture, Kubernetes & DevOps</div>
        <div class="deck-service-desc">Multi-Cloud deployments (AWS/Azure/GCP), CI/CD pipelines, container orchestration, microservices decoupling, automated failover and 99.99% SLA.</div>
      </div>
    </div>
    <div class="deck-service">
      <div class="deck-service-icon">💼</div>
      <div>
        <div class="deck-service-title">ERP Engineering & Automated Tax (BTW/VAT/IFRS)</div>
        <div class="deck-service-desc">Custom ERP & Odoo implementations compliant with Dutch Belastingdienst (BTW 21%), GCC VAT, automated multi-currency invoicing and banking integrations (iDEAL, SEPA, Stripe).</div>
      </div>
    </div>
    <div class="deck-service">
      <div class="deck-service-icon">🤖</div>
      <div>
        <div class="deck-service-title">Custom AI & Intelligent Automation</div>
        <div class="deck-service-desc">RAG pipelines, predictive analytics models for logistics and cash-flow forecasting, enterprise NLP agents, and automated reconciliation bots.</div>
      </div>
    </div>
  </div>

  <div class="deck-section">
    <h2>👥 Co-Founders & Executive Leadership</h2>
    <div class="deck-leaders">
      <div class="deck-leader">
        <div class="deck-leader-name">Eng. Mohammad Salim Aziza</div>
        <div class="deck-leader-role">Co-Founder · CTO & Lead Cloud Systems Architect</div>
        <p style="font-size:0.74rem;color:rgba(255,255,255,0.6);margin-top:6px;line-height:1.45;">10+ years engineering cloud infrastructures across EU and the Middle East. Expert in AWS, Azure, GCP, Kubernetes, high-concurrency microservices, and system resilience.</p>
      </div>
      <div class="deck-leader">
        <div class="deck-leader-name">Mr. Mohammad Raed Kaakeh</div>
        <div class="deck-leader-role">Co-Founder · CFO & Lead Financial ERP Architect</div>
        <p style="font-size:0.74rem;color:rgba(255,255,255,0.6);margin-top:6px;line-height:1.45;">Senior financial architect specializing in EU corporate tax (BTW/VAT), IFRS accounting standards, cross-border multi-currency fiscal workflows, and ERP optimization.</p>
      </div>
    </div>
  </div>

  <div class="deck-section">
    <h2>📍 Headquarters & Direct Inquiries</h2>
    <div class="deck-contact">
      <div class="deck-contact-item">🏢<br>Netherlands HQ (Amsterdam)<br>Middle East Regional Ops</div>
      <div class="deck-contact-item">📱<br>WhatsApp Direct<br>+31 6 87764998</div>
      <div class="deck-contact-item">🌐<br>coresync.solutions<br>info@coresync.solutions</div>
    </div>
    <p style="text-align:center;margin-top:14px;font-size:0.7rem;color:rgba(255,255,255,0.35);">
      This document is confidential and proprietary to S&R CoreSync Solutions B.V. Generated on ${new Date().toLocaleDateString('ar', { dateStyle: 'full' })}.
    </p>
  </div>
</div>

<script>
  window.addEventListener('DOMContentLoaded', () => {
    // 1. TCO Bar Chart
    const ctxTCO = document.getElementById('chartTCO');
    if (ctxTCO) {
      new Chart(ctxTCO, {
        type: 'bar',
        data: {
          labels: ['السنة 1', 'السنة 2', 'السنة 3'],
          datasets: [
            { label: 'البنية التقليدية (Legacy)', data: [58000, 62000, 67000], backgroundColor: 'rgba(239, 68, 68, 0.65)' },
            { label: 'مع CoreSync Cloud', data: [24000, 25500, 27000], backgroundColor: 'rgba(16, 185, 129, 0.75)' }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#ffffff', font: { size: 10 } } } },
          scales: {
            x: { ticks: { color: '#cccccc' }, grid: { color: 'rgba(255,255,255,0.06)' } },
            y: { ticks: { color: '#cccccc' }, grid: { color: 'rgba(255,255,255,0.06)' } }
          }
        }
      });
    }

    // 2. Radar Chart
    const ctxRadar = document.getElementById('chartRadar');
    if (ctxRadar) {
      new Chart(ctxRadar, {
        type: 'radar',
        data: {
          labels: ['الحوسبة السحابية', 'أنظمة ERP', 'الذكاء الاصطناعي', 'الأمان والتوافق', 'كفاءة التكلفة'],
          datasets: [{
            label: 'مؤشر CoreSync',
            data: [99, 96, 94, 98, 95],
            backgroundColor: 'rgba(197, 168, 128, 0.25)',
            borderColor: '#c5a880',
            pointBackgroundColor: '#f3dfba'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#ffffff', font: { size: 10 } } } },
          scales: {
            r: {
              grid: { color: 'rgba(255,255,255,0.1)' },
              ticks: { display: false },
              pointLabels: { color: '#ffffff', font: { size: 9 } }
            }
          }
        }
      });
    }

    // 3. ROI Line Chart
    const ctxROI = document.getElementById('chartROI');
    if (ctxROI) {
      new Chart(ctxROI, {
        type: 'line',
        data: {
          labels: ['شهر 1', 'شهر 6', 'شهر 12', 'شهر 18', 'شهر 24', 'شهر 30', 'شهر 36'],
          datasets: [{
            label: 'الوفر المالي التراكمي المحقق (€)',
            data: [2500, 18000, 45000, 78000, 115000, 152000, 194000],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: '#34d399'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#ffffff', font: { size: 10 } } } },
          scales: {
            x: { ticks: { color: '#cccccc' }, grid: { color: 'rgba(255,255,255,0.06)' } },
            y: { ticks: { color: '#cccccc' }, grid: { color: 'rgba(255,255,255,0.06)' } }
          }
        }
      });
    }

    // Auto print prompt after charts render
    setTimeout(() => {
      window.print();
    }, 1200);
  });
<\/script>
</body>
</html>`;

        const win = window.open('', '_blank');
        if (win) {
            win.document.write(deck);
            win.document.close();
        }
    };

    /* =====================================================================
       Inject new feature modals into initEnterpriseSuite
       ===================================================================== */
    const _origInit = initEnterpriseSuite;
    function initEnterpriseSuiteExtended() {
        _origInit();
        injectAIConcierge();
        injectTrackerModal();
        injectROIOptimizer();
        injectNextGenButtons();
        injectServicesComparisonModal();
        init3DCardTilt();
    }

    /* =====================================================================
       Services 3D Tilt Effect & Comparison Modal
       ===================================================================== */
    function init3DCardTilt() {
        const cards = document.querySelectorAll('.dana-signature-card');
        cards.forEach(card => {
            card.addEventListener('mousemove', function(e) {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                card.style.transform = `perspective(1000px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) translateY(-8px) scale(1.015)`;
            });
            card.addEventListener('mouseleave', function() {
                card.style.transform = '';
            });
        });
    }

    function injectServicesComparisonModal() {
        if (document.getElementById('servicesComparisonModal')) return;
        const modal = document.createElement('div');
        modal.id = 'servicesComparisonModal';
        modal.className = 'es-modal-overlay';
        modal.style.display = 'none';
        modal.innerHTML = `
            <div class="es-modal-inner" style="max-width:960px;" role="dialog" aria-label="مقارنة باقات الخدمات">
                <div class="es-modal-header">
                    <div class="es-modal-header-left">
                        <span class="es-modal-tag">مقارنة معتمدة • 2026</span>
                        <h3 class="es-modal-title">مقارنة ميزات باقات الاستوديو والأنظمة المؤسسية</h3>
                    </div>
                    <button class="es-modal-close" onclick="window.closeServicesComparisonModal()" aria-label="إغلاق">&times;</button>
                </div>
                <div class="es-modal-body" style="overflow-x:auto;">
                    
                    <!-- شريط الإجراءات: اسم العميل وتصدير PDF -->
                    <div class="es-compare-actions-bar">
                        <div class="es-client-name-wrap">
                            <span style="font-size:0.85rem; color:#c5a880; font-weight:700;">🏢 المنشأة / العميل:</span>
                            <input type="text" id="esCompareClientName" class="es-client-input" placeholder="أدخل اسم شركتكم لإدراجه بالتقرير (اختياري)">
                        </div>
                        <button type="button" class="es-compare-pdf-btn" onclick="window.exportComparisonPDF()">
                            <span>📄 تصدير جدول المقارنة PDF</span>
                        </button>
                    </div>

                    <table class="es-compare-table" id="esComparisonTableMain">
                        <thead>
                            <tr>
                                <th>الميزة والقدرة التقنية</th>
                                <th>الهوية البصرية<br><span style="color:#c5a880; font-size:0.9rem;" data-eur-price="590" class="base-col-price">€590</span></th>
                                <th>تصميم المواقع<br><span style="color:#c5a880; font-size:0.9rem;" data-eur-price="980" class="base-col-price">€980</span></th>
                                <th>متجر إلكتروني + ERP<br><span style="color:#c5a880; font-size:0.9rem;" data-eur-price="1450" class="base-col-price">€1,450</span></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>مدة التنفيذ والتسليم المعتمدة</td>
                                <td>5 - 7 أيام عمل</td>
                                <td>10 - 14 يوم عمل</td>
                                <td>14 - 20 يوم عمل</td>
                            </tr>
                            <tr>
                                <td>دليل العلامة والهوية الكامل (Brand Guidelines)</td>
                                <td><span class="es-compare-check">✓</span> متكامل 100%</td>
                                <td><span class="es-compare-check">✓</span> تضمين الشعار والخطوط</td>
                                <td><span class="es-compare-check">✓</span> نظام هوية رقمي كامل</td>
                            </tr>
                            <tr>
                                <td>واجهات UI/UX حصرية متوافقة مع جميع الشاشات</td>
                                <td><span class="es-compare-dash">—</span></td>
                                <td><span class="es-compare-check">✓</span> فائق السرعة والأداء</td>
                                <td><span class="es-compare-check">✓</span> تجربة تسوق محسنة للتحويل</td>
                            </tr>
                            <tr>
                                <td>بوابات الدفع الأوروبية (iDEAL, Stripe, Mollie, Apple Pay)</td>
                                <td><span class="es-compare-dash">—</span></td>
                                <td>اختياري</td>
                                <td><span class="es-compare-check">✓</span> ربط مباشر متوافق مع PSD2</td>
                            </tr>
                            <tr>
                                <td>المزامنة السحابية مع دفاتر المحاسبة والـ ERP</td>
                                <td><span class="es-compare-dash">—</span></td>
                                <td><span class="es-compare-dash">—</span></td>
                                <td><span class="es-compare-check">✓</span> فواتير وضريبة BTW/VAT لحظية</td>
                            </tr>
                            <tr>
                                <td>تحسين محركات البحث وسرعة التحميل (SEO & Speed)</td>
                                <td>تصدير بصيغ ويب حديثة (SVG/WebP)</td>
                                <td><span class="es-compare-check">✓</span> PageSpeed 95+ و Schema.org</td>
                                <td><span class="es-compare-check">✓</span> SEO احترافي للمنتجات والتصنيفات</td>
                            </tr>
                            <tr>
                                <td>الدعم الفني وضمان ما بعد الإطلاق</td>
                                <td>30 يوماً</td>
                                <td>60 يوماً</td>
                                <td>90 يوماً شامل التحديثات</td>
                            </tr>
                            <tr class="es-live-total-row">
                                <td>الإجمالي المعتمد (مع الإضافات المختارة)</td>
                                <td id="esTotalCol1" style="color:#f3dfba; font-weight:800;">€590</td>
                                <td id="esTotalCol2" style="color:#f3dfba; font-weight:800;">€980</td>
                                <td id="esTotalCol3" style="color:#f3dfba; font-weight:800;">€1,450</td>
                            </tr>
                            <tr>
                                <td>الإجراء المباشر</td>
                                <td><button type="button" class="dana-btn-booking" style="width:100%;" onclick="window.closeServicesComparisonModal(); openExecutiveBookingModal('identity')">حجز استشارة 📅</button></td>
                                <td><button type="button" class="dana-btn-booking" style="width:100%;" onclick="window.closeServicesComparisonModal(); openExecutiveBookingModal('web')">حجز استشارة 📅</button></td>
                                <td><button type="button" class="dana-btn-booking" style="width:100%;" onclick="window.closeServicesComparisonModal(); openExecutiveBookingModal('store')">حجز استشارة 📅</button></td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- حاسبة الإضافات التكميلية السريعة (Package Add-ons Selector) -->
                    <div class="es-addons-box">
                        <div class="es-addons-title">
                            <span>⚡ حاسبة الإضافات السريعة (Optional Enterprise Add-ons):</span>
                            <span style="font-size:0.75rem; color:rgba(255,255,255,0.6); font-weight:normal;">اختر ما يناسبك لتحديث التكلفة الإجمالية لحظياً</span>
                        </div>
                        <div class="es-addons-grid">
                            <label class="es-addon-item">
                                <input type="checkbox" class="es-addon-check" data-addon-price="150" onchange="window.recalcComparisonAddons()">
                                <span>🌐 لغة إضافية للموقع (+€150)</span>
                            </label>
                            <label class="es-addon-item">
                                <input type="checkbox" class="es-addon-check" data-addon-price="120" onchange="window.recalcComparisonAddons()">
                                <span>💳 بوابة دفع إضافية (+€120)</span>
                            </label>
                            <label class="es-addon-item">
                                <input type="checkbox" class="es-addon-check" data-addon-price="350" onchange="window.recalcComparisonAddons()">
                                <span>🤖 شات بوت ذكاء اصطناعي RAG (+€350)</span>
                            </label>
                            <label class="es-addon-item">
                                <input type="checkbox" class="es-addon-check" data-addon-price="180" onchange="window.recalcComparisonAddons()">
                                <span>🛡️ دعم فني VIP وحماية سنوية (+€180)</span>
                            </label>
                        </div>
                    </div>

                </div>
            </div>
        `;
        document.body.appendChild(modal);

        modal.addEventListener('click', function(e) {
            if (e.target === modal) window.closeServicesComparisonModal();
        });
    }

    window.recalcComparisonAddons = function() {
        let addonTotalEur = 0;
        document.querySelectorAll('.es-addon-check:checked').forEach(chk => {
            addonTotalEur += parseFloat(chk.dataset.addonPrice || 0);
        });

        const cur = CURRENCIES[activeCurrency] || CURRENCIES.EUR;
        const basePrices = [590, 980, 1450];
        const targetIds = ['esTotalCol1', 'esTotalCol2', 'esTotalCol3'];

        targetIds.forEach((id, idx) => {
            const el = document.getElementById(id);
            if (!el) return;
            const totalEur = basePrices[idx] + addonTotalEur;
            const converted = Math.round(totalEur * cur.rate);
            const formatted = converted.toLocaleString('en-US');

            if (activeCurrency === 'SAR' || activeCurrency === 'AED') {
                el.textContent = `${formatted} ${cur.symbol}`;
            } else {
                el.textContent = `${cur.symbol}${formatted}`;
            }
        });
    };

    window.exportComparisonPDF = function() {
        const clientName = (document.getElementById('esCompareClientName') ? document.getElementById('esCompareClientName').value.trim() : '') || 'العميل الموقر (Executive Client)';
        const cur = CURRENCIES[activeCurrency] || CURRENCIES.EUR;
        
        let addonTotalEur = 0;
        const selectedAddons = [];
        document.querySelectorAll('.es-addon-check:checked').forEach(chk => {
            addonTotalEur += parseFloat(chk.dataset.addonPrice || 0);
            selectedAddons.push(chk.parentElement.textContent.trim());
        });

        const printWindow = window.open('', '_blank');
        if (!printWindow) {
            alert('يرجى السماح بالنوافذ المنبثقة لطباعة وثيقة المقارنة الرسمية');
            return;
        }

        const dateStr = new Date().toLocaleDateString('ar-EG', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

        printWindow.document.write(`
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>وثيقة مقارنة الباقات الرسمية - S&R CoreSync Solutions</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 35px; color: #111; line-height: 1.6; }
                    .header { border-bottom: 2px solid #c5a880; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; }
                    .logo { font-size: 22px; font-weight: 800; color: #0a0e0c; }
                    .meta { font-size: 13px; color: #666; text-align: left; }
                    .dossier-tag { display: inline-block; background: #f4ecdf; color: #8e6d3e; padding: 4px 12px; border-radius: 6px; font-weight: bold; font-size: 13px; margin-bottom: 8px; }
                    h2 { margin: 0 0 5px 0; color: #0a0e0c; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 13px; }
                    th, td { border: 1px solid #ddd; padding: 10px 12px; text-align: center; }
                    th { background-color: #fcf9f5; color: #333; }
                    th:first-child, td:first-child { text-align: right; font-weight: 600; width: 35%; }
                    .check { color: #2e7d32; font-weight: bold; }
                    .addons-summary { margin-top: 25px; padding: 15px; background: #fafafa; border: 1px solid #eee; border-radius: 8px; }
                    .footer { margin-top: 40px; border-top: 1px solid #eee; padding-top: 15px; font-size: 12px; color: #777; display: flex; justify-content: space-between; }
                    @media print { body { padding: 0; } }
                </style>
            </head>
            <body>
                <div class="header">
                    <div>
                        <div class="logo">S&R CoreSync Solutions B.V.</div>
                        <div style="font-size:12px; color:#555;">The Netherlands • Enterprise Cloud & Financial AI</div>
                    </div>
                    <div class="meta">
                        <div>التاريخ: ${dateStr}</div>
                        <div>العملة: ${cur.name} (${cur.symbol})</div>
                        <div>الضريبة: ${cur.vatName}</div>
                    </div>
                </div>

                <div class="dossier-tag">وثيقة مقارنة واعتماد العرض التنفيذي</div>
                <h2>مقارنة باقات استوديو الهوية الرقمية والأنظمة المؤسسية</h2>
                <p>مُعدة خصيصاً إلى: <strong>${clientName}</strong></p>

                <table>
                    <thead>
                        <tr>
                            <th>الميزة والقدرة التقنية</th>
                            <th>الهوية البصرية<br>${Math.round(590 * cur.rate)} ${cur.symbol}</th>
                            <th>تصميم المواقع<br>${Math.round(980 * cur.rate)} ${cur.symbol}</th>
                            <th>متجر إلكتروني + ERP<br>${Math.round(1450 * cur.rate)} ${cur.symbol}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>مدة التنفيذ المعتمدة</td><td>5 - 7 أيام عمل</td><td>10 - 14 يوم عمل</td><td>14 - 20 يوم عمل</td></tr>
                        <tr><td>دليل العلامة والهوية الكامل</td><td>✓ متكامل 100%</td><td>✓ الشعار والخطوط</td><td>✓ نظام هوية رقمي شامل</td></tr>
                        <tr><td>واجهات UI/UX حصرية</td><td>—</td><td>✓ فائق السرعة والأداء</td><td>✓ تجربة تسوق محسنة</td></tr>
                        <tr><td>بوابات الدفع الأوروبية (PSD2)</td><td>—</td><td>اختياري</td><td>✓ iDEAL, Stripe, Apple Pay</td></tr>
                        <tr><td>الربط المحاسبي مع الـ ERP والضرائب</td><td>—</td><td>—</td><td>✓ فواتير وضريبة BTW/VAT</td></tr>
                        <tr><td>تحسين محركات البحث SEO والأداء</td><td>صيغ حديثة SVG/WebP</td><td>✓ PageSpeed 95+</td><td>✓ SEO للمنتجات والتصنيفات</td></tr>
                        <tr><td>الدعم الفني والضمان المعتمد</td><td>30 يوماً</td><td>60 يوماً</td><td>90 يوماً شامل التحديثات</td></tr>
                        <tr style="background:#f4ecdf; font-weight:bold;">
                            <td>الإجمالي النهائي المعتمد</td>
                            <td>${Math.round((590 + addonTotalEur) * cur.rate)} ${cur.symbol}</td>
                            <td>${Math.round((980 + addonTotalEur) * cur.rate)} ${cur.symbol}</td>
                            <td>${Math.round((1450 + addonTotalEur) * cur.rate)} ${cur.symbol}</td>
                        </tr>
                    </tbody>
                </table>

                ${selectedAddons.length > 0 ? `
                <div class="addons-summary">
                    <strong>الإضافات والترقيات التكميلية المختارة:</strong>
                    <ul style="margin:5px 0 0 0; padding-right:20px;">
                        ${selectedAddons.map(a => `<li>${a}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}

                <div class="footer">
                    <div>S&R CoreSync Solutions — www.coresync.nl • info@coresync.nl • +31 6 87764998</div>
                    <div>اعتماد رسمي معفى من التوقيع اليدوي</div>
                </div>

                <script>
                    window.onload = function() { window.print(); };
                <\/script>
            </body>
            </html>
        `);
        printWindow.document.close();
    };

    window.openServicesComparisonModal = function() {
        injectServicesComparisonModal();
        const m = document.getElementById('servicesComparisonModal');
        if (m) {
            m.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            if (window.switchCurrency && activeCurrency) {
                window.switchCurrency(activeCurrency);
            }
            window.recalcComparisonAddons();
        }
    };

    window.closeServicesComparisonModal = function() {
        const m = document.getElementById('servicesComparisonModal');
        if (m) {
            m.style.display = 'none';
            document.body.style.overflow = '';
        }
    };

    function injectNextGenButtons() {
        // Inject Tracker button inside the Feedback Hub header if it exists
        const hubHeader = document.querySelector('.es-hub-header');
        if (hubHeader && !document.getElementById('esHubTrackerBtn')) {
            const btn = document.createElement('button');
            btn.id = 'esHubTrackerBtn';
            btn.className = 'btn-tracker-portal';
            btn.innerHTML = '📡 بوابة العملاء وتتبع المشاريع';
            btn.onclick = window.openTrackerModal;
            hubHeader.appendChild(btn);
        }

        // Inject ROI Optimizer button next to Case Studies if present
        const caseStudySec = document.querySelector('.es-case-studies-section');
        if (caseStudySec && !document.getElementById('esRoiOptBtn')) {
            const btn = document.createElement('button');
            btn.id = 'esRoiOptBtn';
            btn.className = 'es-btn-secondary';
            btn.style.margin = '10px 0';
            btn.innerHTML = '🚀 محاكي التكلفة السحابية وROI';
            btn.onclick = window.openROIModal;
            caseStudySec.prepend(btn);
        }

        // Inject Executive Deck Download button
        const heroActions = document.querySelector('.banner-hero-content .box-btn, .banner-hero .box-btn');
        if (heroActions && !document.getElementById('esExecutiveDeckBtn')) {
            const btn = document.createElement('button');
            btn.id = 'esExecutiveDeckBtn';
            btn.className = 'es-deck-download-btn';
            btn.innerHTML = '<span>📊 تحميل ملف القدرات التنفيذي PDF</span>';
            btn.onclick = window.downloadCapabilityDeck;
            heroActions.appendChild(btn);
        }
    }

    // Card activation toggle
    window.toggleDanaCardActive = function (cardEl) {
        if (!cardEl) return;
        const allCards = document.querySelectorAll('.dana-signature-card');
        const wasActive = cardEl.classList.contains('is-active');
        allCards.forEach(function (c) { c.classList.remove('is-active'); });
        if (!wasActive) {
            cardEl.classList.add('is-active');
        }
    };

    // Override init with extended version
    window.initEnterpriseSuite = initEnterpriseSuiteExtended;

    // Auto-bootstrap
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEnterpriseSuiteExtended);
    } else {
        initEnterpriseSuiteExtended();
    }
})();
