/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 * 
 * Interactive Tech Radar & Layered Architecture Controller
 */

(function() {
    'use strict';

    const techCatalog = {
        'ai-private': {
            badge: '🤖 الذكاء الاصطناعي السيادي',
            title: 'Private LLM Core • النماذج اللغوية المعزولة',
            desc: 'محرك ذكاء اصطناعي مؤسسي يتم تنصيبه على خوادم سحابية هولندية خاصة، معزولة تماماً عن أي وصول أو تدريب عام لضمان سرية القرارات والمستندات بنسبة 100%.',
            attrs: [
                { label: 'معيار الأمان والخصوصية', val: 'GDPR / AVG & EU AI Act 2026' },
                { label: 'زمن الاستجابة اللحظي', val: '< 140 Milliseconds' },
                { label: 'توطين البيانات', val: 'أمستردام، مملكة هولندا 🇳🇱' },
                { label: 'حالة التفعيل والتشغيل', val: 'جاهز للإنتاج فوراً (Production Ready)' }
            ]
        },
        'cloud-ams': {
            badge: '☁️ الحوسبة السحابية المعزولة',
            title: 'Amsterdam Tier-IV Datacenter • السحابة السيادية',
            desc: 'بنية تحتية سحابية هجينة مستضافة في مراكز بيانات أمستردام المحمية وفق أعلى معايير توفر الخدمة مع حماية قاطعة من الانقطاع.',
            attrs: [
                { label: 'مستوى الأمان والشهادات', val: 'ISO 27001 / SOC 2 Type II' },
                { label: 'اتفاقية مستوى الخدمة', val: '99.995% High Availability SLA' },
                { label: 'التشغيل والتوسع', val: 'Kubernetes Container Orchestration' },
                { label: 'زمن الوصول بالاتحاد الأوروبي', val: '< 8 Milliseconds' }
            ]
        },
        'peppol': {
            badge: '💳 التكنولوجيا المالية والفوترة',
            title: 'PEPPOL Access Point • شبكة الفواتير الأوروبية',
            desc: 'بوابة إلكترونية متصلة مباشرة بشبكة PEPPOL الدولية لنقل وتدقيق الفواتير الرقمية المشفرة متوافقة مع توجيهات ViDA الأوروبية والضرائب الهولندية.',
            attrs: [
                { label: 'الاعتماد الدولي', val: 'Certified PEPPOL Access Point' },
                { label: 'الربط الضريبي المباشر', val: 'Belastingdienst DigiPoort 🇳🇱' },
                { label: 'صيغ الملفات المدعومة', val: 'UBL 2.1 / XML / Factur-X' },
                { label: 'الدول المغطاة', val: '28 دولة أوروبية وعربية' }
            ]
        },
        'eidas': {
            badge: '🛡️ الأمن السيبراني والتوقيع',
            title: 'eIDAS Digital Signatures • التوقيع الإلكتروني القانوني',
            desc: 'منظومة التوقيع والعقود الرقمية المعتمدة قانونياً في محاكم هولندا والاتحاد الأوروبي وفق المادة 15a من القانون المدني الهولندي ولائحة eIDAS No 910/2014.',
            attrs: [
                { label: 'الحجية القانونية', val: 'ملزمة قانونياً في محاكم الاتحاد الأوروبي' },
                { label: 'خوارزمية التشفير', val: 'SHA-256 + RSA 4096-bit Keys' },
                { label: 'سجل البصمة الزمنية', val: 'Qualified Timestamp Token (TSA)' },
                { label: 'مستوى التوقيع', val: 'Advanced & Qualified e-Signature' }
            ]
        },
        'zerotrust': {
            badge: '🔒 جدار الحماية السيادي',
            title: 'Zero-Trust WAF • درع الحماية والمصادقة',
            desc: 'حماية شاملة لكافة نقاط الاتصال وبوابات البيانات ضد هجمات حجب الخدمة واختراق واجهات البرمجة، مع تدقيق أمني لحظي لكل طلب شبكي.',
            attrs: [
                { label: 'الحماية من الهجمات', val: 'DDoS Protection up to 100 Gbps' },
                { label: 'طبقة التشفير الشبكي', val: 'TLS 1.3 Strict & HSTS Preload' },
                { label: 'الامتثال السيبراني', val: 'EU NIS2 Directive Compliant' },
                { label: 'حوكمة الصلاحيات', val: 'mTLS & Granular RBAC' }
            ]
        },
        'erp-core': {
            badge: '📦 النظم المؤسسية',
            title: 'Real-Time ERP Sync • محرك العمليات وسلاسل الإمداد',
            desc: 'نظام إدارة الموارد المؤسسية الشامل للتحكم بالمخازن، التوريد، التتبع المالي، والطلبات التلقائية في الوقت اللحظي دون أي تأخير.',
            attrs: [
                { label: 'قاعدة البيانات الأساسية', val: 'PostgreSQL Enterprise Cluster' },
                { label: 'التخزين المؤقت فائق السرعة', val: 'In-Memory Redis Distributed Cache' },
                { label: 'قدرة المعالجة اللحظية', val: '100,000+ Transactions / min' },
                { label: 'التكامل البرمجي', val: 'RESTful API & GraphQL Engine' }
            ]
        }
    };

    function initTechRadar() {
        const radarArea = document.getElementById('demoTechRadarArea');
        if (!radarArea) return;

        const specBadge = document.getElementById('radarSpecBadge');
        const specTitle = document.getElementById('radarSpecTitle');
        const specDesc = document.getElementById('radarSpecDesc');
        const specList = document.getElementById('radarSpecList');

        function updateSpec(key) {
            const data = techCatalog[key];
            if (!data) return;

            radarArea.querySelectorAll('.radar-node-interactive').forEach(node => {
                node.classList.remove('active');
                if (node.getAttribute('data-tech') === key) {
                    node.classList.add('active');
                }
            });

            if (specBadge) specBadge.innerText = data.badge;
            if (specTitle) specTitle.innerText = data.title;
            if (specDesc) specDesc.innerText = data.desc;
            if (specList) {
                specList.innerHTML = data.attrs.map(a => `
                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.45); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; font-size:0.84rem;">
                        <span style="color:#94a3b8;">${a.label}</span>
                        <span style="font-weight:800; color:#f3dfba;">${a.val}</span>
                    </div>
                `).join('');
            }
        }

        radarArea.querySelectorAll('.radar-node-interactive').forEach(node => {
            node.addEventListener('click', function() {
                const techKey = this.getAttribute('data-tech');
                updateSpec(techKey);
            });
        });

        // Topology Layer Tabs
        const layerTabs = document.querySelectorAll('.demo-topo-tab');
        layerTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                layerTabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');

                const layer = this.getAttribute('data-layer');
                const nodes = radarArea.querySelectorAll('.radar-node-interactive');
                nodes.forEach(node => {
                    const tech = node.getAttribute('data-tech');
                    if (layer === 'all') {
                        node.style.display = 'flex';
                    } else if (layer === 'ai') {
                        node.style.display = tech.startsWith('ai') ? 'flex' : 'none';
                    } else if (layer === 'cloud') {
                        node.style.display = ['cloud-ams', 'erp-core'].includes(tech) ? 'flex' : 'none';
                    } else if (layer === 'security') {
                        node.style.display = ['eidas', 'zerotrust', 'peppol'].includes(tech) ? 'flex' : 'none';
                    }
                });
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTechRadar);
    } else {
        initTechRadar();
    }
})();

