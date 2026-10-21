/**
 * S&R CoreSync Solutions — Enterprise Tier Matrix & Institutional Calculator
 * Dynamic billing cycle toggle, multi-entity discount, and interactive quote generator.
 */

(function () {
    'use strict';

    if (window.__SR_TIER_MATRIX_INITIALIZED__) return;
    window.__SR_TIER_MATRIX_INITIALIZED__ = true;

    // Base Monthly Prices in EUR
    const BASE_PRICES = {
        starter: {
            monthly: 1490,
            name: 'Core Starter',
            waKey: 'Core Starter'
        },
        pro: {
            monthly: 2890,
            name: 'Business Pro',
            waKey: 'Business Pro'
        },
        enterprise: {
            monthly: 5400,
            name: 'Sovereign Enterprise',
            waKey: 'Sovereign Enterprise'
        }
    };

    let currentBilling = 'annual'; // 'monthly' | 'annual' (default to annual with 20% discount)
    let currentEntities = 1;      // 1 | 2 | 4

    document.addEventListener('DOMContentLoaded', initTierMatrix);
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        initTierMatrix();
    }

    function initTierMatrix() {
        const matrixSection = document.getElementById('tier-matrix');
        if (!matrixSection) return;

        // Billing Cycle Buttons
        const billingBtns = matrixSection.querySelectorAll('.sr-tier-toggle-btn');
        billingBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                billingBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentBilling = this.getAttribute('data-billing') || 'annual';
                updateAllPrices();
            });
        });

        // Entity Count Buttons
        const entityBtns = matrixSection.querySelectorAll('.sr-tier-entity-btn');
        entityBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                entityBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentEntities = parseInt(this.getAttribute('data-entities') || '1', 10);
                updateAllPrices();
            });
        });

        // Initialize prices
        updateAllPrices();
    }

    function updateAllPrices() {
        // Calculation Logic:
        // Annual discount: 20% off base
        // Multi-entity discount: 1 = 0%, 2 = 10%, 4 = 20%
        const isAnnual = currentBilling === 'annual';
        const annualDiscount = isAnnual ? 0.20 : 0.0;
        let entityDiscount = 0.0;
        if (currentEntities === 2) entityDiscount = 0.10;
        else if (currentEntities >= 4) entityDiscount = 0.20;

        const totalDiscountMultiplier = (1 - annualDiscount) * (1 - entityDiscount);

        ['starter', 'pro', 'enterprise'].forEach(tierKey => {
            const base = BASE_PRICES[tierKey].monthly;
            const finalMonthly = Math.round(base * totalDiscountMultiplier);
            const billedText = isAnnual ? 'تُدفع سنوياً (وفّر 20%)' : 'تُدفع شهرياً';

            // DOM Elements
            const amountEl = document.getElementById(`tier-price-${tierKey}`);
            const periodEl = document.getElementById(`tier-period-${tierKey}`);
            const originalEl = document.getElementById(`tier-orig-${tierKey}`);
            const noteEl = document.getElementById(`tier-note-${tierKey}`);
            const ctaBtn = document.getElementById(`tier-cta-${tierKey}`);

            if (amountEl) {
                amountEl.textContent = formatNumber(finalMonthly);
            }

            if (periodEl) {
                periodEl.textContent = isAnnual ? '/ شهرياً' : '/ شهرياً';
            }

            if (originalEl) {
                if (isAnnual || entityDiscount > 0) {
                    originalEl.textContent = `€${formatNumber(base)}`;
                    originalEl.style.display = 'inline-block';
                } else {
                    originalEl.style.display = 'none';
                }
            }

            if (noteEl) {
                if (entityDiscount > 0 && isAnnual) {
                    noteEl.textContent = `خصم مجمّع ${Math.round((1 - totalDiscountMultiplier) * 100)}% (${currentEntities} كيانات)`;
                } else if (entityDiscount > 0) {
                    noteEl.textContent = `خصم مؤسسي ${Math.round(entityDiscount * 100)}% (${currentEntities} كيانات)`;
                } else if (isAnnual) {
                    noteEl.textContent = billedText;
                } else {
                    noteEl.textContent = 'مرونة إلغاء شهرية';
                }
            }

            // Update WhatsApp CTA Link
            if (ctaBtn) {
                const tierName = BASE_PRICES[tierKey].name;
                const billingName = isAnnual ? 'السنوية (مع خصم 20%)' : 'الشهرية';
                const entityText = currentEntities === 1 ? 'كيان واحد' : `${currentEntities} كيانات مؤسسية`;
                const msg = encodeURIComponent(
                    `مرحباً S&R CoreSync، أود الاستفسار وحجز باقة (${tierName}) بدورة الفوترة ${billingName} لعدد ${entityText} بسعر استثماري معتمد €${formatNumber(finalMonthly)}/شهرياً.`
                );
                ctaBtn.href = `https://wa.me/31687764998?text=${msg}`;
            }
        });
    }

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    // Expose Global Helper
    window.srSetTierMatrix = function (billing, entities) {
        if (billing) currentBilling = billing;
        if (entities) currentEntities = entities;
        updateAllPrices();
    };
})();
