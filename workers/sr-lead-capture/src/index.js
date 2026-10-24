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
const MAX_CONTRACT_BYTES = 96 * 1024;
const MAX_CONTRACT_TEXT = 60000;
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

async function deliverEmail(env, to, subject, html, text, attachment) {
    if (!env) return { ok: false, reason: 'no-env' };
    const sender = env.MAIL_FROM || 'leads@sr-coresync.com';
    const attachmentName = attachment && attachment.filename ? attachment.filename : '';
    const attachmentB64 = attachment && attachment.base64 ? attachment.base64 : '';

    if (env.SEND_EMAIL && typeof env.SEND_EMAIL.send === 'function') {
        const message = { to: to, from: sender, subject: subject, html: html, text: text };
        if (attachmentB64) {
            message.attachments = [{ filename: attachmentName, content: attachmentB64, type: 'application/pdf', disposition: 'attachment' }];
        }
        await env.SEND_EMAIL.send(message);
        return { ok: true, provider: 'cloudflare-email' };
    }

    if (env.RESEND_API_KEY) {
        const payload = { from: 'S&R CoreSync <' + sender + '>', to: [to], subject: subject, html: html, text: text };
        if (attachmentB64) payload.attachments = [{ filename: attachmentName, content: attachmentB64 }];
        const res = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + env.RESEND_API_KEY,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            console.error('[LeadWorker] Resend rejected:', res.status, await res.text());
            return { ok: false, reason: 'resend-' + res.status };
        }
        return { ok: true, provider: 'resend' };
    }

    if (env.BREVO_API_KEY) {
        const payload = {
            sender: { email: sender, name: 'S&R CoreSync' },
            to: [{ email: to }],
            subject: subject,
            htmlContent: html,
            textContent: text
        };
        if (attachmentB64) payload.attachment = [{ name: attachmentName, content: attachmentB64 }];
        const res = await fetch('https://api.brevo.com/v3/smtp/email', {
            method: 'POST',
            headers: { 'api-key': env.BREVO_API_KEY, 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            console.error('[LeadWorker] Brevo rejected:', res.status, await res.text());
            return { ok: false, reason: 'brevo-' + res.status };
        }
        return { ok: true, provider: 'brevo' };
    }

    if (env.EMAIL_WEBHOOK_URL) {
        const res = await fetch(env.EMAIL_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                to: to, subject: subject, html: html, text: text,
                attachments: attachmentB64 ? [{ filename: attachmentName, content_base64: attachmentB64, mime: 'application/pdf' }] : []
            })
        });
        if (!res.ok) return { ok: false, reason: 'webhook-' + res.status };
        return { ok: true, provider: 'webhook' };
    }

    return { ok: false, reason: 'no-email-provider' };
}

async function loadContractPdf(env, ref) {
    if (!env || !env.LEADS || !ref) return null;
    const id = String(ref).replace(/[^A-Za-z0-9-]/g, '').slice(0, 40);
    if (!id) return null;
    try {
        const base64 = await env.LEADS.get('contract:' + id);
        if (!base64) return null;
        return { filename: 'S&R-CoreSync-' + id + '.pdf', base64: base64 };
    } catch (err) {
        console.error('[LeadWorker] Contract PDF lookup failed:', err);
        return null;
    }
}

function contractRecipients(env) {
    const raw = (env && env.CONTRACT_RECIPIENTS) || 'mudar@nlbilarabi.nl,info@sr-coresync.com';
    return raw.split(',').map(function (s) { return s.trim().toLowerCase(); }).filter(Boolean);
}

