/**
 * ==============================================================================
 * S&R CoreSync - Header Support Tools Dropdown Controller
 * ==============================================================================
 * Provides seamless management of the luxury Header Support Dropdown:
 * - Readiness Assessment (openReadinessModal)
 * - Executive Scheduler (openSchedulerModal)
 * - Client Feedback (openFeedbackModal)
 * ==============================================================================
 */

(function () {
    'use strict';

    function initHeaderSupport() {
        const wrap = document.getElementById('headerSupportDropdownWrap');
        const btn = document.getElementById('headerSupportBtn');
        const menu = document.getElementById('headerSupportMenu');

        if (!wrap || !btn || !menu) return;

        function closeMenu() {
            if (wrap.classList.contains('is-active')) {
                wrap.classList.remove('is-active');
                btn.setAttribute('aria-expanded', 'false');
            }
        }

        function toggleMenu(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            const isActive = wrap.classList.toggle('is-active');
            btn.setAttribute('aria-expanded', isActive ? 'true' : 'false');
        }

        btn.addEventListener('click', toggleMenu);

        // Action items inside dropdown
        menu.querySelectorAll('.support-menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                closeMenu();

                const action = item.getAttribute('data-action');
                if (action === 'readiness') {
                    if (typeof window.openReadinessModal === 'function') {
                        window.openReadinessModal();
                    }
                } else if (action === 'scheduler') {
                    if (typeof window.openSchedulerModal === 'function') {
                        window.openSchedulerModal();
                    }
                } else if (action === 'feedback') {
                    if (typeof window.openFeedbackModal === 'function') {
                        window.openFeedbackModal();
                    }
                }
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!wrap.contains(e.target)) {
                closeMenu();
            }
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeMenu();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeaderSupport);
    } else {
        initHeaderSupport();
    }
})();
