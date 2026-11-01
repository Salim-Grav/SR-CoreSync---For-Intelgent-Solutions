/**
 * ==============================================================================
 * S&R CoreSync AI Concierge Bridge & Unified Router
 * ==============================================================================
 * Unifies the legacy Concierge with the Sovereign Master Agent (sr-agent-widget.js).
 * Redirects all triggers to the unified agent, eliminating duplicate floating UIs.
 * ==============================================================================
 */

(function () {
    'use strict';

    function initBridge() {
        if (window.srAgentWidget) {
            window.openConcierge = function (query) { window.srAgentWidget.open(query); };
            window.toggleAiChat = function () { window.srAgentWidget.toggle(); };
            window.openAiChat = function (query) { window.srAgentWidget.open(query); };
            window.openAiConcierge = function (query) { window.srAgentWidget.open(query); };
            return true;
        }
        return false;
    }

    if (!initBridge()) {
        window.addEventListener('DOMContentLoaded', function () {
            if (!initBridge() && !window.__SR_AGENT_WIDGET_INITIALIZED__) {
                if (!document.querySelector('script[src*="sr-agent-widget.js"]')) {
                    const script = document.createElement('script');
                    const isSubDir = window.location.pathname.includes('/insights/') || window.location.pathname.includes('/en/');
                    script.src = (isSubDir ? '../js/sr-agent-widget.js' : './js/sr-agent-widget.js') + '?v=20261101';
                    script.defer = true;
                    document.body.appendChild(script);
                }
            }
        });
    }
})();