function buildContractHtml(text) {
    const safe = escapeHtml(text).replace(/\n/g, '<br>');
    return '<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="utf-8">' +
        '<title>S&R CoreSync — Contract</title></head>' +
        '<body style="margin:0;padding:24px;background:#f6f1e6;">' +
        '<div style="max-width:720px;margin:auto;background:#fff;border:1px solid #d9c9a3;border-radius:12px;overflow:hidden;">' +
        '<div style="background:#010907;color:#c5a880;padding:18px 24px;font-size:18px;">S&amp;R CoreSync Solutions &amp; Engineering</div>' +
        '<div style="padding:24px;font-family:Segoe UI,Arial,sans-serif;font-size:14px;line-height:1.9;color:#0b1a14;">' +
        safe + '</div></div></body></html>';
}

async function sendTelegram(lead, env) {
    const token = env && env.TELEGRAM_BOT_TOKEN;
    const chatId = env && env.TELEGRAM_CHAT_ID;
    if (!token || !chatId) return { ok: false, reason: 'telegram-not-configured' };

    const lines = [
        '\u{1F514} New lead \u2014 ' + (lead.leadId || ''),
        '',
        'Name    : ' + (lead.clientName || '-') + (lead.companyName ? ' (' + lead.companyName + ')' : ''),
        'Phone   : ' + (lead.phone || '-'),
        'Email   : ' + (lead.email || '-'),
        'Package : ' + (lead.packageLabel || lead.package || '-'),
        'Advisor : ' + (lead.advisorName || lead.advisor || '-'),
        'Lang    : ' + (lead.language || '-'),
        'When    : ' + (lead.preferredDate || '-') + ' ' + (lead.timeSlotLabel || lead.timeSlot || ''),
        'Source  : ' + (lead.sourceUrl || '-')
    ];
    if (lead.notes) lines.push('Notes   : ' + String(lead.notes).slice(0, 400));

    try {
        const res = await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: chatId,
                text: lines.join('\n'),
                disable_web_page_preview: true
            })
        });
        if (!res.ok) {
            const detail = await res.text().catch(function () { return ''; });
            console.error('[LeadWorker] Telegram rejected:', res.status, detail.slice(0, 200));
            return { ok: false, reason: 'telegram-' + res.status };
        }
        return { ok: true, provider: 'telegram' };
    } catch (err) {
        console.error('[LeadWorker] Telegram failed:', err);
        return { ok: false, reason: 'telegram-error' };
    }
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
        if (env.RESEND_API_KEY) {
            const res = await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + env.RESEND_API_KEY,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    from: env.MAIL_FROM || 'S&R CoreSync <onboarding@resend.dev>',
                    to: [env.NOTIFY_EMAIL],
                    subject: 'New Lead ' + lead.leadId,
                    html: buildNotificationHtml(lead)
                })
            });
            if (!res.ok) console.error('[LeadWorker] Resend rejected:', res.status, await res.text());
            return;
        }
        if (env.BREVO_API_KEY) {
            const res = await fetch('https://api.brevo.com/v3/smtp/email', {
                method: 'POST',
                headers: {
                    'api-key': env.BREVO_API_KEY,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sender: { email: env.MAIL_FROM || 'leads@sr-coresync.com', name: 'S&R CoreSync' },
                    to: [{ email: env.NOTIFY_EMAIL }],
                    subject: 'New Lead ' + lead.leadId,
                    htmlContent: buildNotificationHtml(lead)
                })
            });
            if (!res.ok) console.error('[LeadWorker] Brevo rejected:', res.status, await res.text());
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

// ---------------------------------------------------------------------------
// Public, identity-free signals for the on-site notification stream.
// The previous UI invented "a client in Rotterdam downloaded the kit" events.
// These builders only ever expose aggregates and a generic label.
// ---------------------------------------------------------------------------

const PUBLIC_SOURCE_LABELS = {
    booking: 'Consultation',
    vip: 'VIP consultation',
    contact: 'Contact request',
    whatsapp: 'WhatsApp enquiry',
    quote: 'Quotation request'
};

