/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Sovereign GDPR & Dutch AVG Cookie & Privacy Consent Hub (Zero-Subscription)
 * ==============================================================================
 */

(function () {
    'use strict';

    if (window.__SR_PRIVACY_BANNER_INITIALIZED__) return;
    window.__SR_PRIVACY_BANNER_INITIALIZED__ = true;

    const STORAGE_KEY = 'sr_cookie_consent';
    const GA_MEASUREMENT_ID = 'G-FBVELVRGCP';

    const I18N = {
        ar: {
            title: 'الخصوصية والامتثال الأوروبي',
            badge: 'GDPR & Dutch AVG',
            desc: 'نستخدم ملفات تعريف الارتباط الأساسية لضمان تشغيل المنظومة بأمان ومطابقة معايير الاتحاد الأوروبي، وملفات التحليلات لتحسين التجربة المؤسسية. نحترم سرية بياناتكم بالكامل.',
            acceptAll: 'قبول الكل 👑',
            essentialOnly: 'الضروري فقط',
            customize: 'تخصيص الخيارات ⚙️',
            modalTitle: 'مركز إدارة الخصوصية وملفات الارتباط',
            modalSubtitle: 'امتثال تام لمعايير اللائحة العامة لحماية البيانات الأوروبية (GDPR) وقانون الخصوصية الهولندي (AVG)',
            essentialTitle: 'ملفات تعريف الارتباط التشغيلية (إلزامية)',
            essentialDesc: 'ضرورية لأمان الجلسات المشفرة، الحماية من التهديدات، وعمل الأنظمة السحابية والربط المؤسسي. لا يمكن تعطيلها.',
            alwaysActiveBadge: 'نشطة دائماً (إلزامية)',
            analyticsTitle: 'تحليلات الأداء والسرعة (Google Analytics)',
            analyticsDesc: 'تساعد كوادرنا على قياس كفاءة المنصة وسرعة استجابة السحابة بصورة مجهولة الهوية تماماً دون جمع أي بيانات شخصية.',
            uiPrefTitle: 'تفضيلات التجربة المؤسسية والواجهة (UI State)',
            uiPrefDesc: 'حفظ خيارات لغة العرض، نمط التباين البصري، وحالة أدوات الدعم لتوفير تجربة فورية متكاملة عند زيارتك القادمة.',
            savePreferences: 'حفظ التفضيلات المحددة 🛡️',
            close: 'إغلاق'
        },
        en: {
            title: 'Privacy & European Compliance',
            badge: 'GDPR & Dutch AVG',
            desc: 'We use essential cookies to ensure secure operations compliant with EU standards, and performance analytics to refine enterprise workflows. We fully respect your data sovereignty.',
            acceptAll: 'Accept All 👑',
            essentialOnly: 'Essential Only',
            customize: 'Customize Choices ⚙️',
            modalTitle: 'Privacy & Cookie Consent Center',
            modalSubtitle: 'Strict adherence to EU GDPR and Dutch Telecommunications Act (AVG) standards',
            essentialTitle: 'Core Operational Cookies (Mandatory)',
            essentialDesc: 'Crucial for session integrity, cryptographic defense, and foundational cloud platform operations. Cannot be disabled.',
            alwaysActiveBadge: 'Always Active (Required)',
            analyticsTitle: 'Performance & Latency Telemetry (Google Analytics)',
            analyticsDesc: 'Enables aggregate measurement of platform throughput and system performance anonymously without storing identifiable data.',
            uiPrefTitle: 'Enterprise Interface Preferences (UI State)',
            uiPrefDesc: 'Persists language selection, high-contrast themes, and workspace presets across browser sessions.',
            savePreferences: 'Save Preferences 🛡️',
            close: 'Close'
        },
        nl: {
            title: 'Privacy & Europese Naleving',
            badge: 'AVG & GDPR',
            desc: 'Wij gebruiken essentiële cookies om een veilige werking te garanderen conform de Nederlandse AVG, en analytische cookies om onze zakelijke diensten te verbeteren.',
            acceptAll: 'Alles Accepteren 👑',
            essentialOnly: 'Alleen Noodzakelijk',
            customize: 'Voorkeuren Aanpassen ⚙️',
            modalTitle: 'Privacy- & Cookiebeheer',
            modalSubtitle: 'Volledige naleving van de Algemene Verordening Gegevensbescherming (AVG / GDPR)',
            essentialTitle: 'Noodzakelijke Functionele Cookies (Verplicht)',
            essentialDesc: 'Essentieel voor veilige sessies en de werking van het cloudplatform conform EU-richtlijnen. Kan niet worden uitgeschakeld.',
            alwaysActiveBadge: 'Altijd Actief (Vereist)',
            analyticsTitle: 'Prestaties & Analytics (Google Analytics)',
            analyticsDesc: 'Helpt ons de systeemprestaties en responstijden anoniem te meten zonder privégegevens op te slaan.',
            uiPrefTitle: 'Gebruikersvoorkeuren (UI State)',
            uiPrefDesc: 'Onthoudt taalvoorkeuren en interface-instellingen voor een naadloze ervaring.',
            savePreferences: 'Voorkeuren Opslaan 🛡️',
            close: 'Sluiten'
        },
        de: {
            title: 'Datenschutz & EU-Konformität',
            badge: 'DSGVO & AVG',
            desc: 'Wir verwenden essenzielle Cookies für einen sicheren Betrieb und Analysecookies zur Optimierung unserer Unternehmensdienste.',
            acceptAll: 'Alle Akzeptieren 👑',
            essentialOnly: 'Nur Notwendige',
            customize: 'Anpassen ⚙️',
            modalTitle: 'Datenschutz- & Cookie-Einstellungen',
            modalSubtitle: 'Vollständige Konformität mit DSGVO und niederländischen Datenschutzgesetzen (AVG)',
            essentialTitle: 'Essenzielle Cookies (Erforderlich)',
            essentialDesc: 'Erforderlich für die Systemsicherheit und Grundfunktionen gemäß DSGVO.',
            alwaysActiveBadge: 'Immer Aktiv (Erforderlich)',
            analyticsTitle: 'Analyse & Leistung (Google Analytics)',
            analyticsDesc: 'Ermöglicht anonyme Messung der Plattformgeschwindigkeit ohne personenbezogene Speicherung.',
            uiPrefTitle: 'Benutzer- und Spracheinstellungen',
            uiPrefDesc: 'Speichert Sprache und Darstellungseinstellungen.',
            savePreferences: 'Einstellungen Speichern 🛡️',
            close: 'Schließen'
        },
        fr: {
            title: 'Confidentialité & Conformité Européenne',
            badge: 'RGPD & AVG',
            desc: 'Nous utilisons des cookies essentiels pour garantir un fonctionnement sécurisé conforme aux normes de l\'UE, ainsi que des cookies d\'analyse.',
            acceptAll: 'Tout Accepter 👑',
            essentialOnly: 'Essentiels Uniquement',
            customize: 'Personnaliser ⚙️',
            modalTitle: 'Centre de Préférences de Confidentialité',
            modalSubtitle: 'Conformité stricte avec le RGPD européen et la loi néerlandaise (AVG)',
            essentialTitle: 'Cookies Opérationnels Essentiels (Obligatoires)',
            essentialDesc: 'Indispensables pour la sécurité des sessions et les opérations de base de la plateforme cloud.',
            alwaysActiveBadge: 'Toujours Actif (Requis)',
            analyticsTitle: 'Performance & Télémétrie (Google Analytics)',
            analyticsDesc: 'Permet de mesurer l\'efficacité de la plateforme de manière totalement anonyme.',
            uiPrefTitle: 'Préférences d\'Interface Utilisateur',
            uiPrefDesc: 'Mémorise la langue et les préférences d\'affichage.',
            savePreferences: 'Enregistrer les Préférences 🛡️',
            close: 'Fermer'
        },
        tr: {
            title: 'Gizlilik ve Avrupa Uyumluluğu',
            badge: 'GDPR & AVG',
            desc: 'Güvenli sistem işleyişi için zorunlu çerezleri ve kurumsal deneyimi geliştirmek için analitik çerezleri kullanıyoruz.',
            acceptAll: 'Tümünü Kabul Et 👑',
            essentialOnly: 'Yalnızca Gerekli',
            customize: 'Özelleştir ⚙️',
            modalTitle: 'Gizlilik ve Çerez Yönetim Merkezi',
            modalSubtitle: 'Avrupa GDPR ve Hollanda AVG mevzuatına tam uyumluluk',
            essentialTitle: 'Zorunlu İşletim Çerezleri (Gerekli)',
            essentialDesc: 'Oturum güvenliği ve temel platform işlevleri için gereklidir.',
            alwaysActiveBadge: 'Her Zaman Aktif (Zorunlu)',
            analyticsTitle: 'Performans ve Analitik (Google Analytics)',
            analyticsDesc: 'Kişisel veri toplamaksızın sistem verimliliğini anonim olarak ölçmemize yardımcı olur.',
            uiPrefTitle: 'Arayüz ve Dil Tercihleri',
            uiPrefDesc: 'Dil ve ekran tercihlerini hatırlar.',
            savePreferences: 'Tercihleri Kaydet 🛡️',
            close: 'Kapat'
        }
    };

    function detectLang() {
        const docLang = (document.documentElement.getAttribute('lang') || '').toLowerCase().split('-')[0];
        if (I18N[docLang]) return docLang;
        const p = window.location.pathname.toLowerCase();
        for (const code of Object.keys(I18N)) {
            if (p.includes('/' + code + '/')) return code;
        }
        return 'ar';
    }

    function getConsent() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    }

    function saveConsent(data) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (e) {}
        applyConsent(data);
    }

    function applyConsent(consent) {
        if (!consent) return;
        if (consent.analytics) {
            window['ga-disable-' + GA_MEASUREMENT_ID] = false;
        } else {
            window['ga-disable-' + GA_MEASUREMENT_ID] = true;
        }
    }

    function createBanner() {
        if (document.getElementById('srPrivacyBannerWrap')) return;
        const lang = detectLang();
        const t = I18N[lang] || I18N.ar;

        const wrap = document.createElement('div');
        wrap.id = 'srPrivacyBannerWrap';
        wrap.className = 'sr-privacy-banner-wrap';
        wrap.innerHTML = `
            <div class="sr-privacy-banner" role="region" aria-label="${t.title}">
                <div class="sr-privacy-content">
                    <div class="sr-privacy-icon-box" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        </svg>
                    </div>
                    <div class="sr-privacy-texts">
                        <h4 class="sr-privacy-title">
                            ${t.title}
                            <span class="badge-gdpr">${t.badge}</span>
                        </h4>
                        <p class="sr-privacy-desc">${t.desc}</p>
                    </div>
                </div>
                <div class="sr-privacy-actions">
                    <button type="button" class="sr-privacy-btn sr-privacy-btn--accept" id="srPrivacyAcceptAll">
                        ${t.acceptAll}
                    </button>
                    <button type="button" class="sr-privacy-btn sr-privacy-btn--reject" id="srPrivacyEssentialOnly">
                        ${t.essentialOnly}
                    </button>
                    <button type="button" class="sr-privacy-btn sr-privacy-btn--custom" id="srPrivacyCustomize">
                        ${t.customize}
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(wrap);

        document.getElementById('srPrivacyAcceptAll').addEventListener('click', function () {
            saveConsent({ essential: true, analytics: true, preferences: true, timestamp: Date.now() });
            hideBanner();
        });

        document.getElementById('srPrivacyEssentialOnly').addEventListener('click', function () {
            saveConsent({ essential: true, analytics: false, preferences: false, timestamp: Date.now() });
            hideBanner();
        });

        document.getElementById('srPrivacyCustomize').addEventListener('click', function () {
            openPreferencesModal();
        });

        requestAnimationFrame(() => {
            setTimeout(() => {
                wrap.classList.add('sr-visible');
            }, 300);
        });
    }

    function hideBanner() {
        const wrap = document.getElementById('srPrivacyBannerWrap');
        if (wrap) {
            wrap.classList.remove('sr-visible');
            setTimeout(() => {
                if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
            }, 400);
        }
    }

    function openPreferencesModal() {
        let modal = document.getElementById('srPrivacyModalOverlay');
        const lang = detectLang();
        const t = I18N[lang] || I18N.ar;
        const consent = getConsent() || { essential: true, analytics: true, preferences: true };

        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'srPrivacyModalOverlay';
            modal.className = 'sr-privacy-modal-overlay';
            modal.innerHTML = `
                <div class="sr-privacy-modal-card" role="dialog" aria-modal="true" aria-labelledby="srPrivacyModalTitle">
                    <div class="sr-privacy-modal-header">
                        <div class="sr-privacy-modal-title-wrap">
                            <h3 id="srPrivacyModalTitle">
                                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#c5a880" stroke-width="2.2">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                </svg>
                                <span>${t.modalTitle}</span>
                            </h3>
                            <span class="sr-privacy-modal-sub">${t.modalSubtitle}</span>
                        </div>
                        <button type="button" class="sr-privacy-modal-close" id="srPrivacyModalClose" aria-label="${t.close}">&times;</button>
                    </div>

                    <div class="sr-privacy-pref-group">
                        <!-- فئة 1: الملفات التشغيلية الضرورية -->
                        <div class="sr-privacy-pref-item">
                            <div class="sr-privacy-pref-info">
                                <div class="sr-privacy-pref-header-row">
                                    <h4>${t.essentialTitle}</h4>
                                    <span class="badge-pref-status badge-pref-status--locked">${t.alwaysActiveBadge}</span>
                                </div>
                                <p>${t.essentialDesc}</p>
                            </div>
                            <label class="sr-privacy-switch">
                                <input type="checkbox" checked disabled />
                                <span class="sr-privacy-slider"></span>
                            </label>
                        </div>

                        <!-- فئة 2: تحليلات الأداء والسرعة -->
                        <div class="sr-privacy-pref-item">
                            <div class="sr-privacy-pref-info">
                                <div class="sr-privacy-pref-header-row">
                                    <h4>${t.analyticsTitle}</h4>
                                </div>
                                <p>${t.analyticsDesc}</p>
                            </div>
                            <label class="sr-privacy-switch">
                                <input type="checkbox" id="srPrefToggleAnalytics" ${consent.analytics !== false ? 'checked' : ''} />
                                <span class="sr-privacy-slider"></span>
                            </label>
                        </div>

                        <!-- فئة 3: تفضيلات الواجهة والمستخدم -->
                        <div class="sr-privacy-pref-item">
                            <div class="sr-privacy-pref-info">
                                <div class="sr-privacy-pref-header-row">
                                    <h4>${t.uiPrefTitle}</h4>
                                </div>
                                <p>${t.uiPrefDesc}</p>
                            </div>
                            <label class="sr-privacy-switch">
                                <input type="checkbox" id="srPrefToggleUi" ${consent.preferences !== false ? 'checked' : ''} />
                                <span class="sr-privacy-slider"></span>
                            </label>
                        </div>
                    </div>

                    <div class="sr-privacy-modal-actions">
                        <button type="button" class="sr-privacy-btn sr-privacy-btn--accept" id="srPrivacyModalAcceptAll">
                            ${t.acceptAll}
                        </button>
                        <button type="button" class="sr-privacy-btn sr-privacy-btn--save" id="srPrivacySavePrefs">
                            ${t.savePreferences}
                        </button>
                        <button type="button" class="sr-privacy-btn sr-privacy-btn--reject" id="srPrivacyModalEssentialOnly">
                            ${t.essentialOnly}
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);

            document.getElementById('srPrivacyModalClose').addEventListener('click', closePreferencesModal);
            modal.addEventListener('click', function (e) {
                if (e.target === modal) closePreferencesModal();
            });

            document.getElementById('srPrivacyModalAcceptAll').addEventListener('click', function () {
                saveConsent({ essential: true, analytics: true, preferences: true, timestamp: Date.now() });
                closePreferencesModal();
                hideBanner();
            });

            document.getElementById('srPrivacyModalEssentialOnly').addEventListener('click', function () {
                saveConsent({ essential: true, analytics: false, preferences: false, timestamp: Date.now() });
                closePreferencesModal();
                hideBanner();
            });

            document.getElementById('srPrivacySavePrefs').addEventListener('click', function () {
                const isAnalyticsChecked = document.getElementById('srPrefToggleAnalytics').checked;
                const isUiChecked = document.getElementById('srPrefToggleUi').checked;
                saveConsent({ essential: true, analytics: isAnalyticsChecked, preferences: isUiChecked, timestamp: Date.now() });
                closePreferencesModal();
                hideBanner();
            });
        }

        requestAnimationFrame(() => {
            modal.classList.add('sr-visible');
        });
    }

    function closePreferencesModal() {
        const modal = document.getElementById('srPrivacyModalOverlay');
        if (modal) {
            modal.classList.remove('sr-visible');
        }
    }

    // Expose global controller
    window.openSrPrivacyModal = openPreferencesModal;

    // Attach to any trigger buttons in page or footer
    function bindTriggers() {
        document.querySelectorAll('[data-sr-privacy="open"], [href="#privacy-preferences"], [href="#cookie-settings"]').forEach(el => {
            el.addEventListener('click', function (e) {
                e.preventDefault();
                openPreferencesModal();
            });
        });
    }

    function init() {
        const consent = getConsent();
        if (consent) {
            applyConsent(consent);
        } else {
            createBanner();
        }
        bindTriggers();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
