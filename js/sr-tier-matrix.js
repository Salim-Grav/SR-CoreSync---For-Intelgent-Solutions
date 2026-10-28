/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

/**
 * S&R CoreSync For Intelligent Solutions — Enterprise Tier Matrix & Institutional Calculator
 * Multilingual dynamic billing cycle toggle, multi-entity discount, and quote generator (AR, EN, NL, DE).
 */

(function () {
    'use strict';

    if (window.__SR_TIER_MATRIX_INITIALIZED__) return;
    window.__SR_TIER_MATRIX_INITIALIZED__ = true;

    const BASE_PRICES = {
        starter: {
            monthly: 1490,
            names: { ar: 'Core Starter', en: 'Core Starter', nl: 'Core Starter', de: 'Core Starter' }
        },
        pro: {
            monthly: 2890,
            names: { ar: 'Business Pro', en: 'Business Pro', nl: 'Business Pro', de: 'Business Pro' }
        },
        enterprise: {
            monthly: 5400,
            names: { ar: 'Sovereign Enterprise', en: 'Sovereign Enterprise', nl: 'Sovereign Enterprise', de: 'Sovereign Enterprise' }
        }
    };

    const I18N = {
        ar: {
            period: '/ شهرياً',
            billedAnnual: 'تُدفع سنوياً (وفّر 20%)',
            billedMonthly: 'مرونة إلغاء شهرية',
            comboDiscount: (pct, ent) => `خصم مجمّع ${pct}% (${ent} كيانات)`,
            entityDiscount: (pct, ent) => `خصم مؤسسي ${pct}% (${ent} كيانات)`,
            entitySingle: 'كيان واحد',
            entityMultiple: (n) => `${n} كيانات مؤسسية`,
            billingAnnualText: 'السنوية (مع خصم 20%)',
            billingMonthlyText: 'الشهرية',
            waMsg: (tier, bill, ent, price) =>
                `مرحباً S&R CoreSync، أود الاستفسار وحجز باقة (${tier}) بدورة الفوترة ${bill} لعدد ${ent} بسعر استثماري معتمد €${price}/شهرياً.`
        },
        en: {
            period: '/ month',
            billedAnnual: 'Billed annually (Save 20%)',
            billedMonthly: 'Monthly flexible billing',
            comboDiscount: (pct, ent) => `Combined discount ${pct}% (${ent} entities)`,
            entityDiscount: (pct, ent) => `Corporate discount ${pct}% (${ent} entities)`,
            entitySingle: 'Single Entity',
            entityMultiple: (n) => `${n} Corporate Entities`,
            billingAnnualText: 'Annual (with 20% discount)',
            billingMonthlyText: 'Monthly',
            waMsg: (tier, bill, ent, price) =>
                `Hello S&R CoreSync, I would like to inquire about and book the (${tier}) package on the ${bill} cycle for ${ent} at the corporate rate of €${price}/month.`
        },
        nl: {
            period: '/ maand',
            billedAnnual: 'Jaarlijks gefactureerd (Bespaar 20%)',
            billedMonthly: 'Maandelijks opzegbaar',
            comboDiscount: (pct, ent) => `Gecombineerde korting ${pct}% (${ent} entiteiten)`,
            entityDiscount: (pct, ent) => `Bedrijfskorting ${pct}% (${ent} entiteiten)`,
            entitySingle: 'Enkele entiteit',
            entityMultiple: (n) => `${n} Zakelijke entiteiten`,
            billingAnnualText: 'Jaarlijks (met 20% korting)',
            billingMonthlyText: 'Maandelijks',
            waMsg: (tier, bill, ent, price) =>
                `Hallo S&R CoreSync, ik wil graag het (${tier}) pakket reserveren met ${bill} facturatie voor ${ent} tegen het zakelijke tarief van €${price}/maand.`
        },
        de: {
            period: '/ Monat',
            billedAnnual: 'Jährliche Abrechnung (20% sparen)',
            billedMonthly: 'Monatlich kündbar',
            comboDiscount: (pct, ent) => `Kombirabatt ${pct}% (${ent} Einheiten)`,
            entityDiscount: (pct, ent) => `Unternehmensrabatt ${pct}% (${ent} Einheiten)`,
            entitySingle: 'Einzelne Einheit',
            entityMultiple: (n) => `${n} Unternehmenseinheiten`,
            billingAnnualText: 'Jährlich (inkl. 20% Rabatt)',
            billingMonthlyText: 'Monatlich',
            waMsg: (tier, bill, ent, price) =>
                `Hallo S&R CoreSync, ich möchte das (${tier}) Paket mit ${bill} Abrechnung für ${ent} zum Unternehmenskurs von €${price}/Monat anfragen und buchen.`
        }
    };

    let currentBilling = 'annual';
    let currentEntities = 1;

    document.addEventListener('DOMContentLoaded', initTierMatrix);
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        initTierMatrix();
    }

    function getLang() {
        const docLang = (document.documentElement.lang || 'ar').toLowerCase().slice(0, 2);
        return I18N[docLang] ? docLang : 'en';
    }

    function initTierMatrix() {
        const matrixSection = document.getElementById('tier-matrix');
        if (!matrixSection) return;

        const billingBtns = matrixSection.querySelectorAll('.sr-tier-toggle-btn');
        billingBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                billingBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentBilling = this.getAttribute('data-billing') || 'annual';
                updateAllPrices();
            });
        });

        const entityBtns = matrixSection.querySelectorAll('.sr-tier-entity-btn');
        entityBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                entityBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentEntities = parseInt(this.getAttribute('data-entities') || '1', 10);
                updateAllPrices();
            });
        });

        updateAllPrices();
    }

    function updateAllPrices() {
        const lang = getLang();
        const dict = I18N[lang] || I18N.en;

        const isAnnual = currentBilling === 'annual';
        const annualDiscount = isAnnual ? 0.20 : 0.0;
        let entityDiscount = 0.0;
        if (currentEntities === 2) entityDiscount = 0.10;
        else if (currentEntities >= 4) entityDiscount = 0.20;

        const totalDiscountMultiplier = (1 - annualDiscount) * (1 - entityDiscount);

        ['starter', 'pro', 'enterprise'].forEach(tierKey => {
            const base = BASE_PRICES[tierKey].monthly;
            const finalMonthly = Math.round(base * totalDiscountMultiplier);

            const amountEl = document.getElementById(`tier-price-${tierKey}`);
            const periodEl = document.getElementById(`tier-period-${tierKey}`);
            const originalEl = document.getElementById(`tier-orig-${tierKey}`);
            const noteEl = document.getElementById(`tier-note-${tierKey}`);
            const ctaBtn = document.getElementById(`tier-cta-${tierKey}`);

            if (amountEl) {
                amountEl.textContent = formatNumber(finalMonthly);
            }

            if (periodEl) {
                periodEl.textContent = dict.period;
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
                    noteEl.textContent = dict.comboDiscount(Math.round((1 - totalDiscountMultiplier) * 100), currentEntities);
                } else if (entityDiscount > 0) {
                    noteEl.textContent = dict.entityDiscount(Math.round(entityDiscount * 100), currentEntities);
                } else if (isAnnual) {
                    noteEl.textContent = dict.billedAnnual;
                } else {
                    noteEl.textContent = dict.billedMonthly;
                }
            }

            if (ctaBtn) {
                const tierName = BASE_PRICES[tierKey].names[lang] || BASE_PRICES[tierKey].names.en;
                const billingName = isAnnual ? dict.billingAnnualText : dict.billingMonthlyText;
                const entityText = currentEntities === 1 ? dict.entitySingle : dict.entityMultiple(currentEntities);
                const rawMsg = dict.waMsg(tierName, billingName, entityText, formatNumber(finalMonthly));
                ctaBtn.href = `https://wa.me/31618111116?text=${encodeURIComponent(rawMsg)}`;
            }
        });
    }

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    window.srSetTierMatrix = function (billing, entities) {
        if (billing) currentBilling = billing;
        if (entities) currentEntities = entities;
        updateAllPrices();
    };
})();
