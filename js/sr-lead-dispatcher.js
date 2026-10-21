/**
 * S&R CoreSync Solutions - Sovereign Lead Dispatcher (Client Runtime)
 * -----------------------------------------------------------------------------
 * Dispatches consultation / VIP booking leads to the Cloudflare Worker API.
 *
 * Deployment note:
 *   The former endpoint `/api/lead-capture.php` is a PHP file and CANNOT be
 *   executed on GitHub Pages (static hosting). It is now served by the
 *   Cloudflare Worker "sr-lead-capture".
 *
 * Endpoint resolution order (first one that answers wins):
 *   1. window.SR_LEAD_ENDPOINT        - explicit override (any deployment)
 *   2. https://api.sr-coresync.com/lead - Worker custom domain
 *   3. /api/lead                        - Worker route on the current origin
 *
 * Guarantees:
 *   - Every lead is ALWAYS persisted to the local vault (localStorage) first.
 *   - Failures are NEVER swallowed: the resolved promise carries `ok:false`
 *     and the reason, and a console warning is emitted.
 *   - The UI can await `SRLeadDispatcher.dispatch()` to know the real outcome.
 */
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.SRLeadDispatcher = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    const STORAGE_KEY = 'sr_leads_vault';
    const VAULT_LIMIT = 200;
    const REQUEST_TIMEOUT_MS = 8000;

    const DEFAULT_ENDPOINTS = [
        'https://api.sr-coresync.com/lead',
        '/api/lead'
    ];

    function getEndpoints() {
        const list = [];
        const override = (typeof window !== 'undefined' && window.SR_LEAD_ENDPOINT) || '';
        if (override) list.push(override);
        DEFAULT_ENDPOINTS.forEach(function (e) { if (list.indexOf(e) === -1) list.push(e); });
        return list;
    }

    function generateLeadId() {
        const d = new Date();
        const dateStr = d.getFullYear() +
            String(d.getMonth() + 1).padStart(2, '0') +
            String(d.getDate()).padStart(2, '0');
        const rand = Math.random().toString(36).substring(2, 6).toUpperCase();
        return 'LEAD-SR-' + dateStr + '-' + rand;
    }

    function saveToLocalVault(lead) {
        try {
            const raw = localStorage.getItem(STORAGE_KEY) || '[]';
            const vault = JSON.parse(raw);
            vault.unshift(lead);
            if (vault.length > VAULT_LIMIT) vault.length = VAULT_LIMIT;
            localStorage.setItem(STORAGE_KEY, JSON.stringify(vault));
            return true;
        } catch (e) {
            console.warn('[LeadDispatcher] LocalStorage save error:', e);
            return false;
        }
    }

    function postToEndpoint(endpoint, lead) {
        const controller = new AbortController();
        const timer = setTimeout(function () { controller.abort(); }, REQUEST_TIMEOUT_MS);

        return fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lead),
            signal: controller.signal
        }).then(function (res) {
            clearTimeout(timer);
            if (!res.ok) {
                return res.text().then(function (t) {
                    throw new Error('HTTP ' + res.status + ' from ' + endpoint + ' :: ' + t.slice(0, 180));
                });
            }
            return res.json().catch(function () { return { status: 'success' }; });
        }).catch(function (err) {
            clearTimeout(timer);
            throw err;
        });
    }

    async function dispatch(leadInput) {
        const lead = Object.assign({
            leadId: generateLeadId(),
            timestamp: new Date().toISOString(),
            sourceUrl: typeof window !== 'undefined' ? window.location.href : '',
            language: (typeof document !== 'undefined' && document.documentElement.getAttribute('lang')) || 'ar'
        }, leadInput || {});

        // 1. Always persist locally first - never lose a lead.
        const vaulted = saveToLocalVault(lead);

        // 2. Try each endpoint in order until one accepts the lead.
        const endpoints = getEndpoints();
        const errors = [];

        for (let i = 0; i < endpoints.length; i++) {
            const endpoint = endpoints[i];
            try {
                const data = await postToEndpoint(endpoint, lead);
                console.info('[LeadDispatcher] Lead accepted by ' + endpoint, data);
                return {
                    status: 'success',
                    ok: true,
                    endpoint: endpoint,
                    leadId: lead.leadId,
                    vaulted: vaulted,
                    lead: lead,
                    response: data
                };
            } catch (err) {
                errors.push(endpoint + ' :: ' + (err && err.message ? err.message : String(err)));
                console.warn('[LeadDispatcher] Endpoint failed: ' + endpoint, err);
            }
        }

        // 3. No endpoint answered. Surface it loudly instead of failing silently.
        const failure = new Error('[LeadDispatcher] All lead endpoints failed: ' + errors.join(' | '));
        console.error(failure.message);
        return {
            status: 'error',
            ok: false,
            leadId: lead.leadId,
            vaulted: vaulted,
            lead: lead,
            errors: errors
        };
    }

    return {
        dispatch: dispatch,
        generateLeadId: generateLeadId,
        getEndpoints: getEndpoints,
        getLocalVault: function () {
            try {
                return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            } catch (e) {
                return [];
            }
        }
    };
}));
