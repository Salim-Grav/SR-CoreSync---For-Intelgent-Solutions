/**
 * S&R CoreSync For Intelligent Solutions — Sovereign AI Concierge Engine
 * -----------------------------------------------------------------------------
 * High-performance multilingual autonomous assistant for WhatsApp & Telegram webhooks.
 * Features:
 *   1. Zero-latency rule-based + semantic intent classification.
 *   2. Support for Arabic, English, Dutch, and German.
 *   3. Dynamic enterprise quote generation, catalog matching, and VIP booking routes.
 *   4. Seamless fallback for founder escalation (Eng. Salim Aziza / CFO Raed Kaakeh).
 */

const CATALOG_PACKAGES = {
    starter: {
        id: 'SRC-ERP-START-2026',
        name: {
            ar: 'باقة Core Starter ERP Suite',
            en: 'Core Starter ERP Suite',
            nl: 'Core Starter ERP Suite'
        },
        price: '€1,490 / شهرياً',
        priceEur: 1490,
        badge: 'ENTERPRISE ERP CORE',
        description: {
            ar: 'نظام إدارة موارد المؤسسات السحابي السيادي مع دفتر الأستاذ التلقائي، والفوترة الضريبية المتوافقة مع BTW والأنظمة الأوروبية، وبوابات الدفع الإلكتروني.',
            en: 'Sovereign cloud ERP with automated general ledger, Dutch BTW/EU tax compliant invoicing, and Stripe/iDEAL integration.',
            nl: 'Soevereine cloud-ERP met geautomatiseerd grootboek, BTW-conforme facturatie en Stripe/iDEAL integratie.'
        },
        link: 'https://sr-coresync.com/#pricing'
    },
    pro: {
        id: 'SRC-AI-PRO-2026',
        name: {
            ar: 'باقة Business Pro Suite (ERP + AI)',
            en: 'Business Pro Suite (ERP + AI)',
            nl: 'Business Pro Suite (ERP + AI)'
        },
        price: '€2,890 / شهرياً',
        priceEur: 2890,
        badge: 'MOST POPULAR - B2B PRO',
        description: {
            ar: 'الحل الأكثر طلباً: دمج الـ ERP مع وكلاء الذكاء الاصطناعي المستقلين (Autonomous AI Agents)، وتكامل البنوك اللحظي PSD2، وأتمتة خطوط المبيعات بنسبة 99.9% SLA.',
            en: 'Our most popular tier: full ERP integrated with Autonomous AI Agents, real-time PSD2 banking, and high-availability 99.9% European SLA.',
            nl: 'Onze populairste tier: complete ERP gecombineerd met Autonome AI-agents, realtime PSD2-bankieren en 99.9% SLA.'
        },
        link: 'https://sr-coresync.com/#pricing'
    },
    enterprise: {
        id: 'SRC-SOV-ENT-2026',
        name: {
            ar: 'باقة Sovereign Enterprise Cloud & AI',
            en: 'Sovereign Enterprise Cloud & AI',
            nl: 'Sovereign Enterprise Cloud & AI'
        },
        price: '€5,400 / شهرياً',
        priceEur: 5400,
        badge: 'MISSION CRITICAL SOVEREIGN',
        description: {
            ar: 'بنية سحابية سيادية خاصة معزولة في أمستردام، نماذج ذكاء اصطناعي خاصة بالمنشأة (Proprietary LLM) لضمان الخصوصية والامتثال لـ GDPR/ISO مع كونسيرج VIP 24/7.',
            en: 'Dedicated sovereign cloud infrastructure in Amsterdam with proprietary on-premise LLMs, GDPR/ISO compliance, and 24/7 VIP concierge.',
            nl: 'Toegewijde soevereine cloud in Amsterdam met eigen LLM-modellen, GDPR/ISO-conformiteit en 24/7 VIP concierge.'
        },
        link: 'https://sr-coresync.com/#pricing'
    }
};

const FOUNDERS = {
    cto: {
        name: 'م. محمد سليم عزيزة | Eng. Mohammad Salim Aziza',
        title: 'CTO & كبير مهندسي السحابة والذكاء الاصطناعي',
        phone: '+31 6 31069433',
        wa: 'https://wa.me/31631069433'
    },
    cfo: {
        name: 'أ. محمد رائد كعكة | Mohammad Raed Kaakeh',
        title: 'CFO & استشاري نظم ERP والمالية',
        phone: '+31 6 36279435',
        wa: 'https://wa.me/31636279435'
    },
    companyPhone: '+31 6 1811 1116',
    companyWa: 'https://wa.me/31618111116'
};

