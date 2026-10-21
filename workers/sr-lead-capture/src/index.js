/**
 * S&R CoreSync Solutions - Sovereign Lead Capture Worker
 * -----------------------------------------------------------------------------
 * Cloudflare Worker that replaces the former `/api/lead-capture.php` endpoint.
 *
 * Why:
 *   The production site is hosted on GitHub Pages, which is STATIC ONLY and
 *   cannot execute PHP. The previous PHP gateway was served as plain source
 *   code (HTTP 200, Content-Type: application/x-httpd-php) and every POST was
 *   rejected with HTTP 405 - so no consultation lead was ever recorded.
 *
 * Responsibilities:
 *   1. Accept and validate an executive consultation / VIP booking lead.
 *   2. Sanitize every field (no HTML, bounded length).
 *   3. Reject bot traffic (honeypot + rate limiting).
 *   4. Persist to Cloudflare KV (optional, binding name: LEADS).
 *   5. Relay to the external automation webhooks (Make / n8n / Google Sheets).
 *   6. Optionally notify the executive inbox through a Cloudflare Email binding.
 *
 * Deploy:  npx wrangler deploy
 * Secrets: npx wrangler secret put LEAD_WEBHOOK_URLS
 *          npx wrangler secret put NOTIFY_EMAIL
 */

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const DEFAULT_ALLOWED_ORIGINS = [
    'https://sr-coresync.com',
    'https://www.sr-coresync.com',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
];

const MAX_BODY_BYTES = 16 * 1024;
const RATE_LIMIT_WINDOW_SEC = 600;
const RATE_LIMIT_MAX = 8;

const FIELD_LIMITS = {
    clientName: 120,
    companyName: 160,
    phone: 40,
    email: 160,
    advisor: 40,
    advisorName: 120,
    sessionType: 40,
    sessionLabel: 160,
    package: 80,
    packageLabel: 160,
    preferredDate: 60,
    timeSlot: 40,
    timeSlotLabel: 120,
    notes: 1200,
    language: 8,
    channel: 60,
    sourceUrl: 600
};

const ALLOWED_FIELDS = Object.keys(FIELD_LIMITS).concat(['leadId', 'timestamp', 'website']);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function cleanText(value, maxLength) {
    if (value === null || value === undefined) return '';
    let out = String(value);
    out = out.replace(/<[^>]*>/g, '');
    out = out.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '');
    out = out.trim();
    if (out.length > maxLength) out = out.slice(0, maxLength);
    return out;
}

function cleanUrl(value) {
    const raw = cleanText(value, 600);
    if (!raw) return '';
    try {
        const u = new URL(raw);
        if (u.protocol !== 'http:' && u.protocol !== 'https:') return '';
        return u.href.slice(0, 600);
    } catch (e) {
        return '';
    }
}

function jsonResponse(payload, status, extraHeaders) {
    const headers = Object.assign({
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff'
    }, extraHeaders || {});
    return new Response(JSON.stringify(payload), { status: status, headers: headers });
}

function resolveAllowedOrigins(env) {
    const raw = (env && env.ALLOWED_ORIGINS) || '';
    const list = raw.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    return list.length ? list : DEFAULT_ALLOWED_ORIGINS;
}

function buildCorsHeaders(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = resolveAllowedOrigins(env);
    const headers = {
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
        'Access-Control-Max-Age': '86400',
        'Vary': 'Origin'
    };
    if (origin && allowed.indexOf(origin) !== -1) {
        headers['Access-Control-Allow-Origin'] = origin;
    }
    return headers;
}

function generateLeadId() {
    const d = new Date();
    const pad = function (n) { return String(n).padStart(2, '0'); };
    const dateStr = d.getUTCFullYear() + pad(d.getUTCMonth() + 1) + pad(d.getUTCDate());
    const rand = Math.random().toString(36).substring(2, 6).toUpperCase();
    return 'LEAD-SR-' + dateStr + '-' + rand;
}

function clientKey(request) {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const agent = request.headers.get('User-Agent') || '';
    return ip + '|' + agent.slice(0, 80);
}

async function checkRateLimit(request, env) {
    // KV backed limiter when the LEADS namespace is bound, otherwise a
    // best-effort in-memory limiter scoped to the current isolate.
    const key = 'ratelimit:' + clientKey(request);
    const now = Date.now();

    if (env && env.LEADS) {
        try {
            const raw = await env.LEADS.get(key, 'json');
            const hits = (raw && raw.hits) || [];
            const fresh = hits.filter(function (t) { return now - t < RATE_LIMIT_WINDOW_SEC * 1000; });
            if (fresh.length >= RATE_LIMIT_MAX) {
                return { allowed: false, retryAfter: Math.ceil((RATE_LIMIT_WINDOW_SEC * 1000 - (now - fresh[0])) / 1000) };
            }
            fresh.push(now);
            await env.LEADS.put(key, JSON.stringify({ hits: fresh }), { expirationTtl: RATE_LIMIT_WINDOW_SEC * 2 });
            return { allowed: true, retryAfter: 0 };
        } catch (e) {
            // Never block a real lead because the limiter failed.
            return { allowed: true, retryAfter: 0 };
        }
    }

    const memory = rateMemory();
    const hits = memory.get(key) || [];
    const fresh = hits.filter(function (t) { return now - t < RATE_LIMIT_WINDOW_SEC * 1000; });
    if (fresh.length >= RATE_LIMIT_MAX) {
        return { allowed: false, retryAfter: Math.ceil((RATE_LIMIT_WINDOW_SEC * 1000 - (now - fresh[0])) / 1000) };
    }
    fresh.push(now);
    memory.set(key, fresh);
    return { allowed: true, retryAfter: 0 };
}

