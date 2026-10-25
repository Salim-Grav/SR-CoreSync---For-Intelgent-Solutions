/**
 * S&R CoreSync For Intelligent Solutions — Sovereign Floating Quick-Dock Engine
 * Ultra-responsive macOS-style floating dock for seamless cross-navigation.
 */

(function () {
    'use strict';

    if (window.__SR_QUICK_DOCK_INITIALIZED__) return;
    window.__SR_QUICK_DOCK_INITIALIZED__ = true;

    document.addEventListener('DOMContentLoaded', initQuickDock);
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        initQuickDock();
    }

    function initQuickDock() {
        if (document.getElementById('srQuickDockContainer')) return;

        // Detect Subfolder (nl, en, de)
        const path = window.location.pathname.toLowerCase();
        const isSubdir = /\/(en|nl|de|fr|es|it|ckb|ar)\//.test(path);
        const prefix = isSubdir ? '../' : './';

        // Detect Language
        const htmlLang = (document.documentElement.getAttribute('lang') || 'ar').toLowerCase();

        // Localized dictionary
        const i18n = {
            ar: {
                home: 'الرئيسية ⌂',
                work: 'معرض الأعمال 💼',
                software: 'سوق البرمجيات 💻',
                whitelabel: 'حاسبة التراخيص 🧮',
                estimator: 'حاسبة المشاريع 📊',
                readiness: 'جاهزيتك الرقمية 🎯',
                whatsapp: 'استشارة VIP واتساب 💬',
                top: 'للأعلى ⬆️',
                toggle: 'إخفاء / إظهار'
            },
            en: {
                home: 'Home ⌂',
                work: 'Portfolio 💼',
                software: 'Software Hub 💻',
                whitelabel: 'License Quote 🧮',
                estimator: 'Estimator 📊',
                readiness: 'Digital Readiness 🎯',
                whatsapp: 'WhatsApp VIP 💬',
                top: 'Back to Top ⬆️',
                toggle: 'Toggle Dock'
            },
            nl: {
                home: 'Home ⌂',
                work: 'Portfolio 💼',
                software: 'Software Hub 💻',
                whitelabel: 'Licentie Offerte 🧮',
                estimator: 'Project Calculator 📊',
                readiness: 'Digitale Gereedheid 🎯',
                whatsapp: 'WhatsApp VIP 💬',
                top: 'Naar Boven ⬆️',
                toggle: 'Dock Wisselen'
            },
            de: {
                home: 'Startseite ⌂',
                work: 'Portfolio 💼',
                software: 'Software Hub 💻',
                whitelabel: 'Lizenzangebot 🧮',
                estimator: 'Projektrechner 📊',
                readiness: 'Digitale Reife 🎯',
                whatsapp: 'WhatsApp VIP 💬',
                top: 'Nach Oben ⬆️',
                toggle: 'Dock Umschalten'
            }
        };

        const t = i18n[htmlLang] || i18n.ar;

        // Determine which page we are on to highlight active dock icon
        const filename = path.split('/').pop() || 'index.html';
        const isIndex = filename === 'index.html' || filename === '';
        const isWork = filename.includes('preview-work');
        const isSoftware = filename.includes('preview-software');
        const isWlCalc = filename.includes('preview-whitelabel-calculator');
        const isEstimator = filename.includes('preview-estimator');
        const isReadiness = filename.includes('preview-readiness');

        // Ensure stylesheet is loaded
        const cssId = 'sr-quick-dock-css';
        if (!document.getElementById(cssId)) {
            const link = document.createElement('link');
            link.id = cssId;
            link.rel = 'stylesheet';
            link.href = prefix + 'css/sr-quick-dock.css';
            document.head.appendChild(link);
        }

        // WhatsApp direct link with localized message
        const waText = htmlLang === 'nl' 
            ? 'Hallo S&R CoreSync, ik wil graag een VIP-adviesgesprek inplannen.' 
            : (htmlLang === 'de' 
                ? 'Hallo S&R CoreSync, ich möchte eine VIP-Beratung vereinbaren.' 
                : (htmlLang === 'en' 
                    ? 'Hello S&R CoreSync, I would like to schedule a VIP consultation.' 
                    : 'مرحباً S&R CoreSync، أود حجز استشارة تنفيذية VIP مباشرة.'));
        const waUrl = 'https://wa.me/31687764998?text=' + encodeURIComponent(waText);

        // Build HTML
        const container = document.createElement('div');
        container.className = 'sr-quick-dock-container';
        container.id = 'srQuickDockContainer';

        container.innerHTML = `
            <nav class="sr-quick-dock" aria-label="Sovereign Quick Navigation Dock">
                <a href="${isIndex ? '#hero' : prefix + 'index.html'}" class="sr-dock-item ${isIndex ? 'active' : ''}" data-target="home" aria-label="${t.home}">
                    <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                    <span class="sr-dock-tooltip">${t.home}</span>
                </a>

                <a href="${prefix}work.html#platforms" class="sr-dock-item ${isWork ? 'active' : ''}" data-target="work" aria-label="${t.work}">
                    <svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                    <span class="sr-dock-tooltip">${t.work}</span>
                </a>

                <a href="${prefix}software.html" class="sr-dock-item ${isSoftware ? 'active' : ''}" data-target="software" aria-label="${t.software}">
                    <svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <span class="sr-dock-tooltip">${t.software}</span>
                </a>

                <div class="sr-dock-divider" aria-hidden="true"></div>

                <a href="${prefix}whitelabel-calculator.html" class="sr-dock-item sr-dock-item--special ${isWlCalc ? 'active' : ''}" data-target="whitelabel" aria-label="${t.whitelabel}">
                    <svg viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line><path d="M16 10h.01"></path><path d="M12 10h.01"></path><path d="M8 10h.01"></path><path d="M12 14h.01"></path><path d="M8 14h.01"></path><path d="M12 18h.01"></path><path d="M8 18h.01"></path></svg>
                    <span class="sr-dock-tooltip">${t.whitelabel}</span>
                </a>

                <a href="${prefix}estimator.html" class="sr-dock-item ${isEstimator ? 'active' : ''}" data-target="estimator" aria-label="${t.estimator}">
                    <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                    <span class="sr-dock-tooltip">${t.estimator}</span>
                </a>

                <a href="${prefix}preview-readiness.html" class="sr-dock-item ${isReadiness ? 'active' : ''}" data-target="readiness" aria-label="${t.readiness}">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                    <span class="sr-dock-tooltip">${t.readiness}</span>
                </a>

                <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="sr-dock-item sr-dock-item--whatsapp" aria-label="${t.whatsapp}">
                    <svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                    <span class="sr-dock-tooltip">${t.whatsapp}</span>
                </a>

                <div class="sr-dock-divider" aria-hidden="true"></div>

                <button type="button" class="sr-dock-item" id="srDockScrollTop" aria-label="${t.top}">
                    <svg viewBox="0 0 24 24"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
                    <span class="sr-dock-tooltip">${t.top}</span>
                </button>

                <button type="button" class="sr-dock-toggle" id="srDockToggle" aria-label="${t.toggle}" title="${t.toggle}">
                    <svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
                </button>
            </nav>
        `;

        document.body.appendChild(container);

        // Scroll Top Handler
        const btnTop = document.getElementById('srDockScrollTop');
        if (btnTop) {
            btnTop.addEventListener('click', (e) => {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }

        // Minimize / Toggle Handler
        const btnToggle = document.getElementById('srDockToggle');
        if (btnToggle) {
            btnToggle.addEventListener('click', () => {
                container.classList.toggle('minimized');
                const isMin = container.classList.contains('minimized');
                try {
                    localStorage.setItem('sr_quick_dock_minimized', isMin ? '1' : '0');
                } catch (e) {}
            });

            // Restore state
            try {
                if (localStorage.getItem('sr_quick_dock_minimized') === '1') {
                    container.classList.add('minimized');
                }
            } catch (e) {}
        }

        // Smart Visibility:
        // Dedicated app tools/calculators/hubs show dock by default; Homepage shows on scroll > 200px
        const isToolPage = isWork || isSoftware || isWlCalc || isEstimator || isReadiness;

        function updateVisibility() {
            const scrollY = window.scrollY || document.documentElement.scrollTop;
            if (isToolPage || scrollY > 200) {
                container.classList.add('visible');
            } else {
                container.classList.remove('visible');
            }
        }

        let scrollTimeout;
        function handleScroll() {
            if (scrollTimeout) return;
            scrollTimeout = setTimeout(() => {
                updateVisibility();
                scrollTimeout = null;
            }, 40);
        }

        window.addEventListener('scroll', handleScroll, { passive: true });
        // Initial trigger
        setTimeout(updateVisibility, 150);
    }
})();
