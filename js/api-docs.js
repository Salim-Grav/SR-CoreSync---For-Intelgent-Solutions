/**
 * api-docs.js — منطق توثيق API السيادي
 * S&R CoreSync For Intelligent Solutions
 * يدعم 29 لغة عالمية + ربط المستشار الذكي بالتدقيق الضريبي
 */

'use strict';

// ═══════════════════════════════════════════
// 1. بيانات الـ 29 لغة وروابط بوابات API
// ═══════════════════════════════════════════
const LANG_PORTALS = [
    { code: 'ar', flag: '🇸🇦', name: 'العربية',          portal: './index.html',     dir: 'rtl' },
    { code: 'en', flag: '🇬🇧', name: 'English',           portal: 'en/index.html',    dir: 'ltr' },
    { code: 'nl', flag: '🇳🇱', name: 'Nederlands',        portal: 'nl/index.html',    dir: 'ltr' },
    { code: 'de', flag: '🇩🇪', name: 'Deutsch',           portal: 'de/index.html',    dir: 'ltr' },
    { code: 'fr', flag: '🇫🇷', name: 'Français',          portal: 'fr/index.html',    dir: 'ltr' },
    { code: 'es', flag: '🇪🇸', name: 'Español',           portal: 'es/index.html',    dir: 'ltr' },
    { code: 'it', flag: '🇮🇹', name: 'Italiano',          portal: 'it/index.html',    dir: 'ltr' },
    { code: 'pt', flag: '🇵🇹', name: 'Português',         portal: 'pt/index.html',    dir: 'ltr' },
    { code: 'sv', flag: '🇸🇪', name: 'Svenska',          portal: 'sv/index.html',    dir: 'ltr' },
    { code: 'no', flag: '🇳🇴', name: 'Norsk',            portal: 'no/index.html',    dir: 'ltr' },
    { code: 'da', flag: '🇩🇰', name: 'Dansk',            portal: 'da/index.html',    dir: 'ltr' },
    { code: 'fi', flag: '🇫🇮', name: 'Suomi',            portal: 'fi/index.html',    dir: 'ltr' },
    { code: 'pl', flag: '🇵🇱', name: 'Polski',           portal: 'pl/index.html',    dir: 'ltr' },
    { code: 'el', flag: '🇬🇷', name: 'Ελληνικά',          portal: 'el/index.html',    dir: 'ltr' },
    { code: 'cs', flag: '🇨🇿', name: 'Čeština',          portal: 'cs/index.html',    dir: 'ltr' },
    { code: 'ro', flag: '🇷🇴', name: 'Română',           portal: 'ro/index.html',    dir: 'ltr' },
    { code: 'hu', flag: '🇭🇺', name: 'Magyar',           portal: 'hu/index.html',    dir: 'ltr' },
    { code: 'bg', flag: '🇧🇬', name: 'Български',        portal: 'bg/index.html',    dir: 'ltr' },
    { code: 'sk', flag: '🇸🇰', name: 'Slovenčina',       portal: 'sk/index.html',    dir: 'ltr' },
    { code: 'hr', flag: '🇭🇷', name: 'Hrvatski',         portal: 'hr/index.html',    dir: 'ltr' },
    { code: 'lt', flag: '🇱🇹', name: 'Lietuvių',         portal: 'lt/index.html',    dir: 'ltr' },
    { code: 'sl', flag: '🇸🇮', name: 'Slovenščina',      portal: 'sl/index.html',    dir: 'ltr' },
    { code: 'lv', flag: '🇱🇻', name: 'Latviešu',         portal: 'lv/index.html',    dir: 'ltr' },
    { code: 'et', flag: '🇪🇪', name: 'Eesti',            portal: 'et/index.html',    dir: 'ltr' },
    { code: 'ga', flag: '🇮🇪', name: 'Gaeilge',          portal: 'ga/index.html',    dir: 'ltr' },
    { code: 'mt', flag: '🇲🇹', name: 'Malti',            portal: 'mt/index.html',    dir: 'ltr' },
    { code: 'tr', flag: '🇹🇷', name: 'Türkçe',           portal: 'tr/index.html',    dir: 'ltr' },
    { code: 'ku', flag: '☀️', name: 'Kurdî (Kurmancî)', portal: 'ku/index.html',    dir: 'ltr' },
    { code: 'ckb', flag: '☀️', name: 'کوردی (سۆرانی)',  portal: 'ckb/index.html',   dir: 'rtl' }
];