const rateMemory = (function () {
    const store = new Map();
    return function () {
        if (store.size > 5000) store.clear();
        return store;
    };
})();

// ---------------------------------------------------------------------------
// Lead normalisation
// ---------------------------------------------------------------------------

function normalizeLead(payload) {
    const lead = {};
    const leadIdRaw = cleanText(payload.leadId, 64).replace(/[^a-zA-Z0-9_-]/g, '');
    lead.leadId = leadIdRaw || generateLeadId();

    const ts = cleanText(payload.timestamp, 40);
    lead.timestamp = ts || new Date().toISOString();

    Object.keys(FIELD_LIMITS).forEach(function (field) {
        if (field === 'sourceUrl') {
            lead.sourceUrl = cleanUrl(payload.sourceUrl);
        } else if (field === 'email') {
            lead.email = cleanText(payload.email, FIELD_LIMITS.email);
        } else {
            lead[field] = cleanText(payload[field], FIELD_LIMITS[field]);
        }
    });

    lead.receivedAt = new Date().toISOString();
    lead.source = 'cloudflare-worker';
    return lead;
}

function isValidLead(lead) {
    const hasName = !!(lead.clientName && lead.clientName.length >= 2);
    const hasContact = !!(lead.email || lead.phone);
    return hasName && hasContact;
}

// ---------------------------------------------------------------------------
// Relays
// ---------------------------------------------------------------------------

function parseWebhookUrls(env) {
    const raw = (env && env.LEAD_WEBHOOK_URLS) || '';
    return raw.split(',').map(function (s) { return s.trim(); }).filter(Boolean).filter(function (u) {
        try {
            const parsed = new URL(u);
            return parsed.protocol === 'https:';
        } catch (e) {
            return false;
        }
    });
}

async function relayToWebhooks(lead, env, ctx) {
    const urls = parseWebhookUrls(env);
    if (!urls.length) return { dispatched: 0, targets: [] };

    const targets = urls.map(function (url) { return url; });
    const body = JSON.stringify(lead);

    const work = Promise.all(urls.map(function (url) {
        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json; charset=utf-8' },
            body: body
        }).then(function (res) {
            return { url: url, status: res.status, ok: res.ok };
        }).catch(function (err) {
            return { url: url, status: 0, ok: false, error: String(err && err.message ? err.message : err) };
        });
    })).then(function (results) {
        return { dispatched: results.filter(function (r) { return r.ok; }).length, targets: results };
    });

    if (ctx && typeof ctx.waitUntil === 'function') {
        ctx.waitUntil(work);
        return { dispatched: urls.length, targets: targets.map(function (u) { return { url: u, queued: true }; }) };
    }
    return work;
}

function buildNotificationHtml(lead) {
    const rows = Object.keys(FIELD_LIMITS).map(function (field) {
        if (!lead[field]) return '';
        return '<tr><td style="padding:6px 12px;border:1px solid #d9c9a3;color:#6b5a3e;width:180px;">' +
            escapeHtml(field) + '</td><td style="padding:6px 12px;border:1px solid #d9c9a3;color:#0b1a14;">' +
            escapeHtml(lead[field]) + '</td></tr>';
    }).join('');

    return '<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="utf-8">' +
        '<title>New Consultation Lead</title></head>' +
        '<body style="font-family:Segoe UI,Arial,sans-serif;background:#f6f1e6;padding:24px;">' +
        '<div style="max-width:680px;margin:auto;background:#fff;border:1px solid #d9c9a3;border-radius:12px;overflow:hidden;">' +
        '<div style="background:#010907;color:#c5a880;padding:18px 24px;font-size:18px;">S&amp;R CoreSync Solutions — New Consultation Lead</div>' +
        '<div style="padding:20px 24px;"><p style="color:#0b1a14;">Lead ID: <strong>' + escapeHtml(lead.leadId) + '</strong></p>' +
        '<table style="border-collapse:collapse;width:100%;font-size:14px;">' + rows + '</table></div></div></body></html>';
}

