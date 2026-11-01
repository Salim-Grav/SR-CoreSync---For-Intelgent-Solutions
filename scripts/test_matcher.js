// Test matcher in JS
const KB = [
    {
        tags: "خدمات خدماتكم ماذا تقدمون حلول الشركة تخصص",
        q: "ما الخدمات التي تقدمونها؟",
        a: "نغطي ستة مجالات: <strong>الهوية البصرية</strong>، <strong>المواقع والمتاجر</strong>، <strong>البرمجيات السحابية وERP</strong>، <strong>تطبيقات الجوال</strong>، <strong>أتمتة العمليات والذكاء الاصطناعي</strong>، و<strong>الأمن والبنية السحابية</strong>.",
        actions: [{ label: "استعرض الخدمات", url: "./index.html#service" }]
    },
    {
        tags: "سعر اسعار تكلفة كم بكم ميزانية باقات الباقات",
        q: "كم تكلفة الخدمات والباقات؟",
        a: "الأسعار الرسمية: الهوية البصرية <strong>€590</strong> · الموقع الفاخر <strong>€980</strong> · المتجر الإلكتروني <strong>€1,450</strong> · باقة السوشيال ميديا 8K بقيمة <strong>€890</strong> · باقة السحابة Core Starter <strong>€1,490</strong> · تهيئة ERP <strong>€1,890</strong> · وتوجد باقة انطلاقة شاملة <strong>€1,990</strong> بدلاً من €3,020.",
        actions: [{ label: "كل الباقات", url: "./index.html#pricing" }]
    },
    {
        tags: "سوشيال ميديا تسويق حملات 8k سوشال انستغرام لينكد",
        q: "ما هي باقة السوشيال ميديا 8K؟",
        a: "باقة السوشيال ميديا 8K الحصرية (<strong>€890</strong>): إدارة وتدشين 9 منصات تواصل بمحتوى وأصول بصرية بدقة 8K، جدول نشر آلي، وتكامل واتساب VIP.",
        actions: [{ label: "بوابة السوشيال", url: "./social-campaign-hub.html" }]
    },
    {
        tags: "تحكيم قضائي نزاع محكمة دولية عقد نيويورك",
        q: "ما هو مركز التحكيم السيادي الدولي؟",
        a: "بوابة التحكيم التجاري الدولي (المهمة 104) تتيح إدارة وفض النزاعات العابرة للحدود بموجب اتفاقية نيويورك 1958 مع توثيق تشفيري للأحكام وربطها بالضمان المالي الذكي.",
        actions: [{ label: "بوابة التحكيم", url: "./sovereign-arbitration-hub.html" }]
    }
];

function matchKB(query) {
    const qLower = query.toLowerCase().trim();
    let bestMatch = null;
    let maxScore = 0;
    
    for (const item of KB) {
        let score = 0;
        const words = qLower.split(/\s+/);
        for (const w of words) {
            if (w.length < 2) continue;
            if (item.tags.includes(w)) score += 3;
            if (item.q.toLowerCase().includes(w)) score += 5;
        }
        if (score > maxScore) {
            maxScore = score;
            bestMatch = item;
        }
    }
    return maxScore > 0 ? bestMatch : null;
}

console.log("Test 'بكم باقة السوشيال':", matchKB("بكم باقة السوشيال")?.q);
console.log("Test 'قضية تحكيم':", matchKB("قضية تحكيم")?.q);
console.log("Test 'ما هي الاسعار':", matchKB("ما هي الاسعار")?.q);