async function buildPublicStats(env) {
    const empty = { available: false, consultations30d: null, updatedAt: new Date().toISOString() };
    if (!env) return empty;

    // D1 is the system of record: exact counts, including leads older than the
    // KV index window (which is capped at 500 entries).
    if (env.DB) {
        try {
            const now = Date.now();
            const iso = (days) => new Date(now - days * 86400000).toISOString();
            const row = await env.DB.prepare(
                'SELECT COUNT(*) AS total, ' +
                'SUM(CASE WHEN received_at >= ?1 THEN 1 ELSE 0 END) AS d30, ' +
                'SUM(CASE WHEN received_at >= ?2 THEN 1 ELSE 0 END) AS d7 FROM leads'
            ).bind(iso(30), iso(7)).first();
            if (row) {
                return {
                    available: true,
                    source: 'd1',
                    consultations30d: Number(row.d30 || 0),
                    consultations7d: Number(row.d7 || 0),
                    total: Number(row.total || 0),
                    updatedAt: new Date().toISOString()
                };
            }
        } catch (err) {
            console.error('[LeadWorker] D1 stats failed, falling back to KV:', err);
        }
    }

    if (!env.LEADS) return empty;
    try {
        const index = await env.LEADS.get('lead:index', 'json');
        const list = Array.isArray(index) ? index : [];
        const now = Date.now();
        const within = (days) => list.filter((entry) => {
            const t = Date.parse(entry && entry.at);
            return Number.isFinite(t) && (now - t) <= days * 86400000;
        }).length;
        return {
            available: true,
            source: 'kv',
            consultations30d: within(30),
            consultations7d: within(7),
            total: list.length,
            updatedAt: new Date().toISOString()
        };
    } catch (err) {
        console.error('[LeadWorker] stats failed:', err);
        return empty;
    }
}

async function buildRecentEvents(env, limit) {
    if (!env || !env.LEADS) return [];
    let list = [];
    try {
        list = (await env.LEADS.get('lead:index', 'json')) || [];
    } catch (err) {
        return [];
    }
    const items = [];
    for (const entry of list.slice(0, Math.max(limit * 2, limit))) {
        if (items.length >= limit) break;
        if (!entry || !entry.id || !entry.at) continue;
        let lead = null;
        try { lead = await env.LEADS.get('lead:' + entry.id, 'json'); } catch (err) { lead = null; }
        const source = String((lead && lead.source) || '').toLowerCase();
        items.push({
            label: PUBLIC_SOURCE_LABELS[source] || 'Consultation',
            at: (lead && lead.receivedAt) || entry.at
        });
    }
    return items;
}

// ---------------------------------------------------------------------------
// Money, payment signatures and bot protection
// ---------------------------------------------------------------------------

function roundMoney(value) {
    return Math.round((value + Number.EPSILON) * 100) / 100;
}

function calculateVat(amount, rate, mode) {
    var net, vat, gross;
    if (mode === 'inclusive') {
        gross = roundMoney(amount);
        net = roundMoney(gross / (1 + rate / 100));
        vat = roundMoney(gross - net);
    } else {
        net = roundMoney(amount);
        vat = roundMoney(net * rate / 100);
        gross = roundMoney(net + vat);
    }
    return {
        amount: roundMoney(amount), rate: rate, mode: mode,
        base_amount: net, vat_amount: vat, total_amount: gross,
        net: net, vat: vat, gross: gross, currency: 'EUR'
    };
}

async function readBodyLimited(request, limit) {
    var text;
    try { text = await request.text(); } catch (err) { return ''; }
    if (typeof text !== 'string') return '';
    if (text.length > limit) return null;
    return text;
}

function timingSafeEqual(a, b) {
    if (typeof a !== 'string' || typeof b !== 'string') return false;
    if (a.length !== b.length) return false;
    var diff = 0;
    for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
    return diff === 0;
}

async function hmacHex(secret, payload) {
    const key = await crypto.subtle.importKey(
        'raw', new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));
    return Array.from(new Uint8Array(sig)).map(function (b) {
        return b.toString(16).padStart(2, '0');
    }).join('');
}

