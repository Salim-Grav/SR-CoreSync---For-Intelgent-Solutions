/**
 * S&R CoreSync For Intelligent Solutions - Sovereign Master Shell Engine (MSE)
 * Governs Global Navigation, Universal Drawer (31+ Studios), Typography Resizer & Layout Inheritance
 * Version: 2026.11-MasterSovereign
 */

(function () {
    'use strict';

    // 1. Directory of all Official S&R CoreSync Platforms, Studios & Portals
    const SR_PLATFORM_REGISTRY = [
        { id: 'home', title: 'الرئيسية والمنظومة الأم', num: '01 /', url: './index.html', tag: 'الرئيسية 🏠' },
        { id: 'demo', title: 'النظام التجريبي السحابي', num: '02 /', url: './demo.html', tag: 'تجريبي ⚡' },
        { id: 'software', title: 'سوق البرمجيات والأنظمة', num: '03 /', url: './software.html', tag: 'سوق 💻' },
        { id: 'api_docs', title: 'توثيق الـ API السيادي (OpenAPI 3.1)', num: '04 /', url: './api-docs.html', tag: 'توثيق 📖' },
        { id: 'brand_studio', title: 'استوديو الهوية البصرية والمطابقة', num: '05 /', url: './brand-identity-studio.html', tag: 'هوية 🎨' },
        { id: 'web_showcase', title: 'معرض واجهات الويب والمتاجر الفاخرة', num: '06 /', url: './web-showcase-studio.html', tag: 'معرض 🌐' },
        { id: 'device_simulator', title: 'استوديو محاكاة الأجهزة 3D', num: '07 /', url: './device-simulator-studio.html', tag: 'محاكاة 📱' },
        { id: 'invoice_engine', title: 'محرك الفوترة الرقمية ZATCA', num: '08 /', url: './invoice-engine.html', tag: 'فوترة 🧾' },
        { id: 'smart_proposal', title: 'بوابة العروض والتعاقد الذكي المباشر', num: '09 /', url: './smart-proposal-portal.html', tag: 'عقود 🤝' },
        { id: 'crm_dashboard', title: 'لوحة CRM والتحليلات الحية', num: '10 /', url: './crm-dashboard.html', tag: 'تحليلات 📊' },
        { id: 'payment_gateway', title: 'بوابة المدفوعات الدولية الموحدة', num: '11 /', url: './payment-gateway.html', tag: 'دفع 💳' },
        { id: 'ecommerce_launchpad', title: 'استوديو توليد المتاجر الفورية', num: '12 /', url: './ecommerce-launchpad.html', tag: 'متاجر 🛍️' },
        { id: 'landing_builder', title: 'مولّد صفحات الهبوط فائقة التحويل', num: '13 /', url: './landing-page-builder.html', tag: 'هبوط 🚀' },
        { id: 'webhook_hub', title: 'مركز أتمتة الـ Webhooks والربط السحابي', num: '14 /', url: './webhook-integration-hub.html', tag: 'سحابي ⚡' },
        { id: 'security_center', title: 'مركز الأمان وشارات التوثيق', num: '15 /', url: './security-trust-center.html', tag: 'أمان 🛡️' },
        { id: 'social_ads', title: 'استوديو أصول التواصل 8K', num: '16 /', url: './social-ads-studio.html', tag: 'إعلانات 🎨' },
        { id: 'badge_3d', title: 'محرك الشارات والأيقونات 3D', num: '17 /', url: './icon-badge-3d-generator.html', tag: 'شارات 3D ✨' },
        { id: 'api_playground', title: 'بيئة اختبار واجهات البرمجة (Playground)', num: '18 /', url: './api-playground.html', tag: 'API 🌐' },
        { id: 'financial_charts', title: 'استوديو الرسوم البيانية المالية', num: '19 /', url: './financial-charts-studio.html', tag: 'مخططات 📈' },
        { id: 'ip_nda', title: 'محرك عقود الملكية الفكرية وNDA', num: '20 /', url: './ip-nda-smart-contract.html', tag: 'عقود 📜' },
        { id: 'executive_id', title: 'استوديو الهويات الرقمية التنفيذية 3D', num: '21 /', url: './executive-digital-id.html', tag: 'هويات 🪪' },
        { id: '3d_configurator', title: 'محرك تخصيص المنتجات الفاخرة 3D', num: '22 /', url: './3d-product-configurator.html', tag: 'منتجات 3D 💎' },
        { id: 'dynamic_qr', title: 'استوديو أكواد QR الديناميكية المشفرة', num: '23 /', url: './dynamic-qr-studio.html', tag: 'QR ذكي 📲' }
    ];

    // 2. Universal Typography Scale Controller (A+ / A- Persistent Engine)
    const SR_FONT_SCALE_KEY = 'sr_unified_font_scale';
    let currentScalePercent = parseInt(localStorage.getItem(SR_FONT_SCALE_KEY), 10) || 100;

    function applyFontScale(percent) {
        currentScalePercent = Math.max(85, Math.min(130, percent));
        localStorage.setItem(SR_FONT_SCALE_KEY, currentScalePercent);
        document.documentElement.style.setProperty('--sr-font-scale', `${currentScalePercent}%`);
        
        // Update all indicators on page
        document.querySelectorAll('.sr-resizer-val, [data-sr-resizer-val]').forEach(el => {
            el.textContent = `${currentScalePercent}%`;
        });
    }

    window.srAdjustFontSize = function (delta) {
        applyFontScale(currentScalePercent + (delta * 5));
    };

    window.srResetFontSize = function () {
        applyFontScale(100);
    };

    // Apply scale on boot
    applyFontScale(currentScalePercent);

    // 3. Universal Offcanvas Drawer Generator & Controller
    function createMasterDrawer() {
        if (document.getElementById('srMasterDrawer')) return;

        const currentPath = window.location.pathname.split('/').pop() || 'index.html';

        const backdrop = document.createElement('div');
        backdrop.id = 'srMasterDrawerBackdrop';
        backdrop.className = 'sr-master-drawer-backdrop';
        backdrop.onclick = closeMasterDrawer;

        const drawer = document.createElement('aside');
        drawer.id = 'srMasterDrawer';
        drawer.className = 'sr-master-drawer';
        drawer.setAttribute('aria-label', 'خريطة المنصة السيادية الموحدة');

        let itemsHtml = '';
        SR_PLATFORM_REGISTRY.forEach(item => {
            const isActive = currentPath === item.url.replace('./', '');
            itemsHtml += `
                <li class="sr-drawer-item">
                    <a href="${item.url}" class="${isActive ? 'active' : ''}">
                        <span>${item.title}</span>
                        <span class="sr-drawer-item-num">${item.num}</span>
                    </a>
                </li>
            `;
        });

        drawer.innerHTML = `
            <div class="sr-drawer-header">
                <div style="display:flex; align-items:center; gap:10px;">
                    <img src="./assets/sr-core-emblem.svg" alt="S&R Emblem" width="30" height="30">
                    <span style="font-weight:900; color:var(--sr-gold-light); font-size:0.95rem;">خريطة المنظومة الموحدة</span>
                </div>
                <button type="button" onclick="srCloseMasterDrawer()" style="background:none; border:none; color:#cbd5e1; font-size:1.4rem; cursor:pointer; line-height:1;">✕</button>
            </div>
            <div style="padding: 12px 24px; border-bottom: 1px solid var(--sr-border-subtle); display:flex; align-items:center; justify-content:space-between;">
                <span style="font-size:0.78rem; color:var(--sr-text-muted);">حجم الخط والقراءة:</span>
                <div class="sr-text-resizer-widget">
                    <button type="button" class="sr-resizer-btn" onclick="srAdjustFontSize(-1)" title="تصغير الخط (A-)">A-</button>
                    <button type="button" class="sr-resizer-indicator" onclick="srResetFontSize()" title="إعادة الضبط (100%)">
                        <span class="sr-resizer-val">${currentScalePercent}%</span>
                    </button>
                    <button type="button" class="sr-resizer-btn" onclick="srAdjustFontSize(1)" title="تكبير الخط (A+)">A+</button>
                </div>
            </div>
            <div class="sr-drawer-body">
                <ul class="sr-drawer-list">
                    ${itemsHtml}
                </ul>
            </div>
            <div style="padding:16px 24px; border-top:1px solid var(--sr-border-subtle); font-size:0.75rem; color:var(--sr-text-muted); text-align:center;">
                S&R CoreSync For Intelligent Solutions • 2026
            </div>
        `;

        document.body.appendChild(backdrop);
        document.body.appendChild(drawer);
    }

    window.srOpenMasterDrawer = function () {
        createMasterDrawer();
        document.getElementById('srMasterDrawer').classList.add('open');
        document.getElementById('srMasterDrawerBackdrop').classList.add('open');
        document.body.style.overflow = 'hidden';
    };

    window.srCloseMasterDrawer = function () {
        const drawer = document.getElementById('srMasterDrawer');
        const backdrop = document.getElementById('srMasterDrawerBackdrop');
        if (drawer) drawer.classList.remove('open');
        if (backdrop) backdrop.classList.remove('open');
        document.body.style.overflow = '';
    };

    function closeMasterDrawer() {
        window.srCloseMasterDrawer();
    }

    // Escape Key Listener for Accessibility
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            window.srCloseMasterDrawer();
        }
    });

    // 4. Auto-Enhance Existing Navbars Across Studio Pages
    function autoEnhanceNavbar() {
        const nav = document.querySelector('.navbar, .nav, .sr-master-navbar');
        if (!nav) return;

        // Ensure master class
        nav.classList.add('sr-master-navbar');

        // Check if hamburger button exists; if not, append one
        let toggleBtn = nav.querySelector('.sr-master-menu-toggle, [data-sr-call="toggleMobileMenu"]');
        if (!toggleBtn) {
            const actionsBox = document.createElement('div');
            actionsBox.className = 'sr-master-nav-actions';
            actionsBox.innerHTML = `
                <div class="sr-text-resizer-widget" style="display:none; @media(min-width:768px){display:inline-flex;}">
                    <button type="button" class="sr-resizer-btn" onclick="srAdjustFontSize(-1)" title="تصغير الخط">A-</button>
                    <button type="button" class="sr-resizer-indicator" onclick="srResetFontSize()" title="إعادة ضبط">
                        <span class="sr-resizer-val">${currentScalePercent}%</span>
                    </button>
                    <button type="button" class="sr-resizer-btn" onclick="srAdjustFontSize(1)" title="تكبير الخط">A+</button>
                </div>
                <button type="button" class="sr-master-menu-toggle" onclick="srOpenMasterDrawer()">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
                    <span>القائمة الشاملة</span>
                </button>
            `;
            nav.appendChild(actionsBox);
        }
    }

    // Boot on DOMContentLoaded or immediately if ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            createMasterDrawer();
            autoEnhanceNavbar();
        });
    } else {
        createMasterDrawer();
        autoEnhanceNavbar();
    }

})();

