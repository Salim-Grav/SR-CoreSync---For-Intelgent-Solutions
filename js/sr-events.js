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
  var SELECTOR = '[data-sr-call],[data-sr-stop],[data-sr-backdrop-call]';

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
    // data-sr-event reproduces onclick="fn(event)".
    if (el.hasAttribute('data-sr-event')) {
      args = args.concat([event || null]);
    }
    // data-sr-this reproduces onclick="fn(this, ...)" (first) and
    // onclick="fn('literal', this)" (last), exactly as the inline handler did.
    var thisPos = (el.getAttribute('data-sr-this') || '').toLowerCase();
    if (thisPos) {
      args = thisPos === 'last' ? args.concat([el]) : [el].concat(args);
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

    // onclick="if(event.target===this)close()" - a backdrop click, not a click
    // on the dialog content inside it.
    var backdrop = el.getAttribute('data-sr-backdrop-call');
    if (backdrop) {
      if (event.target !== el) return;
      var targetFn = resolve(backdrop);
      if (targetFn) targetFn.apply(el, []);
      return;
    }

    var wanted = (el.getAttribute('data-sr-on') || 'click').toLowerCase();
    if (wanted !== event.type) return;
    invoke(el, event);
  }

  for (var i = 0; i < EVENTS.length; i++) {
    document.addEventListener(EVENTS[i], handler, EVENTS[i] === 'submit' ? true : false);
  }

  // data-sr-stop must stop the event at the element, exactly like an inline
  // onclick="event.stopPropagation()" did. A document-level listener is too
  // late: the clickable ancestors would already have fired.
  function bindStops(root) {
    var nodes = (root || document).querySelectorAll('[data-sr-stop]:not([data-sr-stop-bound])');
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].setAttribute('data-sr-stop-bound', '1');
      nodes[i].addEventListener('click', function (event) {
        if (event && event.stopPropagation) event.stopPropagation();
      }, false);
    }
  }

  function watchStops() {
    bindStops(document);
    if (typeof MutationObserver === 'function') {
      new MutationObserver(function (records) {
        for (var i = 0; i < records.length; i++) {
          var added = records[i].addedNodes;
          for (var j = 0; j < added.length; j++) {
            if (added[j].nodeType === 1) bindStops(added[j]);
          }
        }
      }).observe(document.documentElement, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', watchStops, { once: true });
  } else {
    watchStops();
  }
})();