async function handleStripeWebhook(raw, header, env) {
    const secret = env && env.STRIPE_WEBHOOK_SECRET;
    if (!secret) return { ok: false, status: 503, provider: 'stripe', reason: 'stripe-not-configured' };

    var timestamp = null;
    const signatures = [];
    header.split(',').forEach(function (part) {
        const pair = part.split('=');
        const name = (pair[0] || '').trim();
        const value = (pair[1] || '').trim();
        if (name === 't') timestamp = value;
        if (name === 'v1') signatures.push(value);
    });
    if (!timestamp || !signatures.length) {
        return { ok: false, status: 400, provider: 'stripe', reason: 'malformed-signature' };
    }
    const age = Math.abs(Math.floor(Date.now() / 1000) - Number(timestamp));
    if (!Number.isFinite(age) || age > 300) {
        return { ok: false, status: 400, provider: 'stripe', reason: 'timestamp-out-of-range' };
    }

    const expected = await hmacHex(secret, timestamp + '.' + raw);
    const valid = signatures.some(function (sig) { return timingSafeEqual(sig, expected); });
    if (!valid) return { ok: false, status: 401, provider: 'stripe', reason: 'signature-mismatch' };

    var event = null;
    try { event = JSON.parse(raw); } catch (err) { event = null; }
    const id = (event && (event.id || (event.data && event.data.object && event.data.object.id))) || 'unknown';
    await recordPayment(env, 'stripe', id, {
        type: event && event.type,
        amount: event && event.data && event.data.object && event.data.object.amount_total,
        currency: event && event.data && event.data.object && event.data.object.currency
    });
    return { ok: true, provider: 'stripe', id: id };
}

async function handleMollieWebhook(raw, env) {
    const apiKey = env && env.MOLLIE_API_KEY;
    if (!apiKey) return { ok: false, status: 503, provider: 'mollie', reason: 'mollie-not-configured' };

    var id = null;
    try {
        const parsed = JSON.parse(raw);
        id = parsed && parsed.id ? String(parsed.id) : null;
    } catch (err) {
        // Mollie also posts application/x-www-form-urlencoded: id=tr_xxx
        const match = /(?:^|&)id=([^&]+)/.exec(raw);
        id = match ? decodeURIComponent(match[1]) : null;
    }
    if (!id || !/^[a-zA-Z0-9_]{4,64}$/.test(id)) {
        return { ok: false, status: 400, provider: 'mollie', reason: 'missing-payment-id' };
    }

    // The posted id is untrusted: the payment state is read back from Mollie.
    const res = await fetch('https://api.mollie.com/v2/payments/' + encodeURIComponent(id), {
        headers: { Authorization: 'Bearer ' + apiKey }
    });
    if (!res.ok) {
        return { ok: false, status: 502, provider: 'mollie', reason: 'mollie-' + res.status, id: id };
    }
    const payment = await res.json().catch(function () { return null; });
    if (!payment) return { ok: false, status: 502, provider: 'mollie', reason: 'unreadable-payment', id: id };

    await recordPayment(env, 'mollie', id, {
        status: payment.status,
        amount: payment.amount && payment.amount.value,
        currency: payment.amount && payment.amount.currency,
        method: payment.method
    });
    return { ok: true, provider: 'mollie', id: id };
}

async function recordPayment(env, provider, id, detail) {
    const record = {
        provider: provider,
        id: String(id),
        detail: detail || {},
        receivedAt: new Date().toISOString()
    };
    if (env && env.LEADS) {
        try {
            await env.LEADS.put('payment:' + provider + ':' + id, JSON.stringify(record),
                { expirationTtl: 60 * 60 * 24 * 365 });
        } catch (err) {
            console.error('[LeadWorker] payment KV write failed:', err);
        }
    }
    if (env && env.DB) {
        try {
            await env.DB.prepare(
                'INSERT OR REPLACE INTO payments (provider, payment_id, status, amount, currency, payload, received_at) ' +
                'VALUES (?, ?, ?, ?, ?, ?, ?)')
                .bind(provider, String(id), String((detail && detail.status) || 'received'),
                    detail && detail.amount !== undefined ? String(detail.amount) : null,
                    (detail && detail.currency) || null,
                    JSON.stringify(detail || {}), record.receivedAt)
                .run();
        } catch (err) {
            console.error('[LeadWorker] payment D1 write failed:', err);
        }
    }
}