async function notifyByEmail(lead, env, ctx) {
    if (!env || !env.NOTIFY_EMAIL) return { sent: false, reason: 'no-recipient' };

    const work = (async function () {
        if (env.SEND_EMAIL && typeof env.SEND_EMAIL.send === 'function') {
            await env.SEND_EMAIL.send({
                to: env.NOTIFY_EMAIL,
                from: env.MAIL_FROM || 'leads@sr-coresync.com',
                subject: 'New Consultation Lead ' + lead.leadId,
                html: buildNotificationHtml(lead)
            });
            return;
        }
        if (env.EMAIL_WEBHOOK_URL) {
            await fetch(env.EMAIL_WEBHOOK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    to: env.NOTIFY_EMAIL,
                    subject: 'New Consultation Lead ' + lead.leadId,
                    html: buildNotificationHtml(lead)
                })
            });
        }
    })().catch(function (err) {
        console.error('[LeadWorker] Notification failed:', err);
    });

    if (ctx && typeof ctx.waitUntil === 'function') {
        ctx.waitUntil(work);
    } else {
        await work;
    }
    return { sent: true };
}

async function persistLead(lead, env) {
    if (!env || !env.LEADS) return { stored: false, reason: 'no-kv-binding' };
    try {
        await env.LEADS.put('lead:' + lead.leadId, JSON.stringify(lead), { expirationTtl: 60 * 60 * 24 * 90 });
        const index = await env.LEADS.get('lead:index', 'json');
        const list = Array.isArray(index) ? index : [];
        list.unshift({ id: lead.leadId, at: lead.receivedAt });
        if (list.length > 500) list.length = 500;
        await env.LEADS.put('lead:index', JSON.stringify(list), { expirationTtl: 60 * 60 * 24 * 90 });
        return { stored: true };
    } catch (err) {
        console.error('[LeadWorker] KV persistence failed:', err);
        return { stored: false, reason: String(err && err.message ? err.message : err) };
    }
}

// ---------------------------------------------------------------------------
// Request handler
// ---------------------------------------------------------------------------

export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        const cors = buildCorsHeaders(request, env);
        const path = url.pathname.replace(/\/+$/, '') || '/';

        // ---- Health probe -------------------------------------------------
        if (request.method === 'GET' && (path === '/' || path === '/health' || path === '/healthz')) {
            return jsonResponse({
                status: 'ok',
                service: 'sr-lead-capture',
                version: '1.0.0',
                time: new Date().toISOString(),
                kv: !!(env && env.LEADS),
                webhooks: parseWebhookUrls(env).length
            }, 200, cors);
        }

        // ---- CORS preflight ------------------------------------------------
        if (request.method === 'OPTIONS') {
            return new Response(null, { status: 204, headers: cors });
        }

        // ---- Only POST is accepted on the capture routes -------------------
        const captureRoutes = ['/lead', '/v1/lead', '/api/lead', '/v1/leads'];
        if (captureRoutes.indexOf(path) === -1) {
            return jsonResponse({ status: 'error', message: 'Not found' }, 404, cors);
        }

        if (request.method !== 'POST') {
            return jsonResponse({ status: 'error', message: 'Method not allowed. Use POST.' }, 405, cors);
        }

        // ---- Body size guard ------------------------------------------------
        const declaredLength = Number(request.headers.get('Content-Length') || '0');
        if (declaredLength > MAX_BODY_BYTES) {
            return jsonResponse({ status: 'error', message: 'Payload too large' }, 413, cors);
        }

        let raw;
        try {
            raw = await request.text();
        } catch (err) {
            return jsonResponse({ status: 'error', message: 'Unable to read request body' }, 400, cors);
        }
        if (!raw || raw.length > MAX_BODY_BYTES) {
            return jsonResponse({ status: 'error', message: 'Invalid or oversized payload' }, 400, cors);
        }

        let payload;
        try {
            payload = JSON.parse(raw);
        } catch (err) {
            return jsonResponse({ status: 'error', message: 'Invalid JSON payload' }, 400, cors);
        }
        if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
            return jsonResponse({ status: 'error', message: 'Invalid JSON payload' }, 400, cors);
        }

        // ---- Honeypot: bots fill hidden fields. Accept silently, store nothing.
        if (payload.website) {
            return jsonResponse({ status: 'success', leadId: 'LEAD-SR-RECEIVED', recorded: false }, 200, cors);
        }

        // ---- Rate limiting ---------------------------------------------------
        const limit = await checkRateLimit(request, env);
        if (!limit.allowed) {
            return jsonResponse({
                status: 'error',
                message: 'Too many requests. Please try again later.'
            }, 429, Object.assign({}, cors, { 'Retry-After': String(limit.retryAfter || 60) }));
        }

        // ---- Normalise + validate ---------------------------------------------
        const lead = normalizeLead(payload);
        if (!isValidLead(lead)) {
            return jsonResponse({
                status: 'error',
                message: 'A name and at least one contact channel (email or phone) are required.'
            }, 422, cors);
        }

        // ---- Persist + relay ---------------------------------------------------
        const stored = await persistLead(lead, env);
        const relayed = await relayToWebhooks(lead, env, ctx);
        await notifyByEmail(lead, env, ctx);

        console.log('[LeadWorker] Lead captured', lead.leadId, 'stored=' + stored.stored, 'dispatched=' + relayed.dispatched);

        return jsonResponse({
            status: 'success',
            leadId: lead.leadId,
            recorded: stored.stored,
            stored: stored.stored,
            dispatched: relayed.dispatched,
            timestamp: lead.receivedAt
        }, 200, cors);
    }
};
