/*
 * S&R CoreSync For Intelligent Solutions - Services Section Enhancements
 *  - Dynamic WhatsApp link generation (data-wa-key -> href)
 *  - Service Detail Modal (openServiceDetail / closeServiceDetail)
 *  - RFQ (Request for Quote) form -> WhatsApp + optional worker POST
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 */
(function () {
    'use strict';

    var WA_NUMBER = '31618111116';

    var SERVICES = {
        identity: { title: 'الهوية البصرية', price: '€590', desc: 'هويات بصرية مميزة تُبنى باستراتيجية ووضوح واتساق. شعار، لوحة ألوان، دليل هوية، وملفات مصدر.', deliverables: ['شعار (Logo) بـ 5 مفاهيم', 'لوحة ألوان + أنواع خطوط', 'دليل هوية (Brand Guidelines) PDF', 'ملفات SVG/PNG/EPS', 'موك آب (Mockups) 3D'] , faq: ['كم يستغرق؟ 7-14 يوم عمل.', 'هل أملك حقوق الملكية؟ نعم، 100%.', 'هل تشمل تعديلات؟ حتى 3 جولات.'] },
        web: { title: 'تصميم المواقع وتحسينها', price: '€980', desc: 'مواقع عصرية عالية الأداء مصممة للوضوح والثقة والنمو. Astro/Next.js، SEO، Core Web Vitals.', deliverables: ['تصميم UI/UX (Figma)', 'تطوير responsive (mobile-first)', 'SEO on-page + sitemap', 'Core Web Vitals ≥ 90', 'CMS (اختياري)'], faq: ['كم صفحة؟ حتى 8 صفحات.', 'هل يشمل الاستضافة؟ 3 أشهر مجاناً.', 'الصيانة؟ باقة شهرية متاحة.'] },
        ecommerce: { title: 'متجر إلكتروني', price: '€1,490', desc: 'متجر إلكتروني متكامل: كتالوج، سلة، دفع (Stripe/Mollie/iDEAL)، إدارة طلبات، VAT/BTW.', deliverables: ['كتالوج منتجات + فئات', 'سلة + دفع (Stripe/Mollie/iDEAL)', 'حساب VAT/BTW تلقائي', 'لوحة إدارة (Admin)', 'بريد تأكيد + فاتورة PDF'], faq: ['كم منتج؟ غير محدود.', 'الدفع؟ Stripe/Mollie/iDEAL/Bancontact.', 'الشحن؟ تكامل مع مزودي الشحن.'] },
        'cloud-software': { title: 'البرمجيات السحابية المخصصة', price: '€4,900+', desc: 'برمجيات سحابية مخصصة: ERP/CRM/Portals، بنية microservices، أمان Zero-Trust.', deliverables: ['تحليل متطلبات + خارطة طريق', 'بنية microservices على Cloudflare/AWS', 'API REST/GraphQL', 'SSO + RBAC', 'SLA 99.9%'], faq: ['المدة؟ 8-16 أسبوع.', 'الملكية؟ كود مصدري 100% لك.', 'الصيانة؟ SLA 12 شهر.'] },
        'mobile-web': { title: 'تطبيقات الجوال والويب', price: '€3,200+', desc: 'تطبيقات جوال (iOS/Android) وويب (PWA) بتجربة مستخدم سلسة ومتصلة بالـ ERP.', deliverables: ['UI/UX (Figma prototype)', 'React Native / Flutter', 'PWA (offline-first)', 'Push notifications', 'ربط API'], faq: ['منصة واحدة أم كلتاها؟ كلتاها.', 'التحديث؟ Over-the-air.', 'النشر؟ App Store + Play Store.'] },
        enterprise: { title: 'حلول أنظمة المؤسسات والربط المالي', price: '€6,500+', desc: 'ربط ERP/CRM/Banking (PSD2), توحيد بيانات المؤسسة, لوحات KPI, تدقيق.', deliverables: ['تكامل ERP/CRM/Banking', 'PSD2 Open Banking', 'ETL + Data Warehouse', 'لوحة KPI (real-time)', 'تدقيق + امتثال (GDPR)'], faq: ['الأمان؟ Zero-Trust + encryption.', 'الامتثال؟ GDPR/BTW/VAT.', 'التدريب؟ 2 جلسات.'] },
        'automation-ai': { title: 'أتمتة العمليات والذكاء الاصطناعي', price: '€2,800+', desc: 'أتمتة RPA + AI: استخراج فواتير، chatbots، تنبؤ، تحليل مستندات.', deliverables: ['RPA (UiPath/Make)', 'OCR + AI extraction', 'Chatbot (RAG)', 'تنبؤ (forecasting)', 'لوحة مراقبة'], faq: ['ROI؟ 3-6 أشهر.', 'البيانات؟ on-prem/Cloud.', 'التدريب؟ نموذج مخصص.'] },
        'finance-gov': { title: 'استشارات مالية وحوكمة رقمية', price: '€1,200+', desc: 'استشارات مالية: VAT/BTW, IFRS, CSRD/ESG, حوكمة, تدقيق.', deliverables: ['VAT/BTW compliance', 'IFRS reporting', 'CSRD/ESG report', 'خطة حوكمة', 'تدقيق داخلي'], faq: ['النطاق؟ SME/Enterprise.', 'اللغات؟ AR/NL/EN/DE.', 'المدة؟ 2-4 أسابيع.'] },
        'cloud-security': { title: 'البنية السحابية والأمن السيبراني', price: '€3,500+', desc: 'هندسة سحابية AWS/Azure + أمن: WAF, SIEM, SOC, penetration testing.', deliverables: ['Cloud architecture (AWS/Azure)', 'WAF + DDoS protection', 'SIEM/SOC setup', 'Penetration test', 'Disaster recovery (RTO/RPO)'], faq: ['SLA؟ 99.99%.', 'الامتثال؟ ISO 27001.', 'المراقبة؟ 24/7 SOC.'] }
    };

    var WA_MESSAGES = {
        identity: '*طلب خدمة الهوية البصرية - S&R CoreSync*\nأرغب في طلب تصميم هوية بصرية متكاملة بالسعر التنافسي (€590)',
        web: '*طلب خدمة تصميم المواقع - S&R CoreSync*\nأرغب في طلب تصميم موقع عصري عالي الأداء بالسعر التنافسي (€980)',
        ecommerce: '*طلب خدمة متجر إلكتروني - S&R CoreSync*\nأرغب في طلب متجر إلكتروني متكامل',
        'cloud-software': '*طلب برمجيات سحابية مخصصة - S&R CoreSync*\nأرغب في استشارة حول برمجيات سحابية مخصصة',
        'mobile-web': '*طلب تطبيقات جوال وويب - S&R CoreSync*\nأرغب في استشارة حول تطبيقات جوال وويب',
        enterprise: '*طلب حلول أنظمة مؤسسات - S&R CoreSync*\nأرغب في استشارة حول ربط أنظمة المؤسسات',
        'automation-ai': '*طلب أتمتة وذكاء اصطناعي - S&R CoreSync*\nأرغب في استشارة حول أتمتة العمليات والذكاء الاصطناعي',
        'finance-gov': '*طلب استشارات مالية وحوكمة - S&R CoreSync*\nأرغب في استشارة مالية وحوكمة رقمية',
        'cloud-security': '*طلب بنية سحابية وأمن سيبراني - S&R CoreSync*\nأرغب في استشارة حول البنية السحابية والأمن السيبراني'
    };

    function waUrl(key) {
        var msg = WA_MESSAGES[key] || ('*طلب خدمة - S&R CoreSync*\nأرغب في استشارة');
        return 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg);
    }

    // --- Dynamic WhatsApp links ---
    function enhanceWaLinks() {
        var links = document.querySelectorAll('a[data-wa-key]');
        for (var i = 0; i < links.length; i++) {
            var key = links[i].getAttribute('data-wa-key');
            links[i].setAttribute('href', waUrl(key));
            links[i].setAttribute('target', '_blank');
            links[i].setAttribute('rel', 'noopener noreferrer');
        }
    }

    // --- Service Detail Modal ---
    function ensureModal() {
        var m = document.getElementById('serviceDetailModal');
        if (m) { return m; }
        m = document.createElement('div');
        m.id = 'serviceDetailModal';
        m.className = 'sr-service-modal';
        m.setAttribute('role', 'dialog');
        m.setAttribute('aria-modal', 'true');
        m.setAttribute('aria-labelledby', 'sdm-title');
        m.innerHTML =
            '<div class="sr-service-modal-backdrop" data-sr-backdrop-call="closeServiceDetail"></div>' +
            '<div class="sr-service-modal-card">' +
                '<button type="button" class="sr-service-modal-close" data-sr-call="closeServiceDetail" aria-label="إغلاق">×</button>' +
                '<h3 id="sdm-title" class="sr-service-modal-title"></h3>' +
                '<p id="sdm-price" class="sr-service-modal-price"></p>' +
                '<p id="sdm-desc" class="sr-service-modal-desc"></p>' +
                '<h4 class="sr-service-modal-h4">المخرجات (Deliverables)</h4>' +
                '<ul id="sdm-deliv" class="sr-service-modal-list"></ul>' +
                '<h4 class="sr-service-modal-h4">أسئلة شائعة (FAQ)</h4>' +
                '<ul id="sdm-faq" class="sr-service-modal-list"></ul>' +
                '<div class="sr-service-modal-actions">' +
                    '<a id="sdm-wa" class="dana-whatsapp-cta" target="_blank" rel="noopener noreferrer">طلب عبر واتساب</a>' +
                    '<button type="button" class="dana-btn-booking" data-sr-call="openRfqModal" data-sr-args=\'["__KEY__"]\'>طلب عرض سعر (RFQ)</button>' +
                '</div>' +
            '</div>';
        document.body.appendChild(m);
        return m;
    }

    window.openServiceDetail = function (key) {
        var s = SERVICES[key];
        if (!s) { return; }
        var m = ensureModal();
        document.getElementById('sdm-title').textContent = s.title;
        document.getElementById('sdm-price').textContent = 'السعر: ' + s.price;
        document.getElementById('sdm-desc').textContent = s.desc;
        var dl = document.getElementById('sdm-deliv');
        dl.textContent = '';
        s.deliverables.forEach(function (d) { var li = document.createElement('li'); li.textContent = d; dl.appendChild(li); });
        var fl = document.getElementById('sdm-faq');
        fl.textContent = '';
        s.faq.forEach(function (f) { var li = document.createElement('li'); li.textContent = f; fl.appendChild(li); });
        var wa = document.getElementById('sdm-wa');
        wa.setAttribute('href', waUrl(key));
        // patch RFQ button arg
        var btn = m.querySelector('.dana-btn-booking');
        if (btn) { btn.setAttribute('data-sr-args', JSON.stringify([key])); }
        m.classList.add('open');
        document.body.style.overflow = 'hidden';
    };

    window.closeServiceDetail = function () {
        var m = document.getElementById('serviceDetailModal');
        if (m) { m.classList.remove('open'); }
        document.body.style.overflow = '';
    };

    // --- RFQ Modal ---
    function ensureRfqModal() {
        var m = document.getElementById('rfqModal');
        if (m) { return m; }
        m = document.createElement('div');
        m.id = 'rfqModal';
        m.className = 'sr-service-modal';
        m.setAttribute('role', 'dialog');
        m.setAttribute('aria-modal', 'true');
        m.setAttribute('aria-labelledby', 'rfq-title');
        m.innerHTML =
            '<div class="sr-service-modal-backdrop" data-sr-backdrop-call="closeRfqModal"></div>' +
            '<div class="sr-service-modal-card">' +
                '<button type="button" class="sr-service-modal-close" data-sr-call="closeRfqModal" aria-label="إغلاق">×</button>' +
                '<h3 id="rfq-title" class="sr-service-modal-title">طلب عرض سعر (RFQ)</h3>' +
                '<form id="rfqForm" novalidate>' +
                    '<div class="form-grid">' +
                        '<label class="form-field">الاسم<input type="text" name="name" required maxlength="80"></label>' +
                        '<label class="form-field">البريد الإلكتروني<input type="email" name="email" required></label>' +
                        '<label class="form-field">الخدمة<select name="service"></select></label>' +
                        '<label class="form-field">الميزانية (€)<input type="text" name="budget" placeholder="مثال: 1000-5000"></label>' +
                    '</div>' +
                    '<label class="form-field">متطلبات المشروع<textarea name="notes" rows="4" required></textarea></label>' +
                    '<div class="btn-row">' +
                        '<button type="submit" class="btn-action">إرسال الطلب</button>' +
                        '<button type="button" class="btn-secondary" data-sr-call="closeRfqModal">إلغاء</button>' +
                    '</div>' +
                    '<span id="rfq-msg" class="kpi-foot" role="status"></span>' +
                '</form>' +
            '</div>';
        document.body.appendChild(m);
        // populate service select
        var sel = m.querySelector('select[name="service"]');
        for (var k in SERVICES) {
            if (Object.prototype.hasOwnProperty.call(SERVICES, k)) {
                var opt = document.createElement('option');
                opt.value = k;
                opt.textContent = SERVICES[k].title;
                sel.appendChild(opt);
            }
        }
        var rfqLastSubmit = 0;
        m.querySelector('form').addEventListener('submit', function (e) {
            var now = Date.now();
            if (now - rfqLastSubmit < 30000) {
                var msgEl = document.getElementById('rfq-msg');
                msgEl.textContent = '⏳ يرجى الانتظار 30 ثانية قبل إرسال طلب آخر';
                msgEl.style.color = '#fda4af';
                e.preventDefault();
                return;
            }
            rfqLastSubmit = now;
            e.preventDefault();
            var fd = new FormData(e.target);
            var name = (fd.get('name') || '').toString().trim();
            var email = (fd.get('email') || '').toString().trim();
            var service = (fd.get('service') || '').toString();
            var budget = (fd.get('budget') || '').toString().trim();
            var notes = (fd.get('notes') || '').toString().trim();
            var msgEl = document.getElementById('rfq-msg');
            if (!name || !email || !notes) {
                msgEl.textContent = '⚠️ يرجى تعبئة الحقول المطلوبة';
                msgEl.style.color = '#fda4af';
                return;
            }
            var svcTitle = (SERVICES[service] && SERVICES[service].title) || service;
            var text = '*طلب عرض سعر (RFQ) - S&R CoreSync*\n' +
                'الاسم: ' + name + '\n' +
                'البريد: ' + email + '\n' +
                'الخدمة: ' + svcTitle + '\n' +
                (budget ? 'الميزانية: ' + budget + '\n' : '') +
                'المتطلبات: ' + notes;
            // optional worker POST (best-effort)
            try {
                fetch('https://sr-lead-capture.sr-coresync.workers.dev/lead', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ clientName: name, email: email, service: service, budget: budget, notes: notes, source: 'rfq-modal' })
                }).catch(function () {});
            } catch (err) {}
            msgEl.textContent = '✅ تم إرسال الطلب — سيتم فتح واتساب';
            msgEl.style.color = '#6ee7b7';
            window.open('https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(text), '_blank');
            e.target.reset();
        });
        return m;
    }

    window.openRfqModal = function (key) {
        var m = ensureRfqModal();
        var sel = m.querySelector('select[name="service"]');
        if (key && sel) { sel.value = key; }
        m.classList.add('open');
        document.body.style.overflow = 'hidden';
    };

    window.closeRfqModal = function () {
        var m = document.getElementById('rfqModal');
        if (m) { m.classList.remove('open'); }
        document.body.style.overflow = '';
    };

    // --- init ---
    function init() {
        enhanceWaLinks();
    }

    // --- Newsletter signup ---
    function initNewsletter() {
        var form = document.getElementById('newsletterForm');
        if (!form) { return; }
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var email = (form.querySelector('input[name="email"]').value || '').trim();
            var msg = document.getElementById('newsletter-msg');
            if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
                msg.textContent = '⚠️ بريد إلكتروني غير صالح';
                msg.style.color = '#fda4af';
                return;
            }
            try {
                fetch('https://sr-lead-capture.sr-coresync.workers.dev/lead', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ clientName: 'Newsletter', email: email, notes: 'Newsletter signup', source: 'newsletter' })
                }).catch(function () {});
            } catch (err) {}
            msg.textContent = '✅ تم الاشتراك — شكرًا!';
            msg.style.color = '#6ee7b7';
            form.reset();
        });
    }

    function enhanceA11y() {
        var cards = document.querySelectorAll('.dana-signature-card, .wg-tech-v2');
        for (var i = 0; i < cards.length; i++) {
            if (!cards[i].hasAttribute('role')) { cards[i].setAttribute('role', 'button'); }
            if (!cards[i].hasAttribute('tabindex')) { cards[i].setAttribute('tabindex', '0'); }
            cards[i].addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.click(); }
            });
        }
    }

    function init() {
        enhanceWaLinks();
        enhanceA11y();
        initNewsletter();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