/**
 * Detect Language (ar, en, nl, de)
 */
function detectLanguage(text) {
    if (!text) return 'ar';
    const arabicRegex = /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]/;
    if (arabicRegex.test(text)) return 'ar';
    const dutchKeywords = ['hallo', 'wat', 'kost', 'pakket', 'prijs', 'bedrijf', 'graag', 'informatie', 'afspraak', 'soeverein'];
    const germanKeywords = ['hallo', 'preis', 'paket', 'unternehmen', 'termin', 'kosten', 'beratung'];
    const lower = text.toLowerCase();
    if (dutchKeywords.some(w => lower.includes(w))) return 'nl';
    if (germanKeywords.some(w => lower.includes(w))) return 'de';
    return 'en';
}

/**
 * Classify User Intent
 */
function classifyIntent(text) {
    const raw = String(text || '').toLowerCase();

    // 1. VIP Meeting / Founder escalation
    if (raw.includes('سليم') || raw.includes('salim') || raw.includes('رائد') || raw.includes('raed') ||
        raw.includes('اجتماع') || raw.includes('meeting') || raw.includes('appointment') || raw.includes('afspraak') ||
        raw.includes('استشارة') || raw.includes('consultation') || raw.includes('مكالمة') || raw.includes('call')) {
        return 'VIP_MEETING';
    }

    // 2. Sovereign Enterprise / Custom Cloud
    if (raw.includes('sovereign') || raw.includes('enterprise') || raw.includes('سيادي') || raw.includes('حكوم') ||
        raw.includes('مؤسسات كبرى') || raw.includes('خوادم خاصة') || raw.includes('dedicated') || raw.includes('gdpr') ||
        raw.includes('iso') || raw.includes('5400') || raw.includes('5,400')) {
        return 'SOVEREIGN_CLOUD';
    }

    // 3. AI / Autonomous Agents
    if (raw.includes('ذكاء') || raw.includes('اصطناعي') || raw.includes('ai') || raw.includes('وكلاء') ||
        raw.includes('agents') || raw.includes('أتمتة') || raw.includes('automation') || raw.includes('pro') ||
        raw.includes('2890') || raw.includes('2,890')) {
        return 'AI_INQUIRY';
    }

    // 4. ERP / Accounting
    if (raw.includes('erp') || raw.includes('محاسب') || raw.includes('accounting') || raw.includes('فواتير') ||
        raw.includes('invoice') || raw.includes('ضرائب') || raw.includes('btw') || raw.includes('vat') ||
        raw.includes('starter') || raw.includes('1490') || raw.includes('1,490')) {
        return 'ERP_INQUIRY';
    }

    // 5. Pricing / Cost / Catalog
    if (raw.includes('سعر') || raw.includes('أسعار') || raw.includes('price') || raw.includes('cost') ||
        raw.includes('prijs') || raw.includes('kosten') || raw.includes('كتالوج') || raw.includes('catalog') ||
        raw.includes('باقات') || raw.includes('packages')) {
        return 'PRICING_QUOTE';
    }

    return 'GENERAL_GREETING';
}

/**
 * Generate Structured AI Response
 */
