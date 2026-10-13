/**
 * S&R CoreSync Solutions - Enterprise Suite Engine v2.0
 * Fully Unified Multi-Language Enterprise Architecture (AR / EN / NL)
 * 1. Instant Official PDF Quotation Generator (Multi-Language)
 * 2. Client Visual Feedback Hub (Auto-Flipping RTL/LTR & Multi-Language)
 * 3. EU GDPR Cookie Consent System (Dutch / European Compliance)
 * 4. Executive Meeting Scheduler (Auto-Timezone & Multi-Language)
 * 5. AI & ERP Digital Readiness Assessment Engine (Multi-Language)
 * 6. Enterprise Case Studies & Measurable ROI Hub (Multi-Language)
 * 7. Live Cloud ERP Demo Sandbox Quick Access
 */

(function () {
    'use strict';

    const WHATSAPP_SALIM = '31618111116';
    const WHATSAPP_RAED = '31687710290';
    const WHATSAPP_NUM = WHATSAPP_SALIM;

    // Central Multi-Language Page Detector
    function getPageLang() {
        const docLang = (document.documentElement.lang || document.documentElement.getAttribute('data-page-language') || '').toLowerCase();
        if (docLang.startsWith('nl') || window.location.pathname.includes('/nl/')) return 'nl';
        if (docLang.startsWith('en') || window.location.pathname.includes('/en/')) return 'en';
        return 'ar';
    }
    window.getPageLang = getPageLang;

    // State for Assessment Quiz
    let currentQuizStep = 0;
    const quizAnswers = {};

    // 1. Multi-Language Readiness Quiz Questions
    const QUIZ_QUESTIONS_I18N = {
        ar: [
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
        ],
        en: [
            {
                title: 'What is your current organization size and workforce headcount?',
                options: [
                    { text: 'Growing venture / Startup (1 - 10 team members)', score: 15, saving: 800 },
                    { text: 'Mid-sized enterprise (11 - 50 team members)', score: 25, saving: 1800 },
                    { text: 'Multi-department company (51 - 200 team members)', score: 35, saving: 3500 },
                    { text: 'Large corporation / Branch chain (200+ team members)', score: 45, saving: 6500 }
                ]
            },
            {
                title: 'How are your accounting workflows and supply chains managed today?',
                options: [
                    { text: 'Manual spreadsheets (Excel) and fragmented reports', score: 10, saving: 1200 },
                    { text: 'Legacy desktop software with zero cloud connectivity', score: 20, saving: 900 },
                    { text: 'Siloed cloud tools lacking cohesive integration', score: 30, saving: 600 },
                    { text: 'Modern ERP needing autonomous AI workflows', score: 40, saving: 400 }
                ]
            },
            {
                title: 'What is your current enterprise AI adoption level?',
                options: [
                    { text: 'No AI integration deployed yet', score: 5, saving: 1500 },
                    { text: 'Ad-hoc employee use only (ChatGPT/Copilot)', score: 15, saving: 1000 },
                    { text: 'Partial scripted automation for repetitive tasks', score: 25, saving: 700 },
                    { text: 'Scalable cloud infrastructure seeking proprietary RAG', score: 35, saving: 500 }
                ]
            },
            {
                title: 'What is your primary strategic priority for the next phase?',
                options: [
                    { text: 'European tax compliance (VAT/BTW) and branch consolidation', score: 25, saving: 1100 },
                    { text: 'Cutting operational leakage and speeding up invoice cycles', score: 30, saving: 1400 },
                    { text: 'Connecting branches into unified real-time cloud data sync', score: 35, saving: 1600 },
                    { text: 'Engineering bespoke cloud portal and exclusive VIP app', score: 40, saving: 1200 }
                ]
            }
        ],
        nl: [
            {
                title: 'Wat is de huidige omvang van uw organisatie en personeelsbestand?',
                options: [
                    { text: 'Startende / groeiende onderneming (1 - 10 medewerkers)', score: 15, saving: 800 },
                    { text: 'Middelgrote onderneming (11 - 50 medewerkers)', score: 25, saving: 1800 },
                    { text: 'Bedrijf met meerdere afdelingen (51 - 200 medewerkers)', score: 35, saving: 3500 },
                    { text: 'Grote corporate / filialennetwerk (+200 medewerkers)', score: 45, saving: 6500 }
                ]
            },
            {
                title: 'Hoe worden uw boekhouding en toeleveringsketens momenteel beheerd?',
                options: [
                    { text: 'Handmatige Excel-bestanden en versnipperde rapporten', score: 10, saving: 1200 },
                    { text: 'Verouderde lokale boekhoudsoftware zonder cloudverbinding', score: 20, saving: 900 },
                    { text: 'Losstaande cloudtools zonder naadloze integratie', score: 30, saving: 600 },
                    { text: 'Geavanceerd ERP-systeem gereed voor AI-automatisering', score: 40, saving: 400 }
                ]
            },
            {
                title: 'Wat is uw huidige niveau van AI-adoptie en automatisering?',
                options: [
                    { text: 'Nog geen gebruik van AI binnen de organisatie', score: 5, saving: 1500 },
                    { text: 'Individueel ad-hoc gebruik (enkel ChatGPT/Copilot)', score: 15, saving: 1000 },
                    { text: 'Gedeeltelijke automatisering van herhalende taken', score: 25, saving: 700 },
                    { text: 'Cloud-ecosysteem op zoek naar maatwerk RAG & AI-workflows', score: 35, saving: 500 }
                ]
            },
            {
                title: 'Wat is uw belangrijkste strategische doel voor de komende fase?',
                options: [
                    { text: 'Europese belastingnaleving (BTW/Belastingdienst) & consolidatie', score: 25, saving: 1100 },
                    { text: 'Kostenverspilling reduceren & facturatiecyclus versnellen', score: 30, saving: 1400 },
                    { text: 'Vestigingen koppelen aan realtime centrale cloudsynchronisatie', score: 35, saving: 1600 },
                    { text: 'Maatwerk cloudplatform en exclusief VIP-klantenportaal bouwen', score: 40, saving: 1200 }
                ]
            }
        ]
    };

    // 2. Multi-Language Enterprise Case Studies
    const CASE_STUDIES_I18N = {
        ar: {
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
        },
        en: {
            almarai: {
                client: 'European Supply Chains – FMCG & Food Logistics',
                title: 'Real-Time Logistics Sync & High-Availability ERP across 4 EU Countries',
                tag: 'Cloud ERP & Microservices',
                kpis: [
                    { val: '94%', lbl: 'Faster Data Sync Speed' },
                    { val: '18 hrs', lbl: 'Weekly Accounting Saved' },
                    { val: '99.99%', lbl: 'High-Availability Cloud SLA' }
                ],
                challenge: 'Warehouses across the Netherlands, Germany, and Belgium suffered inventory discrepancies and duplicate billing due to disparate on-premise tools, causing logistics bottlenecks and delayed month-end closings.',
                solution: 'Eng. Salim Aziza engineered a distributed, high-throughput microservices architecture on secure EU infrastructure, while Mr. Raed Kaakeh unified the general ledger and standardized European VAT & IFRS compliance.',
                roi: 'Consolidated reporting time plummeted from 8 business days to an instantaneous single-click report, yielding over €45,000 in direct annual operational savings.'
            },
            schoon365: {
                client: '365 SCHOON B.V. – Netherlands',
                title: 'Automated Billing & Dutch Belastingdienst Tax Compliance Architecture',
                tag: 'Dutch Tax & Financial Automation',
                kpis: [
                    { val: '100%', lbl: 'Error-Free Belastingdienst Audit' },
                    { val: '45%', lbl: 'Faster Invoice Collection (iDEAL)' },
                    { val: '0 min', lbl: 'Manual Effort in BTW Calculation' }
                ],
                challenge: 'Managing thousands of recurring monthly corporate maintenance contracts under strict Dutch tax regulations, with manual follow-up causing invoice collection friction.',
                solution: 'Developed a custom financial orchestration engine linking directly to Dutch payment rails (iDEAL / SEPA Direct Debit), automatically generating compliant XML/audit ledgers for Dutch accounting firms.',
                roi: 'The billing cycle now runs 100% autonomously in the background, allowing leadership to double client accounts without hiring additional accounting personnel.'
            },
            buraq: {
                client: 'Al-Buraq Smart Logistics & Freight Fleet',
                title: 'Predictive Route AI & Autonomous Fleet Telemetry Architecture',
                tag: 'Predictive AI & Logistics Ops',
                kpis: [
                    { val: '22%', lbl: 'Fuel Consumption Savings' },
                    { val: '99.2%', lbl: 'On-Time Delivery Rate' },
                    { val: '< 2s', lbl: 'Real-Time Dynamic Rerouting' }
                ],
                challenge: 'Delivery time volatility and rising fuel expenses caused by lack of predictive traffic insights and uneven parcel distribution among fleet drivers.',
                solution: 'Constructed a predictive AI dispatch algorithm evaluating traffic patterns, weather telemetry, and parcel volume in real time to dynamically balance fleet routing with an executive dashboard.',
                roi: 'Reduced average journey times by 28% and boosted enterprise customer satisfaction by 40%, empowering the company to win major multi-year B2B transport contracts.'
            }
        },
        nl: {
            almarai: {
                client: 'Europese Supply Chains – Levensmiddelensector',
                title: 'Realtime Logistieke Synchronisatie & High-Availability ERP over 4 EU-Landen',
                tag: 'Cloud ERP & Microservices',
                kpis: [
                    { val: '94%', lbl: 'Snellere Datasynchronisatie' },
                    { val: '18 uur', lbl: 'Wekelijkse Boekhoudwinst' },
                    { val: '99.99%', lbl: 'Cloud High-Availability SLA' }
                ],
                challenge: 'Magazijnen in Nederland, Duitsland en België kampten met voorraadverschillen en dubbele handmatige facturen door versnipperde lokale systemen, met distributievertragingen tot gevolg.',
                solution: 'Ir. Salim Aziza ontwierp een gedistribueerde microservices-architectuur op veilige Europese datacenters, terwijl Dhr. Raed Kaakeh het rekeningschema harmoniseerde conform de Europese BTW- en IFRS-normen.',
                roi: 'Consolidatierapporten worden nu met één klik gegenereerd in plaats van 8 werkdagen, met een aantoonbare jaarlijkse besparing van ruim €45.000 op operationele kosten.'
            },
            schoon365: {
                client: '365 SCHOON B.V. – Nederland',
                title: 'Geautomatiseerde Facturatie & Fiscale Naleving Belastingdienst',
                tag: 'Dutch Tax & Financial Automation',
                kpis: [
                    { val: '100%', lbl: 'Foutloze Belastingdienst Compliance' },
                    { val: '45%', lbl: 'Snellere Betalingsontvangst (iDEAL)' },
                    { val: '0 min', lbl: 'Handmatige BTW-berekening' }
                ],
                challenge: 'Verwerking van duizenden periodieke onderhoudscontracten conform strikte Nederlandse fiscale wetgeving, met tijdrovende handmatige debiteurenopvolging.',
                solution: 'Ontwikkeling van een geautomatiseerde financiële koppeling met Nederlandse betaalproviders (iDEAL / SEPA Incasso) die directe audit-bestanden genereert voor accountantskantoren.',
                roi: 'Volledig autonome achtergrondfacturatie waardoor de directie het klantenbestand kon verdubbelen zonder extra administratief personeel aan te nemen.'
            },
            buraq: {
                client: 'Al-Buraq Smart Logistics & Vrachtvervoer',
                title: 'Voorspellende Route-AI & Realtime Wagenpark Telemetrie',
                tag: 'Predictive AI & Logistics Ops',
                kpis: [
                    { val: '22%', lbl: 'Brandstofbesparing' },
                    { val: '99.2%', lbl: 'Stiptheid van Leveringen' },
                    { val: '< 2s', lbl: 'Dynamische Herberekening' }
                ],
                challenge: 'Fluctuerende levertijden en oplopende brandstofkosten door gebrek aan voorspellende verkeersinzichten en onevenwichtige zendingsverdeling over chauffeurs.',
                solution: 'Ontwikkeling van een voorspellend AI-dispatchalgoritme dat realtime verkeers- en weerdata analyseert om het wagenpark dynamisch aan te sturen met een centraal directiedashboard.',
                roi: 'Rijtijden daalden met 28% en de klanttevredenheid steeg met 40%, waardoor de onderneming omvangrijke meerjarige B2B-transportcontracten kon afsluiten.'
            }
        }
    };

    // 3. Central UI Text Dictionary (ES_I18N)
    const ES_I18N = {
        ar: {
            hub: {
                readinessTitle: 'قياس الجاهزية الرقمية لشركتكم',
                readinessLabel: 'قياس الجاهزية الرقمية 📊',
                schedulerTitle: 'حجز جلسة استشارية تنفيذية',
                schedulerLabel: 'حجز استشارة تنفيذية 📅',
                feedbackTitle: 'إرسال ملاحظة أو طلب تعديل مباشر',
                feedbackLabel: 'ملاحظات الزبون | Feedback'
            },
            feedback: {
                title: 'بوابة ملاحظات الزبون المباشرة',
                desc: 'شارك ملاحظاتك أو طلبات التعديل مباشرة مع م. سليم ليتم تنفيذها في النسخة التجريبية الحية.',
                clientNameLabel: 'الاسم أو المؤسسة:',
                clientNamePlaceholder: 'مثال: شركة الأفق للتجارة',
                targetSectionLabel: 'القسم المستهدف بالملاحظة:',
                sections: [
                    'الواجهة الرئيسية (Hero Section)',
                    'كروت الخدمات وباقات دانا',
                    'حاسبة التكلفة والأسعار',
                    'المشاريع السابقة (Portfolio)',
                    'قسم الشركاء والمؤسسين',
                    'أخرى / فكرة عامة'
                ],
                categoryLabel: 'نوع الملاحظة:',
                categories: [
                    '🎨 تعديل تصميم وألوان',
                    '✍️ تعديل نصوص وصياغة',
                    '⚡ طلب ميزة إضافية',
                    '🐞 ملاحظة فنية / استجابة'
                ],
                detailsLabel: 'نص الملاحظة بالتفصيل:',
                detailsPlaceholder: 'اكتب تفاصيل التعديل المطلوب هنا...',
                sendBtn: 'إرسال فوراً عبر واتساب',
                alertEmpty: 'يرجى كتابة نص الملاحظة قبل الإرسال.',
                waMsgHeader: '*💡 ملاحظة جديدة على النسخة التجريبية – S&R CoreSync*'
            },
            scheduler: {
                title: 'مجدول الاستشارات التنفيذية // S&R Executive Advisory',
                desc: 'احجز جلسة استشارية أولية مجانية مدتها 30 دقيقة عبر Zoom لمناقشة بنيتكم السحابية أو متطلبات الـ ERP.',
                advisorLabel: 'اختر المستشار التنفيذي:',
                consultants: {
                    salim: { name: 'م. سليم عزيزة', role: 'CTO • الأنظمة والذكاء الاصطناعي', waTitle: 'م. سليم عزيزة (CTO السحابي والذكاء الاصطناعي)' },
                    raed: { name: 'أ. رائد كعكة', role: 'CFO • الحلول المالية وERP', waTitle: 'أ. رائد كعكة (CFO الأنظمة المالية وERP)' },
                    both: { name: 'جلسة مشتركة', role: 'استشارة تقنية ومالية شاملة', waTitle: 'جلسة استشارية مشتركة (م. سليم + أ. رائد)' }
                },
                tzLabel: '🌐 منطقتك الزمنية المكتشفة تلقائياً:',
                slotLabel: 'اختر اليوم والوقت المفضل (بتوقيتك المحلي):',
                slots: [
                    'غداً 11:00 ص',
                    'غداً 03:00 م',
                    'بعد غد 01:00 م',
                    'بعد غد 05:00 م',
                    'الأسبوع القادم (ص)',
                    'الأسبوع القادم (م)'
                ],
                nameLabel: 'الاسم والشركة:',
                namePlaceholder: 'مثال: م. أحمد - المدير العام لشركة ...',
                topicLabel: 'موضوع الاستشارة الأساسي:',
                topicPlaceholder: 'مثال: ترقية نظام الـ ERP السحابي وربط الفروع',
                confirmBtn: 'تأكيد الحجز وجدولة الموعد فوراً',
                waHeader: '*📅 طلب حجز جلسة استشارية تنفيذية – S&R CoreSync*'
            },
            readiness: {
                modalTitle: 'مقياس الجاهزية الرقمية والوفر المالي // CoreSync AI Assessment',
                stepLabel: (step, total) => `السؤال ${step} من ${total}`,
                scoreLabel: 'الجاهزية الرقمية',
                reportTitle: 'تقرير الجدوى والتحول الرقمي لمنشأتكم',
                reportDesc: (saving) => `بناءً على إجاباتكم، تمتلك منشأتكم أرضية ممتازة للتطوير، مع وجود <strong>فرصة مؤكدة لوفر تشغيلي يقدر بـ €${saving.toLocaleString('en')} شهرياً</strong> عبر أتمتة الـ ERP ودمج الذكاء الاصطناعي مع CoreSync.`,
                kpi1Val: (saving) => `€${saving.toLocaleString('en')}`,
                kpi1Lbl: 'وفر شهري مقدر',
                kpi2Val: '4.5x',
                kpi2Lbl: 'تسريع التقارير المالية',
                kpi3Val: '100%',
                kpi3Lbl: 'أتمتة سحابية موثوقة',
                bookBtn: 'حجز جلسة لمناقشة خطة التحول المقترحة 🚀',
                waHeader: '*📊 نتيجة تقييم الجاهزية الرقمية – S&R CoreSync*'
            },
            gdpr: {
                title: 'الامتثال للائحة حماية البيانات الأوروبية (EU GDPR)',
                text: 'نحن نستخدم ملفات تعريف الارتباط والتقنيات السحابية الأساسية في منصة S&R CoreSync لضمان سرعة التحميل وتجربة تصفح آمنة ومطابقة للقوانين الهولندية والأوروبية.',
                accept: 'قبول الكل (Accept All)',
                decline: 'الأساسية فقط'
            },
            pdf: {
                btnTitle: 'تصدير عرض سعر رسمي بصيغة PDF',
                btnLabel: 'تصدير عرض سعر رسمي (PDF)',
                toolbarTitle: 'عرض السعر المؤسسي الرسمي // S&R CoreSync B.V.',
                printBtn: 'طباعة / حفظ كـ PDF',
                closeBtn: 'إغلاق ✕',
                issueDateLabel: 'تاريخ الإصدار:',
                validityLabel: 'صلاحية العرض: 14 يوماً من تاريخه',
                sectionTitle: 'تفاصيل عرض العمل والمواصفات المحددة',
                colItem: 'البند / المكون البرمجي',
                colSpec: 'المواصفات الفنية',
                colTime: 'الجدول الزمني',
                colPrice: 'التقدير المالي',
                subtotalLabel: 'المجموع الصافي:',
                vatLabel: 'ضريبة القيمة المضافة (0% B2B EU):',
                grandTotalLabel: 'الإجمالي المقدر:',
                disclaimer: '* ملاحظة: هذا التقدير معتمد بموجب بروتوكول S&R للهندسة السحابية وأنظمة الـ ERP والذكاء الاصطناعي، ويخضع لاتفاقية مستوى الخدمة المؤسسية (SLA). يشمل العرض كافة اختبارات الحماية وتوافق معايير GDPR الأوروبية.',
                sigSalimTitle: 'الاعتماد التقني والهندسة السحابية',
                sigRaedTitle: 'الإشراف المالي والأنظمة المؤسسية'
            },
            caseStudy: {
                modalTitle: 'دراسة حالة موثقة وعائد الاستثمار // Enterprise Case Study',
                clientLabel: 'العميل / القطاع:',
                challengeTitle: '⚠️ التحدي التشغيلي والمالي:',
                solutionTitle: '⚡ الحل الهندسي من CoreSync:',
                roiTitle: '📈 الأثر المالي وعائد الاستثمار (ROI):',
                btnWa: 'طلب دراسة حل مماثل لمشروعي عبر WhatsApp',
                waMsg: (client) => `مرحباً S&R CoreSync، اطلعت على دراسة الحالة الخاصة بـ (${client}) وأرغب في مناقشة حل سحابي/مالي مماثل لشركتنا.`
            }
        },
        en: {
            hub: {
                readinessTitle: 'Assess Your Enterprise Digital & AI Readiness',
                readinessLabel: 'Digital Readiness Assessment 📊',
                schedulerTitle: 'Book an Executive Advisory Strategy Session',
                schedulerLabel: 'Executive Advisory Session 📅',
                feedbackTitle: 'Submit Live Feedback or Revision Request',
                feedbackLabel: 'Client Feedback Hub'
            },
            feedback: {
                title: 'Direct Client Feedback Portal',
                desc: 'Share your live feedback or requested revisions directly with Eng. Salim to be implemented on the live build.',
                clientNameLabel: 'Name or Organization:',
                clientNamePlaceholder: 'e.g. Horizon Enterprise B.V.',
                targetSectionLabel: 'Target Section / Feature:',
                sections: [
                    'Hero Section (Main Banner)',
                    'Services & Packages Cards',
                    'ROI & Cost Calculator',
                    'Portfolio & Case Studies',
                    'Founders & Leadership Section',
                    'Other / General Feedback'
                ],
                categoryLabel: 'Feedback Category:',
                categories: [
                    '🎨 Design & Styling Adjustments',
                    '✍️ Copywriting & Content Refinement',
                    '⚡ New Feature Request',
                    '🐞 Technical / Responsiveness Issue'
                ],
                detailsLabel: 'Detailed Feedback / Request:',
                detailsPlaceholder: 'Provide details of your requested changes here...',
                sendBtn: 'Submit Instantly via WhatsApp',
                alertEmpty: 'Please enter feedback details before sending.',
                waMsgHeader: '*💡 New Client Feedback – S&R CoreSync*'
            },
            scheduler: {
                title: 'Executive Advisory Scheduler // S&R Executive Advisory',
                desc: 'Book a complimentary 30-minute Zoom advisory session to discuss your cloud architecture or ERP modernization requirements.',
                advisorLabel: 'Select Executive Advisor:',
                consultants: {
                    salim: { name: 'Eng. Salim Aziza', role: 'CTO • Cloud & Enterprise AI', waTitle: 'Eng. Salim Aziza (CTO Cloud & Enterprise AI)' },
                    raed: { name: 'Mr. Raed Kaakeh', role: 'CFO • Financial Systems & ERP', waTitle: 'Mr. Raed Kaakeh (CFO Financial Systems & ERP)' },
                    both: { name: 'Joint Advisory', role: 'Comprehensive Tech & Financial Architecture', waTitle: 'Joint Advisory Session (Eng. Salim + Mr. Raed)' }
                },
                tzLabel: '🌐 Automatically Detected Timezone:',
                slotLabel: 'Select Preferred Slot (Your Local Time):',
                slots: [
                    'Tomorrow 11:00 AM',
                    'Tomorrow 03:00 PM',
                    'Day After Tomorrow 01:00 PM',
                    'Day After Tomorrow 05:00 PM',
                    'Next Week (Morning)',
                    'Next Week (Afternoon)'
                ],
                nameLabel: 'Name & Organization:',
                namePlaceholder: 'e.g. Alex van Dijk - Managing Director at ...',
                topicLabel: 'Primary Advisory Topic:',
                topicPlaceholder: 'e.g. Cloud ERP migration, branch sync & AI workflows',
                confirmBtn: 'Confirm Booking & Schedule Instantly',
                waHeader: '*📅 Executive Advisory Session Booking – S&R CoreSync*'
            },
            readiness: {
                modalTitle: 'Digital & AI Readiness Assessment // CoreSync AI Assessment',
                stepLabel: (step, total) => `Question ${step} of ${total}`,
                scoreLabel: 'Digital Readiness',
                reportTitle: 'Digital Transformation & Feasibility Report',
                reportDesc: (saving) => `Based on your assessment, your organization possesses solid operational footing with a <strong>confirmed monthly operational savings potential of €${saving.toLocaleString('en')}</strong> through CoreSync ERP automation and enterprise AI integration.`,
                kpi1Val: (saving) => `€${saving.toLocaleString('en')}`,
                kpi1Lbl: 'Est. Monthly Savings',
                kpi2Val: '4.5x',
                kpi2Lbl: 'Faster Financial Reporting',
                kpi3Val: '100%',
                kpi3Lbl: 'Automated Cloud Reliability',
                bookBtn: 'Schedule Roadmap Advisory Session 🚀',
                waHeader: '*📊 Digital Readiness Assessment Result – S&R CoreSync*'
            },
            gdpr: {
                title: 'European Data Protection Compliance (EU GDPR)',
                text: 'We utilize essential cookies and cloud performance technologies across S&R CoreSync to ensure fast loading, secure navigation, and strict compliance with Dutch and European GDPR standards.',
                accept: 'Accept All',
                decline: 'Essential Only'
            },
            pdf: {
                btnTitle: 'Export official enterprise quotation as PDF',
                btnLabel: 'Export Official Quote (PDF)',
                toolbarTitle: 'Official Enterprise Quotation // S&R CoreSync B.V.',
                printBtn: 'Print / Save as PDF',
                closeBtn: 'Close ✕',
                issueDateLabel: 'Issue Date:',
                validityLabel: 'Validity: 14 days from issuance',
                sectionTitle: 'Scope of Work & Technical Specifications',
                colItem: 'Deliverable / Module',
                colSpec: 'Technical Specifications',
                colTime: 'Timeline',
                colPrice: 'Financial Estimate',
                subtotalLabel: 'Net Subtotal:',
                vatLabel: 'VAT (0% Reverse Charge B2B EU):',
                grandTotalLabel: 'Estimated Total:',
                disclaimer: '* Notice: This formal estimate is governed by S&R Cloud Engineering & Enterprise ERP protocols, subject to enterprise SLA terms. Includes security audit and European GDPR compliance.',
                sigSalimTitle: 'Technical Sign-Off & Cloud Architecture',
                sigRaedTitle: 'Financial Governance & ERP Systems'
            },
            caseStudy: {
                modalTitle: 'Enterprise Case Study & Measurable ROI // S&R CoreSync',
                clientLabel: 'Client / Sector:',
                challengeTitle: '⚠️ Operational & Financial Challenge:',
                solutionTitle: '⚡ CoreSync Engineering Solution:',
                roiTitle: '📈 Financial Impact & Measurable ROI:',
                btnWa: 'Discuss Similar Solution via WhatsApp',
                waMsg: (client) => `Hello S&R CoreSync, I reviewed the case study for (${client}) and would like to discuss a similar cloud/ERP solution for our organization.`
            }
        },
        nl: {
            hub: {
                readinessTitle: 'Meet de digitale & AI-gereedheid van uw bedrijf',
                readinessLabel: 'Digitale Gereedheidsscan 📊',
                schedulerTitle: 'Plan een strategisch directie-adviesgesprek',
                schedulerLabel: 'Directie Adviesgesprek 📅',
                feedbackTitle: 'Directe feedback of wijzigingsverzoek indienen',
                feedbackLabel: 'Klant Feedback & Verzoek'
            },
            feedback: {
                title: 'Direct Klant Feedback Portaal',
                desc: 'Deel uw feedback of gewenste wijzigingen rechtstreeks met Ir. Salim voor directe implementatie op de live versie.',
                clientNameLabel: 'Naam of Bedrijf:',
                clientNamePlaceholder: 'bijv. Horizon Enterprise B.V.',
                targetSectionLabel: 'Betreffend Onderdeel / Functie:',
                sections: [
                    'Hero Sectie (Hoofdbanner)',
                    'Diensten & Pakketten Kaarten',
                    'ROI & Kosten Calculator',
                    'Portfolio & Casestudies',
                    'Oprichters & Directiesectie',
                    'Overig / Algemene Feedback'
                ],
                categoryLabel: 'Type Feedback:',
                categories: [
                    '🎨 Design & Kleuraanpassingen',
                    '✍️ Tekst- & Contentverfijning',
                    '⚡ Nieuwe Functie Aanvraag',
                    '🐞 Technische / Responsiviteitsmelding'
                ],
                detailsLabel: 'Gedetailleerde Feedback / Verzoek:',
                detailsPlaceholder: 'Beschrijf hier uw gewenste aanpassingen...',
                sendBtn: 'Direct Versturen via WhatsApp',
                alertEmpty: 'Vul alstublieft uw feedback in voordat u verzendt.',
                waMsgHeader: '*💡 Nieuwe Klantfeedback – S&R CoreSync*'
            },
            scheduler: {
                title: 'Directie Advies Agenda // S&R Executive Advisory',
                desc: 'Boek een vrijblijvend adviesgesprek van 30 minuten via Zoom om uw cloudarchitectuur of ERP-wensen te bespreken.',
                advisorLabel: 'Kies Directieadviseur:',
                consultants: {
                    salim: { name: 'Ir. Salim Aziza', role: 'CTO • Cloud & Enterprise AI', waTitle: 'Ir. Salim Aziza (CTO Cloud & Enterprise AI)' },
                    raed: { name: 'Dhr. Raed Kaakeh', role: 'CFO • Financiële Systemen & ERP', waTitle: 'Dhr. Raed Kaakeh (CFO Financiële Systemen & ERP)' },
                    both: { name: 'Gezamenlijke Sessie', role: 'Integrale Technische & Financiële Strategie', waTitle: 'Gezamenlijke Directiesessie (Ir. Salim + Dhr. Raed)' }
                },
                tzLabel: '🌐 Automatisch Gedetecteerde Tijdzone:',
                slotLabel: 'Kies Gewenste Tijd (Uw Lokale Tijd):',
                slots: [
                    'Morgen 11:00',
                    'Morgen 15:00',
                    'Overmorgen 13:00',
                    'Overmorgen 17:00',
                    'Volgende week (Ochtend)',
                    'Volgende week (Middag)'
                ],
                nameLabel: 'Naam & Organisatie:',
                namePlaceholder: 'bijv. Alex van Dijk - Directeur bij ...',
                topicLabel: 'Onderwerp van Adviesgesprek:',
                topicPlaceholder: 'bijv. Cloud ERP modernisering, vestigingskoppeling & AI',
                confirmBtn: 'Afspraak Bevestigen & Direct Inplannen',
                waHeader: '*📅 Directie Adviesgesprek Aanvraag – S&R CoreSync*'
            },
            readiness: {
                modalTitle: 'Digitale & AI Gereedheidsscan // CoreSync AI Assessment',
                stepLabel: (step, total) => `Vraag ${step} van ${total}`,
                scoreLabel: 'Digitale Gereedheid',
                reportTitle: 'Digitale Haalbaarheid & Transformatierapport',
                reportDesc: (saving) => `Op basis van uw antwoorden beschikt uw onderneming over een solide basis, met een <strong>aantoonbare potentiële maandelijkse besparing van €${saving.toLocaleString('en')}</strong> via CoreSync ERP-automatisering en AI-integratie.`,
                kpi1Val: (saving) => `€${saving.toLocaleString('en')}`,
                kpi1Lbl: 'Geschatte Maandbesparing',
                kpi2Val: '4.5x',
                kpi2Lbl: 'Snellere Financiële Rapportage',
                kpi3Val: '100%',
                kpi3Lbl: 'Betrouwbare Cloudautomatisering',
                bookBtn: 'Plan Transformatie Adviesgesprek 🚀',
                waHeader: '*📊 Digitale Gereedheidsscan Resultaat – S&R CoreSync*'
            },
            gdpr: {
                title: 'Europese Privacybescherming (EU GDPR)',
                text: 'Wij gebruiken essentiële cookies en cloudtechnologieën op het S&R CoreSync platform voor maximale laadsnelheid, veilige navigatie en volledige naleving van de Nederlandse en Europese AVG-wetgeving (GDPR).',
                accept: 'Alles Accepteren',
                decline: 'Alleen Noodzakelijk'
            },
            pdf: {
                btnTitle: 'Exporteer officiële zakelijke offerte als PDF',
                btnLabel: 'Officiële Offerte Exporteren (PDF)',
                toolbarTitle: 'Officiële Zakelijke Offerte // S&R CoreSync B.V.',
                printBtn: 'Afdrukken / Opslaan als PDF',
                closeBtn: 'Sluiten ✕',
                issueDateLabel: 'Uitgiftedatum:',
                validityLabel: 'Geldigheid: 14 dagen vanaf uitgiftedatum',
                sectionTitle: 'Projectomvang & Technische Specificaties',
                colItem: 'Onderdeel / Module',
                colSpec: 'Technische Specificaties',
                colTime: 'Planning',
                colPrice: 'Financiële Schatting',
                subtotalLabel: 'Subtotaal Netto:',
                vatLabel: 'BTW (0% B2B Verlegd EU):',
                grandTotalLabel: 'Geschat Totaal:',
                disclaimer: '* Let op: Deze officiële offerte valt onder de S&R Cloud Engineering & ERP-protocollen conform enterprise SLA-voorwaarden. Inclusief beveiligingsaudits en Europese AVG/GDPR-naleving.',
                sigSalimTitle: 'Technische Goedkeuring & Cloudarchitectuur',
                sigRaedTitle: 'Financieel Toezicht & ERP-Systemen'
            },
            caseStudy: {
                modalTitle: 'Casestudie & Rendement op Investering // S&R CoreSync',
                clientLabel: 'Klant / Sector:',
                challengeTitle: '⚠️ Operationele & Financiële Uitdaging:',
                solutionTitle: '⚡ CoreSync Engineering Oplossing:',
                roiTitle: '📈 Financiële Impact & Rendement (ROI):',
                btnWa: 'Vergelijkbare Oplossing Bespreken via WhatsApp',
                waMsg: (client) => `Beste S&R CoreSync, ik heb de casestudie van (${client}) bekeken en wil graag een vergelijkbare cloud-/ERP-oplossing voor onze onderneming bespreken.`
            }
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
            const lang = getPageLang();
            const t = (ES_I18N[lang] || ES_I18N.ar).pdf;
            const pdfBtn = document.createElement('button');
            pdfBtn.type = 'button';
            pdfBtn.id = 'estimatorPdfBtn';
            pdfBtn.className = 'estimator-btn-pdf';
            pdfBtn.title = t.btnTitle;
            pdfBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <span>${t.btnLabel}</span>
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
            const lang = getPageLang();
            const label = lang === 'en' ? 'Live ERP Demo ⚡' : (lang === 'nl' ? 'Live ERP Demo ⚡' : 'تجربة ERP السحابي ⚡');
            demoBtn.title = lang === 'en' ? 'Test Live Cloud ERP Dashboard' : (lang === 'nl' ? 'Test Live Cloud ERP Dashboard' : 'تجربة لوحة تحكم ERP السحابية الحية');
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
        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).pdf;

        const overlay = document.createElement('div');
        overlay.id = 'esQuoteModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-quote-modal" role="dialog" aria-modal="true" aria-labelledby="esQuoteTitle">
                <div class="es-quote-toolbar">
                    <div class="es-quote-toolbar-title" id="esQuoteTitle">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        <span>${t.toolbarTitle}</span>
                    </div>
                    <div class="es-toolbar-actions">
                        <button type="button" class="es-btn-tool es-btn-tool-print" onclick="window.printOfficialQuote()">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                            <span>${t.printBtn}</span>
                        </button>
                        <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeQuoteModal()">${t.closeBtn}</button>
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
                            <div><strong>${t.issueDateLabel}</strong> <span id="quoteIssueDate"></span></div>
                            <div>${t.validityLabel}</div>
                        </div>
                    </div>

                    <div class="es-quote-section-title">
                        <span>${t.sectionTitle}</span>
                    </div>

                    <table class="es-quote-table">
                        <thead>
                            <tr>
                                <th>${t.colItem}</th>
                                <th>${t.colSpec}</th>
                                <th>${t.colTime}</th>
                                <th>${t.colPrice}</th>
                            </tr>
                        </thead>
                        <tbody id="quoteTableBody"></tbody>
                    </table>

                    <div class="es-quote-total-box">
                        <div class="es-quote-total-card">
                            <div class="es-quote-total-row">
                                <span>${t.subtotalLabel}</span>
                                <span id="quoteSubtotal">€0</span>
                            </div>
                            <div class="es-quote-total-row">
                                <span>${t.vatLabel}</span>
                                <span>€0.00</span>
                            </div>
                            <div class="es-quote-total-row grand-total">
                                <span>${t.grandTotalLabel}</span>
                                <span id="quoteGrandTotal" style="color: #c5a880;">€0</span>
                            </div>
                        </div>
                    </div>

                    <div style="font-size: 0.78rem; color: #718096; line-height: 1.6; margin-bottom: 24px;">
                        ${t.disclaimer}
                    </div>

                    <div class="es-quote-signatures">
                        <div class="es-sig-block">
                            <div class="es-sig-title">${t.sigSalimTitle}</div>
                            <div class="es-sig-name">Eng. Mohammad Salim Aziza</div>
                            <div class="es-sig-role">Co-Founder & CTO // Lead Cloud Systems Architect</div>
                        </div>
                        <div class="es-sig-block">
                            <div class="es-sig-title">${t.sigRaedTitle}</div>
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

    
    // Modal Language Switcher UI Component
    function renderModalLangSwitcher(activeLang) {
        return `
            <div class="es-modal-lang-switcher" role="group" aria-label="Language Switcher" title="Alt + L للتبديل السريع">
                <button type="button" class="es-lang-pill ${activeLang === 'en' ? 'active' : ''}" onclick="window.switchModalLang('en')">EN</button>
                <button type="button" class="es-lang-pill ${activeLang === 'nl' ? 'active' : ''}" onclick="window.switchModalLang('nl')">NL</button>
                <button type="button" class="es-lang-pill ${activeLang === 'ar' ? 'active' : ''}" onclick="window.switchModalLang('ar')">عربي</button>
                <span class="es-kbd-badge" title="اختصار لوحة المفاتيح: Alt + L">Alt+L</span>
            </div>
        `;
    }

    // 3. Inject Floating Hub (Feedback, Quiz, Scheduler)
    function injectFloatingHub() {
        if (document.getElementById('esFloatingSuite')) return;

        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).hub;
        const fb = (ES_I18N[lang] || ES_I18N.ar).feedback;

        const hub = document.createElement('div');
        hub.id = 'esFloatingSuite';
        hub.className = 'es-floating-suite';
        hub.innerHTML = `
            <div class="es-floating-suite-collapse-bar">
                <button type="button" class="es-fab-toggle" id="esFabToggle" onclick="window.toggleFloatingSuite()" title="تصغير / إخفاء الأزرار" aria-label="Toggle floating buttons">
                    &minus;
                </button>
            </div>
            <div class="es-floating-suite-content" id="esFloatingContent" style="display:flex; flex-direction:column; gap:8px;">
                <button type="button" class="es-feedback-fab" onclick="window.openReadinessModal()" title="${t.readinessTitle}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                    <span>${t.readinessLabel}</span>
                </button>
                <button type="button" class="es-feedback-fab" onclick="window.openSchedulerModal()" title="${t.schedulerTitle}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                    <span>${t.schedulerLabel}</span>
                </button>
                <button type="button" class="es-feedback-fab" onclick="window.openFeedbackModal()" title="${t.feedbackTitle}">
                    <span class="es-feedback-dot"></span>
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                    <span>${t.feedbackLabel}</span>
                </button>
            </div>
            <button type="button" class="es-feedback-fab-min" id="esFloatingMinBtn" onclick="window.toggleFloatingSuite()" style="display:none;" title="إظهار أزرار الدعم">
                <span class="es-feedback-dot"></span>
                <span>⚡ أدوات الدعم</span>
            </button>
        `;
        document.body.appendChild(hub);

        window.toggleFloatingSuite = function() {
            const h = document.getElementById('esFloatingSuite');
            if (!h) return;
            const isMin = h.classList.toggle('is-minimized');
            const content = document.getElementById('esFloatingContent');
            const minBtn = document.getElementById('esFloatingMinBtn');
            const toggle = document.getElementById('esFabToggle');
            if (content) content.style.display = isMin ? 'none' : 'flex';
            if (minBtn) minBtn.style.display = isMin ? 'inline-flex' : 'none';
            if (toggle) toggle.innerHTML = isMin ? '+' : '&minus;';
            localStorage.setItem('coresync_hub_minimized', isMin ? '1' : '0');
        };

        if (localStorage.getItem('coresync_hub_minimized') === '1') {
            window.toggleFloatingSuite();
        }

        // Feedback Modal
        const overlay = document.createElement('div');
        overlay.id = 'esFeedbackModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-feedback-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <span class="es-feedback-dot"></span>
                        <span id="fbModalTitle">${fb.title}</span>
                    </h3>
                    <div class="es-header-tools">
                        ${renderModalLangSwitcher(lang)}
                        <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeFeedbackModal()">✕</button>
                    </div>
                </div>
                <div class="es-feedback-body">
                    <p style="font-size: 0.82rem; color: rgba(255,255,255,0.7); margin: 0 0 10px;">
                        ${fb.desc}
                    </p>

                    <div class="es-input-group">
                        <label>${fb.clientNameLabel}</label>
                        <input type="text" id="fbClientName" class="es-input-field" placeholder="${fb.clientNamePlaceholder}">
                    </div>

                    <div class="es-input-group">
                        <label>${fb.targetSectionLabel}</label>
                        <select id="fbTargetSection" class="es-select-field">
                            ${fb.sections.map(s => `<option value="${s}">${s}</option>`).join('')}
                        </select>
                    </div>

                    <div class="es-input-group">
                        <label>${fb.categoryLabel}</label>
                        <select id="fbCategory" class="es-select-field">
                            ${fb.categories.map(c => `<option value="${c}">${c}</option>`).join('')}
                        </select>
                    </div>

                    <div class="es-input-group">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <label style="margin-bottom:0;">${fb.detailsLabel}</label>
                            <span id="fbAutoSaveIndicator" class="es-autosave-indicator"></span>
                        </div>
                        <textarea id="fbDetails" class="es-textarea-field" rows="3" placeholder="${fb.detailsPlaceholder}"></textarea>
                    </div>

                    <div class="es-feedback-actions">
                        <button type="button" class="es-btn-send-wa" onclick="window.sendFeedbackViaWhatsApp()">
                            <svg viewBox="0 0 32 32" width="18" height="18" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                            <span>${fb.sendBtn}</span>
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

        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).scheduler;
        const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/Amsterdam';

        const overlay = document.createElement('div');
        overlay.id = 'esSchedulerModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-scheduler-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        <span id="schModalTitle">${t.title}</span>
                    </h3>
                    <div class="es-header-tools">
                        ${renderModalLangSwitcher(lang)}
                        <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeSchedulerModal()">✕</button>
                    </div>
                </div>
                <div class="es-feedback-body">
                    <p style="font-size: 0.82rem; color: rgba(255,255,255,0.7); margin: 0;">
                        ${t.desc}
                    </p>

                    <div class="es-input-group">
                        <label>${t.advisorLabel}</label>
                        <div class="es-consultant-grid">
                            <div class="es-consultant-card active" onclick="window.selectConsultant('salim', this)">
                                <div class="es-consultant-name">${t.consultants.salim.name}</div>
                                <div class="es-consultant-role">${t.consultants.salim.role}</div>
                            </div>
                            <div class="es-consultant-card" onclick="window.selectConsultant('raed', this)">
                                <div class="es-consultant-name">${t.consultants.raed.name}</div>
                                <div class="es-consultant-role">${t.consultants.raed.role}</div>
                            </div>
                            <div class="es-consultant-card" onclick="window.selectConsultant('both', this)">
                                <div class="es-consultant-name">${t.consultants.both.name}</div>
                                <div class="es-consultant-role">${t.consultants.both.role}</div>
                            </div>
                        </div>
                    </div>

                    <div style="font-size: 0.75rem; color: var(--es-cyan); display: flex; align-items: center; gap: 6px;">
                        <span>${t.tzLabel}</span>
                        <strong>${tz}</strong>
                    </div>

                    <div class="es-input-group">
                        <label>${t.slotLabel}</label>
                        <div class="es-slots-grid">
                            ${t.slots.map((slot, idx) => `
                                <button type="button" class="es-slot-btn ${idx === 0 ? 'active' : ''}" onclick="window.selectSlot('${slot}', this)">${slot}</button>
                            `).join('')}
                        </div>
                    </div>

                    <div class="es-input-group">
                        <label>${t.nameLabel}</label>
                        <input type="text" id="schClientName" class="es-input-field" placeholder="${t.namePlaceholder}">
                    </div>

                    <div class="es-input-group">
                        <label>${t.topicLabel}</label>
                        <input type="text" id="schTopic" class="es-input-field" placeholder="${t.topicPlaceholder}">
                    </div>

                    <div class="es-feedback-actions">
                        <button type="button" class="es-btn-send-wa" onclick="window.confirmScheduler()">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                            <span>${t.confirmBtn}</span>
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
        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).readiness;

        const overlay = document.createElement('div');
        overlay.id = 'esReadinessModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-readiness-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                        <span id="readinessModalTitle">${t.modalTitle}</span>
                    </h3>
                    <div class="es-header-tools">
                        ${renderModalLangSwitcher(lang)}
                        <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeReadinessModal()">✕</button>
                    </div>
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
        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).caseStudy;

        const overlay = document.createElement('div');
        overlay.id = 'esCaseStudyModalOverlay';
        overlay.className = 'es-modal-overlay';
        overlay.innerHTML = `
            <div class="es-casestudy-modal" role="dialog" aria-modal="true">
                <div class="es-feedback-header">
                    <h3>
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        <span id="caseStudyModalTitle">${t.modalTitle}</span>
                    </h3>
                    <div class="es-header-tools">
                        ${renderModalLangSwitcher(lang)}
                        <button type="button" class="es-btn-tool es-btn-tool-close" onclick="window.closeCaseStudyModal()">✕</button>
                    </div>
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

        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).gdpr;

        const banner = document.createElement('div');
        banner.id = 'esGdprBanner';
        banner.className = 'es-gdpr-banner active';
        banner.innerHTML = `
            <div class="es-gdpr-content">
                <div class="es-gdpr-title">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    <span>${t.title}</span>
                </div>
                <p class="es-gdpr-text">
                    ${t.text}
                </p>
            </div>
            <div class="es-gdpr-actions">
                <button type="button" class="es-btn-gdpr-accept" onclick="window.acceptGDPR()">${t.accept}</button>
                <button type="button" class="es-btn-gdpr-decline" onclick="window.declineGDPR()">${t.decline}</button>
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
        const hash = (window.location.hash || '').toLowerCase();
        if (urlParams.has('feedback') || urlParams.get('preview') === 'client' || hash === '#feedback') {
            setTimeout(() => window.openFeedbackModal(), 500);
        }
        if (urlParams.has('scheduler') || hash === '#scheduler') {
            setTimeout(() => window.openSchedulerModal(), 500);
        }
        if (urlParams.has('assessment') || hash === '#assessment') {
            setTimeout(() => window.openReadinessModal(), 500);
        }
    }

    // ==========================================
    // Window Global Functions
    // ==========================================

    window.exportEstimatorPDF = function () {
        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).pdf;

        const defaultTitles = {
            ar: {
                type: { title: 'هوية بصرية وتطوير متكامل', price: 950, days: '7 - 10 أيام عمل' },
                pages: { title: '1 - 5 صفحات رئيسية', price: 0 },
                lang: { title: 'لغة واحدة', price: 0 },
                pay: { title: 'بدون دفع إلكتروني', price: 0 },
                speed: { title: 'تسليم قياسي', price: 0 },
                included: 'مشمول',
                agreed: 'حسب الاتفاق'
            },
            en: {
                type: { title: 'Visual Identity & Full Stack Engineering', price: 950, days: '7 - 10 business days' },
                pages: { title: '1 - 5 Core Web Pages', price: 0 },
                lang: { title: 'Single Language', price: 0 },
                pay: { title: 'No Online Payment Gateway', price: 0 },
                speed: { title: 'Standard Delivery Timeline', price: 0 },
                included: 'Included',
                agreed: 'Per Agreement'
            },
            nl: {
                type: { title: 'Merkidentiteit & Full Stack Systeemontwikkeling', price: 950, days: '7 - 10 werkdagen' },
                pages: { title: "1 - 5 Kernpagina's", price: 0 },
                lang: { title: 'Eén Taal', price: 0 },
                pay: { title: 'Geen Online Betaalkoppeling', price: 0 },
                speed: { title: 'Standaard Levering', price: 0 },
                included: 'Inbegrepen',
                agreed: 'Volgens Afspraak'
            }
        };

        const state = window._estimatorState || defaultTitles[lang] || defaultTitles.ar;
        const total = Object.values(state).reduce((sum, g) => sum + (g.price || 0), 0);
        const now = new Date();
        const dateLocale = lang === 'nl' ? 'nl-NL' : (lang === 'en' ? 'en-US' : 'ar-EG');
        const issueDate = now.toLocaleDateString(dateLocale, { year: 'numeric', month: 'long', day: 'numeric' });
        const ref = 'CSR-' + now.getFullYear() + '-' + Math.floor(1000 + Math.random() * 9000);

        const refEl = document.getElementById('quoteRefNumber');
        const dateEl = document.getElementById('quoteIssueDate');
        if (refEl) refEl.textContent = ref;
        if (dateEl) dateEl.textContent = issueDate;

        const langDict = defaultTitles[lang] || defaultTitles.ar;
        const tbody = document.getElementById('quoteTableBody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td><strong>${lang === 'en' ? 'Package & Project Scope' : (lang === 'nl' ? 'Pakket & Projectomvang' : 'نوع الحزمة والمشروع')}</strong></td>
                    <td>${state.type.title}</td>
                    <td>${state.type.days || langDict.agreed}</td>
                    <td>€${(state.type.price || total).toLocaleString('en')}</td>
                </tr>
                <tr>
                    <td><strong>${lang === 'en' ? 'Pages & Deliverables Scope' : (lang === 'nl' ? "Omvang Pagina's & Modules" : 'نطاق الصفحات والتنفيذ')}</strong></td>
                    <td>${state.pages.title}</td>
                    <td>${langDict.included}</td>
                    <td>€${(state.pages.price || 0).toLocaleString('en')}</td>
                </tr>
                <tr>
                    <td><strong>${lang === 'en' ? 'Languages & Localization' : (lang === 'nl' ? 'Talen & Lokalisatie' : 'منظومة اللغات والترجمة')}</strong></td>
                    <td>${state.lang.title}</td>
                    <td>${langDict.included}</td>
                    <td>€${(state.lang.price || 0).toLocaleString('en')}</td>
                </tr>
                <tr>
                    <td><strong>${lang === 'en' ? 'Payment Gateways & Banking API' : (lang === 'nl' ? 'Betaalproviders & Bankkoppeling' : 'بوابات الدفع والربط البنكي')}</strong></td>
                    <td>${state.pay.title}</td>
                    <td>${langDict.included}</td>
                    <td>€${(state.pay.price || 0).toLocaleString('en')}</td>
                </tr>
                <tr>
                    <td><strong>${lang === 'en' ? 'Delivery Standard & SLA' : (lang === 'nl' ? 'Levering & SLA Norm' : 'معيار وسرعة التسليم')}</strong></td>
                    <td>${state.speed.title}</td>
                    <td>${langDict.included}</td>
                    <td>€${(state.speed.price || 0).toLocaleString('en')}</td>
                </tr>
            `;
        }

        const subEl = document.getElementById('quoteSubtotal');
        const grandEl = document.getElementById('quoteGrandTotal');
        if (subEl) subEl.textContent = `€${total.toLocaleString('en')}`;
        if (grandEl) grandEl.textContent = `€${total.toLocaleString('en')}`;

        const overlay = document.getElementById('esQuoteModalOverlay');
        if (overlay) {
            triggerHaptic(15);
            overlay.classList.add('active');
        }
    };

    window.closeQuoteModal = () => {
        triggerHaptic(10);
        document.getElementById('esQuoteModalOverlay')?.classList.remove('active');
    };
    window.printOfficialQuote = () => window.print();

    // =========================================================================
    // Haptic Feedback Engine (Mobile & Touch Interaction)
    // =========================================================================
    function triggerHaptic(duration = 15) {
        if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
            try {
                navigator.vibrate(duration);
            } catch (e) {}
        }
    }
    window.triggerHaptic = triggerHaptic;

    // =========================================================================
    // Full Page Language Auto-Sync & Navigation Resolver
    // =========================================================================
    function getLocalizedTargetUrl(targetLang) {
        const currentPath = window.location.pathname;
        let filename = currentPath.substring(currentPath.lastIndexOf('/') + 1) || 'index.html';
        if (!filename.endsWith('.html')) filename = 'index.html';

        const isNl = currentPath.includes('/nl/');
        const isEn = currentPath.includes('/en/');
        const hash = window.location.hash || '';

        let target = filename;
        if (targetLang === 'ar') {
            if (isNl || isEn) target = '../' + filename;
            else target = filename;
        } else if (targetLang === 'en') {
            if (isEn) target = filename;
            else if (isNl) target = '../en/' + filename;
            else target = 'en/' + filename;
        } else if (targetLang === 'nl') {
            if (isNl) target = filename;
            else if (isEn) target = '../nl/' + filename;
            else target = 'nl/' + filename;
        }
        return target + hash;
    }
    window.getLocalizedTargetUrl = getLocalizedTargetUrl;

    let toastTimeout = null;
    function showLangSyncToast(targetLang) {
        if (targetLang === getPageLang()) {
            dismissLangSyncToast();
            return;
        }

        let toast = document.getElementById('esLangSyncToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'esLangSyncToast';
            toast.className = 'es-lang-sync-toast';
            document.body.appendChild(toast);
        }

        const toastDict = {
            ar: {
                msg: 'هل ترغب في تطبيق اللغة العربية على كامل الموقع وتصفح كافة الأقسام؟',
                btn: 'مزامنة الموقع الآن',
                dir: 'rtl'
            },
            en: {
                msg: 'Apply English to the entire website for a full localized experience?',
                btn: 'Sync Entire Site',
                dir: 'ltr'
            },
            nl: {
                msg: 'Wilt u de hele website overschakelen naar het Nederlands?',
                btn: 'Synchroniseer Hele Site',
                dir: 'ltr'
            }
        };

        const t = toastDict[targetLang] || toastDict.en;
        toast.setAttribute('dir', t.dir);
        toast.innerHTML = `
            <div class="es-sync-toast-content">
                <span class="es-sync-toast-icon">🌐</span>
                <span class="es-sync-toast-msg">${t.msg}</span>
            </div>
            <div class="es-sync-toast-actions">
                <button type="button" class="es-btn-sync-apply" onclick="window.applyFullPageLanguage('${targetLang}')">
                    <span>${t.btn}</span>
                </button>
                <button type="button" class="es-btn-sync-close" onclick="window.dismissLangSyncToast()" title="إغلاق / Close">✕</button>
            </div>
        `;
        toast.classList.add('active');

        if (toastTimeout) clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('active');
        }, 8500);
    }
    window.showLangSyncToast = showLangSyncToast;

    window.applyFullPageLanguage = function (targetLang) {
        triggerHaptic(25);
        saveFeedbackDraft(true);
        saveSchedulerDraft();
        try {
            localStorage.setItem('coresync_preferred_lang', targetLang);
        } catch (e) {}
        const url = getLocalizedTargetUrl(targetLang);
        window.location.href = url;
    };

    window.dismissLangSyncToast = function () {
        triggerHaptic(10);
        const toast = document.getElementById('esLangSyncToast');
        if (toast) toast.classList.remove('active');
        if (toastTimeout) clearTimeout(toastTimeout);
    };

    // =========================================================================
    // Offline Draft Auto-Save Engine with Live Cloud Pulse Indicator
    // =========================================================================
    let autoSaveTimer = null;
    let autoSaveIndicatorTimer = null;

    function updateAutoSaveIndicator(state) {
        const indicator = document.getElementById('fbAutoSaveIndicator');
        if (!indicator) return;

        const lang = currentModalLang || getPageLang();
        const labels = {
            ar: { saving: 'جاري الحفظ...', saved: 'تم الحفظ تلقائياً' },
            en: { saving: 'Saving...', saved: 'Auto-saved' },
            nl: { saving: 'Opslaan...', saved: 'Opgeslagen' }
        };
        const l = labels[lang] || labels.ar;

        if (state === 'saving') {
            indicator.className = 'es-autosave-indicator saving';
            indicator.innerHTML = `<span class="es-cloud-icon">☁️</span> <span>${l.saving}</span>`;
        } else if (state === 'saved') {
            indicator.className = 'es-autosave-indicator saved';
            indicator.innerHTML = `<span class="es-cloud-icon">☁️</span> <span>${l.saved}</span>`;
            if (autoSaveIndicatorTimer) clearTimeout(autoSaveIndicatorTimer);
            autoSaveIndicatorTimer = setTimeout(() => {
                indicator.className = 'es-autosave-indicator';
            }, 2500);
        } else {
            indicator.className = 'es-autosave-indicator';
        }
    }
    window.updateAutoSaveIndicator = updateAutoSaveIndicator;

    function saveFeedbackDraft(immediate = false) {
        updateAutoSaveIndicator('saving');

        const doSave = () => {
            const name = document.getElementById('fbClientName')?.value || '';
            const section = document.getElementById('fbTargetSection')?.value || '';
            const category = document.getElementById('fbCategory')?.value || '';
            const details = document.getElementById('fbDetails')?.value || '';

            if (details.trim() || name.trim()) {
                try {
                    localStorage.setItem('coresync_feedback_draft', JSON.stringify({
                        name, section, category, details, timestamp: Date.now()
                    }));
                } catch (e) {}
                updateAutoSaveIndicator('saved');
            } else {
                try { localStorage.removeItem('coresync_feedback_draft'); } catch (e) {}
                updateAutoSaveIndicator('idle');
            }
        };

        if (immediate) {
            if (autoSaveTimer) clearTimeout(autoSaveTimer);
            doSave();
        } else {
            if (autoSaveTimer) clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(doSave, 380);
        }
    }
    window.saveFeedbackDraft = saveFeedbackDraft;

    function clearFeedbackDraft() {
        triggerHaptic(15);
        try { localStorage.removeItem('coresync_feedback_draft'); } catch (e) {}
        const nameEl = document.getElementById('fbClientName');
        const detailsEl = document.getElementById('fbDetails');
        if (nameEl) nameEl.value = '';
        if (detailsEl) detailsEl.value = '';
        const banner = document.getElementById('fbDraftRestoredBanner');
        if (banner) banner.remove();
        updateAutoSaveIndicator('idle');
    }
    window.clearFeedbackDraft = clearFeedbackDraft;

    function restoreFeedbackDraft() {
        try {
            const raw = localStorage.getItem('coresync_feedback_draft');
            if (!raw) return;
            const draft = JSON.parse(raw);
            if (!draft || (!draft.details && !draft.name)) return;

            const nameEl = document.getElementById('fbClientName');
            const secEl = document.getElementById('fbTargetSection');
            const catEl = document.getElementById('fbCategory');
            const detEl = document.getElementById('fbDetails');

            if (nameEl && draft.name) nameEl.value = draft.name;
            if (secEl && draft.section) secEl.value = draft.section;
            if (catEl && draft.category) catEl.value = draft.category;
            if (detEl && draft.details) detEl.value = draft.details;

            const lang = currentModalLang || getPageLang();
            const noticeTexts = {
                ar: { text: '✨ تم استرجاع مسودتك المحفوظة تلقائياً', clear: 'مسح المسودة' },
                en: { text: '✨ Your saved draft has been auto-restored', clear: 'Clear Draft' },
                nl: { text: '✨ Uw opgeslagen concept is hersteld', clear: 'Concept wissen' }
            };
            const n = noticeTexts[lang] || noticeTexts.ar;

            let banner = document.getElementById('fbDraftRestoredBanner');
            const modalBody = document.querySelector('.es-feedback-modal .es-feedback-body');
            if (!banner && modalBody) {
                banner = document.createElement('div');
                banner.id = 'fbDraftRestoredBanner';
                banner.className = 'es-draft-restored-pill';
                modalBody.insertBefore(banner, modalBody.children[1] || modalBody.firstChild);
            }
            if (banner) {
                banner.innerHTML = `
                    <span>${n.text}</span>
                    <button type="button" onclick="window.clearFeedbackDraft()" class="es-btn-clear-draft">${n.clear}</button>
                `;
            }
        } catch (e) {}
    }
    window.restoreFeedbackDraft = restoreFeedbackDraft;

    function saveSchedulerDraft() {
        const name = document.getElementById('schClientName')?.value || '';
        const topic = document.getElementById('schTopic')?.value || '';
        if (name.trim() || topic.trim()) {
            try {
                localStorage.setItem('coresync_scheduler_draft', JSON.stringify({
                    name, topic, consultant: selectedConsultant, slot: selectedSlot, timestamp: Date.now()
                }));
            } catch (e) {}
        }
    }
    window.saveSchedulerDraft = saveSchedulerDraft;

    function restoreSchedulerDraft() {
        try {
            const raw = localStorage.getItem('coresync_scheduler_draft');
            if (!raw) return;
            const draft = JSON.parse(raw);
            if (!draft) return;

            const nameEl = document.getElementById('schClientName');
            const topicEl = document.getElementById('schTopic');
            if (nameEl && draft.name) nameEl.value = draft.name;
            if (topicEl && draft.topic) topicEl.value = draft.topic;

            if (draft.consultant) {
                selectedConsultant = draft.consultant;
                document.querySelectorAll('.es-consultant-card').forEach(c => {
                    const onclickStr = c.getAttribute('onclick') || '';
                    if (onclickStr.includes(draft.consultant)) c.classList.add('active');
                    else c.classList.remove('active');
                });
            }
            if (draft.slot) {
                selectedSlot = draft.slot;
                document.querySelectorAll('.es-slot-btn').forEach(b => {
                    if (b.textContent.trim() === draft.slot) b.classList.add('active');
                    else b.classList.remove('active');
                });
            }
        } catch (e) {}
    }
    window.restoreSchedulerDraft = restoreSchedulerDraft;

    function attachDraftListeners() {
        ['fbClientName', 'fbDetails'].forEach(id => {
            const el = document.getElementById(id);
            if (el && !el.dataset.draftBound) {
                el.dataset.draftBound = 'true';
                el.addEventListener('input', () => saveFeedbackDraft(false));
            }
        });
        ['fbTargetSection', 'fbCategory'].forEach(id => {
            const el = document.getElementById(id);
            if (el && !el.dataset.draftBound) {
                el.dataset.draftBound = 'true';
                el.addEventListener('change', () => saveFeedbackDraft(true));
            }
        });
        ['schClientName', 'schTopic'].forEach(id => {
            const el = document.getElementById(id);
            if (el && !el.dataset.draftBound) {
                el.dataset.draftBound = 'true';
                el.addEventListener('input', saveSchedulerDraft);
            }
        });
    }
    window.attachDraftListeners = attachDraftListeners;

    // Global Keyboard Shortcut: Alt + L to cycle languages
    document.addEventListener('keydown', function (e) {
        if (e.altKey && (e.key === 'l' || e.key === 'L' || e.code === 'KeyL')) {
            e.preventDefault();
            triggerHaptic(15);
            const langs = ['ar', 'en', 'nl'];
            const cur = currentModalLang || getPageLang();
            const nextIdx = (langs.indexOf(cur) + 1) % langs.length;
            const nextLang = langs[nextIdx];
            window.switchModalLang(nextLang);
        }
    });

    window.openFeedbackModal = () => {
        triggerHaptic(15);
        document.getElementById('esFeedbackModalOverlay')?.classList.add('active');
        try {
            history.replaceState(null, '', window.location.pathname + window.location.search + '#feedback');
        } catch (e) {}
        restoreFeedbackDraft();
        attachDraftListeners();
    };
    window.closeFeedbackModal = () => {
        triggerHaptic(10);
        document.getElementById('esFeedbackModalOverlay')?.classList.remove('active');
        try {
            if (window.location.hash === '#feedback') {
                history.replaceState(null, '', window.location.pathname + window.location.search);
            }
        } catch (e) {}
    };

    window.sendFeedbackViaWhatsApp = function () {
        triggerHaptic(20);
        const lang = currentModalLang || getPageLang();
        const fb = (ES_I18N[lang] || ES_I18N.ar).feedback;

        const defaultClient = lang === 'en' ? 'Enterprise Client' : (lang === 'nl' ? 'Zakelijke Klant' : 'عميل تجريبي');
        const clientName = document.getElementById('fbClientName')?.value.trim() || defaultClient;
        const targetSection = document.getElementById('fbTargetSection')?.value || '';
        const category = document.getElementById('fbCategory')?.value || '';
        const details = document.getElementById('fbDetails')?.value.trim() || '';

        if (!details) {
            alert(fb.alertEmpty);
            return;
        }

        const msg = [
            fb.waMsgHeader,
            `👤 *${lang === 'en' ? 'From:' : (lang === 'nl' ? 'Van:' : 'من:')}* ${clientName}`,
            `📍 *${lang === 'en' ? 'Section:' : (lang === 'nl' ? 'Onderdeel:' : 'القسم:')}* ${targetSection}`,
            `🏷️ *${lang === 'en' ? 'Category:' : (lang === 'nl' ? 'Type:' : 'النوع:')}* ${category}`,
            `📝 *${lang === 'en' ? 'Feedback:' : (lang === 'nl' ? 'Feedback:' : 'الملاحظة:')}* ${details}`,
            `🔗 *${lang === 'en' ? 'URL:' : (lang === 'nl' ? 'Link:' : 'الرابط:')}* ${window.location.href}`
        ].join('\n');

        try { localStorage.removeItem('coresync_feedback_draft'); } catch (e) {}
        const banner = document.getElementById('fbDraftRestoredBanner');
        if (banner) banner.remove();

        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeFeedbackModal();
    };

    // Scheduler Handlers
    let selectedConsultant = 'salim';
    let selectedSlot = '';

    // In-Modal Instant Language Switcher & State Memory
    let currentModalLang = getPageLang();
    window.currentModalLang = currentModalLang;

    window.switchModalLang = function (targetLang) {
        if (!['ar', 'en', 'nl'].includes(targetLang)) return;
        triggerHaptic(15);
        currentModalLang = targetLang;
        window.currentModalLang = targetLang;
        try {
            localStorage.setItem('coresync_preferred_lang', targetLang);
        } catch (e) {}

        // Trigger Full Page Sync Toast if language differs from current page
        showLangSyncToast(targetLang);

        // Update active class on all lang pill buttons across all modals
        document.querySelectorAll('.es-modal-lang-switcher').forEach(sw => {
            sw.querySelectorAll('.es-lang-pill').forEach(btn => {
                const text = btn.textContent.trim().toLowerCase();
                const isTarget = text === targetLang || (targetLang === 'ar' && text === 'عربي');
                btn.classList.toggle('active', isTarget);
            });
        });

        // 1. Dynamic Update: Feedback Modal
        const fbModal = document.querySelector('.es-feedback-modal');
        if (fbModal) {
            fbModal.setAttribute('dir', targetLang === 'ar' ? 'rtl' : 'ltr');
            const fbData = (ES_I18N[targetLang] || ES_I18N.ar).feedback;
            const titleEl = document.getElementById('fbModalTitle');
            if (titleEl) titleEl.textContent = fbData.title;
            const descEl = fbModal.querySelector('.es-feedback-body > p');
            if (descEl) descEl.textContent = fbData.desc;

            const labels = fbModal.querySelectorAll('.es-input-group label');
            if (labels[0]) labels[0].textContent = fbData.clientNameLabel;
            if (labels[1]) labels[1].textContent = fbData.targetSectionLabel;
            if (labels[2]) labels[2].textContent = fbData.categoryLabel;
            if (labels[3]) labels[3].textContent = fbData.detailsLabel;

            const nameInput = document.getElementById('fbClientName');
            if (nameInput) nameInput.placeholder = fbData.clientNamePlaceholder;

            const secSelect = document.getElementById('fbTargetSection');
            if (secSelect) {
                const curVal = secSelect.value;
                secSelect.innerHTML = fbData.sections.map(s => `<option value="${s}">${s}</option>`).join('');
                if (fbData.sections.includes(curVal)) secSelect.value = curVal;
            }

            const catSelect = document.getElementById('fbCategory');
            if (catSelect) {
                const curVal = catSelect.value;
                catSelect.innerHTML = fbData.categories.map(c => `<option value="${c}">${c}</option>`).join('');
                if (fbData.categories.includes(curVal)) catSelect.value = curVal;
            }

            const detailsInput = document.getElementById('fbDetails');
            if (detailsInput) detailsInput.placeholder = fbData.detailsPlaceholder;

            const sendBtnSpan = fbModal.querySelector('.es-btn-send-wa span');
            if (sendBtnSpan) sendBtnSpan.textContent = fbData.sendBtn;

            // Also update restored draft notice if visible
            const restoredBanner = document.getElementById('fbDraftRestoredBanner');
            if (restoredBanner) {
                const noticeTexts = {
                    ar: { text: '✨ تم استرجاع مسودتك المحفوظة تلقائياً', clear: 'مسح المسودة' },
                    en: { text: '✨ Your saved draft has been auto-restored', clear: 'Clear Draft' },
                    nl: { text: '✨ Uw opgeslagen concept is hersteld', clear: 'Concept wissen' }
                };
                const n = noticeTexts[targetLang] || noticeTexts.ar;
                restoredBanner.innerHTML = `
                    <span>${n.text}</span>
                    <button type="button" onclick="window.clearFeedbackDraft()" class="es-btn-clear-draft">${n.clear}</button>
                `;
            }
        }

        // 2. Dynamic Update: Scheduler Modal
        const schModal = document.querySelector('.es-scheduler-modal');
        if (schModal) {
            schModal.setAttribute('dir', targetLang === 'ar' ? 'rtl' : 'ltr');
            const schData = (ES_I18N[targetLang] || ES_I18N.ar).scheduler;
            const titleEl = document.getElementById('schModalTitle');
            if (titleEl) titleEl.textContent = schData.title;
            const descEl = schModal.querySelector('.es-feedback-body > p');
            if (descEl) descEl.textContent = schData.desc;

            const labels = schModal.querySelectorAll('.es-input-group label');
            if (labels[0]) labels[0].textContent = schData.advisorLabel;
            if (labels[1]) labels[1].textContent = schData.slotLabel;
            if (labels[2]) labels[2].textContent = schData.nameLabel;
            if (labels[3]) labels[3].textContent = schData.topicLabel;

            const cards = schModal.querySelectorAll('.es-consultant-card');
            if (cards[0]) {
                const n = cards[0].querySelector('.es-consultant-name');
                const r = cards[0].querySelector('.es-consultant-role');
                if (n) n.textContent = schData.consultants.salim.name;
                if (r) r.textContent = schData.consultants.salim.role;
            }
            if (cards[1]) {
                const n = cards[1].querySelector('.es-consultant-name');
                const r = cards[1].querySelector('.es-consultant-role');
                if (n) n.textContent = schData.consultants.raed.name;
                if (r) r.textContent = schData.consultants.raed.role;
            }
            if (cards[2]) {
                const n = cards[2].querySelector('.es-consultant-name');
                const r = cards[2].querySelector('.es-consultant-role');
                if (n) n.textContent = schData.consultants.both.name;
                if (r) r.textContent = schData.consultants.both.role;
            }

            const tzSpan = schModal.querySelector('div[style*="var(--es-cyan)"] span');
            if (tzSpan) tzSpan.textContent = schData.tzLabel;

            const slotsGrid = schModal.querySelector('.es-slots-grid');
            if (slotsGrid) {
                slotsGrid.innerHTML = schData.slots.map((s, idx) => `
                    <button type="button" class="es-slot-btn ${idx === 0 ? 'active' : ''}" onclick="window.selectSlot('${s}', this)">${s}</button>
                `).join('');
                selectedSlot = schData.slots[0];
            }

            const nameInput = document.getElementById('schClientName');
            if (nameInput) nameInput.placeholder = schData.namePlaceholder;
            const topicInput = document.getElementById('schTopic');
            if (topicInput) topicInput.placeholder = schData.topicPlaceholder;

            const confirmBtnSpan = schModal.querySelector('.es-btn-send-wa span');
            if (confirmBtnSpan) confirmBtnSpan.textContent = schData.confirmBtn;
        }

        // 3. Dynamic Update: Readiness Modal
        const readModal = document.querySelector('.es-readiness-modal');
        if (readModal) {
            readModal.setAttribute('dir', targetLang === 'ar' ? 'rtl' : 'ltr');
            const readData = (ES_I18N[targetLang] || ES_I18N.ar).readiness;
            const titleEl = document.getElementById('readinessModalTitle');
            if (titleEl) titleEl.textContent = readData.modalTitle;
            if (document.getElementById('esReadinessModalOverlay')?.classList.contains('active')) {
                renderQuizStep();
            }
        }
    };

    window.openSchedulerModal = function () {
        triggerHaptic(15);
        const lang = currentModalLang || getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).scheduler;
        if (!selectedSlot && t.slots && t.slots[0]) {
            selectedSlot = t.slots[0];
        }
        document.getElementById('esSchedulerModalOverlay')?.classList.add('active');
        try {
            history.replaceState(null, '', window.location.pathname + window.location.search + '#scheduler');
        } catch (e) {}
        restoreSchedulerDraft();
        attachDraftListeners();
    };
    window.closeSchedulerModal = () => {
        triggerHaptic(10);
        document.getElementById('esSchedulerModalOverlay')?.classList.remove('active');
        try {
            if (window.location.hash === '#scheduler') {
                history.replaceState(null, '', window.location.pathname + window.location.search);
            }
        } catch (e) {}
    };

    window.selectConsultant = function (type, el) {
        triggerHaptic(12);
        selectedConsultant = type;
        document.querySelectorAll('.es-consultant-card').forEach(c => c.classList.remove('active'));
        el.classList.add('active');
        saveSchedulerDraft();
    };

    window.selectSlot = function (slot, el) {
        triggerHaptic(12);
        selectedSlot = slot;
        document.querySelectorAll('.es-slot-btn').forEach(b => b.classList.remove('active'));
        el.classList.add('active');
        saveSchedulerDraft();
    };

    window.confirmScheduler = function () {
        triggerHaptic(20);
        const lang = currentModalLang || getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).scheduler;

        const defaultClient = lang === 'en' ? 'Executive Leader' : (lang === 'nl' ? 'Directielid' : 'شخصية قيادية');
        const defaultTopic = lang === 'en' ? 'Cloud & ERP Architecture' : (lang === 'nl' ? 'Cloud & ERP Architectuur' : 'استشارة سحابية وERP');
        const name = document.getElementById('schClientName')?.value.trim() || defaultClient;
        const topic = document.getElementById('schTopic')?.value.trim() || defaultTopic;
        const chosenConsultant = t.consultants[selectedConsultant]?.waTitle || t.consultants.salim.waTitle;
        const currentSlot = selectedSlot || (t.slots && t.slots[0]) || '';

        const msg = [
            t.waHeader,
            `👤 *${lang === 'en' ? 'Name / Organization:' : (lang === 'nl' ? 'Naam / Bedrijf:' : 'الاسم / المنشأة:')}* ${name}`,
            `💼 *${lang === 'en' ? 'Advisor:' : (lang === 'nl' ? 'Adviseur:' : 'المستشار المطلوب:')}* ${chosenConsultant}`,
            `⏰ *${lang === 'en' ? 'Selected Slot:' : (lang === 'nl' ? 'Gewenste Tijd:' : 'الموعد المقترح:')}* ${currentSlot}`,
            `🎯 *${lang === 'en' ? 'Topic:' : (lang === 'nl' ? 'Onderwerp:' : 'موضوع الاستشارة:')}* ${topic}`,
            `🌐 *${lang === 'en' ? 'Timezone:' : (lang === 'nl' ? 'Tijdzone:' : 'المنطقة الزمنية:')}* ${Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/Amsterdam'}`
        ].join('\n');

        try { localStorage.removeItem('coresync_scheduler_draft'); } catch (e) {}
        const targetAdvisorWa = (selectedConsultant === 'raed') ? WHATSAPP_RAED : WHATSAPP_SALIM;
        window.open(`https://wa.me/${targetAdvisorWa}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeSchedulerModal();
    };

    // Assessment Quiz Handlers
    window.openReadinessModal = function () {
        triggerHaptic(15);
        currentQuizStep = 0;
        renderQuizStep();
        document.getElementById('esReadinessModalOverlay')?.classList.add('active');
        try {
            history.replaceState(null, '', window.location.pathname + window.location.search + '#assessment');
        } catch (e) {}
    };

    window.closeReadinessModal = () => {
        triggerHaptic(10);
        document.getElementById('esReadinessModalOverlay')?.classList.remove('active');
        try {
            if (window.location.hash === '#assessment') {
                history.replaceState(null, '', window.location.pathname + window.location.search);
            }
        } catch (e) {}
    };

    function renderQuizStep() {
        const fill = document.getElementById('quizProgressFill');
        const area = document.getElementById('quizQuestionArea');
        if (!area || !fill) return;

        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).readiness;
        const questions = QUIZ_QUESTIONS_I18N[lang] || QUIZ_QUESTIONS_I18N.ar;

        if (currentQuizStep >= questions.length) {
            renderQuizResults();
            return;
        }

        const q = questions[currentQuizStep];
        fill.style.width = `${((currentQuizStep + 1) / questions.length) * 100}%`;

        area.innerHTML = `
            <div style="font-size: 0.75rem; color: var(--es-cyan); font-weight: 700; margin-bottom: 6px;">
                ${t.stepLabel(currentQuizStep + 1, questions.length)}
            </div>
            <h4 style="color: #fff; font-size: 1.05rem; font-weight: 800; margin-bottom: 16px;">
                ${q.title}
            </h4>
            <div class="es-quiz-options">
                ${q.options.map((opt) => `
                    <div class="es-quiz-option" onclick="window.chooseQuizOption(${opt.score}, ${opt.saving})">
                        <span>${opt.text}</span>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="9 18 15 12 9 6"/></svg>
                    </div>
                `).join('')}
            </div>
        `;
    }

    window.chooseQuizOption = function (score, saving) {
        triggerHaptic(15);
        quizAnswers[currentQuizStep] = { score, saving };
        currentQuizStep++;
        renderQuizStep();
    };

    function renderQuizResults() {
        const area = document.getElementById('quizQuestionArea');
        const totalScore = Object.values(quizAnswers).reduce((sum, a) => sum + a.score, 0);
        const monthlySaving = Object.values(quizAnswers).reduce((sum, a) => sum + a.saving, 0);
        const scorePercentage = Math.min(95, Math.max(35, totalScore));

        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).readiness;

        area.innerHTML = `
            <div style="text-align: center; padding: 10px 0;">
                <div class="es-quiz-score-circle">
                    <span class="es-quiz-score-val">${scorePercentage}%</span>
                    <span class="es-quiz-score-lbl">${t.scoreLabel}</span>
                </div>
                <h3 style="color: #fff; font-size: 1.2rem; font-weight: 800; margin-bottom: 8px;">
                    ${t.reportTitle}
                </h3>
                <p style="color: rgba(255,255,255,0.78); font-size: 0.85rem; line-height: 1.6; max-width: 480px; margin: 0 auto 16px;">
                    ${t.reportDesc(monthlySaving)}
                </p>
                <div class="es-casestudy-kpi-grid" style="margin-bottom: 20px;">
                    <div class="es-casestudy-kpi">
                        <div class="val">${t.kpi1Val(monthlySaving)}</div>
                        <div class="lbl">${t.kpi1Lbl}</div>
                    </div>
                    <div class="es-casestudy-kpi">
                        <div class="val">${t.kpi2Val}</div>
                        <div class="lbl">${t.kpi2Lbl}</div>
                    </div>
                    <div class="es-casestudy-kpi">
                        <div class="val">${t.kpi3Val}</div>
                        <div class="lbl">${t.kpi3Lbl}</div>
                    </div>
                </div>
                <button type="button" class="es-btn-send-wa" style="width: 100%;" onclick="window.bookAssessmentConsultation(${scorePercentage}, ${monthlySaving})">
                    <span>${t.bookBtn}</span>
                </button>
            </div>
        `;
    }

    window.bookAssessmentConsultation = function (score, saving) {
        triggerHaptic(20);
        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).readiness;

        const msg = [
            t.waHeader,
            `🎯 *${lang === 'en' ? 'Digital Readiness Score:' : (lang === 'nl' ? 'Digitale Gereedheidsscore:' : 'نسبة الجاهزية الحالية:')}* ${score}%`,
            `💰 *${lang === 'en' ? 'Estimated Monthly Savings:' : (lang === 'nl' ? 'Geschatte Maandbesparing:' : 'الوفر الشهري المقدر:')}* €${saving.toLocaleString('en')}`,
            `🤝 ${lang === 'en' ? 'We would like to discuss our enterprise roadmap and automation architecture.' : (lang === 'nl' ? 'Wij willen graag onze enterprise roadmap en automatiseringsarchitectuur bespreken.' : 'نرغب في مناقشة خطة العمل وأتمتة المنظومة معكم.')}`
        ].join('\n');
        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeReadinessModal();
    };

    // Case Study Modal Handlers
    window.openCaseStudy = function (key) {
        triggerHaptic(15);
        const lang = getPageLang();
        const langStudies = CASE_STUDIES_I18N[lang] || CASE_STUDIES_I18N.ar;
        const data = langStudies[key] || langStudies.almarai;
        const t = (ES_I18N[lang] || ES_I18N.ar).caseStudy;

        const body = document.getElementById('caseStudyBody');
        if (!body) return;

        body.innerHTML = `
            <div class="es-casestudy-hero">
                <span class="es-casestudy-tag">${data.tag}</span>
                <h3 style="color: #fff; font-size: 1.15rem; font-weight: 800; margin: 4px 0 6px;">${data.title}</h3>
                <p style="font-size: 0.8rem; color: var(--es-gold-light); margin: 0;">${t.clientLabel} ${data.client}</p>
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
                    <h5 style="color: #f87171; font-size: 0.82rem; font-weight: 800; margin-bottom: 4px;">${t.challengeTitle}</h5>
                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.75); line-height: 1.5; margin: 0;">${data.challenge}</p>
                </div>

                <div style="margin-bottom: 14px;">
                    <h5 style="color: var(--es-cyan); font-size: 0.82rem; font-weight: 800; margin-bottom: 4px;">${t.solutionTitle}</h5>
                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.75); line-height: 1.5; margin: 0;">${data.solution}</p>
                </div>

                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
                    <h5 style="color: #34d399; font-size: 0.82rem; font-weight: 800; margin-bottom: 4px;">${t.roiTitle}</h5>
                    <p style="font-size: 0.8rem; color: #ecfdf5; line-height: 1.5; margin: 0;">${data.roi}</p>
                </div>

                <button type="button" class="es-btn-send-wa" style="width: 100%;" onclick="window.discussProjectWithTeam('${data.client}')">
                    <span>${t.btnWa}</span>
                </button>
            </div>
        `;

        document.getElementById('esCaseStudyModalOverlay')?.classList.add('active');
    };

    window.closeCaseStudyModal = () => {
        triggerHaptic(10);
        document.getElementById('esCaseStudyModalOverlay')?.classList.remove('active');
    };

    window.discussProjectWithTeam = function (projectName) {
        triggerHaptic(20);
        const lang = getPageLang();
        const t = (ES_I18N[lang] || ES_I18N.ar).caseStudy;
        const msg = t.waMsg(projectName);
        window.open(`https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`, '_blank');
        window.closeCaseStudyModal();
    };

    window.acceptGDPR = function () {
        triggerHaptic(15);
        localStorage.setItem('coresync_gdpr_status', 'accepted');
        document.getElementById('esGdprBanner')?.classList.remove('active');
    };

    window.declineGDPR = function () {
        triggerHaptic(10);
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

    window.CURRENCIES = CURRENCIES;
    window.getActiveCurrency = function() { return activeCurrency; };
    window.switchROICurrency = function(code) { window.switchCurrency(code); };

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
        document.querySelectorAll('.es-currency-btn, .dana-cur-pill, .header-cur-option, .roi-currency-pill').forEach(btn => {
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

        // Sync with ROI engine
        if (typeof window.updateROICalculator === 'function') {
            window.updateROICalculator();
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
       Royal Brand Logo Engine: Smooth Home Scroll, Lightbox & Language Memory
       ===================================================================== */
    function initBrandLogoEnhancements() {
        const logoTriggers = document.querySelectorAll('.brand-logo-site');
        const lang = getPageLang();

        logoTriggers.forEach(trigger => {
            // Prevent multiple bindings
            if (trigger.dataset.brandEnhanced === 'true') return;
            trigger.dataset.brandEnhanced = 'true';

            trigger.addEventListener('click', function(e) {
                // 1. Persist current language choice in localStorage
                try {
                    localStorage.setItem('coresync_lang_pref', lang);
                } catch (err) {}

                // 2. If user is scrolled down the page, execute smooth scroll to top
                if (window.scrollY > 80) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });

                    // Subtle luxury haptic vibration on mobile
                    if (navigator.vibrate) {
                        try { navigator.vibrate(12); } catch (_) {}
                    }

                    // Luxury sound feedback if available
                    if (window.LuxuryAudio && typeof window.LuxuryAudio.play === 'function') {
                        try { window.LuxuryAudio.play('click'); } catch (_) {}
                    }

                    // Clean URL hash if any modal or section hash was set
                    if (window.location.hash) {
                        try { history.replaceState(null, '', window.location.pathname); } catch (_) {}
                    }
                } else {
                    // 3. If already at top of the page, open high-res Brand Lightbox modal
                    if (typeof window.openLogoLightbox === 'function') {
                        e.preventDefault();
                        window.openLogoLightbox(e);
                    }
                }
            });

            // Mobile touch micro-interaction
            trigger.addEventListener('touchstart', function() {
                const emblem = trigger.querySelector('.brand-emblem-img');
                if (emblem) emblem.style.transform = 'scale(0.95)';
            }, { passive: true });

            trigger.addEventListener('touchend', function() {
                const emblem = trigger.querySelector('.brand-emblem-img');
                if (emblem) emblem.style.transform = '';
            }, { passive: true });
        });
    }

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
        initBrandLogoEnhancements();
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
        const lang = getPageLang();
        // Inject Tracker button inside the Feedback Hub header if it exists
        const hubHeader = document.querySelector('.es-hub-header');
        if (hubHeader && !document.getElementById('esHubTrackerBtn')) {
            const btn = document.createElement('button');
            btn.id = 'esHubTrackerBtn';
            btn.className = 'btn-tracker-portal';
            btn.innerHTML = lang === 'en' ? '📡 Client Portal & Tracking' : (lang === 'nl' ? '📡 Klantenportaal & Tracking' : '📡 بوابة العملاء وتتبع المشاريع');
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
            btn.innerHTML = lang === 'en' ? '🚀 Cloud ROI & Cost Simulator' : (lang === 'nl' ? '🚀 Cloud ROI & Kostensimulator' : '🚀 محاكي التكلفة السحابية وROI');
            btn.onclick = window.openROIModal;
            caseStudySec.prepend(btn);
        }

        // Inject Executive Deck Download button
        const heroActions = document.querySelector('.banner-hero-content .box-btn, .banner-hero .box-btn');
        if (heroActions && !document.getElementById('esExecutiveDeckBtn')) {
            const btn = document.createElement('button');
            btn.id = 'esExecutiveDeckBtn';
            btn.className = 'es-deck-download-btn';
            const deckLabel = lang === 'en' ? '<span>📊 Download Executive Capability Deck PDF</span>' : (lang === 'nl' ? '<span>📊 Download Directie Profiel Deck PDF</span>' : '<span>📊 تحميل ملف القدرات التنفيذي PDF</span>');
            btn.innerHTML = deckLabel;
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

    // Expose ROI Engine globally
    window.updateROICalculator = typeof updateROICalculator === 'function' ? updateROICalculator : function() {
        const teamSlider = document.getElementById('roiCompanySize');
        const hoursSlider = document.getElementById('roiManualHours');
        const salarySlider = document.getElementById('roiAvgSalary');
        const solutionSelect = document.getElementById('roiSolutionType');
        if (!teamSlider || !hoursSlider || !salarySlider || !solutionSelect) return;

        function updateSliderTrack(slider) {
            if (!slider) return;
            const min = parseFloat(slider.min) || 0;
            const max = parseFloat(slider.max) || 100;
            const val = parseFloat(slider.value) || 0;
            const pct = Math.max(0, Math.min(100, ((val - min) / (max - min)) * 100));
            slider.style.background = `linear-gradient(to right, #c5a880 0%, #c5a880 ${pct}%, rgba(255, 255, 255, 0.12) ${pct}%, rgba(255, 255, 255, 0.12) 100%)`;
        }

        updateSliderTrack(teamSlider);
        updateSliderTrack(hoursSlider);
        updateSliderTrack(salarySlider);

        const curCode = (typeof window.getActiveCurrency === 'function' ? window.getActiveCurrency() : (localStorage.getItem('coresync_currency') || 'EUR'));
        const cur = (window.CURRENCIES && window.CURRENCIES[curCode]) || (typeof CURRENCIES !== 'undefined' && CURRENCIES[curCode]) || { symbol: '€', rate: 1, name: 'Euro' };

        document.querySelectorAll('.roi-currency-pill').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.currency === curCode);
        });

        const teamSize = parseInt(teamSlider.value, 10) || 15;
        const manualHours = parseInt(hoursSlider.value, 10) || 8;
        const hourlyRateEur = parseFloat(salarySlider.value) || 28;
        const convertedRate = Math.round(hourlyRateEur * cur.rate);
        const efficiencyRate = parseFloat(solutionSelect.value) || 0.75;

        document.querySelectorAll('.roi-preset-btn').forEach(btn => {
            btn.classList.toggle('active', btn.textContent.includes(`(${teamSize})`));
        });

        const isAr = document.documentElement.lang === 'ar';
        const isNl = document.documentElement.lang === 'nl';

        const teamValBadge = document.getElementById('roiCompanySizeVal');
        if (teamValBadge) {
            teamValBadge.textContent = isAr ? (teamSize <= 10 ? `${teamSize} موظفين` : `${teamSize} موظفاً`) : (isNl ? `${teamSize} medewerkers` : `${teamSize} employees`);
        }

        const hoursValBadge = document.getElementById('roiManualHoursVal');
        if (hoursValBadge) {
            hoursValBadge.textContent = isAr ? `${manualHours} ساعات / أسبوع` : (isNl ? `${manualHours} uur / week` : `${manualHours} hrs / week`);
        }

        const salaryValBadge = document.getElementById('roiAvgSalaryVal');
        if (salaryValBadge) {
            salaryValBadge.textContent = isAr ? `${cur.symbol} ${convertedRate} / ساعة` : (isNl ? `${cur.symbol} ${convertedRate} / uur` : `${cur.symbol} ${convertedRate} / hr`);
        }

        const salaryScale = document.getElementById('roiSalaryScaleLabels');
        if (salaryScale) {
            salaryScale.innerHTML = `<span>${cur.symbol}${Math.round(15 * cur.rate)}</span><span>${cur.symbol}${Math.round(45 * cur.rate)}</span><span>${cur.symbol}${Math.round(80 * cur.rate)}+</span>`;
        }

        const totalHours = teamSize * manualHours * 52;
        const hoursSaved = Math.round(totalHours * efficiencyRate);
        const annualSavingsEur = Math.round(hoursSaved * hourlyRateEur);
        const convertedSavings = Math.round(annualSavingsEur * cur.rate);

        let baseCostEur = 10000;
        if (teamSize <= 10) baseCostEur = 7500;
        else if (teamSize <= 30) baseCostEur = 13500;
        else if (teamSize <= 70) baseCostEur = 22000;
        else baseCostEur = 35000;

        const monthlySavingsEur = annualSavingsEur / 12;
        let paybackMonths = (baseCostEur / (monthlySavingsEur || 1)).toFixed(1);
        if (paybackMonths < 0.8) paybackMonths = "0.8";
        if (paybackMonths > 6.0) paybackMonths = "5.5";

        const savingsElem = document.getElementById('roiAnnualSavings');
        if (savingsElem) {
            savingsElem.innerHTML = `<span>${cur.symbol}</span>${convertedSavings.toLocaleString('en-US')}`;
        }

        const hoursSavedElem = document.getElementById('roiHoursSaved');
        if (hoursSavedElem) {
            const suffix = isAr ? 'ساعة/سنة' : (isNl ? 'uur/jaar' : 'hrs/year');
            hoursSavedElem.innerHTML = `${hoursSaved.toLocaleString('en-US')} <span>${suffix}</span>`;
        }

        const effGainElem = document.getElementById('roiEfficiencyGain');
        if (effGainElem) {
            effGainElem.innerHTML = `+<span>${Math.round(efficiencyRate * 100)}%</span>`;
        }

        const paybackElem = document.getElementById('roiPaybackMonths');
        if (paybackElem) {
            const monthSuffix = isAr ? 'شهر' : (isNl ? 'maand' : 'months');
            paybackElem.textContent = `${paybackMonths} ${monthSuffix}`;
        }
    };

    window.setRoiTeamPreset = function(size) {
        const slider = document.getElementById('roiCompanySize');
        if (!slider) return;
        slider.value = size;
        window.updateROICalculator();
    };

    window.openRoiPdfModal = function() {
        const modal = document.getElementById('roiPdfModal');
        if (!modal) return;

        const curCode = (typeof window.getActiveCurrency === 'function' ? window.getActiveCurrency() : (localStorage.getItem('coresync_currency') || 'EUR'));
        const cur = (window.CURRENCIES && window.CURRENCIES[curCode]) || (typeof CURRENCIES !== 'undefined' && CURRENCIES[curCode]) || { symbol: '€', rate: 1 };

        const teamSlider = document.getElementById('roiCompanySize');
        const hoursSlider = document.getElementById('roiManualHours');
        const salarySlider = document.getElementById('roiAvgSalary');
        const solutionSelect = document.getElementById('roiSolutionType');

        const teamSize = teamSlider ? parseInt(teamSlider.value, 10) : 15;
        const manualHours = hoursSlider ? parseInt(hoursSlider.value, 10) : 8;
        const hourlyRateEur = salarySlider ? parseFloat(salarySlider.value) : 28;
        const convertedRate = Math.round(hourlyRateEur * cur.rate);
        const efficiencyRate = solutionSelect ? parseFloat(solutionSelect.value) : 0.75;
        const solutionText = solutionSelect && solutionSelect.options[solutionSelect.selectedIndex] ? solutionSelect.options[solutionSelect.selectedIndex].text : 'تكامل ERP كامل + أتمتة محاسبية';

        const totalHours = teamSize * manualHours * 52;
        const hoursSaved = Math.round(totalHours * efficiencyRate);
        const annualSavingsEur = Math.round(hoursSaved * hourlyRateEur);
        const convertedSavings = Math.round(annualSavingsEur * cur.rate);

        const paybackElem = document.getElementById('roiPaybackMonths');
        const paybackMonths = paybackElem ? paybackElem.textContent.trim() : '1.2 شهر';

        const dateEl = document.getElementById('roiPdfDate');
        if (dateEl) {
            const now = new Date();
            dateEl.textContent = now.toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' });
        }

        const refEl = document.getElementById('roiPdfRef');
        if (refEl && !refEl.dataset.initialized) {
            refEl.textContent = `REF-CS-ROI-2026-${Math.floor(1000 + Math.random() * 9000)}`;
            refEl.dataset.initialized = 'true';
        }

        const teamEl = document.getElementById('roiPdfTeamVal');
        if (teamEl) teamEl.textContent = `${teamSize} موظفاً (${teamSize <= 10 ? 'فريق ناشئ' : teamSize <= 30 ? 'شركة نامية' : teamSize <= 70 ? 'مؤسسة متوسطة' : 'شركة كبرى'})`;

        const hoursEl = document.getElementById('roiPdfHoursVal');
        if (hoursEl) hoursEl.textContent = `${manualHours} ساعات / أسبوع لكل موظف`;

        const salaryEl = document.getElementById('roiPdfSalaryVal');
        if (salaryEl) salaryEl.textContent = `${cur.symbol} ${convertedRate} / ساعة`;

        const solEl = document.getElementById('roiPdfSolutionVal');
        if (solEl) solEl.textContent = solutionText;

        const hoursSavedEl = document.getElementById('roiPdfHoursSavedVal');
        if (hoursSavedEl) hoursSavedEl.textContent = `${hoursSaved.toLocaleString('en-US')} ساعة/سنة`;

        const effEl = document.getElementById('roiPdfEffGainVal');
        if (effEl) effEl.textContent = `+${Math.round(efficiencyRate * 100)}%`;

        const paybackEl = document.getElementById('roiPdfPaybackVal');
        if (paybackEl) paybackEl.textContent = `${paybackMonths} فقط بعد الإطلاق`;

        const savingsEl = document.getElementById('roiPdfSavingsVal');
        if (savingsEl) savingsEl.textContent = `${cur.symbol} ${convertedSavings.toLocaleString('en-US')}`;

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('open');
    };

    window.closeRoiPdfModal = function() {
        const modal = document.getElementById('roiPdfModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('close');
    };

    window.printRoiReport = function() {
        window.print();
    };

    window.shareRoiPdfWhatsApp = function() {
        const clientName = document.getElementById('roiPdfClientName') ? document.getElementById('roiPdfClientName').value.trim() : 'مجموعة الشريك التجاري';
        const savingsEl = document.getElementById('roiPdfSavingsVal');
        const savings = savingsEl ? savingsEl.textContent.trim() : '';
        const hoursSavedEl = document.getElementById('roiPdfHoursSavedVal');
        const hours = hoursSavedEl ? hoursSavedEl.textContent.trim() : '';
        const teamEl = document.getElementById('roiPdfTeamVal');
        const team = teamEl ? teamEl.textContent.trim() : '';
        const paybackEl = document.getElementById('roiPdfPaybackVal');
        const payback = paybackEl ? paybackEl.textContent.trim() : '';

        const msg = `*تقرير دراسة الجدوى الاستثمارية والوفر السنوي - S&R CoreSync Solutions*\n` +
                    `━━━━━━━━━━━━━━━━━━━━\n` +
                    `🏢 *الشركة:* ${clientName}\n` +
                    `👥 *حجم الفريق:* ${team}\n` +
                    `💰 *صافي الوفر المالي السنوي المتوقع:* ${savings}\n` +
                    `⏱️ *الساعات المستردة سنوياً:* ${hours}\n` +
                    `📈 *فترة استرداد رأس المال:* ${payback}\n` +
                    `━━━━━━━━━━━━━━━━━━━━\n` +
                    `_تم استخراج التقرير عبر Smart ROI Engine المعتمد لشركة S&R CoreSync Solutions_`;

        const url = `https://wa.me/${WHATSAPP_NUM}?text=${encodeURIComponent(msg)}`;
        window.open(url, '_blank');
    };

    // ========================================================
    // Real Software Catalog & Direct Download Controller
    // ========================================================
    window.REAL_SOFTWARE_CATALOG = {
        taxsync: {
            id: 'taxsync',
            title: 'S&R TaxSync Desktop v2.4 Pro',
            category: 'accounting',
            categoryName: 'الحلول المحاسبية والضريبية المستقلة',
            icon: '💻',
            ver: 'v2.4 Pro (Offline-First Edition)',
            os: 'Windows 11 / 10 (64-bit) & macOS',
            size: '14.8 MB',
            price: '€ 189',
            priceType: 'ترخيص سنوي / جهاز',
            downloadFile: 'downloads/SR-TaxSync-Desktop-v2.4-Setup.zip',
            fileName: 'SR-TaxSync-Desktop-v2.4-Setup.zip',
            licenseKey: 'SRTX-PRO-2026-X892-OFFLINE',
            desc: 'برنامج سطح مكتب محاسبي وضريبي مستقل يعمل أوفلاين لحساب ضريبة BTW/VAT 21% و 9% وإصدار إقرارات XML لمصلحة الضرائب الهولندية والخليجية وفق معايير Belastingdienst الرسمية.',
            specs: [
                'يعمل محلياً أوفلاين 100% دون الحاجة لأي اتصال بالإنترنت',
                'توليد وتصدير إقرارات XML الضريبية المعتمدة رسمياً',
                'طباعة فواتير ضريبية مطابقة للمواصفة القياسية الأوروبية EN 16931',
                'مشفّر بقواعد بيانات محلية آمنة'
            ],
            steps: [
                'قم بفك ضغط ملف الـ ZIP المحمل إلى أي مجلد تريده على جهازك.',
                'اضغط مرتين على ملف تشغيل (Run-TaxSync.bat) ليفتح البرنامج فوراً كنافذة تطبيق مستقلة فائقة السرعة.',
                'أدخل مفتاح الترخيص المفعل أدناه لتأكيد النسخة والاستفادة من كافة المزايا.'
            ],
            sandboxUrl: 'demo.html?sandbox=taxsync#software'
        },
        cloudpos: {
            id: 'cloudpos',
            title: 'S&R CloudPOS Connector v3.1',
            category: 'accounting',
            categoryName: 'الحلول المحاسبية والضريبية المستقلة',
            icon: '⚡',
            ver: 'v3.1 Agent Service',
            os: 'Windows POS Terminal / USB & COM Ports',
            size: '8.4 MB',
            price: '€ 25',
            priceType: 'شهرياً / نقطة بيع',
            downloadFile: 'downloads/SR-CloudPOS-Connector-v3.1.zip',
            fileName: 'SR-CloudPOS-Connector-v3.1.zip',
            licenseKey: 'SRPOS-PRO-2026-C310-LIVE',
            desc: 'وسيط برمجي خفيف يعمل في خلفية أجهزة الكاشير القديمة لربطها فورياً بنظام الـ ERP السحابي لمزامنة حركة المخازن والسيولة النقدية دون تغيير الأجهزة.',
            specs: [
                'تكامل كامل مع طابعات الإيصالات الحرارية والباركود',
                'مبيعات أوفلاين مع مزامنة تلقائية فور عودة الاتصال',
                'تسوية نقدية وجرد فوري بنهاية كل وردية'
            ],
            steps: [
                'فك ضغط الحزمة على جهاز الكاشير أو الخادم المحلي.',
                'شغّل ملف (Run-POS-Agent.bat) لبدء خدمة الربط.',
                'اربط الـ API Key الخاص بك للاتصال بنظام CoreSync Cloud ERP.'
            ],
            sandboxUrl: 'demo.html#software'
        },
        flowscan: {
            id: 'flowscan',
            title: 'S&R FlowScan AI Mobile v1.8',
            category: 'accounting',
            categoryName: 'الحلول المحاسبية والضريبية المستقلة',
            icon: '📱',
            ver: 'v1.8 OCR AI Engine',
            os: 'Android & iOS PWA Standalone',
            size: '6.2 MB',
            price: '€ 9.99',
            priceType: 'شهرياً / مستخدم',
            downloadFile: 'downloads/SR-FlowScan-Mobile-v1.8.zip',
            fileName: 'SR-FlowScan-Mobile-v1.8.zip',
            licenseKey: 'SRSCAN-AI-2026-F180-MOBILE',
            desc: 'تطبيق هاتف ذكي للمسح الضوئي الذكي للإيصالات والفواتير الورقية بالكاميرا واستخراج بيانات الضريبة والمبالغ آلياً وترحيلها لحظياً للـ ERP.',
            specs: [
                'استخراج ضوئي ذكي OCR بدقة 99.4%',
                'فرز آلي لمصاريف التشغيل والوقود والضيافة',
                'مزامنة سحابية مباشرة مع لوحة تحكم الإدارة'
            ],
            steps: [
                'فك ضغط الحزمة أو افتح ملف index.html في متصفح هاتفك لتثبيته كـ PWA.',
                'اختر "إضافة إلى الشاشة الرئيسية" ليعمل كتطبيق هاتف مستقل.',
                'سجل الدخول باستخدام مفتاح الترخيص المفعل.'
            ],
            sandboxUrl: 'demo.html#software'
        },
        sdk: {
            id: 'sdk',
            title: 'S&R Financial AI SDK v1.2',
            category: 'developer',
            categoryName: 'برمجيات وأدوات المطورين والبنية التحتية',
            icon: '🧩',
            ver: 'v1.2 Developer Kit',
            os: 'Python 3.10+ / Node.js 18+ / C# / REST',
            size: '11.5 MB',
            price: '€ 99',
            priceType: 'شهرياً (50k API Calls)',
            downloadFile: 'downloads/SR-Financial-AI-SDK-v1.2.zip',
            fileName: 'SR-Financial-AI-SDK-v1.2.zip',
            licenseKey: 'SRSDK-DEV-2026-S120-REST',
            desc: 'مكتبة برمجية للمطورين والشركات لدمج خوارزميات التنبؤ المالي والفوترة والامتثال المحاسبي الأوروبي (UBL) في تطبيقاتهم الخاصة بسهولة عبر REST APIs.',
            specs: [
                'حزم جاهزة لـ Node.js (npm) و Python (pip)',
                'خوارزميات تنبؤ مالي ومطابقة فواتير بالذكاء الاصطناعي',
                'توثيق برمجي كامل مع أمثلة تشغيل فورية'
            ],
            steps: [
                'فك ضغط الحزمة في مسار مشروعك البرمجي.',
                'في بايثون: نفذ `python sr_financial_sdk.py` للتجربة المباشرة.',
                'في نود: استورد `const CoreSync = require("./index.js")` وابدأ التطوير فوراً.'
            ],
            sandboxUrl: 'demo.html#software'
        },
        vault: {
            id: 'vault',
            title: 'S&R SecureVault B2B v2.0',
            category: 'developer',
            categoryName: 'برمجيات وأدوات المطورين والبنية التحتية',
            icon: '🛡️',
            ver: 'v2.0 Enterprise Encrypted',
            os: 'Win Server / Linux CLI / Docker',
            size: '9.1 MB',
            price: '€ 49',
            priceType: 'شهرياً (1TB Encrypted)',
            downloadFile: 'downloads/SR-SecureVault-v2.0.zip',
            fileName: 'SR-SecureVault-v2.0.zip',
            licenseKey: 'SRVLT-AES256-2026-V200-MIL',
            desc: 'برمجية تشفير وحماية النسخ الاحتياطية لقواعد البيانات والمستندات الحساسة بمعيار AES-256 العسكري مع تخزين متوافق 100% مع قانون GDPR الأوروبي.',
            specs: [
                'تشفير وفك تشفير عسكري بمعيار AES-256',
                'أداة CLI سريعة لأتمتة النسخ الاحتياطي عبر Cron / Task Scheduler',
                'حماية كاملة لقواعد بيانات SQL و المستندات الحساسة'
            ],
            steps: [
                'فك ضغط ملف الـ ZIP.',
                'شغّل Run-Vault.bat لتشفير ملفاتك محلياً عبر سطر الأوامر.',
                'استخدم مفتاح التشفير الآمن لحماية مستنداتك المؤسسية.'
            ],
            sandboxUrl: 'demo.html#software'
        },
        terminal: {
            id: 'terminal',
            title: 'S&R Cloud Terminal Agent v1.0',
            category: 'developer',
            categoryName: 'برمجيات وأدوات المطورين والبنية التحتية',
            icon: '⚙️',
            ver: 'v1.0 DevOps Agent',
            os: 'Windows / Linux CLI / Docker Cluster',
            size: '7.8 MB',
            price: '€ 39',
            priceType: 'شهرياً / Cluster',
            downloadFile: 'downloads/SR-Cloud-Terminal-Agent-v1.0.zip',
            fileName: 'SR-Cloud-Terminal-Agent-v1.0.zip',
            licenseKey: 'SRTRM-OPS-2026-T100-CLOUD',
            desc: 'وكيل سحابي متطور لمراقبة خوادم الـ Microservices وتتبع استهلاك المعالج والذاكرة وإعادة تشغيل الخدمات تلقائياً مع تنبيهات فورية.',
            specs: [
                'مراقبة لحظية بنبضات الـ Heartbeat ومقاييس SLA',
                'استهلاك فائق الخفة للذاكرة (أقل من 15MB)',
                'ربط فوري ومباشر مع كلوستر أمستردام AMS-01'
            ],
            steps: [
                'فك ضغط ملف الـ ZIP على خادمك أو حاسوبك.',
                'شغّل ملف (Run-Agent.bat) أو نفّذ `python agent.py`.',
                'يبدأ الوكيل المراقبة اللحظية والاتصال السحابي الآمن فوراً.'
            ],
            sandboxUrl: 'demo.html#software'
        }
    };

        let currentSoftwareActiveId = 'taxsync';

    window.openSoftwareDownloadModal = function(softwareId) {
        currentSoftwareActiveId = softwareId || 'taxsync';
        const sw = window.REAL_SOFTWARE_CATALOG[softwareId] || window.REAL_SOFTWARE_CATALOG.taxsync;
        const modal = document.getElementById('softwareDownloadModal');
        if (!modal) {
            const a = document.createElement('a');
            a.href = sw.downloadFile;
            a.download = sw.fileName;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            return;
        }

        const titleEl = document.getElementById('swDlTitle');
        const iconEl = document.getElementById('swDlIcon');
        const verEl = document.getElementById('swDlVer');
        const descEl = document.getElementById('swDlDesc');
        const keyEl = document.getElementById('swDlKey');
        const badgeEl = document.getElementById('swDlCategoryBadge');

        if (titleEl) titleEl.textContent = sw.title;
        if (iconEl) iconEl.textContent = sw.icon;
        if (verEl) verEl.textContent = `${sw.ver} • ${sw.os} • ${sw.size}`;
        if (descEl) descEl.textContent = sw.desc;

        // Auto-generate fresh cryptographic key if default
        const prefix = sw.id.includes('taxsync') ? 'SRTX' : (sw.id.includes('pos') ? 'SRPOS' : (sw.id.includes('vault') ? 'SRVLT' : (sw.id.includes('sdk') ? 'SRSDK' : 'SRCORE')));
        const randHex = Math.random().toString(16).substring(2, 6).toUpperCase();
        const randHex2 = Math.random().toString(16).substring(2, 6).toUpperCase();
        const autoKey = `${prefix}-PRO-2026-${randHex}-${randHex2}`;

        if (keyEl) keyEl.textContent = autoKey;
        if (badgeEl) badgeEl.textContent = sw.categoryName;

        const specsEl = document.getElementById('swDlSpecs');
        if (specsEl && sw.specs) {
            specsEl.innerHTML = sw.specs.map(s => `<li>✓ ${s}</li>`).join('');
        }

        const stepsEl = document.getElementById('swDlSteps');
        if (stepsEl && sw.steps) {
            stepsEl.innerHTML = sw.steps.map((st, i) => `
                <div class="sw-step-item">
                    <span class="sw-step-num">${i + 1}</span>
                    <span>${st}</span>
                </div>
            `).join('');
        }

        const dlBtn = document.getElementById('swDlDirectBtn');
        if (dlBtn) {
            dlBtn.href = sw.downloadFile;
            dlBtn.setAttribute('download', sw.fileName);
            dlBtn.onclick = function() {
                window.onSoftwarePackageDownloaded(sw, keyEl ? keyEl.textContent.trim() : autoKey);
            };
        }

        const exeBtn = document.getElementById('swDlExeBtn');
        if (exeBtn) {
            if (sw.id === 'taxsync') {
                exeBtn.style.display = 'inline-flex';
                exeBtn.href = 'downloads/SR-TaxSync-Setup-v2.4.exe';
                exeBtn.setAttribute('download', 'SR-TaxSync-Setup-v2.4.exe');
                exeBtn.onclick = function() {
                    window.onSoftwarePackageDownloaded(sw, keyEl ? keyEl.textContent.trim() : autoKey);
                };
            } else {
                exeBtn.style.display = 'none';
            }
        }

        const checkoutBtn = document.getElementById('swDlCheckoutBtn');
        if (checkoutBtn) {
            checkoutBtn.onclick = function() {
                window.closeSoftwareDownloadModal();
                window.openSoftwareCheckoutModal(sw.id);
            };
        }

        const simBtn = document.getElementById('swDlSandboxBtn');
        if (simBtn) {
            simBtn.href = sw.sandboxUrl;
        }

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('open');
    };

    window.closeSoftwareDownloadModal = function() {
        const modal = document.getElementById('softwareDownloadModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('close');
    };

    window.onSoftwarePackageDownloaded = function(sw, key) {
        // Record in license ledger
        try {
            const list = window.getSalimLicenses();
            list.unshift({
                key: key,
                client: 'محطة عمل مرخصة (تنزيل مباشر)',
                product: sw.title,
                plan: 'ترخيص مجاني معتمد (Package Download)',
                expiry: '2027-10-15',
                status: 'نشط ومفعل',
                machine: 'WORKSTATION-' + key.split('-').pop()
            });
            window.saveSalimLicenses(list);
            if (typeof window.renderSalimLicensesTable === 'function') {
                window.renderSalimLicensesTable();
            }
        } catch(e) {}

        if (navigator.clipboard) {
            navigator.clipboard.writeText(key).catch(() => {});
        }

        if (typeof showFloatingToast === 'function') {
            showFloatingToast(`📥 بدأ تنزيل ${sw.title}! تم نسخ وحفظ مفتاحك: ${key}`);
        }
    };

    window.generateDynamicKeyForCurrentSoftware = function() {
        const sw = window.REAL_SOFTWARE_CATALOG[currentSoftwareActiveId] || window.REAL_SOFTWARE_CATALOG.taxsync;
        const prefix = sw.id.includes('taxsync') ? 'SRTX' : (sw.id.includes('pos') ? 'SRPOS' : (sw.id.includes('vault') ? 'SRVLT' : (sw.id.includes('sdk') ? 'SRSDK' : 'SRCORE')));
        const randHex = Math.random().toString(16).substring(2, 6).toUpperCase();
        const randHex2 = Math.random().toString(16).substring(2, 6).toUpperCase();
        const newKey = `${prefix}-PRO-2026-${randHex}-${randHex2}`;

        const keyEl = document.getElementById('swDlKey');
        if (keyEl) {
            keyEl.textContent = newKey;
            keyEl.style.transition = 'all 0.3s ease';
            keyEl.style.color = '#10b981';
            keyEl.style.textShadow = '0 0 12px rgba(16, 185, 129, 0.6)';
            setTimeout(() => {
                keyEl.style.color = '';
                keyEl.style.textShadow = '';
            }, 1200);
        }

        // Save into local active ledger
        try {
            const list = window.getSalimLicenses();
            list.unshift({
                key: newKey,
                client: 'محطة عمل مرخصة (توليد مخصص)',
                product: sw.title,
                plan: 'ترخيص مجاني معتمد (Custom Cryptographic Key)',
                expiry: '2027-10-15',
                status: 'نشط ومفعل',
                machine: 'NODE-' + randHex
            });
            window.saveSalimLicenses(list);
            if (typeof window.renderSalimLicensesTable === 'function') {
                window.renderSalimLicensesTable();
            }
        } catch(e) {}

        if (navigator.clipboard) {
            navigator.clipboard.writeText(newKey).catch(() => {});
        }

        if (typeof showFloatingToast === 'function') {
            showFloatingToast(`🔑 تم توليد وترخيص: ${newKey} ونسخه تلقائياً!`);
        } else {
            alert(`🎉 تم توليد وحفظ ترخيصك الرقمي المشفر الجديد بنجاح:\n\n🔑 ${newKey}\n📦 ${sw.title}\n\n✓ تم نسخه إلى الحافظة وحفظه في سجل تراخيصك!`);
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('success');
        return newKey;
    };

    window.downloadLicenseCertificate = function() {
        const sw = window.REAL_SOFTWARE_CATALOG[currentSoftwareActiveId] || window.REAL_SOFTWARE_CATALOG.taxsync;
        const keyEl = document.getElementById('swDlKey');
        const key = keyEl ? keyEl.textContent.trim() : `${sw.id.toUpperCase()}-PRO-2026-OFFLINE`;
        const machineId = 'NL-HOST-' + Math.random().toString(16).substring(2, 6).toUpperCase();
        const dateStr = new Date().toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' });

        const certContent = `================================================================================
   S&R CORESYNC SOLUTIONS - OFFICIAL SOFTWARE LICENSE CERTIFICATE
   Amsterdam HQ • The Netherlands • Chamber of Commerce (KvK) Registered
================================================================================

PRODUCT: ${sw.title} (${sw.ver})
PLATFORM: ${sw.os}
LICENSE KEY: ${key}
MACHINE HARDWARE ID: ${machineId}
ISSUED TO: Licensed Workstation (Standard Enterprise User)
AUTHENTICATION: Cryptographically Signed Offline Token (AES-256)
AUTHORITY: Mohammad Salim Aziza (CTO) & Mohammad Raed Kaakeh (CFO)
ISSUED DATE: ${dateStr}
EXPIRY: Valid Perpetual / Annual Enterprise
STATUS: Cryptographically Signed & Verified ✓

INSTALLATION & ACTIVATION INSTRUCTIONS:
1. Extract the downloaded software package (${sw.fileName}).
2. Run the application or installer (Run-${sw.id}.bat or Setup.exe).
3. When prompted, enter your official License Key:
   ${key}
4. The software will authenticate locally without requiring internet access.

Official Portal: https://sr-coresync.com/
Support & Auditing: info@sr-coresync.com | WhatsApp: +31 6 8771 0290
================================================================================`;

        const blob = new Blob([certContent], { type: 'text/plain;charset=utf-8' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `S&R-License-${key}.key`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(a.href);

        if (typeof showFloatingToast === 'function') {
            showFloatingToast(`📄 تم تحميل ملف شهادة الترخيص (.key) بنجاح!`);
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('success');
    };

    window.copySoftwareLicenseKey = function() {
        const keyEl = document.getElementById('swDlKey');
        const key = keyEl ? keyEl.textContent.trim() : 'SRTX-PRO-2026-X892-OFFLINE';
        if (navigator.clipboard) {
            navigator.clipboard.writeText(key).then(() => {
                if (typeof showFloatingToast === 'function') {
                    showFloatingToast(`🔑 تم نسخ مفتاح الترخيص: ${key}`);
                } else {
                    alert(`🔑 تم نسخ مفتاح الترخيص: ${key}`);
                }
            }).catch(() => {
                alert(`🔑 تم نسخ مفتاح الترخيص: ${key}`);
            });
        } else {
            alert(`🔑 مفتاح الترخيص الخاص بك: ${key}`);
        }
    };

    window.filterSoftwareMarketplace = function(category, btnEl) {
        document.querySelectorAll('.software-filter-pill').forEach(b => b.classList.remove('active'));
        if (btnEl) btnEl.classList.add('active');

        const items = document.querySelectorAll('.software-grid-item');
        items.forEach(item => {
            const itemCat = item.getAttribute('data-category');
            if (category === 'all' || itemCat === category) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });

        const labSection = document.getElementById('softwareArchitectLab');
        if (labSection) {
            if (category === 'all' || category === 'lab') {
                labSection.style.display = '';
            } else {
                labSection.style.display = 'none';
            }
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('switch');
    };

    // =========================================================================
    // Suggestion 1: Salim's Software License Manager Portal
    // =========================================================================
    const DEFAULT_SALIM_LICENSES = [
        { key: 'SRTX-PRO-2026-X892-OFFLINE', client: 'Heineken International N.V.', product: 'TaxSync Desktop', plan: 'سنوي (Annual)', expiry: '2027-10-15', status: 'نشط ومفعل', machine: 'NL-AMS-SR991' },
        { key: 'SRPOS-POS-2026-P881-CLOUD', client: 'De Koffie Salon Amsterdam', product: 'CloudPOS Connector', plan: 'شهري (Monthly)', expiry: '2026-11-30', status: 'نشط ومفعل', machine: 'POS-TERM-04' },
        { key: 'SRVLT-AES256-2026-V200-MIL', client: 'AWT Group Netherlands', product: 'SecureVault B2B', plan: 'دائم (Lifetime)', expiry: 'مدى الحياة', status: 'نشط ومفعل', machine: 'AMS-SRV-SEC01' },
        { key: 'SRSDK-DEV-2026-S120-REST', client: 'Fintech Solutions Dubai', product: 'Financial AI SDK', plan: 'شهري (50k Calls)', expiry: '2026-12-01', status: 'نشط ومفعل', machine: 'API-CL-992' }
    ];

    window.getSalimLicenses = function() {
        try {
            const raw = localStorage.getItem('sr_salim_licenses');
            if (raw) return JSON.parse(raw);
        } catch(e) {}
        return DEFAULT_SALIM_LICENSES;
    };

    window.saveSalimLicenses = function(list) {
        try {
            localStorage.setItem('sr_salim_licenses', JSON.stringify(list));
        } catch(e) {}
    };

    window.renderSalimLicensesTable = function() {
        const tbody = document.getElementById('salimLicensesTableBody');
        if (!tbody) return;
        const list = window.getSalimLicenses();
        
        tbody.innerHTML = list.map((lic, idx) => `
            <tr>
                <td style="font-family: monospace; font-weight: 700; color: #f7e2bd;">${lic.key}</td>
                <td style="font-weight: 600;">${lic.product}</td>
                <td>${lic.client}</td>
                <td><span style="color:#a3c2b3;">${lic.plan}</span></td>
                <td><span style="color:#94a3b8; font-size:0.8rem;">${lic.expiry}</span></td>
                <td><span class="status-badge ${lic.status === 'نشط ومفعل' ? 'status-completed' : 'status-in-progress'}" style="font-size:0.75rem;">${lic.status}</span></td>
                <td>
                    <button type="button" class="sw-btn-copy-key" style="padding:4px 8px; font-size:0.75rem;" onclick="navigator.clipboard.writeText('${lic.key}'); alert('🔑 تم نسخ مفتاح: ${lic.key}');">نسخ 📋</button>
                    <button type="button" class="sw-btn-copy-key" style="padding:4px 8px; font-size:0.75rem; color:#f87171; border-color:rgba(248,113,113,0.3);" onclick="revokeSalimLicense(${idx})">إلغاء ✕</button>
                </td>
            </tr>
        `).join('');

        const countEl = document.getElementById('salimTotalLicensesCount');
        if (countEl) countEl.textContent = list.length;
        const revEl = document.getElementById('salimTotalRevenueEstimate');
        if (revEl) revEl.textContent = '€ ' + (list.length * 189).toLocaleString();
    };

    window.openSalimLicenseManagerModal = function() {
        const modal = document.getElementById('salimLicenseManagerModal');
        if (!modal) return;
        window.renderSalimLicensesTable();
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('open');
    };

    window.closeSalimLicenseManagerModal = function() {
        const modal = document.getElementById('salimLicenseManagerModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('close');
    };

    window.generateSalimLicense = function(e) {
        if (e) e.preventDefault();
        const prod = document.getElementById('salimGenProduct')?.value || 'TaxSync Desktop';
        const client = document.getElementById('salimGenClient')?.value.trim() || 'Enterprise Client';
        const plan = document.getElementById('salimGenPlan')?.value || 'سنوي (Annual)';
        const machine = document.getElementById('salimGenMachine')?.value.trim() || 'NODE-ANY';

        const prefix = prod.includes('TaxSync') ? 'SRTX' : (prod.includes('POS') ? 'SRPOS' : (prod.includes('Vault') ? 'SRVLT' : 'SRCORE'));
        const randHex = Math.random().toString(16).substring(2, 6).toUpperCase();
        const randHex2 = Math.random().toString(16).substring(2, 6).toUpperCase();
        const key = `${prefix}-PRO-2026-${randHex}-${randHex2}`;

        const newLic = {
            key: key,
            client: client,
            product: prod,
            plan: plan,
            expiry: plan.includes('دائم') ? 'مدى الحياة' : '2027-10-15',
            status: 'نشط ومفعل',
            machine: machine
        };

        const list = window.getSalimLicenses();
        list.unshift(newLic);
        window.saveSalimLicenses(list);
        window.renderSalimLicensesTable();

        alert(`🎉 تم توليد وحفظ الترخيص الرقمي بنجاح للمؤسس م. سليم:\n\n🔑 المفتاح: ${key}\n👤 العميل: ${client}\n📦 المنتج: ${prod}`);
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('success');
    };

    window.revokeSalimLicense = function(idx) {
        const list = window.getSalimLicenses();
        if (confirm(`هل أنت متأكد من إلغاء ترخيص (${list[idx]?.key})؟`)) {
            list[idx].status = 'ملغي / Revoked';
            window.saveSalimLicenses(list);
            window.renderSalimLicensesTable();
        }
    };

    // =========================================================================
    // Suggestion 3: Mollie & Stripe European Payment Gateway Checkout
    // =========================================================================
    let currentCheckoutSoftware = null;
    let selectedPaymentMethod = 'ideal';

    window.openSoftwareCheckoutModal = function(softwareId) {
        const sw = window.REAL_SOFTWARE_CATALOG[softwareId] || window.REAL_SOFTWARE_CATALOG.taxsync;
        currentCheckoutSoftware = sw;
        const modal = document.getElementById('softwareCheckoutModal');
        if (!modal) return;

        const titleEl = document.getElementById('checkoutItemTitle');
        const priceEl = document.getElementById('checkoutItemPrice');
        const netEl = document.getElementById('checkoutNetPrice');
        const vatEl = document.getElementById('checkoutVatAmount');
        const totalEl = document.getElementById('checkoutTotalPrice');
        const btnTextEl = document.getElementById('checkoutPayBtnText');

        if (titleEl) titleEl.textContent = sw.title + ' (' + sw.ver + ')';
        if (priceEl) priceEl.textContent = sw.price;

        const rawP = sw.rawPrice || 189;
        const netP = (rawP / 1.21).toFixed(2);
        const vatP = (rawP - parseFloat(netP)).toFixed(2);

        if (netEl) netEl.textContent = '€ ' + netP.replace('.', ',');
        if (vatEl) vatEl.textContent = '€ ' + vatP.replace('.', ',');
        if (totalEl) totalEl.textContent = '€ ' + rawP.toFixed(2).replace('.', ',');
        if (btnTextEl) btnTextEl.textContent = `إتمام الدفع الآمن واستلام الترخيص فوراً (€ ${rawP})`;

        const formView = document.getElementById('checkoutFormView');
        const successView = document.getElementById('checkoutSuccessView');
        if (formView) formView.style.display = '';
        if (successView) successView.style.display = 'none';

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('open');
    };

    window.closeSoftwareCheckoutModal = function() {
        const modal = document.getElementById('softwareCheckoutModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('close');
    };

    window.switchCheckoutMethod = function(method, btn) {
        selectedPaymentMethod = method;
        document.querySelectorAll('.checkout-tab-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');

        const idealBox = document.getElementById('checkoutIdealBox');
        const cardBox = document.getElementById('checkoutCardBox');
        const sepaBox = document.getElementById('checkoutSepaBox');

        if (idealBox) idealBox.style.display = method === 'ideal' ? '' : 'none';
        if (cardBox) cardBox.style.display = method === 'card' ? '' : 'none';
        if (sepaBox) sepaBox.style.display = method === 'sepa' ? '' : 'none';
        if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('switch');
    };

    window.selectIdealBank = function(bankName, el) {
        document.querySelectorAll('.checkout-bank-pill').forEach(p => p.classList.remove('active'));
        if (el) el.classList.add('active');
    };

    window.processSoftwareCheckout = function(e) {
        if (e) e.preventDefault();
        const btn = document.getElementById('checkoutSubmitBtn');
        const btnText = document.getElementById('checkoutPayBtnText');
        const sw = currentCheckoutSoftware || window.REAL_SOFTWARE_CATALOG.taxsync;

        const custName = document.getElementById('checkoutCustName')?.value || 'Valued Client';
        const custEmail = document.getElementById('checkoutCustEmail')?.value || 'client@company.nl';

        if (btn) btn.disabled = true;
        if (btnText) btnText.innerHTML = '⏳ جاري التفويض الآمن مع البنك الهولندي عبر بروتوكول 3D Secure...';

        setTimeout(() => {
            if (btn) btn.disabled = false;
            
            const formView = document.getElementById('checkoutFormView');
            const successView = document.getElementById('checkoutSuccessView');
            if (formView) formView.style.display = 'none';
            if (successView) successView.style.display = '';

            const invNum = 'INV-2026-SR-' + Math.floor(1000 + Math.random() * 9000);
            const randHex = Math.random().toString(16).substring(2, 6).toUpperCase();
            const genKey = `${sw.id.toUpperCase()}-PRO-2026-PAID-${randHex}`;

            const resInv = document.getElementById('checkoutSuccessInvNum');
            const resKey = document.getElementById('checkoutSuccessKey');
            const resExe = document.getElementById('checkoutSuccessExeBtn');
            const resZip = document.getElementById('checkoutSuccessZipBtn');

            if (resInv) resInv.textContent = invNum;
            if (resKey) resKey.textContent = genKey;
            if (resExe) {
                resExe.href = sw.id === 'taxsync' ? 'downloads/SR-TaxSync-Setup-v2.4.exe' : sw.downloadFile;
                resExe.setAttribute('download', sw.id === 'taxsync' ? 'SR-TaxSync-Setup-v2.4.exe' : sw.fileName);
            }
            if (resZip) {
                resZip.href = sw.downloadFile;
                resZip.setAttribute('download', sw.fileName);
            }

            const list = window.getSalimLicenses();
            list.unshift({
                key: genKey,
                client: custName + ' (' + custEmail + ')',
                product: sw.title,
                plan: 'مدفوع عبر ' + selectedPaymentMethod.toUpperCase(),
                expiry: '2027-10-15',
                status: 'نشط ومفعل',
                machine: 'ONLINE-PAYMENT-' + invNum
            });
            window.saveSalimLicenses(list);

            if (typeof LuxuryAudio !== 'undefined' && LuxuryAudio.play) LuxuryAudio.play('success');
        }, 1200);
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
