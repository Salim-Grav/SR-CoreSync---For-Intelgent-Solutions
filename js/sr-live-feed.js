/**
 * S&R CoreSync For Intelligent Solutions — Live trust feed
 * =======================================
 * Replaces the previous `sr-live-feed.js`, which displayed invented
 * customer activity ("a client in Rotterdam downloaded the kit", "7 minutes
 * ago") in every language. Fabricated social proof is a misleading commercial
 * practice under the EU Omnibus Directive, so this module shows nothing unless
 * real, aggregated data comes back from the lead worker.
 *
 * Contract:
 *   GET {base}/events/recent -> { enabled: boolean, items: [{ label, at }] }
 *   GET {base}/stats         -> { available: boolean, consultations30d: number }
 *
 * When neither answers, or the worker is not deployed, the module stays silent.
 */
(function () {
  'use strict';

  var BASE = (function () {
    var fromGlobal = (typeof window !== 'undefined' && window.SR_FEED_BASE) ? String(window.SR_FEED_BASE) : '';
    if (fromGlobal) return fromGlobal.replace(/\/+$/, '');
    // Configuration lives in a meta tag so the page needs no inline <script>,
    // which is what a strict script-src would otherwise block.
    var meta = document.querySelector('meta[name="sr-feed-base"]');
    return meta ? String(meta.getAttribute('content') || '').replace(/\/+$/, '') : '';
  })();
  var DISMISS_KEY = 'sr_live_feed_dismissed_at';
  var BACKOFF_KEY = 'sr_live_feed_backoff_at';
  var BACKOFF_HOURS = 6;
  var MAX_CARDS = 3;
  var GAP_MS = 60000;
  var STORAGE_HOURS = 24;

  var COPY = {
    ar: {
      dismiss: 'إغلاق الإشعار',
      consultation: 'استشارة جديدة',
      viplead: 'استشارة VIP جديدة',
      contact: 'طلب تواصل جديد',
      whatsapp: 'استفسار واتساب',
      quote: 'طلب عرض سعر',
      statsOne: 'استشارة خلال آخر 30 يوماً',
      statsMany: '{n} استشارة خلال آخر 30 يوماً',
      ago: 'منذ'
    },
    en: {
      dismiss: 'Dismiss notification',
      consultation: 'New consultation',
      viplead: 'New VIP consultation',
      contact: 'New contact request',
      whatsapp: 'WhatsApp enquiry',
      quote: 'Quotation request',
      statsOne: 'consultation in the last 30 days',
      statsMany: '{n} consultations in the last 30 days',
      ago: 'ago'
    },
    nl: {
      dismiss: 'Melding sluiten',
      consultation: 'Nieuwe consultatie',
      viplead: 'Nieuwe VIP-consultatie',
      contact: 'Nieuw contactverzoek',
      whatsapp: 'WhatsApp-aanvraag',
      quote: 'Offerteaanvraag',
      statsOne: 'consultatie in de afgelopen 30 dagen',
      statsMany: '{n} consultaties in de afgelopen 30 dagen',
      ago: 'geleden'
    }
  };

  function lang() {
    var l = (document.documentElement.lang || 'ar').toLowerCase();
    if (l.indexOf('nl') === 0) return 'nl';
    if (l.indexOf('en') === 0) return 'en';
    return 'ar';
  }

  function text() {
    return COPY[lang()] || COPY.ar;
  }

  function dismissedRecently() {
    try {
      var at = parseInt(localStorage.getItem(DISMISS_KEY) || '0', 10);
      return at && (Date.now() - at) < STORAGE_HOURS * 3600000;
    } catch (e) {
      return false;
    }
  }

  function rememberDismiss() {
    try { localStorage.setItem(DISMISS_KEY, String(Date.now())); } catch (e) { /* private mode */ }
  }

  function backoffActive() {
    try {
      var at = parseInt(localStorage.getItem(BACKOFF_KEY) || '0', 10);
      return at && (Date.now() - at) < BACKOFF_HOURS * 3600000;
    } catch (e) {
      return false;
    }
  }

  function rememberFailure() {
    try { localStorage.setItem(BACKOFF_KEY, String(Date.now())); } catch (e) { /* private mode */ }
  }

  function withTimeout(promise, ms) {
    return new Promise(function (resolve, reject) {
      var timer = setTimeout(function () { reject(new Error('timeout')); }, ms);
      promise.then(function (v) { clearTimeout(timer); resolve(v); },
        function (e) { clearTimeout(timer); reject(e); });
    });
  }

  function fetchJson(path, ms) {
    return withTimeout(fetch(BASE + path, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      credentials: 'omit',
      mode: 'cors',
      cache: 'no-store'
    }).then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    }), ms || 6000);
  }

  function relative(iso) {
    var then = Date.parse(iso);
    if (!isFinite(then)) return '';
    var diffMin = Math.round((then - Date.now()) / 60000);
    // Never claim activity that has not happened yet (clock skew or seeded data).
    if (diffMin > 2) diffMin = 0;
    try {
      var rtf = new Intl.RelativeTimeFormat(lang(), { numeric: 'auto' });
      if (Math.abs(diffMin) < 60) return rtf.format(diffMin, 'minute');
      var diffH = Math.round(diffMin / 60);
      if (Math.abs(diffH) < 24) return rtf.format(diffH, 'hour');
      return rtf.format(Math.round(diffH / 24), 'day');
    } catch (e) {
      return '';
    }
  }

  function injectStyles() {
    if (document.getElementById('srlf-styles')) return;
    var css = ''
      + '.srlf-wrap{position:fixed;inset-inline-start:18px;bottom:18px;z-index:2147482000;'
      + 'display:flex;flex-direction:column;gap:10px;max-width:min(340px,calc(100vw - 36px));'
      + 'pointer-events:none}'
      + '@media (max-width:600px){.srlf-wrap{bottom:88px;inset-inline-start:12px}}'
      + '.srlf-card{pointer-events:auto;display:flex;gap:10px;align-items:flex-start;padding:12px 14px;'
      + 'border-radius:14px;border:1px solid rgba(216,178,94,.28);background:rgba(9,11,14,.94);'
      + 'color:#e9e6df;font:500 13px/1.55 "Alexandria","Plus Jakarta Sans",system-ui,sans-serif;'
      + 'box-shadow:0 18px 40px -20px rgba(0,0,0,.9);backdrop-filter:blur(14px);'
      + 'opacity:0;transform:translateY(10px);transition:opacity .35s ease,transform .35s ease}'
      + '.srlf-card.is-in{opacity:1;transform:none}'
      + '@media (prefers-reduced-motion:reduce){.srlf-card{transition:none;opacity:1;transform:none}}'
      + '.srlf-dot{width:8px;height:8px;border-radius:50%;background:#4ade80;margin-top:6px;flex:0 0 auto;'
      + 'box-shadow:0 0 0 3px rgba(74,222,128,.16)}'
      + '.srlf-body{flex:1;min-width:0}'
      + '.srlf-title{display:block;font-weight:700;color:#f0d79a}'
      + '.srlf-time{display:block;color:#9aa0aa;font-size:11.5px;margin-top:2px}'
      + '.srlf-close{pointer-events:auto;background:none;border:0;color:#7c828c;font-size:15px;'
      + 'line-height:1;cursor:pointer;padding:2px 4px;border-radius:6px}'
      + '.srlf-close:hover,.srlf-close:focus-visible{color:#f0d79a;background:rgba(216,178,94,.12)}'
      + '.srlf-stats{align-items:center}'
      + '.srlf-stats .srlf-title{color:#e9e6df;font-weight:600}';
    var style = document.createElement('style');
    style.id = 'srlf-styles';
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
  }

  function host() {
    var wrap = document.getElementById('srlf-wrap');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.id = 'srlf-wrap';
      wrap.className = 'srlf-wrap';
      document.body.appendChild(wrap);
    }
    return wrap;
  }

  function card(title, time, onClose) {
    var copy = text();
    var el = document.createElement('div');
    el.className = 'srlf-card';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    el.setAttribute('aria-atomic', 'true');

    var dot = document.createElement('span');
    dot.className = 'srlf-dot';
    dot.setAttribute('aria-hidden', 'true');

    var body = document.createElement('div');
    body.className = 'srlf-body';

    var t = document.createElement('span');
    t.className = 'srlf-title';
    t.textContent = title;
    body.appendChild(t);

    if (time) {
      var s = document.createElement('span');
      s.className = 'srlf-time';
      s.textContent = time;
      body.appendChild(s);
    }

    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'srlf-close';
    close.setAttribute('aria-label', copy.dismiss);
    close.textContent = '\u00d7';
    close.addEventListener('click', function () { onClose(el); });

    el.appendChild(dot);
    el.appendChild(body);
    el.appendChild(close);
    return el;
  }

  function remove(el) {
    el.classList.remove('is-in');
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 400);
  }

  function showEvents(items) {
    injectStyles();
    var copy = text();
    var wrap = host();
    var shown = 0;
    var index = 0;

    function step() {
      if (shown >= MAX_CARDS || index >= items.length) return;
      var item = items[index++];
      var label = copy.consultation;
      var at = relative(item && item.at);

      var el = card(label, at, function (node) {
        remove(node);
        rememberDismiss();
      });
      wrap.appendChild(el);
      requestAnimationFrame(function () { el.classList.add('is-in'); });
      shown++;

      setTimeout(function () {
        remove(el);
        setTimeout(step, GAP_MS);
      }, 9000);
    }

    setTimeout(step, 2500);
  }

  function showStats(stats) {
    var copy = text();
    var n = Number(stats && stats.consultations30d);
    if (!isFinite(n) || n < 1) return;  // show real data as soon as there is any
    injectStyles();
    var wrap = host();
    var label = copy.statsMany.replace('{n}', String(n));
    var el = card(label, '', function (node) { remove(node); rememberDismiss(); });
    el.classList.add('srlf-stats');
    wrap.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('is-in'); });
    setTimeout(function () { remove(el); }, 9000);
  }

  function start() {
    // No endpoint configured (worker not deployed yet) -> make no request at all.
    // That keeps the console and the network panel clean on every page.
    if (!BASE) return;
    if (dismissedRecently() || backoffActive() || !document.body) return;

    fetchJson('/events/recent', 6000).then(function (data) {
      if (data && data.enabled && Array.isArray(data.items) && data.items.length) {
        showEvents(data.items);
        return;
      }
      return fetchJson('/stats', 6000).then(function (stats) {
        if (stats && stats.available) showStats(stats);
      });
    }).catch(function () {
      // Host unreachable: back off for a few hours instead of retrying on every page.
      rememberFailure();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();