// ═══════════════════════════════════════════
// 2. ترجمات العناوين الرئيسية
// ═══════════════════════════════════════════
const TRANSLATIONS = {
    ar: { title: '📡 توثيق API السيادي الموحّد', desc: 'الوصول الكامل لجميع نقاط نهاية منظومة S&R CoreSync بـ 29 لغة عالمية.', stat: 'لغة عالمية' },
    nl: { title: '📡 Uniforme Soevereine API Documentatie', desc: 'Volledige toegang tot alle S&R CoreSync endpoints in 29 wereldtalen.', stat: 'wereldtalen' },
    en: { title: '📡 Unified Sovereign API Documentation', desc: 'Full access to all S&R CoreSync endpoints in 29 world languages.', stat: 'world languages' },
    fr: { title: '📡 Documentation API Souveraine Unifiée', desc: 'Accès complet à tous les endpoints S&R CoreSync en 29 langues mondiales.', stat: 'langues mondiales' },
    de: { title: '📡 Einheitliche Souveräne API-Dokumentation', desc: 'Vollständiger Zugriff auf alle S&R CoreSync-Endpunkte in 29 Weltsprachen.', stat: 'Weltsprachen' },
    es: { title: '📡 Documentación API Soberana Unificada', desc: 'Acceso completo a todos los endpoints de S&R CoreSync en 29 idiomas.', stat: 'idiomas mundiales' },
    pt: { title: '📡 Documentação Unificada da API Soberana', desc: 'Acesso completo a todos os endpoints do S&R CoreSync em 29 idiomas.', stat: 'idiomas mundiais' },
    zh: { title: '📡 统一主权API文档', desc: '完整访问S&R CoreSync所有端点，支持29种世界语言。', stat: '种世界语言' },
    ja: { title: '📡 統合ソブリンAPIドキュメント', desc: 'S&R CoreSyncの全エンドポイントへの完全アクセス（29言語対応）。', stat: '言語対応' },
    ru: { title: '📡 Единая Суверенная API Документация', desc: 'Полный доступ ко всем конечным точкам S&R CoreSync на 29 языках мира.', stat: 'мировых языков' },
};

// ═══════════════════════════════════════════
// 3. بناء شبكة بوابات الـ 29 لغة
// ═══════════════════════════════════════════
function buildLangGrid() {
    const grid = document.getElementById('lang-portal-grid');
    if (!grid) return;

    grid.innerHTML = LANG_PORTALS.map(lang => `
        <div class="lang-card" data-code="${lang.code}" role="button" tabindex="0" aria-label="بوابة ${lang.name}">
            <span class="flag">${lang.flag}</span>
            <span class="name">${lang.name}</span>
            <a class="portal-link" href="${lang.portal}" onclick="event.stopPropagation()">فتح البوابة ↗</a>
        </div>
    `).join('');

    // ربط الكارت بتغيير اللغة
    grid.querySelectorAll('.lang-card').forEach(card => {
        card.addEventListener('click', () => {
            const code = card.dataset.code;
            switchLanguage(code);
            card.closest('.card').scrollIntoView({ behavior: 'smooth' });
        });
        card.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') card.click();
        });
    });
}

// ═══════════════════════════════════════════
// 4. تبديل اللغة
// ═══════════════════════════════════════════
function switchLanguage(code) {
    // تحديث الـ select
    const sel = document.getElementById('lang-select');
    if (sel) sel.value = code;

    // تحديث pills
    document.querySelectorAll('.lang-pill').forEach(p => {
        p.classList.toggle('active', p.dataset.lang === code);
    });

    // تحديث grid
    document.querySelectorAll('.lang-card').forEach(c => {
        c.classList.toggle('active', c.dataset.code === code);
    });

    // ترجمة العناوين
    const t = TRANSLATIONS[code] || TRANSLATIONS['en'];
    const heroTitle = document.getElementById('hero-title');
    const heroDesc = document.getElementById('hero-desc');
    const statLang = document.getElementById('stat-lang');
    if (heroTitle) heroTitle.textContent = t.title;
    if (heroDesc) heroDesc.textContent = t.desc;
    if (statLang) statLang.textContent = t.stat;

    // تحديث dir للصفحة بناءً على اللغة
    const lang = LANG_PORTALS.find(l => l.code === code);
    if (lang) document.documentElement.setAttribute('dir', lang.dir);
}