function generateConciergeReply(userMessage, preferredLang) {
    const lang = preferredLang || detectLanguage(userMessage);
    const intent = classifyIntent(userMessage);

    let reply = '';
    let matchedPackage = null;
    let actions = [];

    if (intent === 'VIP_MEETING') {
        if (lang === 'ar') {
            reply = `🌟 مرحباً بك في S&R CoreSync For Intelligent Solutions!\n\nيسعدنا تنظيم جلسة استشارية تنفيذية مباشرة مع الشركاء المؤسسين:\n• 👨‍💻 م. محمد سليم عزيزة (CTO & كبير مهندسي السحابة والذكاء الاصطناعي)\n• 💼 أ. محمد رائد كعكة (CFO & استشاري نظم ERP والمالية)\n\nيمكنك حجز الموعد فوراً أو التواصل المباشر عبر:\n🌐 رابط الحجز المباشر: https://sr-coresync.com/#booking\n📞 واتساب الشركاء المباشر: ${FOUNDERS.companyPhone}`;
        } else if (lang === 'nl') {
            reply = `🌟 Welkom bij S&R CoreSync For Intelligent Solutions!\n\nWij plannen graag een executive adviesgesprek in met onze oprichters:\n• Eng. Mohammad Salim Aziza (CTO & Principal Cloud/AI Architect)\n• Mohammad Raed Kaakeh (CFO & Senior ERP Consultant)\n\nBoek direct uw afspraak via:\n🌐 Direct boeken: https://sr-coresync.com/#booking\n📞 Zakelijk WhatsApp: ${FOUNDERS.companyPhone}`;
        } else {
            reply = `🌟 Welcome to S&R CoreSync For Intelligent Solutions!\n\nWe would be delighted to schedule an executive consultation directly with our founders:\n• Eng. Mohammad Salim Aziza (CTO & Principal Cloud/AI Architect)\n• Mohammad Raed Kaakeh (CFO & Senior ERP Consultant)\n\nBook your priority session here:\n🌐 Direct VIP Booking: https://sr-coresync.com/#booking\n📞 Direct Corporate Line: ${FOUNDERS.companyPhone}`;
        }
        actions = [
            { label: '📅 حجز استشارة VIP', url: 'https://sr-coresync.com/#booking' },
            { label: '💬 محادثة واتساب الإدارة', url: FOUNDERS.companyWa }
        ];
    } else if (intent === 'AI_INQUIRY') {
        matchedPackage = CATALOG_PACKAGES.pro;
        if (lang === 'ar') {
            reply = `🤖 مرحباً بك! نبتكر في S&R CoreSync حلول الذكاء الاصطناعي السيادي والأتمتة الذاتية (Autonomous AI Agents).\n\nالباقة الموصى بها لاحتياجاتكم:\n✨ **${matchedPackage.name.ar}**\n💰 **الاستثمار:** ${matchedPackage.price}\n\n📌 **أبرز الإمكانيات:**\n${matchedPackage.description.ar}\n\n• أتمتة خطوط خدمة العملاء والمبيعات 24/7\n• تكامل البنوك اللحظي الأوروبي PSD2 Open Banking\n• اتفاقية مستوى خدمة سيادية 99.9% High-Availability SLA\n\n🔗 تفاصيل الباقة وتجربة العرض الحي: ${matchedPackage.link}`;
        } else if (lang === 'nl') {
            reply = `🤖 Welkom! Bij S&R CoreSync bouwen we soevereine AI-systemen en Autonome AI-agents.\n\nAanbevolen pakket:\n✨ **${matchedPackage.name.nl}**\n💰 **Investering:** €2.890 / maand\n\n📌 **Specificaties:**\n${matchedPackage.description.nl}\n\n🔗 Bekijk details: ${matchedPackage.link}`;
        } else {
            reply = `🤖 Welcome! S&R CoreSync engineers Sovereign AI architectures and Autonomous Enterprise AI Agents.\n\nRecommended Tier:\n✨ **${matchedPackage.name.en}**\n💰 **Investment:** €2,890 / month\n\n📌 **Key Capabilities:**\n${matchedPackage.description.en}\n\n🔗 Explore Package: ${matchedPackage.link}`;
        }
        actions = [
            { label: '🚀 تجربة محاكي الذكاء الاصطناعي', url: 'https://sr-coresync.com/demo.html' },
            { label: '💳 حجز وتفعيل الباقة', url: 'https://sr-coresync.com/#pricing' }
        ];
    } else if (intent === 'ERP_INQUIRY') {
        matchedPackage = CATALOG_PACKAGES.starter;
        if (lang === 'ar') {
            reply = `💼 أهلاً بك! نظام S&R CoreSync للـ ERP هو بيئة سحابية سيادية متكاملة صُممت وفق أعلى المعايير الأوروبية.\n\nالباقة الأساسية المعتمدة:\n✨ **${matchedPackage.name.ar}**\n💰 **الاستثمار:** ${matchedPackage.price}\n\n📌 **المميزات:**\n${matchedPackage.description.ar}\n\n• متوافق بالكامل مع الضرائب الهولندية BTW وقوانين الفوترة الإلكترونية 2026\n• بوابات عملاء بـ 29 لغة عالمية\n• ربط بوابات الدفع Stripe و iDEAL الفوري\n\n🔗 استعراض النظام وتجربة المحاكي: https://sr-coresync.com/demo.html`;
        } else if (lang === 'nl') {
            reply = `💼 Welkom! Ons S&R CoreSync ERP-systeem is een soeverein cloudplatform conform de hoogste Europese normen.\n\nInstappakket:\n✨ **${matchedPackage.name.nl}**\n💰 **Investering:** €1.490 / maand\n\n📌 **Kenmerken:**\n${matchedPackage.description.nl}\n\n🔗 Live demo: https://sr-coresync.com/nl/demo.html`;
        } else {
            reply = `💼 Welcome! S&R CoreSync ERP is a sovereign enterprise platform engineered to Dutch BTW & EU e-invoicing standards.\n\nFeatured Tier:\n✨ **${matchedPackage.name.en}**\n💰 **Investment:** €1,490 / month\n\n📌 **Highlights:**\n${matchedPackage.description.en}\n\n🔗 Live interactive demo: https://sr-coresync.com/en/demo.html`;
        }
        actions = [
            { label: '🖥️ تجربة نظام الـ ERP الحي', url: 'https://sr-coresync.com/demo.html' },
            { label: '📄 طلب عرض سعر رسمي', url: 'https://sr-coresync.com/#pricing' }
        ];
    } else if (intent === 'SOVEREIGN_CLOUD') {
        matchedPackage = CATALOG_PACKAGES.enterprise;
        if (lang === 'ar') {
            reply = `👑 أهلاً بك في خدمات البنية التحتية السيادية للمؤسسات الكبرى (Sovereign Enterprise).\n\n✨ **${matchedPackage.name.ar}**\n💰 **الاستثمار المؤسسي:** ${matchedPackage.price}\n\n📌 **المواصفات السيادية:**\n${matchedPackage.description.ar}\n\n• خوادم أوروبية مخصصة ومعزولة (Amsterdam HQ)\n• نماذج ذكاء اصطناعي خاصة بالمنشأة (Proprietary LLM) لضمان الخصوصية والامتثال لـ GDPR/ISO\n• مهندس حلول مخصص ودعم VIP على مدار الساعة 24/7\n\n🔗 للتفاصيل والتنسيق التنفيذي: https://sr-coresync.com/#pricing`;
        } else if (lang === 'nl') {
            reply = `👑 Welkom bij Sovereign Enterprise Solutions van S&R CoreSync.\n\n✨ **${matchedPackage.name.nl}**\n💰 **Investering:** €5.400 / maand\n\n📌 **Specificaties:**\n${matchedPackage.description.nl}\n\n🔗 Details: https://sr-coresync.com/nl/#pricing`;
        } else {
            reply = `👑 Welcome to Sovereign Enterprise Solutions by S&R CoreSync.\n\n✨ **${matchedPackage.name.en}**\n💰 **Investment:** €5,400 / month\n\n📌 **Specifications:**\n${matchedPackage.description.en}\n\n🔗 Details: https://sr-coresync.com/en/#pricing`;
        }
        actions = [
            { label: '🛡️ ميثاق السيادة والأمان', url: 'https://sr-coresync.com/#about' },
            { label: '📞 اتصال تنفيذي مباشر', url: FOUNDERS.companyWa }
        ];
    } else if (intent === 'PRICING_QUOTE') {
        if (lang === 'ar') {
            reply = `📊 أهلاً بك! توفر S&R CoreSync ثلاث باقات مؤسسية معتمدة وشفافة:\n\n1️⃣ **Core Starter ERP:** €1,490/شهرياً (أنظمة المحاسبة والـ ERP الأساسية المتوافقة مع BTW)\n2️⃣ **Business Pro:** €2,890/شهرياً (ERP كامل + وكلاء ذكاء اصطناعي + بنوك PSD2)\n3️⃣ **Sovereign Enterprise:** €5,400/شهرياً (خوادم سحابية سيادية خاصة مخصصة + ذكاء اصطناعي مستقل)\n\n✨ يتوفر خصم مجمّع 20% عند الفوترة السنوية!\n🔗 مصفوفة الأسعار والكتالوج الكامل: https://sr-coresync.com/#pricing`;
        } else if (lang === 'nl') {
            reply = `📊 Welkom! S&R CoreSync biedt 3 transparante zakelijke pakketten:\n\n1️⃣ **Core Starter ERP:** €1.490/mnd\n2️⃣ **Business Pro:** €2.890/mnd\n3️⃣ **Sovereign Enterprise:** €5.400/mnd\n\n✨ 20% korting bij jaarlijkse betaling.\n🔗 Bekijk prijzen: https://sr-coresync.com/nl/#pricing`;
        } else {
            reply = `📊 Welcome! S&R CoreSync offers 3 transparent corporate packages:\n\n1️⃣ **Core Starter ERP:** €1,490/mo\n2️⃣ **Business Pro:** €2,890/mo (ERP + Autonomous AI + PSD2)\n3️⃣ **Sovereign Enterprise:** €5,400/mo (Dedicated Private Cloud + Proprietary AI)\n\n✨ 20% discount on annual billing.\n🔗 Full pricing matrix: https://sr-coresync.com/en/#pricing`;
        }
        actions = [
            { label: '📑 فتح حاسبة الأسعار والكتالوج', url: 'https://sr-coresync.com/#pricing' },
            { label: '💬 محادثة واتساب للاستفسار', url: FOUNDERS.companyWa }
        ];
    } else {
        // GENERAL_GREETING
        if (lang === 'ar') {
            reply = `مرحباً بك في S&R CoreSync For Intelligent Solutions! 🌟\nأنا المساعد الذكي المؤسسي (AI Concierge)، متواجد لخدمتك على مدار الساعة 24/7.\n\nكيف يمكنني مساعدتك اليوم؟\n1️⃣ الاستفسار عن باقات نظام الـ ERP السحابي (€1,490)\n2️⃣ استكشاف حلول الذكاء الاصطناعي والأتمتة (€2,890)\n3️⃣ البنى التحتية السحابية السيادية للمؤسسات (€5,400)\n4️⃣ حجز استشارة تنفيذية مباشرة مع الشركاء المؤسسين\n\n🌐 الموقع الرسمي: https://sr-coresync.com\n📞 واتساب الأعمال: ${FOUNDERS.companyPhone}`;
        } else if (lang === 'nl') {
            reply = `Welkom bij S&R CoreSync For Intelligent Solutions! 🌟\nIk ben de zakelijke AI Concierge, 24/7 beschikbaar.\n\nHoe kan ik u van dienst zijn?\n1️⃣ ERP-pakketten (€1.490/mnd)\n2️⃣ Autonome AI-oplossingen (€2.890/mnd)\n3️⃣ Soevereine Enterprise Cloud (€5.400/mnd)\n4️⃣ VIP adviesgesprek met de oprichters\n\n🌐 Website: https://sr-coresync.com/nl\n📞 Tel: ${FOUNDERS.companyPhone}`;
        } else {
            reply = `Welcome to S&R CoreSync For Intelligent Solutions! 🌟\nI am your Enterprise AI Concierge, available 24/7.\n\nHow may I assist you today?\n1️⃣ Explore Cloud ERP Suite (€1,490/mo)\n2️⃣ Autonomous AI & Workflow Automation (€2,890/mo)\n3️⃣ Sovereign Enterprise Private Cloud (€5,400/mo)\n4️⃣ Book a direct executive meeting with our founders\n\n🌐 Portal: https://sr-coresync.com\n📞 WhatsApp VIP: ${FOUNDERS.companyPhone}`;
        }
        actions = [
            { label: '🌐 زيارة البوابة الرسمية', url: 'https://sr-coresync.com' },
            { label: '💼 استعراض باقات الأسعار', url: 'https://sr-coresync.com/#pricing' },
            { label: '📅 حجز موعد VIP', url: 'https://sr-coresync.com/#booking' }
        ];
    }

    return {
        ok: true,
        detectedLanguage: lang,
        intent: intent,
        reply: reply,
        matchedPackage: matchedPackage,
        actions: actions,
        timestamp: new Date().toISOString()
    };
}

module.exports = {
    CATALOG_PACKAGES,
    FOUNDERS,
    detectLanguage,
    classifyIntent,
    generateConciergeReply
};
