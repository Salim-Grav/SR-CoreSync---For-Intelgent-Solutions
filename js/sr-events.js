/**
 * S&R CoreSync Solutions — delegated event runtime
 * ==============================================
 * Replaces inline `onclick="fn()"` attributes, which force a Content-Security-
 * Policy that allows `'unsafe-inline'` for scripts and therefore blocks any
 * real XSS mitigation.
 *
 * Markup contract:
 *   <button data-sr-call="closeMobileMenu">                      → window.closeMobileMenu()
 *   <button data-sr-call="toggleFaq" data-sr-args='["faq-3"]'>   → window.toggleFaq('faq-3')
 *   <input  data-sr-call="updateRoi" data-sr-on="input">         → on input
 *
 * Semantics match the inline original: the element is `this`, no synthetic
 * arguments are injected, and the default action is not prevented unless the
 * element carries `data-sr-prevent`.
 */
(function () {
  'use strict';

  var EVENTS = ['click', 'input', 'change', 'submit', 'keypress', 'mousemove'];
  var SELECTOR = '[data-sr-call]';

  function resolve(name) {
    if (!name) return null;
    var fn = window[name];
    return typeof fn === 'function' ? fn : null;
  }

  function invoke(el, event) {
    var fn = resolve(el.getAttribute('data-sr-call'));
    if (!fn) {
      // Keep the failure visible in development without breaking the page.
      if (window.console && console.warn) {
        console.warn('[SREvents] missing handler:', el.getAttribute('data-sr-call'));
      }
      return;
    }
    var args = [];
    var raw = el.getAttribute('data-sr-args');
    if (raw) {
      try {
        args = JSON.parse(raw);
      } catch (err) {
        if (window.console && console.error) {
          console.error('[SREvents] bad data-sr-args on', el, err);
        }
        args = [];
      }
      if (!Array.isArray(args)) args = [args];
    }
    if (el.hasAttribute('data-sr-prevent') && event && event.preventDefault) {
      event.preventDefault();
    }
    fn.apply(el, args);
  }

  function handler(event) {
    var target = event.target;
    if (!target || !target.closest) return;
    var el = target.closest(SELECTOR);
    if (!el) return;
    var wanted = (el.getAttribute('data-sr-on') || 'click').toLowerCase();
    if (wanted !== event.type) return;
    invoke(el, event);
  }

  for (var i = 0; i < EVENTS.length; i++) {
    document.addEventListener(EVENTS[i], handler, EVENTS[i] === 'submit' ? true : false);
  }
})();