// ═══════════════════════════════════════════
// 5. فتح/إغلاق Endpoints
// ═══════════════════════════════════════════
function initEndpointToggles() {
    const pairs = [
        ['ep-auth-toggle', 'ep-auth-body'],
        ['ep-refresh-toggle', 'ep-refresh-body'],
        ['ep-adv1-toggle', 'ep-adv1-body'],
        ['ep-adv2-toggle', 'ep-adv2-body'],
        ['ep-tax1-toggle', 'ep-tax1-body'],
        ['ep-tax2-toggle', 'ep-tax2-body'],
        ['ep-wh-toggle', 'ep-wh-body'],
    ];

    pairs.forEach(([headId, bodyId]) => {
        const head = document.getElementById(headId);
        const body = document.getElementById(bodyId);
        if (!head || !body) return;
        head.setAttribute('aria-expanded', 'false');
        head.setAttribute('role', 'button');
        head.setAttribute('tabindex', '0');

        const toggle = () => {
            const isOpen = body.classList.toggle('open');
            head.setAttribute('aria-expanded', String(isOpen));
        };
        head.addEventListener('click', toggle);
        head.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
        });
    });
}

// ═══════════════════════════════════════════
// 6. SDK Tabs
// ═══════════════════════════════════════════
function initSDKTabs() {
    const tabs = document.querySelectorAll('.tab[data-tab]');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;
            tabs.forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            const content = document.getElementById('tab-' + target);
            if (content) content.classList.add('active');
        });
    });
}

// ═══════════════════════════════════════════
// 7. ربط المستشار الذكي بالتدقيق (Option 3)
// ═══════════════════════════════════════════
function initAdvisorAuditLink() {
    // إذا وُجد session محفوظ من المستشار، نعرض رابط مباشر
    const savedSession = sessionStorage.getItem('coresync_advisor_session');
    const panel = document.getElementById('advisor-link-section');
    if (!panel) return;

    if (savedSession) {
        const sessionData = JSON.parse(savedSession);
        const extra = document.createElement('div');
        extra.style.cssText = 'margin-top:12px;padding:12px;background:rgba(57,214,160,.08);border:1px solid rgba(57,214,160,.2);border-radius:8px;font-size:.82rem;color:#39d6a0;';
        extra.innerHTML = `✅ جلسة محفوظة: <strong>${sessionData.id || 'sess_latest'}</strong> — ربط تلقائي جاهز مع التدقيق الضريبي`;
        panel.querySelector('.actions').before(extra);
    }

    // زر الربط المباشر
    const auditBtn = panel.querySelector('a[href="autonomous-tax-audit.html"]');
    if (auditBtn && savedSession) {
        auditBtn.href = 'autonomous-tax-audit.html?advisor_session=' + JSON.parse(savedSession).id;
        auditBtn.textContent = '🔗 فتح التدقيق مع ربط المستشار';
        auditBtn.style.borderColor = '#39d6a0';
        auditBtn.style.color = '#39d6a0';
    }
}

// ═══════════════════════════════════════════
// 8. Smooth scroll للـ sidebar
// ═══════════════════════════════════════════
function initSidebarNav() {
    document.querySelectorAll('.sidebar-nav a[href^="#"]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                document.querySelectorAll('.sidebar-nav a').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

// ═══════════════════════════════════════════
// 9. Lang select + pills
// ═══════════════════════════════════════════
function initLangSwitchers() {
    const sel = document.getElementById('lang-select');
    if (sel) sel.addEventListener('change', () => switchLanguage(sel.value));

    document.querySelectorAll('.lang-pill').forEach(pill => {
        pill.addEventListener('click', () => switchLanguage(pill.dataset.lang));
    });
}

// ═══════════════════════════════════════════
// 10. تهيئة كل شيء عند تحميل الصفحة
// ═══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
    buildLangGrid();
    initEndpointToggles();
    initSDKTabs();
    initAdvisorAuditLink();
    initSidebarNav();
    initLangSwitchers();

    // افتح أول endpoint تلقائياً
    const firstBody = document.getElementById('ep-auth-body');
    if (firstBody) firstBody.classList.add('open');
});

