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
 *          npx wrangler secret put PURELYMAIL_PASS   (send through our own mailbox)
 */

import { connect } from 'cloudflare:sockets';

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

// ---------------------------------------------------------------------------
// Outbound mail through our own Purelymail mailbox
// ---------------------------------------------------------------------------
// Workers cannot open port 25, but submission on 587 with STARTTLS is allowed,
// so the worker speaks SMTP to Purelymail directly. That keeps alerts on the
// mailbox the domain already pays for ($10/year, unlimited addresses) instead
// of adding another email vendor, and every message leaves DKIM-signed with the
// keys the DNS already publishes.

const SMTP_HOST = 'smtp.purelymail.com';
const SMTP_PORT = 587;

function smtpConfigured(env) {
    return !!(env && env.PURELYMAIL_USER && env.PURELYMAIL_PASS);
}

// btoa() only takes Latin-1; go through UTF-8 bytes so Arabic survives.
function b64(text) {
    const bytes = new TextEncoder().encode(text);
    let binary = '';
    for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
}

function buildMime(opts) {
    const boundary = 'sr-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    const from = opts.fromName ? opts.fromName + ' <' + opts.from + '>' : opts.from;
    const headers = [
        'From: ' + from,
        'To: ' + opts.to,
        'Subject: =?UTF-8?B?' + b64(opts.subject) + '?=',
        'Date: ' + new Date().toUTCString().replace('GMT', '+0000'),
        'Message-ID: <' + Date.now().toString(36) + '.' + Math.random().toString(36).slice(2, 10) + '@' + opts.from.split('@')[1] + '>',
        'MIME-Version: 1.0',
        'Auto-Submitted: auto-generated'
    ];
    if (opts.replyTo) headers.push('Reply-To: ' + opts.replyTo);
    const wrap = function (value) { return value.replace(/(.{76})/g, '$1\r\n'); };

    // Text and HTML travel as alternative views; a single one needs no wrapper.
    let entityType;
    let entityBody;
    if (opts.text && opts.html) {
        entityType = 'multipart/alternative; boundary="alt-' + boundary + '"';
        entityBody = [
            '--alt-' + boundary,
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: base64',
            '',
            wrap(b64(opts.text)),
            '--alt-' + boundary,
            'Content-Type: text/html; charset=UTF-8',
            'Content-Transfer-Encoding: base64',
            '',
            wrap(b64(opts.html)),
            '--alt-' + boundary + '--'
        ].join('\r\n');
    } else if (opts.html) {
        entityType = 'text/html; charset=UTF-8';
        entityBody = wrap(b64(opts.html));
    } else {
        entityType = 'text/plain; charset=UTF-8';
        entityBody = wrap(b64(opts.text || ''));
    }

    const attachmentName = (opts.attachmentName || '').replace(/"/g, '');
    const attachmentData = opts.attachmentB64;
    if (!attachmentName || !attachmentData) {
        return headers.concat('Content-Type: ' + entityType).join('\r\n') + '\r\n\r\n' + entityBody;
    }

    // A PDF rides along: wrap the entity above into multipart/mixed.
    const mixed = [
        '--mix-' + boundary,
        'Content-Type: ' + entityType,
        '',
        entityBody,
        '--mix-' + boundary,
        'Content-Type: application/pdf; name="' + attachmentName + '"',
        'Content-Transfer-Encoding: base64',
        'Content-Disposition: attachment; filename="' + attachmentName + '"',
        '',
        wrap(String(attachmentData)),
        '--mix-' + boundary + '--'
    ].join('\r\n');
    headers.push('Content-Type: multipart/mixed; boundary="mix-' + boundary + '"');
    return headers.join('\r\n') + '\r\n\r\n' + mixed;
}

function smtpChannel(socket) {
    let active = socket;
    let writer = active.writable.getWriter();
    let reader = active.readable.getReader();
    const decoder = new TextDecoder();
    const encoder = new TextEncoder();
    let buffer = '';

    async function readReply() {
        for (;;) {
            const lines = buffer.split('\r\n');
            for (let i = 0; i < lines.length; i++) {
                if (/^\d{3} /.test(lines[i])) {
                    const code = Number(lines[i].slice(0, 3));
                    const text = lines.slice(0, i + 1).join(' | ');
                    buffer = lines.slice(i + 1).join('\r\n');
                    return { code: code, text: text };
                }
            }
            const chunk = await reader.read();
            if (chunk.done) return { code: 0, text: buffer || 'connection closed' };
            buffer += decoder.decode(chunk.value, { stream: true });
        }
    }

    async function write(line) {
        await writer.write(encoder.encode(line + '\r\n'));
    }

    async function command(line, expect, label) {
        if (line !== null) await write(line);
        const reply = await readReply();
        if (expect && reply.code !== expect) {
            // Never echo the command itself: AUTH arguments carry the mailbox
            // password in base64, and this string reaches HTTP callers and logs.
            const shown = label || (line === null ? 'greeting' : line.split(' ')[0].split('<')[0]);
            throw new Error('SMTP ' + shown + ' rejected: ' + reply.code + ' ' + String(reply.text).slice(0, 120));
        }
        return reply;
    }

    function upgrade() {
        // STARTTLS returns a new socket. The old streams are dead, but their
        // reader/writer still hold the lock on the shared underlying stream, so
        // they must be released first — otherwise getWriter() above throws
        // "This WritableStream is currently locked to a writer".
        try { writer.releaseLock(); } catch (err) { /* already gone */ }
        try { reader.releaseLock(); } catch (err) { /* already gone */ }
        active = socket.startTls();
        writer = active.writable.getWriter();
        reader = active.readable.getReader();
        buffer = '';
        return active;
    }

    function close() {
        try { active.close(); } catch (err) { /* already closed */ }
    }

    return { readReply: readReply, write: write, command: command, upgrade: upgrade, close: close };
}

async function sendViaPurelymail(env, from, to, raw) {
    const recipients = Array.isArray(to) ? to : [to];
    const steps = [];
    const opened = await openAuthedSmtp(env, steps);
    if (!opened.ok) {
        return { ok: false, provider: 'purelymail-smtp', reason: opened.reason, steps: steps };
    }
    const smtp = opened.smtp;
    try {
        await smtp.command('MAIL FROM:<' + from + '>', 250);
        for (const rcpt of recipients) {
            await smtp.command('RCPT TO:<' + rcpt + '>', 250);
        }
        await smtp.command('DATA', 354);
        // dot-stuffing: a line starting with '.' would end the message early
        await smtp.write(raw.replace(/\r\n\./g, '\r\n..') + '\r\n.');
        await smtp.command(null, 250);
        steps.push('sent');
        await smtp.command('QUIT', null).catch(function () { return null; });
        return { ok: true, provider: 'purelymail-smtp', steps: steps };
    } catch (err) {
        return { ok: false, provider: 'purelymail-smtp', reason: String((err && err.message) || err), steps: steps };
    } finally {
        if (smtp) smtp.close();
    }
}

// Open a session and authenticate. Shared by the send path and the probe, and
// retried once on the transient failures Purelymail actually returns: a 421 at
// greeting, or a socket that dies on the way in. Those are worth one more try;
// a 535 must never be retried, because repeating a wrong password looks like an
// attack and gets the mailbox locked.
async function openAuthedSmtp(env, steps) {
    let lastError = null;
    for (let attempt = 1; attempt <= 2; attempt++) {
        let smtp = null;
        try {
            smtp = smtpChannel(connect(
                { hostname: SMTP_HOST, port: SMTP_PORT },
                { secureTransport: 'starttls' }));
            await smtp.command(null, 220);
            if (!steps.includes('connected')) steps.push('connected');
            await smtp.command('EHLO sr-coresync.com', 250);
            await smtp.command('STARTTLS', 220);
            smtp.upgrade();
            await smtp.command('EHLO sr-coresync.com', 250);
            if (!steps.includes('tls')) steps.push('tls');
            await smtp.command('AUTH LOGIN', 334);
            await smtp.command(b64(env.PURELYMAIL_USER), 334, 'AUTH username');
            await smtp.command(b64(env.PURELYMAIL_PASS), 235, 'AUTH password');
            if (!steps.includes('auth')) steps.push('auth');
            return { ok: true, smtp: smtp };
        } catch (err) {
            if (smtp) smtp.close();
            lastError = err;
            const message = String((err && err.message) || err);
            const transient = message.indexOf('421') !== -1
                || message.indexOf('connection closed') !== -1
                || message.indexOf('Network connection lost') !== -1;
            if (!transient || attempt === 2) {
                return { ok: false, reason: message };
            }
            // Short pause: long enough for an overloaded greeting to clear, short
            // enough to stay inside the request budget.
            await new Promise(function (resolve) { setTimeout(resolve, 1200); });
        }
    }
    return { ok: false, reason: String((lastError && lastError.message) || lastError) };
}

// Authenticate only: proves the mailbox password works without sending anything.
async function probeSmtp(env) {
    const steps = [];
    const opened = await openAuthedSmtp(env, steps);
    if (!opened.ok) {
        return { ok: false, verified: false, reason: opened.reason, steps: steps };
    }
    const smtp = opened.smtp;
    try {
        await smtp.command('QUIT', null).catch(function () { return null; });
    } finally {
        smtp.close();
    }
    return { ok: true, verified: true, steps: steps };
}

// DNS over HTTPS, so the status page can show the mail records without
// loosening the site CSP to allow browser DNS queries.
async function doh(name, type) {
    const res = await fetch('https://dns.google/resolve?name=' + encodeURIComponent(name) + '&type=' + type,
        { headers: { accept: 'application/dns-json' } });
    if (!res.ok) throw new Error('doh-' + res.status);
    const payload = await res.json();
    return (payload.Answer || []).map(function (a) { return String(a.data); });
}

async function resolveMailDns(domain) {
    if (!/^[a-z0-9.-]{4,253}$/i.test(domain)) {
        return { ok: false, reason: 'invalid-domain' };
    }
    try {
        const results = await Promise.all([
            doh(domain, 'MX').catch(function () { return []; }),
            doh(domain, 'TXT').catch(function () { return []; }),
            doh('_dmarc.' + domain, 'TXT').catch(function () { return []; }),
            doh('purelymail1._domainkey.' + domain, 'CNAME').catch(function () { return []; })
        ]);
        const mx = results[0]
            .map(function (row) {
                const parts = row.trim().split(/\s+/);
                return { priority: Number(parts[0]), host: String(parts[parts.length - 1]).replace(/\.$/, '') };
            })
            .filter(function (row) { return row.host; })
            .sort(function (a, b) { return a.priority - b.priority; });
        const spf = results[1].map(function (t) { return t.replace(/"/g, ''); })
            .find(function (t) { return t.toLowerCase().indexOf('v=spf1') === 0; }) || null;
        const dmarc = results[2].map(function (t) { return t.replace(/"/g, ''); })
            .find(function (t) { return t.toLowerCase().indexOf('v=dmarc1') === 0; }) || null;
        const dkim = results[3].length > 0 ? results[3][0].replace(/\.$/, '') : null;
        const primary = mx.length ? mx[0].host : null;
        return {
            ok: !!(primary && primary.indexOf('purelymail') !== -1 && spf && dmarc && dkim),
            domain: domain,
            mx: mx,
            primaryMx: primary,
            spf: spf,
            dmarc: dmarc,
            dkim: dkim,
            checkedAt: new Date().toISOString()
        };
    } catch (err) {
        return { ok: false, reason: String((err && err.message) || err) };
    }
}

async function deliverEmail(env, to, subject, html, text, attachment) {
    if (!env) return { ok: false, reason: 'no-env' };
    const recipients = (Array.isArray(to) ? to : [to])
        .map(function (value) { return String(value || '').trim(); })
        .filter(Boolean);
    if (!recipients.length) return { ok: false, reason: 'no-recipient' };
    // Only the SMTP path can address several mailboxes in one message. The
    // legacy providers are single-recipient, so fan out rather than drop a copy.
    if (recipients.length > 1 && !smtpConfigured(env)) {
        const results = [];
        for (const one of recipients) {
            results.push(await deliverEmail(env, one, subject, html, text, attachment));
        }
        return {
            ok: results.every(function (r) { return r && r.ok; }),
            provider: (results[0] || {}).provider || null,
            recipients: recipients,
            reason: results.map(function (r) { return (r && r.reason) || 'ok'; }).join(',')
        };
    }
    const sender = env.MAIL_FROM || 'leads@sr-coresync.com';
    const attachmentName = attachment && attachment.filename ? attachment.filename : '';
    const attachmentB64 = attachment && attachment.base64 ? attachment.base64 : '';
    const toHeader = recipients.join(', ');

    if (env.SEND_EMAIL && typeof env.SEND_EMAIL.send === 'function') {
        const message = { to: toHeader, from: sender, subject: subject, html: html, text: text };
        if (attachmentB64) {
            message.attachments = [{ filename: attachmentName, content: attachmentB64, type: 'application/pdf', disposition: 'attachment' }];
        }
        await env.SEND_EMAIL.send(message);
        return { ok: true, provider: 'cloudflare-email' };
    }

    if (smtpConfigured(env)) {
        // Our own mailbox first: no extra vendor, and DKIM comes from the keys
        // the domain already publishes.
        const from = env.PURELYMAIL_USER;
        const raw = buildMime({
            from: from,
            fromName: env.MAIL_FROM_NAME || 'S&R CoreSync Solutions',
            to: toHeader,
            subject: subject,
            html: html,
            text: text,
            replyTo: env.MAIL_REPLY_TO || from,
            attachmentName: attachmentName,
            attachmentB64: attachmentB64
        });
        return await sendViaPurelymail(env, from, recipients, raw);
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

async function sendTelegramText(text, env) {
    const token = env && env.TELEGRAM_BOT_TOKEN;
    const chatId = env && env.TELEGRAM_CHAT_ID;
    if (!token || !chatId) return { ok: false, reason: 'telegram-not-configured' };
    try {
        const res = await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text: text, disable_web_page_preview: true })
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

    return sendTelegramText(lines.join('\n'), env);
}

// ---------------------------------------------------------------------------
// Who gets told about an enquiry
// ---------------------------------------------------------------------------
// info@ always receives every enquiry: a lead must never depend on a keyword
// guess. Department mailboxes are added on top, matched on whole words in the
// enquiry itself, and the map is overridable from wrangler.toml (LEAD_ROUTES)
// so the owner can change it without touching code.
const DEFAULT_ROUTES = {
    billing: 'billing@sr-coresync.com',
    support: 'support@sr-coresync.com',
    // Big-project signals go to the two founders, not to a shared inbox.
    executive: 'raed@sr-coresync.com,salim@sr-coresync.com'
};

const ROUTE_KEYWORDS = {
    billing: ['invoice', 'factuur', 'facture', 'fattura', 'faktura', 'rechnung', 'payment', 'betaling',
        'quote', 'quotation', 'offerte', 'pricing', 'price', 'prijs', 'tarief', 'vat', 'btw',
        'contract', 'license', 'licence', 'subscription', 'abonnement'],
    support: ['support', 'problem', 'error', 'bug', 'outage', 'incident', 'maintenance', 'fix', 'help',
        'storing', 'hilfe', 'aide', 'aiuto', 'pomoc', 'destek', 'migration', 'migratie'],
    executive: ['enterprise', 'corporate', 'holding', 'group-wide', 'rfp', 'tender', 'aanbesteding',
        'partnership', 'partner', 'reseller', 'white-label', 'whitelabel', 'government', 'overheid',
        'gemeente', 'ministry', 'ministerie', 'acquisition', 'due diligence', 'multinational']
};

function routeTable(env) {
    const table = Object.assign({}, DEFAULT_ROUTES);
    String((env && env.LEAD_ROUTES) || '').split(';').forEach(function (entry) {
        const parts = entry.split('=');
        if (parts.length === 2 && parts[0].trim()) {
            // 'billing=' with an empty value switches that department off.
            table[parts[0].trim().toLowerCase()] = parts[1].trim().toLowerCase() || null;
        }
    });
    return table;
}

function departmentsFor(lead, env) {
    const haystack = [lead.package, lead.packageLabel, lead.sessionLabel, lead.channel, lead.notes, lead.sourceUrl]
        .filter(Boolean).join(' ').toLowerCase();
    if (!haystack) return [];
    const table = routeTable(env);
    return Object.keys(ROUTE_KEYWORDS).filter(function (name) {
        if (!table[name]) return false;
        return ROUTE_KEYWORDS[name].some(function (word) {
            // Word boundaries, otherwise 'vat' fires inside 'private'.
            return new RegExp('(^|[^a-z0-9])' + word + '([^a-z0-9]|$)').test(haystack);
        });
    }).map(function (name) {
        // A department may hold several mailboxes; a comma list keeps that
        // expressible without inventing a second config format.
        return {
            department: name,
            emails: String(table[name]).split(',').map(function (address) {
                return address.trim().toLowerCase();
            }).filter(Boolean)
        };
    });
}

function leadRecipients(lead, env) {
    const primary = (env && env.NOTIFY_EMAIL) || '';
    const hits = departmentsFor(lead, env);
    const list = [primary].filter(Boolean);
    hits.forEach(function (hit) { list.push.apply(list, hit.emails); });
    return { recipients: Array.from(new Set(list)), departments: hits.map(function (hit) { return hit.department; }) };
}

async function notifyByEmail(lead, env, ctx) {
    if (!env || !env.NOTIFY_EMAIL) return { sent: false, reason: 'no-recipient' };
    const routing = leadRecipients(lead, env);

    const lines = [
        'New consultation lead \u2014 ' + (lead.leadId || ''),
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
    if (routing.departments.length) lines.push('Route   : ' + routing.departments.join(', '));

    // One delivery path, not four: deliverEmail already knows every provider.
    const work = deliverEmail(
        env,
        routing.recipients,
        'New Consultation Lead ' + (lead.leadId || ''),
        buildNotificationHtml(lead),
        lines.join('\n')
    ).then(function (result) {
        if (!result || !result.ok) {
            console.error('[LeadWorker] Email notification failed:', (result && result.reason) || 'unknown');
        }
        return result;
    }).catch(function (err) {
        console.error('[LeadWorker] Email notification threw:', err);
        return { ok: false, reason: 'exception' };
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

function leadTextFromRow(row) {
    const lines = [
        '\u{1F514} Lead reminder',
        '',
        'Name    : ' + (row.client_name || '-') + (row.company_name ? ' (' + row.company_name + ')' : ''),
        'Phone   : ' + (row.phone || '-'),
        'Email   : ' + (row.email || '-'),
        'Package : ' + (row.package || '-'),
        'Lang    : ' + (row.language || '-'),
        'Received: ' + String(row.received_at || '').slice(0, 16).replace('T', ' ')
    ];
    if (row.notes) lines.push('Notes   : ' + String(row.notes).slice(0, 400));
    if (row.source_url) lines.push('Source  : ' + row.source_url);
    return lines.join('\n');
}

async function buildDigest(env) {
    const stats = await buildPublicStats(env);
    var recent = [];
    var unannounced = 0;
    if (env && env.DB) {
        try {
            const rows = await env.DB.prepare(
                "SELECT client_name, received_at, notify_status FROM leads " +
                "WHERE received_at >= datetime('now', '-7 days') ORDER BY received_at DESC LIMIT 5"
            ).all();
            recent = (rows && rows.results) || [];
            const bad = await env.DB.prepare(
                "SELECT COUNT(*) AS n FROM leads WHERE notify_status IS NULL "
                + "OR notify_status NOT IN ('sent','resent','sent:webhook')"
            ).first();
            unannounced = Number((bad && bad.n) || 0);
        } catch (err) {
            console.error('[LeadWorker] digest query failed:', err);
        }
    }
    return {
        week: stats.consultations7d || 0,
        month: stats.consultations30d || 0,
        total: stats.total || 0,
        unannounced: unannounced,
        recent: recent
    };
}

function digestText(digest) {
    const lines = [
        '\u{1F4CA} S&R CoreSync \u2014 weekly lead digest',
        '',
        'Last 7 days : ' + digest.week,
        'Last 30 days: ' + digest.month,
        'All time    : ' + digest.total
    ];
    if (digest.unannounced > 0) {
        lines.push('');
        lines.push('\u26A0 ' + digest.unannounced + ' lead(s) were never announced.');
    }
    if (digest.recent && digest.recent.length) {
        lines.push('');
        lines.push('Recent:');
        digest.recent.forEach(function (row) {
            const when = String(row.received_at || '').slice(0, 16).replace('T', ' ');
            const announced = ['sent', 'resent', 'sent:webhook'].indexOf(row.notify_status) !== -1;
            const flag = announced ? '' : ' (no alert)';
            lines.push('  \u2022 ' + (row.client_name || 'unknown') + ' \u2014 ' + when + flag);
        });
    }
    return lines.join('\n');
}

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
    if (!env) return [];

    // D1 first: it is the system of record, so a deleted lead disappears from
    // the public feed immediately instead of lingering in the KV index.
    if (env.DB) {
        try {
            const rows = await env.DB.prepare(
                'SELECT received_at, channel FROM leads ORDER BY received_at DESC LIMIT ?1'
            ).bind(limit).all();
            const records = (rows && rows.results) || [];
            if (records.length) {
                return records.map(function (row) {
                    return { label: 'Consultation', at: row.received_at };
                });
            }
            return [];
        } catch (err) {
            console.error('[LeadWorker] D1 events failed, falling back to KV:', err);
        }
    }

    if (!env.LEADS) return [];
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

async function markNotified(env, leadId, outcome) {
    if (!env || !env.DB || !leadId) return;
    try {
        await env.DB.prepare(
            'UPDATE leads SET notify_status = ?, notified_at = ? WHERE lead_id = ?'
        ).bind(outcome, (outcome === 'sent' || outcome === 'resent') ? new Date().toISOString() : null, leadId).run();
    } catch (err) {
        console.error('[LeadWorker] notify status write failed:', err);
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
        await env.DB.prepare('UPDATE leads SET notify_status = ? WHERE lead_id = ?')
            .bind('pending', lead.leadId).run();
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
            // Deep mode costs one Telegram round-trip; the default stays free.
            let telegramVerified = null;
            if (url.searchParams.get('deep') === '1' && env && env.TELEGRAM_BOT_TOKEN) {
                try {
                    const res = await fetch('https://api.telegram.org/bot' + env.TELEGRAM_BOT_TOKEN + '/getMe');
                    const payload = await res.json().catch(function () { return {}; });
                    telegramVerified = !!payload.ok;
                } catch (err) {
                    telegramVerified = false;
                }
            }
            return jsonResponse({
                status: 'ok',
                service: 'sr-lead-capture',
                version: '1.0.0',
                time: new Date().toISOString(),
                kv: !!(env && env.LEADS),
                webhooks: parseWebhookUrls(env).length,
                email: !!(env && (env.SEND_EMAIL || env.RESEND_API_KEY || env.BREVO_API_KEY || env.EMAIL_WEBHOOK_URL || smtpConfigured(env))),
                emailChannel: !env ? 'none'
                    : (env.SEND_EMAIL ? 'cloudflare-email'
                        : (smtpConfigured(env) ? 'purelymail-smtp'
                        : (env.RESEND_API_KEY ? 'resend'
                            : (env.BREVO_API_KEY ? 'brevo'
                                : (env.EMAIL_WEBHOOK_URL ? 'webhook' : 'none'))))),
                mailFrom: (env && (env.PURELYMAIL_USER || env.MAIL_FROM)) || null,
                // Presence only; /mail/check?deep=1 is what proves the password.
                purelymail: smtpConfigured(env) ? 'on' : 'off',
                leadRoutes: Object.keys(routeTable(env)),
                d1: !!(env && env.DB),
                turnstile: (env && env.TURNSTILE_SECRET)
                    ? (String(env.TURNSTILE_ENFORCE || '') === '1' ? 'enforcing' : 'soft') : 'off',
                eventsPublic: String((env && env.EVENTS_PUBLIC) || '') === '1',
                // 'on' means the secrets exist, nothing more. Validity is a
                // different question - ask /notify/check, or /health?deep=1.
                telegram: (env && env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) ? 'on' : 'off',
                telegramVerified: telegramVerified
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

        // ---- Weekly digest to Telegram ---------------------------------------
        // Public on purpose (a scheduled job has to reach it) but throttled in KV
        // to once every six hours, so the worst an abuser can do is make the
        // owner receive the same summary a little more often.
        if (request.method === 'GET' && (path === '/digest' || path === '/api/digest')) {
            if (!env || !env.LEADS) {
                return jsonResponse({ sent: false, reason: 'no-kv-binding' }, 503, cors);
            }
            const last = await env.LEADS.get('digest:last');
            const now = Date.now();
            if (last && (now - Number(last)) < 6 * 3600 * 1000) {
                return jsonResponse({ sent: false, reason: 'throttled' }, 200,
                    Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
            }
            const digest = await buildDigest(env);
            const result = await sendTelegramText(digestText(digest), env);
            if (result.ok) {
                await env.LEADS.put('digest:last', String(now), { expirationTtl: 7 * 86400 });
            }
            return jsonResponse({
                sent: !!result.ok,
                reason: result.reason || null,
                digest: digest
            }, 200, Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
        }

        // ---- Re-announce leads whose alert never left -------------------------
        // Same trade-off as /digest: reachable without a shared secret so a
        // scheduled job can call it, throttled to once an hour in KV, and it can
        // only ever message the configured owner chat.
        if (request.method === 'GET' && (path === '/notify/resend' || path === '/api/notify/resend')) {
            if (!env || !env.DB) {
                return jsonResponse({ resent: 0, reason: 'no-d1-binding' }, 503, cors);
            }
            const lastKey = 'resend:last';
            const last = env.LEADS ? await env.LEADS.get(lastKey) : null;
            const now = Date.now();
            if (last && (now - Number(last)) < 3600 * 1000) {
                return jsonResponse({ resent: 0, reason: 'throttled' }, 200,
                    Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
            }

            const rows = await env.DB.prepare(
                "SELECT lead_id, client_name, company_name, email, phone, package, notes, "
                + "language, source_url, received_at FROM leads WHERE notify_status IS NULL "
                + "OR notify_status NOT IN ('sent','resent','sent:webhook') ORDER BY received_at ASC LIMIT 20"
            ).all();
            const pending = (rows && rows.results) || [];
            let resent = 0;
            for (const row of pending) {
                const result = await sendTelegramText(leadTextFromRow(row), env);
                if (!result.ok) {
                    return jsonResponse({ resent: resent, reason: result.reason, remaining: pending.length - resent },
                        200, Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
                }
                await markNotified(env, row.lead_id, 'resent');
                resent++;
            }
            if (env.LEADS && resent > 0) {
                await env.LEADS.put(lastKey, String(now), { expirationTtl: 7 * 86400 });
            }
            return jsonResponse({ resent: resent, remaining: pending.length - resent }, 200,
                Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
        }

        // ---- Telegram self-check ---------------------------------------------
        // Presence of a secret is not validity: after a /revoke the stored token
        // answers 401 and every notification is lost. This route asks Telegram.
        if (request.method === 'GET' && (path === '/notify/check' || path === '/api/notify/check')) {
            const token = env && env.TELEGRAM_BOT_TOKEN;
            const chat = env && env.TELEGRAM_CHAT_ID;
            if (!token || !chat) {
                return jsonResponse({ configured: false, ok: false, reason: 'telegram-not-configured' },
                    200, Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
            }
            try {
                const res = await fetch('https://api.telegram.org/bot' + token + '/getMe');
                const payload = await res.json().catch(function () { return {}; });
                return jsonResponse({
                    configured: true,
                    ok: !!payload.ok,
                    status: res.status,
                    bot: payload.ok && payload.result ? '@' + payload.result.username : null,
                    reason: payload.ok ? null : (payload.description || 'telegram-' + res.status)
                }, 200, Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
            } catch (err) {
                return jsonResponse({ configured: true, ok: false, reason: 'telegram-unreachable' },
                    200, Object.assign({}, cors, { 'Cache-Control': 'no-store' }));
            }
        }

        // ---- Mail self-check -------------------------------------------------
        // Same rule as Telegram: two stored variables are not proof. With ?deep=1
        // the worker opens a real STARTTLS session and authenticates, so the
        // answer is "the mailbox works" rather than "the secrets exist".
        if (request.method === 'GET' && (path === '/mail/check' || path === '/api/mail/check')) {
            const headers = Object.assign({}, cors, { 'Cache-Control': 'no-store' });
            const configured = smtpConfigured(env);
            const body = {
                configured: configured,
                channel: configured ? 'purelymail-smtp' : 'none',
                user: (env && env.PURELYMAIL_USER) || null,
                recipient: (env && env.NOTIFY_EMAIL) || null,
                smtp: SMTP_HOST + ':' + SMTP_PORT
            };
            if (!configured) {
                return jsonResponse(Object.assign(body, { ok: false, reason: 'purelymail-not-configured' }), 200, headers);
            }
            if (url.searchParams.get('deep') !== '1') {
                return jsonResponse(Object.assign(body, {
                    ok: true, verified: false, hint: 'add ?deep=1 to authenticate for real'
                }), 200, headers);
            }
            const key = 'mailcheck:last';
            const last = env.LEADS ? await env.LEADS.get(key) : null;
            const now = Date.now();
            if (last && (now - Number(last)) < 5 * 60 * 1000) {
                return jsonResponse(Object.assign(body, {
                    ok: true,
                    verified: false,
                    reason: 'throttled',
                    retryInSeconds: Math.ceil((5 * 60 * 1000 - (now - Number(last))) / 1000)
                }), 200, headers);
            }
            const probe = await probeSmtp(env);
            if (probe.ok && env.LEADS) {
                await env.LEADS.put(key, String(now), { expirationTtl: 3600 });
            }
            return jsonResponse(Object.assign(body, probe), probe.ok ? 200 : 502, headers);
        }

        // ---- One real message, to prove the mailbox sends ---------------------
        // /mail/check authenticates; this actually delivers. Throttled ten
        // minutes in KV so a crawler cannot turn it into a mail bomb, and it only
        // ever posts to the address the owner configured.
        if (request.method === 'GET' && (path === '/mail/selftest' || path === '/api/mail/selftest')) {
            const headers = Object.assign({}, cors, { 'Cache-Control': 'no-store' });
            if (!smtpConfigured(env) || !env.NOTIFY_EMAIL) {
                return jsonResponse({ ok: false, reason: 'mail-not-configured' }, 200, headers);
            }
            const key = 'mailselftest:last';
            const last = env.LEADS ? await env.LEADS.get(key) : null;
            const now = Date.now();
            if (last && (now - Number(last)) < 10 * 60 * 1000) {
                return jsonResponse({ ok: false, reason: 'throttled', retryInSeconds: Math.ceil((10 * 60 * 1000 - (now - Number(last))) / 1000) }, 200, headers);
            }
            const stamp = new Date().toISOString();
            const result = await deliverEmail(
                env,
                env.NOTIFY_EMAIL,
                'S&R CoreSync — SMTP self-test ' + stamp.slice(0, 16).replace('T', ' '),
                '<p dir="rtl">هذه رسالة اختبار من منصة S&amp;R CoreSync Solutions.</p>'
                + '<p>Sent at <strong>' + stamp + '</strong> from <strong>' + env.PURELYMAIL_USER + '</strong>.</p>'
                + '<p>If SPF, DKIM and DMARC show PASS in the headers, the mail path is healthy.</p>',
                'S&R CoreSync SMTP self-test\nSent: ' + stamp + '\nFrom: ' + env.PURELYMAIL_USER
            );
            if (result.ok && env.LEADS) {
                await env.LEADS.put(key, String(now), { expirationTtl: 3600 });
            }
            return jsonResponse({
                ok: !!result.ok,
                to: env.NOTIFY_EMAIL,
                provider: result.provider || null,
                steps: result.steps || [],
                reason: result.reason || null,
                sentAt: stamp
            }, result.ok ? 200 : 502, headers);
        }

        // ---- Mail DNS, resolved server-side ----------------------------------
        if (request.method === 'GET' && (path === '/mail/dns' || path === '/api/mail/dns')) {
            const summary = await resolveMailDns(url.searchParams.get('domain') || 'sr-coresync.com');
            // A failed lookup must never be cached: a single slow DoH call would
            // otherwise show as a ten-minute outage on the status page.
            return jsonResponse(summary, summary.ok ? 200 : 503, Object.assign({}, cors, {
                'Cache-Control': summary.ok ? 'public, max-age=180, stale-while-revalidate=600' : 'no-store'
            }));
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
        // The webhook relay is the independent second channel: if Telegram is
        // down but the relay delivered, the lead did reach a human.
        const announce = (telegram && telegram.ok) ? 'sent'
            : ((relayed && relayed.dispatched > 0) ? 'sent:webhook'
                : ('failed:' + ((telegram && telegram.reason) || 'unknown')));
        await markNotified(env, lead.leadId, announce);
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
            announced: announce,
            timestamp: lead.receivedAt
        }, 200, cors);
    }
};
