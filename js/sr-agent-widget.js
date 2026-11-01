/**
 * ==============================================================================
 * S&R CoreSync Sovereign Agent Floating Widget (Unified Master Edition)
 * ==============================================================================
 * Unifies the legacy Concierge and Enterprise Suite chat into a single master
 * sovereign AI assistant featuring:
 * - Real-time Google Antigravity & SQLite RAG Backend (/api/ai-concierge)
 * - Offline Fallback Engine (32+ Topics, Instant Pricing & Service Knowledge)
 * - Web Speech API: Bilingual Speech-to-Text & Text-to-Speech
 * - Judicial & Business Document Upload (.pdf, .docx, .txt, .md)
 * - Consultation Transcript Export & Session Management
 * ==============================================================================
 */

(function () {
    'use strict';

    if (window.__SR_AGENT_WIDGET_INITIALIZED__) return;
    window.__SR_AGENT_WIDGET_INITIALIZED__ = true;

    // Session Management
    let sessionId = localStorage.getItem('sr_agent_session_id');
    if (!sessionId) {
        sessionId = 'sr_sess_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
        localStorage.setItem('sr_agent_session_id', sessionId);
    }

    const API_ENDPOINT = (typeof localStorage !== 'undefined' && localStorage.getItem('sr_agent_endpoint')) || 'http://127.0.0.1:8000/api/ai-concierge';

    // Auto-inject CSS stylesheet if not present
    if (!document.querySelector('link[href*="sr-agent-widget.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        const isSubDir = window.location.pathname.includes('/insights/') || window.location.pathname.includes('/en/');
        link.href = (isSubDir ? '../css/sr-agent-widget.css' : './css/sr-agent-widget.css') + '?v=20261101';
        document.head.appendChild(link);
    }

    // Unified Offline Knowledge Base (Merged from legacy Concierge & Enterprise Suite)
    const SOVEREIGN_OFFLINE_KB = [
    {
        "tags": "خدمات خدماتكم ماذا تقدمون حلول الشركة تخصص",
        "q": "ما الخدمات التي تقدمونها؟",
        "a": "نغطي ستة مجالات: <strong>الهوية البصرية</strong>، <strong>المواقع والمتاجر</strong>، <strong>البرمجيات السحابية وERP</strong>، <strong>تطبيقات الجوال</strong>، <strong>أتمتة العمليات والذكاء الاصطناعي</strong>، و<strong>الأمن والبنية السحابية</strong>.",
        "actions": [
            {
                "label": "استعرض الخدمات",
                "url": "./index.html#service"
            }
        ]
    },
    {
        "tags": "سعر اسعار تكلفة كم بكم ميزانية باقات الباقات",
        "q": "كم تكلفة الخدمات؟",
        "a": "الأسعار المعلنة: الهوية البصرية <strong>€590</strong> · الموقع <strong>€980</strong> · المتجر <strong>€1,450</strong> · باقة السحابة Core Starter <strong>€1,490</strong> · تهيئة ERP <strong>€1,890</strong> · Enterprise Growth <strong>€2,890</strong> · Core MAX <strong>€4,990</strong>. وتوجد باقة انطلاقة شاملة <strong>€1,990</strong> بدلاً من €3,020.",
        "actions": [
            {
                "label": "كل الباقات",
                "url": "./index.html#pricing"
            }
        ]
    },
    {
        "tags": "هوية شعار لوجو تصميم هوية بصرية براند",
        "q": "كم سعر الهوية البصرية؟",
        "a": "الهوية البصرية المتكاملة <strong>€590</strong>: ثلاثة مفاهيم شعار، دليل هوية كامل، لوحة ألوان وخطوط، قرطاسية وبطاقات، وملفات المصدر. التسليم خلال 7–10 أيام عمل.",
        "actions": [
            {
                "label": "تفاصيل الهوية",
                "url": "./index.html#service"
            }
        ]
    },
    {
        "tags": "موقع مواقع ويب تصميم موقع سعر الموقع",
        "q": "كم سعر الموقع الإلكتروني؟",
        "a": "الموقع الفاخر عالي الأداء <strong>€980</strong>: تصميم متجاوب، سرعة تتجاوز 98%، تهيئة SEO، دعم لغات متعددة، ربط واتساب، واستضافة ونطاق لسنة. التسليم 2–4 أسابيع.",
        "actions": [
            {
                "label": "تفاصيل المواقع",
                "url": "./index.html#service"
            }
        ]
    },
    {
        "tags": "متجر متاجر تجارة الكترونية شوب شوبيفاي سلة",
        "q": "كم سعر المتجر الإلكتروني؟",
        "a": "المتجر الإلكتروني المتكامل <strong>€1,450</strong>: سلة ودفع بخطوة واحدة، iDEAL/Mollie/Stripe/Apple Pay، إدارة مخزون، كوبونات، فواتير متوافقة ضريبياً، وربط محاسبي. التسليم 4–6 أسابيع.",
        "actions": [
            {
                "label": "دليل رفع التحويل",
                "url": "./insights/ecommerce-conversion.html"
            }
        ]
    },
    {
        "tags": "erp نظام تخطيط موارد المؤسسات محاسبة مخزون فواتير",
        "q": "هل تقدمون أنظمة ERP؟",
        "a": "نعم. <strong>ERP Setup €1,890</strong> (تهيئة وربط أساسي)، <strong>Full ERP Sync €3,490</strong> (سلاسل إمداد ورواتب وبنوك)، و<strong>Custom ERP €5,990</strong> (بناء مخصص بالكامل).",
        "actions": [
            {
                "label": "كيف تختار ERP",
                "url": "./insights/erp-selection-2026.html"
            }
        ]
    },
    {
        "tags": "سحابة سحابي cloud برمجية برمجيات منصة saas",
        "q": "ما هي باقات البرمجيات السحابية؟",
        "a": "ثلاث باقات: <strong>Core Starter €1,490</strong> لمنصة أولى، <strong>Enterprise Growth €2,890</strong> مع تطبيقات جوال وأتمتة AI، و<strong>Core MAX Synergy €4,990</strong> لمنظومة مؤسسية متعددة الفروع والعملات.",
        "actions": [
            {
                "label": "مقارنة الباقات",
                "url": "./index.html#pricing"
            }
        ]
    },
    {
        "tags": "ذكاء اصطناعي ai أتمتة rpa شات بوت مساعد",
        "q": "هل تستخدمون الذكاء الاصطناعي؟",
        "a": "نعم: أتمتة RPA، استخراج الفواتير، مساعد ذكي مؤسسي (RAG) يقرأ مستندات شركتك ويجيب مع الاستشهاد، وتحليل تنبؤي. الباقة المؤسسية تشمل نموذجاً سيادياً معزولاً على أنظمتك.",
        "actions": [
            {
                "label": "مقال RAG",
                "url": "./insights/ai-concierge-rag.html"
            }
        ]
    },
    {
        "tags": "أمان امن سيبراني اختراق حماية فحص أمني",
        "q": "هل تقدمون فحصاً أمنياً؟",
        "a": "نعم — <strong>Security &amp; Audit €490</strong>: فحص شامل للثغرات البرمجية والمالية مع تقرير رسمي وتوصيات إصلاح مرتبة بالأولوية.",
        "actions": [
            {
                "label": "اطلب فحصاً",
                "url": "./index.html#contact"
            }
        ]
    },
    {
        "tags": "صيانة دعم شهري corecare sla",
        "q": "هل توجد باقة صيانة شهرية؟",
        "a": "<strong>CoreCare Monthly €149/شهر</strong>: إدارة سحابية، نسخ احتياطي يومي، مراقبة أداء 24/7، ودعم فوري مع اتفاقية مستوى خدمة (SLA).",
        "actions": [
            {
                "label": "تفاصيل الدعم",
                "url": "./index.html#pricing"
            }
        ]
    },
    {
        "tags": "باقة حزمة عرض توفير خصم انطلاقة bundle",
        "q": "هل توجد باقة موحدة بسعر أقل؟",
        "a": "نعم — <strong>باقة الانطلاقة الشاملة €1,990</strong> بدلاً من €3,020 (توفير 34%): الهوية البصرية + الموقع أو المتجر + الربط المحاسبي المالي.",
        "actions": [
            {
                "label": "احجز الباقة",
                "url": "./index.html#pricing"
            }
        ]
    },
    {
        "tags": "مدة وقت كم يستغرق تسليم جاهز متى",
        "q": "كم يستغرق التنفيذ؟",
        "a": "الهوية 7–10 أيام · الموقع 2–4 أسابيع · المتجر 4–6 أسابيع · ERP 3–6 أسابيع. المدة تبدأ من اعتماد المحتوى والتصاميم، لا من تاريخ العرض.",
        "actions": [
            {
                "label": "الأسئلة الشائعة",
                "url": "./index.html#services-faq"
            }
        ]
    },
    {
        "tags": "دفع دفعكم طرق الدفع stripe mollie ideal paypal تحويل",
        "q": "ما طرق الدفع؟",
        "a": "Stripe (بطاقات)، Mollie (iDEAL / Bancontact)، تحويل بنكي SEPA، وPayPal. الفواتير رسمية ومتوافقة مع ضريبة BTW الهولندية.",
        "actions": [
            {
                "label": "الأسعار والفوترة",
                "url": "./index.html#pricing"
            }
        ]
    },
    {
        "tags": "ضريبة vat btw فاتورة محاسبة خصم",
        "q": "هل الأسعار تشمل الضريبة؟",
        "a": "الأسعار باليورو وتُضاف ضريبة <strong>BTW 21%</strong> حيث ينطبق. للشركات المسجلة في هولندا/الاتحاد الأوروبي الضريبة قابلة للخصم، وتصدر فاتورة رسمية متوافقة مع Belastingdienst.",
        "actions": [
            {
                "label": "تفاصيل الفوترة",
                "url": "./index.html#pricing"
            }
        ]
    },
    {
        "tags": "ملكية كود مصدري ملكية الكود حقوق",
        "q": "هل أملك الكود المصدري؟",
        "a": "نعم، <strong>100%</strong>. تسليم الكود المصدري كاملاً مع الوثائق ونقل الملكية — بلا اشتراكات إجبارية ولا قيود على التعديل.",
        "actions": [
            {
                "label": "الأسئلة الشائعة",
                "url": "./index.html#services-faq"
            }
        ]
    },
    {
        "tags": "استضافة دومين نطاق سيرفر هوستنج",
        "q": "هل تشمل الأسعار الاستضافة والدومين؟",
        "a": "باقة الموقع تشمل استضافة سحابية سريعة ونطاقاً مجانياً لسنة. الباقات السحابية تشمل تهيئة واستضافة مُدارة أولية، ثم يمكن الانتقال إلى CoreCare.",
        "actions": [
            {
                "label": "تفاصيل أكثر",
                "url": "./index.html#services-faq"
            }
        ]
    },
    {
        "tags": "لغات لغة ترجمة عربي انجليزي هولندي",
        "q": "هل الموقع يدعم عدة لغات؟",
        "a": "نعم — الموقع الحالي يدعم <strong>29 لغة</strong> مع اتجاه صحيح للعربية والعبرية والفارسية، وتهيئة SEO لكل لغة على حدة.",
        "actions": [
            {
                "label": "شاهد اللغات",
                "url": "./index.html"
            }
        ]
    },
    {
        "tags": "تجربة ديمو عرض تجريبي جرّب",
        "q": "هل يمكنني تجربة النظام قبل الشراء؟",
        "a": "نعم — النظام التجريبي السحابي متاح مباشرة، ويمكن ترتيب بيئة تجريبية ببياناتك لمدة أسبوعين قبل التوقيع.",
        "actions": [
            {
                "label": "افتح العرض التجريبي",
                "url": "./demo.html"
            }
        ]
    },
    {
        "tags": "تواصل اتصال رقم هاتف واتساب بريد ايميل عنوان",
        "q": "كيف أتواصل معكم؟",
        "a": "واتساب: <a href=\"https://wa.me/31618111116?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D9%8B%20S%26R%20CoreSync%D8%8C%20%D8%A3%D9%88%D8%AF%20%D8%A7%D8%B3%D8%AA%D8%B4%D8%A7%D8%B1%D8%A9%20%D8%AA%D9%86%D9%81%D9%8A%D8%B0%D9%8A%D8%A9.\" target=\"_blank\" rel=\"noopener noreferrer\">+31 6 1811 1116</a><br>البريد: <a href=\"mailto:info@sr-coresync.com\">info@sr-coresync.com</a><br>المقر: أمستردام، هولندا.",
        "actions": [
            {
                "label": "نموذج التواصل",
                "url": "./index.html#contact"
            }
        ]
    },
    {
        "tags": "استشارة مجانية حجز موعد اجتماع",
        "q": "هل توجد استشارة مجانية؟",
        "a": "نعم — استشارة تنفيذية <strong>30 دقيقة مجاناً</strong>: نراجع وضعك الحالي ونعطيك خطة عملية واضحة بلا التزام.",
        "actions": [
            {
                "label": "احجز الآن",
                "url": "https://wa.me/31618111116?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D9%8B%20S%26R%20CoreSync%D8%8C%20%D8%A3%D9%88%D8%AF%20%D8%A7%D8%B3%D8%AA%D8%B4%D8%A7%D8%B1%D8%A9%20%D8%AA%D9%86%D9%81%D9%8A%D8%B0%D9%8A%D8%A9."
            }
        ]
    },
    {
        "tags": "مدونة مقالات رؤى insights",
        "q": "هل لديكم مقالات متخصصة؟",
        "a": "نعم — مدونة الرؤى فيها مقالات عن ERP، تكاليف السحابة، RAG، تحويل المتاجر، Zero Trust، وعائد الهوية.",
        "actions": [
            {
                "label": "افتح المدونة",
                "url": "./blog.html"
            }
        ]
    },
    {
        "tags": "شركاء وكيل وكلاء white label ترخيص",
        "q": "هل يوجد برنامج شركاء أو وكلاء؟",
        "a": "نعم — بوابة الشركاء والوكلاء (White-Label) مع تراخيص متعددة الكيانات: خصم 10% لكيانين إلى ثلاثة، و20% لأربعة كيانات أو أكثر.",
        "actions": [
            {
                "label": "بوابة الشركاء",
                "url": "./partner-portal.html"
            }
        ]
    },
    {
        "tags": "خصوصية gdpr بيانات كوكيز",
        "q": "كيف تتعاملون مع الخصوصية؟",
        "a": "نلتزم بلائحة GDPR الأوروبية: لا نبيع بيانات، والقياس مجهول بلا تعريف شخصي، ويمكنك رفض القياس ويبقى الموقع يعمل كاملاً.",
        "actions": [
            {
                "label": "سياسة الخصوصية",
                "url": "./privacy.html"
            }
        ]
    },
    {
        "tags": "تدريب فريق شرح ورشة",
        "q": "هل تقدمون تدريباً للفريق؟",
        "a": "نعم — جلسات تدريب وورشة تشغيل ضمن الباقات المؤسسية، مع وثائق تشغيلية وفيديوهات قصيرة لفريقك.",
        "actions": [
            {
                "label": "الخدمات",
                "url": "./index.html#service"
            }
        ]
    },
    {
        "tags": "تحكيم تحكيمي نزاع محكمة دولية عقد نيويورك فض قضايا 104 arbitration",
        "q": "ما هو مركز التحكيم السيادي التجاري الدولي (المهمة 104)؟",
        "a": "بوابة التحكيم التجاري الدولي تتيح إدارة وفض النزاعات العابرة للحدود متوافقة 100% مع <strong>اتفاقية نيويورك 1958</strong>، مع سجل قضايا بقيمة €12.385M، إيداع طلبات إلكترونية، وتحليل ذكي للقانون والجدارة، ومسودة حكم مختومة تشفيرياً بـ SHA-256 قابلة للتصدير.",
        "actions": [
            {
                "label": "⚖️ بوابة التحكيم الدولي",
                "url": "./sovereign-arbitration-hub.html"
            },
            {
                "label": "لوحة التحكم المركزية",
                "url": "./sovereign-mission-suite-dashboard.html"
            }
        ]
    },
    {
        "tags": "عملات رقمية cbdc بنك مركزي تسوية تسويات ذرية جسر مالي pvp htlc 105",
        "q": "ما هو جسر تسوية العملات الرقمية السيادية (المهمة 105)؟",
        "a": "جسر تسوية متعدد العملات الرقمية للبنوك المركزية (Multi-CBDC Bridge) يدعم 5 عملات رقمية كبرى مع تسوية ذرية فورية (PvP/HTLC) متوافقة مع معيار <strong>ISO 20022 pacs.009</strong> وتوفير فوري في السيولة وحساب العائد التراكمي.",
        "actions": [
            {
                "label": "💳 جسر العملات الرقمية",
                "url": "./multi-cbdc-bridge.html"
            }
        ]
    },
    {
        "tags": "zkp حوسبة سرية بيئة معزولة enclave برهان تشفير خصوصية tee 106",
        "q": "ما هي بيئة الحوسبة السرية وبراهين الصفر (المهمة 106)؟",
        "a": "بيئة الحوسبة السرية (ZKP & Confidential Enclave) تتيح معالجة البيانات الحساسة وفحص الأصول دون كشف القيمة السرية، عبر 3 بيئات عزل موثوقة (TEE) وتوليد براهين صفرية (Zero-Knowledge Proofs) مختومة بالالتزام التشفيري.",
        "actions": [
            {
                "label": "🛡️ بوابة الحوسبة السرية ZKP",
                "url": "./zkp-confidential-enclave.html"
            }
        ]
    },
    {
        "tags": "ادلة جنائية رقمية worm iso 27037 فحص جنائي احراز بصمة 107 forensics",
        "q": "ما هو محرك الأدلة الجنائية الرقمية وخزينة WORM (المهمة 107)؟",
        "a": "مركز الأدلة الجنائية للتقاضي السيادي يوفر مستودعاً حصيناً غير قابل للتعديل (WORM - Write Once, Read Many) متوافقاً مع معيار <strong>ISO/IEC 27037:2012</strong> لتوثيق الأدلة الرقمية وسلسلة الحيازة (Chain of Custody).",
        "actions": [
            {
                "label": "🔬 بوابة الأدلة الجنائية",
                "url": "./digital-forensics-litigation-hub.html"
            }
        ]
    },
    {
        "tags": "ضمان مالي ذكي اسكرو تجميد تحرير ضمانات دفع عقود 107 escrow",
        "q": "ما هو نظام الضمان المالي الذكي (المهمة 107)؟",
        "a": "نظام الضمان المالي الذكي (Smart Milestone Escrow) يربط صرف الدفعات بإنجاز المعالم الفعلية أو أحكام التحكيم، مع إمكانية التجميد التلقائي للضمان (DISPUTE_FROZEN) عند نشوء أي نزاع قضائي.",
        "actions": [
            {
                "label": "💰 بوابة الضمان المالي الذكي",
                "url": "./smart-escrow-milestone.html"
            }
        ]
    },
    {
        "tags": "مستشار قانوني مؤسسي محاماة كونسل worm تدقيق قضائي 111 counsel",
        "q": "ما هي بوابة المستشار القانوني المؤسسي (المهمة 111)؟",
        "a": "بوابة متخصصة لفرق المحاماة وهيئات التحكيم تتيح التحقق الفوري من بصمات WORM التشفيرية للأدلة والمستندات القضائية، ومطابقتها لاتفاقية نيويورك 1958 ومعايير الأرشفة الجنائية الدولية.",
        "actions": [
            {
                "label": "🏛️ بوابة المستشار المؤسسي",
                "url": "./corporate-counsel-portal.html"
            }
        ]
    },
    {
        "tags": "استئناف طعن اعتراض اعادة نظر احكام نزاع 112 appeals",
        "q": "ما هو مسار الاستئناف والاعتراض الذاتي (المهمة 112)؟",
        "a": "تدفق استئنافي ذاتي يتيح قيد طلبات إعادة النظر والطعن القضائي في أحكام التحكيم تلقائياً فور ظهور أدلة WORM جنائية جديدة، مع تجميد فوري لضمانات التنفيذ المالي وبث إشعار SSE لكافة اللوحات.",
        "actions": [
            {
                "label": "⚖️ قيد طلب استئناف",
                "url": "./corporate-counsel-portal.html#appeals"
            }
        ]
    },
    {
        "tags": "سوشيال ميديا باقة تسويق 8k سوشال حملات انستغرام لينكد 890",
        "q": "ما هي باقة السوشيال ميديا الرسمية 8K (€890)؟",
        "a": "باقة متكاملة بـ <strong>€890</strong> لإطلاق وتدشين 9 منصات تواصل (LinkedIn, Instagram, X, YouTube, Telegram, TikTok, Snapchat, Facebook, Pinterest) بهوية بصرية وأصول 8K، جدول نشر أسبوعي آلي، وربط واتساب VIP.",
        "actions": [
            {
                "label": "🎨 منصة السوشيال ميديا 8K",
                "url": "./social-campaign-hub.html"
            },
            {
                "label": "واتساب VIP المباشر",
                "url": "https://wa.me/31618111116"
            }
        ]
    }
];

    function normalizeArabic(text) {
        if (!text) return '';
        return text.toLowerCase()
            .replace(/[إأآا]/g, 'ا')
            .replace(/ة/g, 'ه')
            .replace(/ى/g, 'ي')
            .replace(/[،,.\-?!؛:()[\]"']/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function stripDefiniteArticle(w) {
        if (w.length > 3 && w.startsWith('ال')) {
            return w.substring(2);
        }
        return w;
    }

    function findFallbackAnswer(query) {
        if (!query || typeof query !== 'string') return null;
        const cleanQ = normalizeArabic(query);
        const queryTokens = cleanQ.split(' ').filter(w => w.length >= 2);
        if (queryTokens.length === 0) return null;

        let bestMatch = null;
        let highestScore = 0;

        for (let i = 0; i < SOVEREIGN_OFFLINE_KB.length; i++) {
            const item = SOVEREIGN_OFFLINE_KB[i];
            let score = 0;
            const normTags = normalizeArabic(item.tags);
            const tagWords = normTags.split(' ');
            const normTitle = normalizeArabic(item.q);
            const titleWords = normTitle.split(' ');

            for (const token of queryTokens) {
                const raw = token;
                const stripped = stripDefiniteArticle(token);

                if (titleWords.includes(raw) || titleWords.includes(stripped)) {
                    score += 8;
                } else if (normTitle.includes(stripped)) {
                    score += 5;
                }

                if (tagWords.includes(raw) || tagWords.includes(stripped)) {
                    score += 6;
                } else if (normTags.includes(stripped)) {
                    score += 3;
                }
            }

            if (score > highestScore) {
                highestScore = score;
                bestMatch = item;
            }
        }

        return highestScore >= 6 ? bestMatch : null;
    }

    function buildWidgetUI() {
        if (document.getElementById('sr-agent-widget-container')) return;

        const wrapper = document.createElement('div');
        wrapper.id = 'sr-agent-widget-container';
        wrapper.innerHTML = `
            <!-- Unified Floating Launcher Trigger -->
            <button class="sr-agent-launcher" id="sr-agent-launcher" title="المستشار الذكي التنفيذي — اسأل المساعد" aria-label="المستشار الذكي التنفيذي — اسأل المساعد">
                <span class="sr-agent-pulse-dot" aria-hidden="true"></span>
                <svg class="sr-agent-launcher-icon" viewBox="0 0 24 24" fill="none" stroke="#c5a880" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                <span class="sr-agent-launcher-text">اسأل المستشار الذكي 🤖</span>
            </button>

            <!-- Chat Window Dialog -->
            <div class="sr-agent-window" id="sr-agent-window" role="dialog" aria-modal="false" aria-label="نافذة المستشار الذكي التنفيذي">
                <div class="sr-agent-header">
                    <div class="sr-agent-header-brand">
                        <div class="sr-agent-avatar">
                            <span class="sr-agent-logo-text">S&R</span>
                        </div>
                        <div class="sr-agent-title">
                            <h3>المستشار الذكي التنفيذي</h3>
                            <span><span class="sr-agent-status-indicator"></span> متصل (Google Antigravity & RAG)</span>
                        </div>
                    </div>
                    <div class="sr-agent-header-actions">
                        <button id="sr-agent-voice-lang" class="sr-voice-lang-btn" title="تغيير لغة الصوت (AR / EN)">AR</button>
                        <button id="sr-agent-export" title="تصدير الاستشارة كملف نصي">⬇</button>
                        <button id="sr-agent-clear" title="مسح المحادثة وتجديد الجلسة">↺</button>
                        <button id="sr-agent-close" title="إغلاق النافذة">✕</button>
                    </div>
                </div>

                <div class="sr-agent-messages" id="sr-agent-messages">
                    <div class="sr-msg sr-msg-agent">
                        مرحباً بك! 👋 أنا المستشار الذكي التنفيذي الموحد لمنظومة <strong>S&R CoreSync</strong>.<br>
                        كيف يمكنني مساعدة منشأتكم اليوم بخصوص حلولنا المؤسسية، باقات الأسعار، بوابات التحكيم والـ CBDC، أو أتمتة الأعمال والـ RAG؟
                    </div>
                    <div class="sr-typing" id="sr-typing-indicator">
                        <div class="sr-typing-dot"></div>
                        <div class="sr-typing-dot"></div>
                        <div class="sr-typing-dot"></div>
                    </div>
                </div>

                <div class="sr-agent-chips">
                    <button class="sr-chip" data-query="كم تكلفة الخدمات والباقات؟">💰 أسعار الباقات</button>
                    <button class="sr-chip" data-query="كم سعر الموقع الإلكتروني والمتجر؟">🌐 المواقع والمتاجر</button>
                    <button class="sr-chip" data-query="هل تقدمون أنظمة ERP وما هي باقاتها؟">🏢 تهيئة ERP</button>
                    <button class="sr-chip" data-query="ما هي باقة السوشيال ميديا 8K؟">🎨 سوشيال 8K</button>
                    <button class="sr-chip" data-query="ما هو مركز التحكيم السيادي التجاري الدولي؟">⚖️ التحكيم والضمان</button>
                    <button class="sr-chip" data-query="كيف أطلب عرض سعر رسمي مخصص؟">📋 طلب عرض سعر</button>
                    <button class="sr-chip" data-query="كيف أتواصل معكم مباشرة على واتساب؟">💬 واتساب VIP</button>
                </div>

                <form class="sr-agent-input-box" id="sr-agent-form">
                    <input type="file" id="sr-agent-file-input" accept=".pdf,.docx,.txt,.md" multiple style="display:none;">
                    <button type="button" class="sr-agent-upload-btn" id="sr-agent-upload" title="إرفاق مستند للتحليل الذكي والفهرسة (PDF / DOCX - بحد أقصى 5MB)">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
                        </svg>
                    </button>
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

                <div class="sr-agent-foot-trust">
                    <span>يعمل بمحرك RAG السيادي · حماية البيانات وفق معايير ISO 27001 و GDPR</span>
                </div>
            </div>
        `;
        document.body.appendChild(wrapper);

        // Elements
        const launcher = document.getElementById('sr-agent-launcher');
        const windowEl = document.getElementById('sr-agent-window');
        const closeBtn = document.getElementById('sr-agent-close');
        const clearBtn = document.getElementById('sr-agent-clear');
        const exportBtn = document.getElementById('sr-agent-export');
        const langBtn = document.getElementById('sr-agent-voice-lang');
        const micBtn = document.getElementById('sr-agent-mic');
        const uploadBtn = document.getElementById('sr-agent-upload');
        const fileInput = document.getElementById('sr-agent-file-input');
        const form = document.getElementById('sr-agent-form');
        const input = document.getElementById('sr-agent-input');
        const messagesEl = document.getElementById('sr-agent-messages');
        const typingEl = document.getElementById('sr-typing-indicator');

        let currentVoiceLang = 'ar-SA';

        // Document upload handler
        if (uploadBtn && fileInput) {
            uploadBtn.addEventListener('click', () => {
                fileInput.click();
            });

            fileInput.addEventListener('change', async (e) => {
                const files = e.target.files;
                if (!files || files.length === 0) return;

                const uploadEndpoint = API_ENDPOINT.replace(/\/api\/(ai-concierge|chat)$/, '/api/upload');
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    if (file.size > 5 * 1024 * 1024) {
                        appendMessage(`⚠️ الملف "${file.name}" يتجاوز الحد الأقصى المسموح به (5 ميجابايت).`, false);
                        continue;
                    }

                    appendMessage(`📎 جاري رفع وتحليل المستند: **${file.name}** (${(file.size / 1024).toFixed(1)} KB)...`, true);
                    typingEl.style.display = 'inline-flex';
                    messagesEl.scrollTop = messagesEl.scrollHeight;

                    const formData = new FormData();
                    formData.append('files', file);

                    try {
                        const res = await fetch(uploadEndpoint, {
                            method: 'POST',
                            body: formData
                        });
                        typingEl.style.display = 'none';

                        if (!res.ok) {
                            const errData = await res.json().catch(() => ({}));
                            throw new Error(errData.detail || ('HTTP ' + res.status));
                        }

                        appendMessage(`✅ تم استخراج نصوص **${file.name}** وفهرستها بنجاح في قاعدة المعرفة السيادية (RAG)! يمكنك الآن توجيه أي أسئلة حول محتوى المستند.`, false);
                    } catch (err) {
                        typingEl.style.display = 'none';
                        appendMessage(`❌ تعذر تحليل المستند "${file.name}": ${err.message}`, false);
                    }
                }
                fileInput.value = '';
            });
        }

        // Voice Language Switcher
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

        // Speech-to-Text Setup
        let isListening = false;
        let recognition = null;
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

        // Text-to-Speech (Audio Synthesis)
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

        // Attach TTS to first welcome message
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

        // Open / Close Handlers
        if (launcher) {
            launcher.addEventListener('click', () => {
                windowEl.classList.toggle('sr-open');
                if (windowEl.classList.contains('sr-open')) {
                    input.focus();
                }
            });
        }

        // Direct binding to the Social Media Bar Chat Button (#floatingFollowChatBtn)
        const followChatBtn = document.getElementById('floatingFollowChatBtn');
        if (followChatBtn) {
            followChatBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                windowEl.classList.toggle('sr-open');
                if (windowEl.classList.contains('sr-open')) {
                    input.focus();
                }
            });
        }

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && windowEl.classList.contains('sr-open')) {
                windowEl.classList.remove('sr-open');
            }
        });

        closeBtn.addEventListener('click', () => {
            windowEl.classList.remove('sr-open');
        });

        clearBtn.addEventListener('click', () => {
            messagesEl.querySelectorAll('.sr-msg:not(:first-child)').forEach(m => m.remove());
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

        // Quick Chips
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
                        if (!a.url.startsWith('#') && !a.url.startsWith('./')) {
                            btn.target = '_blank';
                            btn.rel = 'noopener noreferrer';
                        }
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
                const timeoutId = setTimeout(() => controller.abort(), 4000);

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
                console.log('[S&R Sovereign Agent]: Resolving via Offline Intelligence Engine...');
                
                // Smart Offline Knowledge Base Lookup
                const match = findFallbackAnswer(text);
                if (match) {
                    appendMessage(match.a, false, match.actions || []);
                } else {
                    appendMessage(
                        "بصفتي المستشار الذكي التنفيذي لـ S&R CoreSync، توفر منظومتنا 9 ركائز سيادية معتمدة تشمل: السحابة وERP، التحكيم الدولي (104)، جسر تسوية CBDC (105)، حوسبة ZKP (106)، الأدلة الجنائية WORM والضمان المالي (107)، بوابة المستشار القانوني (111)، وباقة السوشيال ميديا 8K (€890). يسعدنا تقديم استشارة مخصصة لمنشأتكم.",
                        false,
                        [
                            { label: '💬 محادثة واتساب VIP المباشرة', url: 'https://wa.me/31618111116' },
                            { label: '📋 طلب عرض سعر مخصص', action: 'open_rfq' },
                            { label: '🌐 دليل الخدمات والباقات', url: './index.html#pricing' }
                        ]
                    );
                }
            }
        }

        // Public API on Window
        window.srAgentWidget = {
            open: function (query) {
                windowEl.classList.add('sr-open');
                if (input) {
                    if (query) input.value = query;
                    input.focus();
                    if (query) sendMessage(query);
                }
            },
            close: function () {
                windowEl.classList.remove('sr-open');
            },
            toggle: function (query) {
                if (windowEl.classList.contains('sr-open')) {
                    this.close();
                } else {
                    this.open(query);
                }
            },
            send: function (text) {
                sendMessage(text);
            },
            isOpen: function () {
                return windowEl.classList.contains('sr-open');
            }
        };

        // Legacy compatibility routes
        window.toggleAiChat = function () { window.srAgentWidget.toggle(); };
        window.openAiChat = function (q) { window.srAgentWidget.open(q); };
        window.openAiConcierge = function (q) { window.srAgentWidget.open(q); };
        window.openConcierge = function (q) { window.srAgentWidget.open(q); };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildWidgetUI);
    } else {
        buildWidgetUI();
    }
})();
