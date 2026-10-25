/**
 * S&R CoreSync For Intelligent Solutions — Sovereign Geo-Language Detection Engine
 * Intelligent, non-intrusive browser language detection with polite visual notification.
 *
 * Strategy:
 *   1. Detect browser/OS preferred language via navigator.languages
 *   2. Compare against current page language
 *   3. If mismatch → show a sovereign-styled top banner offering the switch
 *   4. Respect localStorage preference: once dismissed or switched, don't show again
 *   5. Works alongside the existing inline `srLangAutoDetect` script
 *      (that script should be updated to NOT auto-redirect when this engine is active)
 *
 * Integration: Self-contained modular script. Load via <script src="./js/sr-geo-lang.js" defer>
 */

(function () {
    'use strict';

    // Prevent double initialization
    if (window.__SR_GEO_LANG_INITIALIZED__) return;
    window.__SR_GEO_LANG_INITIALIZED__ = true;

    // ─── Constants ───
    const STORAGE_KEY = 'sr_geolang_dismissed';
    const PREF_KEY = 'sr_lang_pref';
    const BANNER_DELAY_MS = 800;   // Delay before showing banner (let page settle)
    const BANNER_AUTO_HIDE_MS = 20000; // Auto-hide after 20s

    // Map of supported localized landing pages (those that actually exist as /xx/index.html)
    const LANG_PAGES = {
        ar: { dir: null, flag: '🇸🇦', name: 'العربية', nameEn: 'Arabic' },
        en: { dir: 'en', flag: '🇬🇧', name: 'English', nameEn: 'English' },
        nl: { dir: 'nl', flag: '🇳🇱', name: 'Nederlands', nameEn: 'Dutch' },
        de: { dir: 'de', flag: '🇩🇪', name: 'Deutsch', nameEn: 'German' },
        fr: { dir: 'fr', flag: '🇫🇷', name: 'Français', nameEn: 'French' },
        tr: { dir: 'tr', flag: '🇹🇷', name: 'Türkçe', nameEn: 'Turkish' },
        es: { dir: 'es', flag: '🇪🇸', name: 'Español', nameEn: 'Spanish' },
        it: { dir: 'it', flag: '🇮🇹', name: 'Italiano', nameEn: 'Italian' },
        sv: { dir: 'sv', flag: '🇸🇪', name: 'Svenska', nameEn: 'Swedish' },
        no: { dir: 'no', flag: '🇳🇴', name: 'Norsk', nameEn: 'Norwegian' },
        da: { dir: 'da', flag: '🇩🇰', name: 'Dansk', nameEn: 'Danish' },
        fi: { dir: 'fi', flag: '🇫🇮', name: 'Suomi', nameEn: 'Finnish' },
        pl: { dir: 'pl', flag: '🇵🇱', name: 'Polski', nameEn: 'Polish' },
        pt: { dir: 'pt', flag: '🇵🇹', name: 'Português', nameEn: 'Portuguese' },
        el: { dir: 'el', flag: '🇬🇷', name: 'Ελληνικά', nameEn: 'Greek' },
        cs: { dir: 'cs', flag: '🇨🇿', name: 'Čeština', nameEn: 'Czech' },
        ro: { dir: 'ro', flag: '🇷🇴', name: 'Română', nameEn: 'Romanian' },
        hu: { dir: 'hu', flag: '🇭🇺', name: 'Magyar', nameEn: 'Hungarian' },
        bg: { dir: 'bg', flag: '🇧🇬', name: 'Български', nameEn: 'Bulgarian' },
        sk: { dir: 'sk', flag: '🇸🇰', name: 'Slovenčina', nameEn: 'Slovak' },
        hr: { dir: 'hr', flag: '🇭🇷', name: 'Hrvatski', nameEn: 'Croatian' },
        lt: { dir: 'lt', flag: '🇱🇹', name: 'Lietuvių', nameEn: 'Lithuanian' },
        sl: { dir: 'sl', flag: '🇸🇮', name: 'Slovenščina', nameEn: 'Slovenian' },
        lv: { dir: 'lv', flag: '🇱🇻', name: 'Latviešu', nameEn: 'Latvian' },
        et: { dir: 'et', flag: '🇪🇪', name: 'Eesti', nameEn: 'Estonian' },
        ga: { dir: 'ga', flag: '🇮🇪', name: 'Gaeilge', nameEn: 'Irish' },
        mt: { dir: 'mt', flag: '🇲🇹', name: 'Malti', nameEn: 'Maltese' },
        ku: { dir: 'ku', flag: '🏳️', name: 'Kurdî', nameEn: 'Kurdish' },
        ckb: { dir: 'ckb', flag: '🏳️', name: 'سۆرانی', nameEn: 'Sorani' }
    };

    // Localized banner messages per current page language
    const BANNER_MESSAGES = {
        ar: {
            detected: (langName, flag) => `${flag} نلاحظ أن جهازك يفضل <strong>${langName}</strong>. هل ترغب بالانتقال إلى النسخة المحلية؟`,
            switchBtn: (langName) => `الانتقال إلى ${langName}`,
            stayBtn: 'البقاء هنا',
            ariaLabel: 'إشعار اكتشاف اللغة'
        },
        en: {
            detected: (langName, flag) => `${flag} We detected your device prefers <strong>${langName}</strong>. Would you like to switch?`,
            switchBtn: (langName) => `Switch to ${langName}`,
            stayBtn: 'Stay Here',
            ariaLabel: 'Language detection notification'
        },
        nl: {
            detected: (langName, flag) => `${flag} We hebben gedetecteerd dat uw apparaat <strong>${langName}</strong> prefereert. Wilt u overschakelen?`,
            switchBtn: (langName) => `Overschakelen naar ${langName}`,
            stayBtn: 'Hier Blijven',
            ariaLabel: 'Taaldetectie melding'
        },
        de: {
            detected: (langName, flag) => `${flag} Wir haben festgestellt, dass Ihr Gerät <strong>${langName}</strong> bevorzugt. Möchten Sie wechseln?`,
            switchBtn: (langName) => `Zu ${langName} wechseln`,
            stayBtn: 'Hier Bleiben',
            ariaLabel: 'Spracherkennung Benachrichtigung'
        },
        fr: {
            detected: (langName, flag) => `${flag} Nous avons détecté que votre appareil préfère le <strong>${langName}</strong>. Souhaitez-vous changer ?`,
            switchBtn: (langName) => `Passer au ${langName}`,
            stayBtn: 'Rester Ici',
            ariaLabel: 'Notification de détection de langue'
        },
        tr: {
            detected: (langName, flag) => `${flag} Cihazınızın <strong>${langName}</strong> tercih ettiğini algıladık. Geçiş yapmak ister misiniz?`,
            switchBtn: (langName) => `${langName} diline geç`,
            stayBtn: 'Burada Kal',
            ariaLabel: 'Dil algılama bildirimi'
        }
    };

    // ─── Initialization ───
    document.addEventListener('DOMContentLoaded', initGeoLang);
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        initGeoLang();
    }

    function initGeoLang() {
        // Prevent double-run
        if (document.getElementById('srGeoLangBanner')) return;

        // Check if ?noredirect=1 is set
        try {
            const params = new URLSearchParams(window.location.search);
            if (params.get('noredirect') === '1') return;
        } catch (e) {}

        // Check if user already explicitly dismissed or chose
        try {
            const dismissed = localStorage.getItem(STORAGE_KEY);
            if (dismissed) {
                // Check if dismissal is less than 7 days old
                const dismissedTime = parseInt(dismissed, 10);
                if (!isNaN(dismissedTime) && (Date.now() - dismissedTime) < 7 * 24 * 60 * 60 * 1000) {
                    return; // Still within the 7-day dismiss window
                }
            }

            // If user has explicitly saved a preference and is on correct page, skip
            const savedPref = localStorage.getItem(PREF_KEY);
            const currentLang = getCurrentPageLang();
            if (savedPref && savedPref === currentLang) return;
        } catch (e) {}

        // Detect browser language
        const detectedLang = detectBrowserLanguage();
        const currentLang = getCurrentPageLang();

        // If detected matches current, or no detection, skip
        if (!detectedLang || detectedLang === currentLang) return;

        // If detected language has a page, show the banner
        if (LANG_PAGES[detectedLang]) {
            setTimeout(() => showBanner(detectedLang, currentLang), BANNER_DELAY_MS);
        }
    }

    // ─── Language Detection ───
    function detectBrowserLanguage() {
        try {
            const browserLangs = navigator.languages || [navigator.language || navigator.userLanguage || ''];
            for (let i = 0; i < browserLangs.length; i++) {
                const raw = (browserLangs[i] || '').toLowerCase().trim();
                const primary = raw.split('-')[0];

                // Kurdish Sorani special case
                if (raw.indexOf('ckb') !== -1 || raw.indexOf('ku-iq') !== -1) {
                    return 'ckb';
                }

                if (LANG_PAGES[primary]) {
                    return primary;
                }
            }
        } catch (e) {}
        return null;
    }

    function getCurrentPageLang() {
        return (document.documentElement.getAttribute('lang') || 'ar').toLowerCase().split('-')[0];
    }

    // ─── Path Computation ───
    function buildTargetUrl(targetLang) {
        const path = window.location.pathname.toLowerCase();
        const isSubfolder = /\/(ar|en|nl|de|fr|tr|sv|no|es|it|ku|ckb|pl|pt|da|fi|cs|el|ro|hu|bg|sk|hr|lt|sl|lv|et|ga|mt)\//.test(path);
        const prefix = isSubfolder ? '../' : './';

        // Determine if we're on demo.html or index.html
        const isDemo = path.indexOf('demo.html') !== -1;
        const targetFile = isDemo ? 'demo.html' : 'index.html';

        let targetPath;
        if (targetLang === 'ar') {
            targetPath = targetFile;
        } else {
            targetPath = targetLang + '/' + targetFile;
        }

        return prefix + targetPath + window.location.hash;
    }

    // ─── Ensure CSS is loaded ───
    function ensureCSS() {
        const cssId = 'sr-geo-lang-css';
        if (document.getElementById(cssId)) return;

        const path = window.location.pathname.toLowerCase();
        const isSubfolder = /\/(ar|en|nl|de|fr|tr|sv|no|es|it|ku|ckb|pl|pt|da|fi|cs|el|ro|hu|bg|sk|hr|lt|sl|lv|et|ga|mt)\//.test(path);
        const prefix = isSubfolder ? '../' : './';

        const link = document.createElement('link');
        link.id = cssId;
        link.rel = 'stylesheet';
        link.href = prefix + 'css/sr-geo-lang.css';
        document.head.appendChild(link);
    }

    // ─── Show Banner ───
    function showBanner(detectedLang, currentLang) {
        ensureCSS();

        const targetInfo = LANG_PAGES[detectedLang];
        if (!targetInfo) return;

        // Get messages in the current page language (fallback to English)
        const msgs = BANNER_MESSAGES[currentLang] || BANNER_MESSAGES.en;
        const targetUrl = buildTargetUrl(detectedLang);
        const isRtl = currentLang === 'ar' || currentLang === 'ckb' || currentLang === 'ku';

        // Build the banner
        const banner = document.createElement('div');
        banner.className = 'sr-geolang-banner';
        banner.id = 'srGeoLangBanner';
        banner.setAttribute('role', 'alert');
        banner.setAttribute('aria-label', msgs.ariaLabel);
        if (isRtl) banner.setAttribute('dir', 'rtl');

        banner.innerHTML = `
            <div class="sr-geolang-inner">
                <span class="sr-geolang-pulse" aria-hidden="true"></span>
                <span class="sr-geolang-text">
                    ${msgs.detected(targetInfo.name, targetInfo.flag)}
                </span>
                <div class="sr-geolang-actions">
                    <a href="${targetUrl}" class="sr-geolang-btn sr-geolang-btn--primary" id="srGeoLangSwitch" aria-label="${msgs.switchBtn(targetInfo.name)}">
                        ${targetInfo.flag} ${msgs.switchBtn(targetInfo.name)}
                    </a>
                    <button type="button" class="sr-geolang-btn sr-geolang-btn--secondary" id="srGeoLangStay" aria-label="${msgs.stayBtn}">
                        ${msgs.stayBtn}
                    </button>
                </div>
                <button type="button" class="sr-geolang-close" id="srGeoLangClose" aria-label="Close">
                    <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
        `;

        document.body.appendChild(banner);

        // Trigger entrance animation
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                banner.classList.add('visible');
            });
        });

        // ── Event: Switch language ──
        const switchBtn = document.getElementById('srGeoLangSwitch');
        if (switchBtn) {
            switchBtn.addEventListener('click', (e) => {
                e.preventDefault();
                try {
                    localStorage.setItem(PREF_KEY, detectedLang);
                    localStorage.setItem(STORAGE_KEY, String(Date.now()));
                } catch (ex) {}
                window.location.href = targetUrl;
            });
        }

        // ── Event: Stay on current page ──
        const stayBtn = document.getElementById('srGeoLangStay');
        if (stayBtn) {
            stayBtn.addEventListener('click', () => {
                dismissBanner(banner, currentLang);
            });
        }

        // ── Event: Close X ──
        const closeBtn = document.getElementById('srGeoLangClose');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissBanner(banner, currentLang);
            });
        }

        // ── Auto-hide after 20s ──
        setTimeout(() => {
            if (banner.classList.contains('visible')) {
                dismissBanner(banner, currentLang);
            }
        }, BANNER_AUTO_HIDE_MS);
    }

    // ─── Dismiss Banner ───
    function dismissBanner(banner, currentLang) {
        if (!banner) return;

        try {
            localStorage.setItem(STORAGE_KEY, String(Date.now()));
            // Save explicit preference for current page language
            localStorage.setItem(PREF_KEY, currentLang);
        } catch (e) {}

        banner.classList.add('hiding');
        banner.classList.remove('visible');

        // Remove from DOM after animation
        setTimeout(() => {
            if (banner.parentNode) {
                banner.parentNode.removeChild(banner);
            }
        }, 600);
    }
})();
