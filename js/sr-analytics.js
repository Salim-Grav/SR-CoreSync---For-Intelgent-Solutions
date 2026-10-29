/* ==========================================================================
   S&R CoreSync — Privacy-first analytics (first-party, no cookies, no PII)
   --------------------------------------------------------------------------
   • Stores a rolling event log in localStorage (max 200 events).
   • Collects Core Web Vitals + conversion events (WhatsApp, mail, RFQ).
   • Honours Do-Not-Track and Global Privacy Control.
   • Never sends anything unless SR_ANALYTICS_CONFIG.endpoint is set.
   Public API: window.srTrack(name, props), window.srAnalytics
   ========================================================================== */
(function () {
    'use strict';

    var CONSENT_KEY = 'sr-analytics-consent';
    var EVENTS_KEY = 'sr-analytics-events';
    var VITALS_KEY = 'sr-analytics-vitals';
    var MAX_EVENTS = 200;

    var config = window.SR_ANALYTICS_CONFIG || {};
    var endpoint = typeof config.endpoint === 'string' ? config.endpoint : '';

    function safeStorage() {
        try {
            var k = '__sr_probe__';
            localStorage.setItem(k, '1');
            localStorage.removeItem(k);
            return localStorage;
        } catch (e) {
            return null;
        }
    }
    var store = safeStorage();

    function readJSON(key, fallback) {
        if (!store) { return fallback; }
        try {
            var raw = store.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function writeJSON(key, value) {
        if (!store) { return; }
        try { store.setItem(key, JSON.stringify(value)); } catch (e) {}
    }

    function consentState() {
        if (store) {
            var saved = store.getItem(CONSENT_KEY);
            if (saved === 'granted' || saved === 'denied') { return saved; }
        }
        return 'unknown';
    }

    function dntEnabled() {
        var dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
        var gpc = navigator.globalPrivacyControl;
        return dnt === '1' || dnt === 'yes' || gpc === true;
    }

    function normalizePath() {
        var p = location.pathname || '/';
        return p.replace(/\/index\.html$/, '/');
    }

    function pushEvent(name, props) {
        if (consentState() !== 'granted') { return; }
        var log = readJSON(EVENTS_KEY, []);
        log.push({
            t: Date.now(),
            n: name,
            p: props || {},
            path: normalizePath(),
            lang: document.documentElement.lang || '',
            ref: document.referrer ? document.referrer.split('/')[2] || '' : ''
        });
        if (log.length > MAX_EVENTS) { log = log.slice(log.length - MAX_EVENTS); }
        writeJSON(EVENTS_KEY, log);

        if (endpoint && navigator.sendBeacon) {
            try {
                navigator.sendBeacon(endpoint, new Blob([JSON.stringify(log[log.length - 1])], { type: 'application/json' }));
            } catch (e) {}
        }
    }

    function srTrack(name, props) {
        if (typeof name !== 'string' || !name) { return; }
        pushEvent(name, props);
    }
    window.srTrack = srTrack;

    /* ---------------- consent banner ---------------- */
    function buildBanner() {
        var el = document.createElement('div');
        el.className = 'sr-consent';
        el.setAttribute('role', 'dialog');
        el.setAttribute('aria-label', 'إعدادات الخصوصية والقياس');
        el.innerHTML =
            '<p>نقيس أداء الموقع بشكل <strong>مجهول تماماً</strong> (بدون تعريف شخصي وبدون إعلانات). ' +
            'يمكنك الرفض ويبقى الموقع يعمل كاملاً. <a href="./privacy.html#cookies">التفاصيل</a></p>' +
            '<div class="sr-consent__actions">' +
            '<button type="button" class="sr-consent__accept">أوافق على القياس</button>' +
            '<button type="button" class="sr-consent__deny">رفض</button>' +
            '</div>';
        document.body.appendChild(el);

        function choose(value) {
            if (store) { store.setItem(CONSENT_KEY, value); }
            el.remove();
            if (value === 'granted') {
                srTrack('consent_granted', {});
                trackPageView();
                collectVitals();
            }
        }

        el.querySelector('.sr-consent__accept').addEventListener('click', function () { choose('granted'); });
        el.querySelector('.sr-consent__deny').addEventListener('click', function () { choose('denied'); });
    }

    /* ---------------- page view ---------------- */
    function trackPageView() {
        srTrack('page_view', {
            title: (document.title || '').slice(0, 120),
            vw: window.innerWidth,
            vh: window.innerHeight,
            dpr: window.devicePixelRatio || 1
        });
    }

    /* ---------------- web vitals ---------------- */
    function saveVital(name, value) {
        var v = readJSON(VITALS_KEY, {});
        v[name] = Math.round(value * 1000) / 1000;
        v.updated = Date.now();
        writeJSON(VITALS_KEY, v);
        srTrack('vital_' + name.toLowerCase(), { value: v[name] });
    }

    function collectVitals() {
        if (consentState() !== 'granted') { return; }

        try {
            var nav = performance.getEntriesByType('navigation')[0];
            if (nav && nav.responseStart) { saveVital('TTFB', nav.responseStart); }
        } catch (e) {}

        try {
            new PerformanceObserver(function (list) {
                var entries = list.getEntries();
                var last = entries[entries.length - 1];
                if (last) { saveVital('LCP', last.startTime); }
            }).observe({ type: 'largest-contentful-paint', buffered: true });
        } catch (e) {}

        try {
            var cls = 0;
            new PerformanceObserver(function (list) {
                list.getEntries().forEach(function (entry) {
                    if (!entry.hadRecentInput) { cls += entry.value; }
                });
                saveVital('CLS', cls);
            }).observe({ type: 'layout-shift', buffered: true });
        } catch (e) {}

        try {
            new PerformanceObserver(function (list) {
                var entries = list.getEntries();
                var last = entries[entries.length - 1];
                if (last) { saveVital('INP', last.duration || last.processingStart || 0); }
            }).observe({ type: 'event', buffered: true, durationThreshold: 40 });
        } catch (e) {}
    }

    /* ---------------- conversion tracking ---------------- */
    function isTrackableLink(href) {
        if (!href) { return false; }
        return /^https:\/\/wa\.me\//.test(href) || /^mailto:/.test(href) || /^tel:/.test(href);
    }

    function bindOutbound() {
        document.addEventListener('click', function (e) {
            var link = e.target && e.target.closest ? e.target.closest('a[href]') : null;
            if (!link) { return; }
            var href = link.getAttribute('href') || '';
            if (!isTrackableLink(href)) { return; }
            var kind = /^https:\/\/wa\.me\//.test(href) ? 'whatsapp' : (/^mailto:/.test(href) ? 'email' : 'phone');
            srTrack('contact_click', { kind: kind, label: (link.textContent || '').trim().slice(0, 60) });
        }, true);
    }

    /* ---------------- debug panel ---------------- */
    function buildPanel() {
        var panel = document.createElement('div');
        panel.className = 'sr-analytics-panel';
        panel.innerHTML = '<h3>📊 لوحة القياس المحلية</h3><div id="srAnalyticsBody"></div>' +
            '<div><button type="button" data-act="export">تصدير JSON</button>' +
            '<button type="button" data-act="clear">مسح البيانات</button>' +
            '<button type="button" data-act="close">إغلاق</button></div>';
        document.body.appendChild(panel);

        function render() {
            var events = readJSON(EVENTS_KEY, []);
            var vitals = readJSON(VITALS_KEY, {});
            var rows = Object.keys(vitals).filter(function (k) { return k !== 'updated'; }).map(function (k) {
                return '<tr><td>' + k + '</td><td>' + vitals[k] + '</td></tr>';
            }).join('');
            var tail = events.slice(-15).reverse().map(function (ev) {
                return '<tr><td>' + new Date(ev.t).toLocaleTimeString() + '</td><td>' + ev.n + '</td></tr>';
            }).join('');
            panel.querySelector('#srAnalyticsBody').innerHTML =
                '<table><tbody>' + (rows || '<tr><td>لا توجد قياسات بعد</td><td>—</td></tr>') + '</tbody></table>' +
                '<p style="margin:0.6rem 0 0.3rem;color:#6ee7b7">آخر الأحداث (' + events.length + ')</p>' +
                '<table><tbody>' + (tail || '<tr><td>—</td><td>—</td></tr>') + '</tbody></table>';
        }

        panel.addEventListener('click', function (e) {
            var btn = e.target.closest('button[data-act]');
            if (!btn) { return; }
            var act = btn.getAttribute('data-act');
            if (act === 'close') { panel.remove(); }
            if (act === 'clear') {
                if (store) { store.removeItem(EVENTS_KEY); store.removeItem(VITALS_KEY); }
                render();
            }
            if (act === 'export') {
                var payload = { vitals: readJSON(VITALS_KEY, {}), events: readJSON(EVENTS_KEY, []) };
                var blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'sr-analytics-' + Date.now() + '.json';
                document.body.appendChild(a);
                a.click();
                a.remove();
                setTimeout(function () { URL.revokeObjectURL(url); }, 3000);
            }
        });

        render();
    }

    /* ---------------- boot ---------------- */
    function boot() {
        bindOutbound();

        if (dntEnabled()) {
            if (store) { store.setItem(CONSENT_KEY, 'denied'); }
            return;
        }

        var state = consentState();
        if (state === 'unknown') {
            setTimeout(function () {
                if (consentState() === 'unknown') { buildBanner(); }
            }, 1400);
            return;
        }

        if (state === 'granted') {
            trackPageView();
            collectVitals();
        }

        var debug = /(?:^|[?&])analytics=1(?:&|$)/.test(location.search);
        if (debug) { buildPanel(); }
    }

    window.srAnalytics = {
        track: srTrack,
        getConsent: consentState,
        getVitals: function () { return readJSON(VITALS_KEY, {}); },
        getEvents: function () { return readJSON(EVENTS_KEY, []); },
        openPanel: buildPanel
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