async function verifyTurnstile(token, request, env) {
    const secret = env && env.TURNSTILE_SECRET;
    if (!secret) return { ok: true, skipped: true };
    if (!token) return { ok: false, reason: 'missing-token' };
    try {
        const form = new FormData();
        form.append('secret', secret);
        form.append('response', String(token));
        const ip = request.headers.get('CF-Connecting-IP');
        if (ip) form.append('remoteip', ip);
        const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
            method: 'POST', body: form
        });
        const data = await res.json().catch(function () { return {}; });
        return { ok: !!data.success, reason: (data['error-codes'] || []).join(',') || null };
    } catch (err) {
        return { ok: false, reason: 'siteverify-failed' };
    }
}

async function persistLeadD1(lead, env) {
    if (!env || !env.DB) return false;
    try {
        await env.DB.prepare(
            'INSERT OR REPLACE INTO leads (lead_id, client_name, company_name, email, phone, package, notes, language, channel, source_url, received_at) ' +
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
            .bind(
                lead.leadId, lead.clientName || null, lead.companyName || null,
                lead.email || null, lead.phone || null, lead.package || null,
                lead.notes || null, lead.language || null, lead.channel || null,
                lead.sourceUrl || null, lead.receivedAt || new Date().toISOString())
            .run();
        return true;
    } catch (err) {
        console.error('[LeadWorker] D1 persistence failed:', err);
        return false;
    }
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
                webhooks: parseWebhookUrls(env).length,
                email: !!(env && (env.SEND_EMAIL || env.RESEND_API_KEY || env.BREVO_API_KEY || env.EMAIL_WEBHOOK_URL)),
                emailChannel: !env ? 'none'
                    : (env.SEND_EMAIL ? 'cloudflare-email'
                        : (env.RESEND_API_KEY ? 'resend'
                            : (env.BREVO_API_KEY ? 'brevo'
                                : (env.EMAIL_WEBHOOK_URL ? 'webhook' : 'none')))),
                mailFrom: (env && env.MAIL_FROM) || null,
                d1: !!(env && env.DB),
                turnstile: (env && env.TURNSTILE_SECRET)
                    ? (String(env.TURNSTILE_ENFORCE || '') === '1' ? 'enforcing' : 'soft') : 'off',
                eventsPublic: String((env && env.EVENTS_PUBLIC) || '') === '1',
                telegram: !!(env && env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID)
            }, 200, cors);
        }

        // ---- CORS preflight ------------------------------------------------
        if (request.method === 'OPTIONS') {
            return new Response(null, { status: 204, headers: cors });
        }

        // ---- VAT / BTW calculation --------------------------------------------
        // Replaces api.coresync.eu, which never resolved. Pure arithmetic, no PII.
        if (path === '/tax' || path === '/api/tax') {
            if (request.method !== 'POST') {
                return jsonResponse({ status: 'error', message: 'Method not allowed. Use POST.' }, 405, cors);
            }
            let body;
            try { body = await request.json(); } catch (err) {
                return jsonResponse({ status: 'error', message: 'Invalid JSON payload' }, 400, cors);
            }
            const amount = Number(body && (body.amount !== undefined ? body.amount : body.base_amount));
            let rate = body && body.rate !== undefined ? Number(body.rate) : null;
            if (rate === null || rate === undefined || Number.isNaN(rate)) {
                // Legacy shape used by the public SDK snippets: { base_amount, vat_regime }
                const regimes = { STANDARD_21: 21, REDUCED_9: 9, ZERO_0: 0, STANDARD: 21, REDUCED: 9, ZERO: 0 };
                const regime = body && body.vat_regime ? String(body.vat_regime).toUpperCase() : '';
                rate = regimes[regime] !== undefined ? regimes[regime] : 21;
            }
            const mode = (body && (body.mode === 'inclusive' || body.amount_type === 'inclusive')) ? 'inclusive' : 'exclusive';
            if (!Number.isFinite(amount) || amount < 0 || amount > 1e9) {
                return jsonResponse({ status: 'error', message: 'amount must be a number between 0 and 1e9' }, 422, cors);
            }
            if (!Number.isFinite(rate) || rate < 0 || rate > 100) {
                return jsonResponse({ status: 'error', message: 'rate must be between 0 and 100' }, 422, cors);
            }
            return jsonResponse(calculateVat(amount, rate, mode), 200,
                Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
        }

        // ---- Payment webhook ---------------------------------------------------
        // Stripe: HMAC-SHA256 over "timestamp.payload". Mollie: no signature, so the
        // payment is fetched from the API with the secret key and trusted from there.
        if (path === '/pay/webhook' || path === '/api/pay/webhook') {
            if (request.method !== 'POST') {
                return jsonResponse({ status: 'error', message: 'Method not allowed. Use POST.' }, 405, cors);
            }
            const raw = await readBodyLimited(request, MAX_BODY_BYTES);
            if (raw === null) {
                return jsonResponse({ status: 'error', message: 'Payload too large' }, 413, cors);
            }
            const stripeSignature = request.headers.get('stripe-signature');
            const outcome = stripeSignature
                ? await handleStripeWebhook(raw, stripeSignature, env)
                : await handleMollieWebhook(raw, env);
            const status = outcome.ok ? 200 : (outcome.status || 400);
            console.log('[LeadWorker] payment webhook', outcome.provider || 'unknown',
                outcome.id || '-', 'ok=' + outcome.ok, outcome.reason || '');
            return jsonResponse({
                received: outcome.ok,
                provider: outcome.provider || null,
                reason: outcome.reason || null
            }, status, cors);
        }

        // ---- Public trust statistics ----------------------------------------
        // Aggregates only: counts derived from the KV index timestamps. No name,
        // e-mail, phone or city ever leaves this worker through these routes.
        if (request.method === 'GET' && (path === '/stats' || path === '/api/stats')) {
            const stats = await buildPublicStats(env);
            return jsonResponse(stats, 200, Object.assign({}, cors, {
                'Cache-Control': 'public, max-age=900, stale-while-revalidate=3600'
            }));
        }

        // ---- Sanitised recent activity (opt-in, identity-free) ----------------
        if (request.method === 'GET' && (path === '/events/recent' || path === '/api/events/recent')) {
            if (String(env.EVENTS_PUBLIC || '') !== '1') {
                return jsonResponse({ enabled: false, items: [] }, 200, Object.assign({}, cors, {
                    'Cache-Control': 'public, max-age=300'
                }));
            }
            const items = await buildRecentEvents(env, 3);
            return jsonResponse({ enabled: true, items }, 200, Object.assign({}, cors, {
                'Cache-Control': 'public, max-age=300, stale-while-revalidate=900'
            }));
        }

        // ---- Contract delivery: full template text in the email body -------
        if (path === '/contract') {
            if (request.method !== 'POST') {
                return jsonResponse({ status: 'error', message: 'Method not allowed. Use POST.' }, 405, cors);
            }
            const origin = request.headers.get('Origin') || '';
            if (resolveAllowedOrigins(env).indexOf(origin) === -1) {
                return jsonResponse({ status: 'error', message: 'Origin not allowed' }, 403, cors);
            }
            if (Number(request.headers.get('Content-Length') || '0') > MAX_CONTRACT_BYTES) {
                return jsonResponse({ status: 'error', message: 'Payload too large' }, 413, cors);
            }
            let contractRaw;
            try { contractRaw = await request.text(); } catch (e) { contractRaw = ''; }
            if (!contractRaw || contractRaw.length > MAX_CONTRACT_BYTES) {
                return jsonResponse({ status: 'error', message: 'Invalid or oversized payload' }, 400, cors);
            }
            let body;
            try { body = JSON.parse(contractRaw); } catch (e) { return jsonResponse({ status: 'error', message: 'Invalid JSON payload' }, 400, cors); }
            if (!body || typeof body !== 'object' || Array.isArray(body)) {
                return jsonResponse({ status: 'error', message: 'Invalid JSON payload' }, 400, cors);
            }

            const to = cleanText(body.to, 160).toLowerCase();
            if (!to || contractRecipients(env).indexOf(to) === -1) {
                return jsonResponse({ status: 'error', message: 'Recipient not allowed' }, 403, cors);
            }

            const subject = cleanText(body.subject, 160) || 'S&R CoreSync — Official Contract';
            const text = String(body.text || '')
                .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '')
                .trim()
                .slice(0, MAX_CONTRACT_TEXT);
            if (text.length < 40) {
                return jsonResponse({ status: 'error', message: 'Contract text is too short' }, 422, cors);
            }

            const limit = await checkRateLimit(request, env);
            if (!limit.allowed) {
                return jsonResponse({ status: 'error', message: 'Too many requests. Please try again later.' },
                    429, Object.assign({}, cors, { 'Retry-After': String(limit.retryAfter || 60) }));
            }

            const attachPdf = body.attach !== false;
            const pdf = attachPdf ? await loadContractPdf(env, body.contractRef || to) : null;
            const delivered = await deliverEmail(env, to, subject, buildContractHtml(text), text, pdf);
            console.log('[LeadWorker] Contract delivery', to, 'ok=' + delivered.ok, delivered.provider || delivered.reason, 'pdf=' + !!pdf);
            if (!delivered.ok) {
                return jsonResponse({ status: 'error', message: 'Email provider unavailable', reason: delivered.reason }, 502, cors);
            }
            return jsonResponse({
                status: 'success',
                provider: delivered.provider,
                to: to,
                chars: text.length,
                attached: pdf ? pdf.filename : null
            }, 200, cors);
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

        // ---- Bot protection (Cloudflare Turnstile, optional) ------------------
        // Soft-fail by default so the form keeps working before the site sends a
        // token; set TURNSTILE_ENFORCE=1 once the widget is live.
        const turnstile = await verifyTurnstile(
            payload.turnstileToken || payload['cf-turnstile-response'], request, env);
        if (!turnstile.ok) {
            if (String(env.TURNSTILE_ENFORCE || '') === '1') {
                return jsonResponse({
                    status: 'error',
                    message: 'Bot verification failed. Please reload and try again.',
                    reason: turnstile.reason
                }, 403, cors);
            }
            console.warn('[LeadWorker] turnstile soft-fail:', turnstile.reason);
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
        const persistedD1 = await persistLeadD1(lead, env);
        const stored = await persistLead(lead, env);
        const relayed = await relayToWebhooks(lead, env, ctx);
        const telegram = await sendTelegram(lead, env);
        await notifyByEmail(lead, env, ctx);

        console.log('[LeadWorker] Lead captured', lead.leadId, 'stored=' + stored.stored,
            'd1=' + persistedD1, 'dispatched=' + relayed.dispatched,
            'telegram=' + (telegram && telegram.ok ? 'sent' : (telegram && telegram.reason) || 'no'));

        return jsonResponse({
            status: 'success',
            leadId: lead.leadId,
            recorded: stored.stored || persistedD1,
            stored: stored.stored,
            durable: persistedD1,
            dispatched: relayed.dispatched,
            timestamp: lead.receivedAt
        }, 200, cors);
    }
};
