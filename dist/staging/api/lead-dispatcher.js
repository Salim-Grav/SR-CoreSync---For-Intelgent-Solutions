/**
 * S&R CoreSync Solutions - Webhook Lead Dispatcher
 * Dispatches consultation and VIP booking leads to local server, Google Sheets, Make.com, or n8n.
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
    const DEFAULT_CONFIG_URL = '/config/lead-webhook-config.json';
    const LOCAL_ENDPOINT = '/api/lead-capture.php';

    let cachedConfig = null;

    async function loadConfig() {
        if (cachedConfig) return cachedConfig;
        try {
            const res = await fetch(DEFAULT_CONFIG_URL, { cache: 'no-cache' });
            if (res.ok) {
                cachedConfig = await res.json();
                return cachedConfig;
            }
        } catch (e) {
            // Silently continue with fallback defaults
        }
        return {
            enabled: true,
            endpoints: {}
        };
    }

    function generateLeadId() {
        const d = new Date();
        const dateStr = d.getFullYear() +
            String(d.getMonth() + 1).padStart(2, '0') +
            String(d.getDate()).padStart(2, '0');
        const rand = Math.random().toString(36).substring(2, 6).toUpperCase();
        return `LEAD-SR-${dateStr}-${rand}`;
    }

    function saveToLocalVault(lead) {
        try {
            const raw = localStorage.getItem(STORAGE_KEY) || '[]';
            const vault = JSON.parse(raw);
            vault.unshift(lead);
            // Cap at 200 leads in browser storage
            if (vault.length > 200) vault.length = 200;
            localStorage.setItem(STORAGE_KEY, JSON.stringify(vault));
        } catch (e) {
            console.warn('[LeadDispatcher] LocalStorage save error:', e);
        }
    }

    async function dispatch(leadInput) {
        const lead = Object.assign({
            leadId: generateLeadId(),
            timestamp: new Date().toISOString(),
            sourceUrl: typeof window !== 'undefined' ? window.location.href : '',
            language: typeof document !== 'undefined' && document.documentElement.getAttribute('lang') || 'ar'
        }, leadInput);

        // 1. Immediately store in local client vault
        saveToLocalVault(lead);

        // 2. Load webhook config
        const config = await loadConfig();

        const dispatchPromises = [];

        // 3. Post to local Hostinger PHP endpoint (which logs to file and relays to webhooks)
        const postLocal = fetch(LOCAL_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lead)
        }).catch(err => {
            // Non-blocking in case of offline or local static dev server
            return null;
        });
        dispatchPromises.push(postLocal);

        // 4. Direct Client-side Webhook Dispatch (e.g. Google Sheets WebApp / Make / n8n)
        const customUrl = typeof localStorage !== 'undefined' ? localStorage.getItem('sr_custom_webhook_url') : '';
        const targets = [];
        if (customUrl) targets.push(customUrl);

        if (config && config.endpoints) {
            if (config.endpoints.googleSheetsWebhookUrl) targets.push(config.endpoints.googleSheetsWebhookUrl);
            if (config.endpoints.makeWebhookUrl) targets.push(config.endpoints.makeWebhookUrl);
            if (config.endpoints.n8nWebhookUrl) targets.push(config.endpoints.n8nWebhookUrl);
            if (config.endpoints.zapierWebhookUrl) targets.push(config.endpoints.zapierWebhookUrl);
        }

        targets.forEach(targetUrl => {
            if (!targetUrl) return;
            const p = fetch(targetUrl, {
                method: 'POST',
                mode: 'no-cors', // Enables direct posting to Google Apps Script without CORS redirect blocks
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(lead)
            }).catch(err => null);
            dispatchPromises.push(p);
        });

        // 5. Use Promise.race with a 400ms timeout so user UI isn't delayed
        const timeoutPromise = new Promise(resolve => setTimeout(() => resolve({ timeout: true }), 400));

        try {
            await Promise.race([Promise.all(dispatchPromises), timeoutPromise]);
        } catch (e) {
            // Ignore race errors
        }

        return {
            status: 'success',
            leadId: lead.leadId,
            lead: lead
        };
    }

    return {
        dispatch: dispatch,
        generateLeadId: generateLeadId,
        getLocalVault: function () {
            try {
                return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            } catch (e) {
                return [];
            }
        }
    };
}));
