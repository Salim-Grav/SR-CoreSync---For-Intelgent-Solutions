/**
 * S&R CoreSync Solutions — European Trust Ribbon & Compliance Verification Engine
 * Interactive modal verification for European enterprise standards.
 */

(function () {
    'use strict';

    if (window.__SR_TRUST_RIBBON_INITIALIZED__) return;
    window.__SR_TRUST_RIBBON_INITIALIZED__ = true;

    const COMPLIANCE_SPECS = {
        gdpr: {
            code: 'EU 2016/679',
            title: 'اللائحة العامة لحماية البيانات (GDPR)',
            icon: '🛡️',
            desc: 'امتثال تام وصارم لجميع متطلبات حماية الخصوصية للشركات والمستخدمين في الاتحاد الأوروبي، مع تشفير شامل وعزل تام لقواعد البيانات.',
            specs: [
                { key: 'المعيار القانوني', val: 'Regulation (EU) 2016/679' },
                { key: 'مستوى التشفير', val: 'AES-256 (At Rest) / TLS 1.3 (In Transit)' },
                { key: 'موقع تخزين البيانات', val: 'مراكز بيانات سيادية داخل أمستردام (هولندا)' },
                { key: 'حقوق المستخدم', val: 'حق الحذف الكامل (Right to be Forgotten) فوري' }
            ]
        },
        btw: {
            code: 'Belastingdienst Fiscal',
            title: 'الامتثال الضريبي الهولندي (BTW)',
            icon: '🏛️',
            desc: 'توافق كامل مع أنظمة الفوترة الإلكترونية المعتمدة لدى مصلحة الضرائب الهولندية (Belastingdienst)، وحساب لحظي لشرائح BTW (9% و 21%).',
            specs: [
                { key: 'الجهة التنظيمية', val: 'Belastingdienst (وزارة المالية الهولندية)' },
                { key: 'معايير الفاتورة الرقمية', val: 'PEPPOL BIS Billing 3.0 / UBL 2.1 XML' },
                { key: 'حساب الضرائب', val: 'آلي 100% وفق شرائح BTW الهولندية' },
                { key: 'الأرشفة المحاسبية', val: 'حفظ آمن لمدة 7 سنوات وفق القانون الهولندي' }
            ]
        },
        amsix: {
            code: 'AMS-IX Infrastructure',
            title: 'بنية استضافة سيادية في أمستردام (AMS-IX)',
            icon: '🌐',
            desc: 'استضافة الأنظمة السحابية بجوار نقطة تبادل الإنترنت العالمية في أمستردام AMS-IX، لضمان أدنى زمن استجابة وأعلى موثوقية في أوروبا.',
            specs: [
                { key: 'مركز البيانات', val: 'AMS-NODE-01 (Amsterdam Tier 3+ Facility)' },
                { key: 'زمن الاستجابة (Latency)', val: '< 5ms عبر عموم غرب أوروبا' },
                { key: 'الاتصال بالإنترنت', val: 'Direct Multi-100Gbps Peering' },
                { key: 'مصدر الطاقة', val: '100% طاقة خضراء متجددة ومولدات طوارئ' }
            ]
        },
        sla: {
            code: '99.98% High Availability',
            title: 'اتفاقية مستوى الخدمة السحابية (SLA)',
            icon: '⚡',
            desc: 'ضمان تعاقدي لاستمرارية تشغيل الأنظمة بنسبة 99.98% مع منظومة تعافي فوري من الكوارث ونسخ احتياطي لحظي متعدد المراكز.',
            specs: [
                { key: 'نسبة الجاهزية المضمونة', val: '99.98% تشغيل مستمر سنوياً' },
                { key: 'زمن التعافي المستهدف (RTO)', val: 'أقل من 15 دقيقة (Hot Standby)' },
                { key: 'نقطة الاسترجاع المستهدفة (RPO)', val: 'أقل من 5 دقائق من حركة البيانات' },
                { key: 'المراقبة الاستباقية', val: 'رصد لحظي 24/7/365 مع إنذار تلقائي' }
            ]
        },
        iso: {
            code: 'ISO 27001 & SOC 2',
            title: 'حوكمة أمن المعلومات والأمن السيبراني',
            icon: '🔒',
            desc: 'تطبيق إطار العمل الدولي لأمن المعلومات وضوابط الوصول المشددة لمنع أي اختراق أو تسريب في بيئة العمل السحابية.',
            specs: [
                { key: 'إطار العمل', val: 'ISO/IEC 27001:2022 ISMS Controls' },
                { key: 'إدارة الهويات والوصول', val: 'RBAC / MFA / WebAuthn Hardware Tokens' },
                { key: 'فحص الثغرات الدوري', val: 'Penetration Testing & Static Code SAST' },
                { key: 'سجلات المراجعة (Audit)', val: 'Immutable Audit Logs مشفرة ضد التعديل' }
            ]
        },
        zeroknowledge: {
            code: 'Zero-Knowledge Security',
            title: 'بنية التشفير السيادي المعزول',
            icon: '🛡️',
            desc: 'عزل تام لقواعد بيانات كل مؤسسة مع مفاتيح تشفير مستقلة، تضمن عدم إمكانية اطلاع أي طرف خارجي أو تقني على بياناتك.',
            specs: [
                { key: 'ملكية المفاتيح', val: 'Client-Controlled Encryption Keys' },
                { key: 'عزل البيانات (Tenancy)', val: 'Strict Multi-Tenant Database Isolation' },
                { key: 'سياسة الأبواب الخلفية', val: 'ممنوعة ومستحيلة برمجياً (No Backdoors)' },
                { key: 'عقد السرية (NDA)', val: 'محمي بالقانون التجاري الهولندي والأوروبي' }
            ]
        }
    };

    document.addEventListener('DOMContentLoaded', initTrustRibbon);
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        initTrustRibbon();
    }

    function initTrustRibbon() {
        const cards = document.querySelectorAll('.sr-trust-card[data-compliance]');
        if (!cards.length) return;

        // Create modal if not exists
        createTrustModal();

        cards.forEach(card => {
            card.addEventListener('click', function (e) {
                e.preventDefault();
                const key = this.getAttribute('data-compliance');
                openTrustModal(key);
            });
        });
    }

    function createTrustModal() {
        if (document.getElementById('srTrustModal')) return;

        const modal = document.createElement('div');
        modal.className = 'sr-trust-modal';
        modal.id = 'srTrustModal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-labelledby', 'srTrustModalTitle');

        modal.innerHTML = `
            <div class="sr-trust-modal-box">
                <button type="button" class="sr-trust-modal-close" id="srTrustModalClose" aria-label="إغلاق النافذة">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
                <div class="sr-trust-modal-header">
                    <div class="sr-trust-modal-icon" id="srTrustModalIcon">🛡️</div>
                    <div>
                        <span class="sr-trust-modal-code" id="srTrustModalCode">EU 2016/679</span>
                        <h3 class="sr-trust-modal-title" id="srTrustModalTitle">شهادة الاعتماد</h3>
                    </div>
                </div>
                <div class="sr-trust-modal-body">
                    <p id="srTrustModalDesc"></p>
                    <div class="sr-trust-spec-list" id="srTrustModalSpecs"></div>
                    <button type="button" class="sr-trust-modal-btn" onclick="window.srCloseTrustModal()">
                        <span>إغلاق والمتابعة ✓</span>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        modal.addEventListener('click', (e) => {
            if (e.target === modal) window.srCloseTrustModal();
        });

        document.getElementById('srTrustModalClose').addEventListener('click', () => {
            window.srCloseTrustModal();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                window.srCloseTrustModal();
            }
        });
    }

    function openTrustModal(key) {
        const data = COMPLIANCE_SPECS[key];
        if (!data) return;

        const modal = document.getElementById('srTrustModal');
        if (!modal) return;

        document.getElementById('srTrustModalIcon').textContent = data.icon;
        document.getElementById('srTrustModalCode').textContent = data.code;
        document.getElementById('srTrustModalTitle').textContent = data.title;
        document.getElementById('srTrustModalDesc').textContent = data.desc;

        const specsContainer = document.getElementById('srTrustModalSpecs');
        specsContainer.innerHTML = data.specs.map(s => `
            <div class="sr-trust-spec-row">
                <span class="sr-trust-spec-key">${s.key}:</span>
                <span class="sr-trust-spec-val">${s.val}</span>
            </div>
        `).join('');

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    window.srCloseTrustModal = function () {
        const modal = document.getElementById('srTrustModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    };
})();
