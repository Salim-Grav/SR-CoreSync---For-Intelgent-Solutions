/**
 * S&R CoreSync Solutions - Cloudflare Worker test harness
 * Runs the worker handler against mock Request/Response objects without
 * requiring wrangler or a network connection.
 *
 * Usage: node scripts/test_lead_worker.mjs
 */
import worker from '../workers/sr-lead-capture/src/index.js';

let passed = 0;
let failed = 0;

function assert(name, condition, detail) {
    if (condition) {
        passed++;
        console.log(`  PASS  ${name}`);
    } else {
        failed++;
        console.log(`  FAIL  ${name}${detail ? ' -> ' + detail : ''}`);
    }
}

// --- Mock KV ---------------------------------------------------------------
const kvStore = new Map();
const kv = {
    async get(key, type) {
        if (!kvStore.has(key)) return type === 'json' ? null : null;
        const v = kvStore.get(key);
        return type === 'json' ? JSON.parse(v) : v;
    },
    async put(key, value) { kvStore.set(key, value); }
};

// --- Mock webhook target ---------------------------------------------------
const relayed = [];
globalThis.fetch = async (url, init) => {
    if (typeof url === 'string' && url.includes('hook.example.com')) {
        relayed.push({ url, body: init && init.body });
        return new Response('ok', { status: 200 });
    }
    return new Response('unexpected', { status: 500 });
};

const env = {
    ALLOWED_ORIGINS: 'https://sr-coresync.com,https://www.sr-coresync.com',
    LEAD_WEBHOOK_URLS: 'https://hook.example.com/leads',
    NOTIFY_EMAIL: 'info@sr-coresync.com',
    LEADS: kv
};

const ORIGIN = 'https://sr-coresync.com';

function req(path, options = {}) {
    return new Request(`https://api.sr-coresync.com${path}`, {
        method: options.method || 'GET',
        headers: Object.assign(
            { 'Origin': ORIGIN, 'CF-Connecting-IP': options.ip || '1.2.3.4' },
            options.headers || {}
        ),
        body: options.body
    });
}

async function run() {
    console.log('='.repeat(64));
    console.log('S&R Lead Capture Worker - Test Suite');
    console.log('='.repeat(64));

    // 1. Health probe ---------------------------------------------------------
    let res = await worker.fetch(req('/health'), env, {});
    let body = await res.json();
    assert('GET /health returns 200', res.status === 200, `got ${res.status}`);
    assert('GET /health reports service name', body.service === 'sr-lead-capture');
    assert('GET /health reports kv binding', body.kv === true);

    // 2. CORS preflight --------------------------------------------------------
    res = await worker.fetch(req('/lead', { method: 'OPTIONS' }), env, {});
    assert('OPTIONS returns 204', res.status === 204, `got ${res.status}`);
    assert('OPTIONS echoes the allowed origin',
        res.headers.get('Access-Control-Allow-Origin') === ORIGIN);

    // 3. Valid lead -----------------------------------------------------------
    const validLead = {
        clientName: 'Ahmed Al Mansouri',
        companyName: 'Delta Trading BV',
        email: 'ahmed@delta.example',
        phone: '+31612345678',
        advisor: 'salim',
        notes: 'ERP migration inquiry',
        language: 'en',
        sourceUrl: 'https://sr-coresync.com/en/index.html'
    };
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(validLead)
    }), env, {});
    body = await res.json();
    assert('POST valid lead returns 200', res.status === 200, `got ${res.status}`);
    assert('POST valid lead reports success', body.status === 'success');
    assert('POST valid lead returns a leadId', /^LEAD-SR-\d{8}-[A-Z0-9]{4}$/.test(body.leadId || ''), body.leadId);
    assert('POST valid lead is persisted in KV', body.recorded === true);
    assert('POST valid lead is relayed to the webhook', body.dispatched === 1, `got ${body.dispatched}`);
    assert('Webhook received the sanitized payload', relayed.length === 1 && relayed[0].body.includes('Ahmed'));

    // 4. Stored payload must not carry HTML -----------------------------------
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clientName: '<script>alert(1)</script>Bob', email: 'b@example.com' })
    }), env, { });
    await res.json();
    const stored = JSON.parse(kvStore.get('lead:' + [...kvStore.keys()].find(k => k.startsWith('lead:LEAD')).split('lead:')[1]));
    assert('HTML is stripped from the stored name', !stored.clientName.includes('<script>'),
        stored.clientName);

    // 5. Invalid JSON ---------------------------------------------------------
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{not json'
    }), env, {});
    assert('POST invalid JSON returns 400', res.status === 400, `got ${res.status}`);

    // 6. Missing contact channel ----------------------------------------------
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clientName: 'No Contact' })
    }), env, {});
    assert('POST lead without contact returns 422', res.status === 422, `got ${res.status}`);

    // 7. Short name ------------------------------------------------------------
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clientName: 'A', email: 'a@example.com' })
    }), env, {});
    assert('POST lead with a 1-char name returns 422', res.status === 422, `got ${res.status}`);

    // 8. Honeypot --------------------------------------------------------------
    const before = kvStore.size;
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clientName: 'Bot', email: 'bot@spam.example', website: 'http://spam' })
    }), env, {});
    body = await res.json();
    assert('Honeypot lead returns 200 (silent accept)', res.status === 200);
    assert('Honeypot lead is NOT persisted', body.recorded === false);
    assert('Honeypot lead does not grow the KV store', kvStore.size === before);

    // 9. Wrong method ----------------------------------------------------------
    res = await worker.fetch(req('/lead', { method: 'GET' }), env, {});
    assert('GET /lead returns 405', res.status === 405, `got ${res.status}`);

    // 10. Unknown route ---------------------------------------------------------
    res = await worker.fetch(req('/nope', { method: 'POST' }), env, {});
    assert('POST unknown route returns 404', res.status === 404, `got ${res.status}`);

    // 11. Oversized body --------------------------------------------------------
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clientName: 'X', email: 'x@example.com', notes: 'A'.repeat(20000) })
    }), env, {});
    assert('Oversized payload is rejected', res.status === 413 || res.status === 400, `got ${res.status}`);

    // 12. Rate limiting ----------------------------------------------------------
    let limited = false;
    for (let i = 0; i < 12; i++) {
        const r = await worker.fetch(req('/lead', {
            method: 'POST',
            ip: '9.9.9.9',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ clientName: 'Rate Test ' + i, email: 'r@example.com' })
        }), env, {});
        if (r.status === 429) { limited = true; break; }
    }
    assert('Rate limiter blocks after 8 attempts', limited);

    // 13. Disallowed origin -------------------------------------------------------
    res = await worker.fetch(new Request('https://api.sr-coresync.com/lead', {
        method: 'OPTIONS',
        headers: { 'Origin': 'https://evil.example.com' }
    }), env, {});
    assert('Disallowed origin receives no CORS grant',
        res.headers.get('Access-Control-Allow-Origin') === null);

    // 13b. Health must report the mail channel honestly ---------------------------
    body = await (await worker.fetch(req('/health'), env, {})).json();
    assert('health reports no mail channel when unconfigured',
        body.emailChannel === 'none' && body.email === false,
        JSON.stringify({ channel: body.emailChannel, email: body.email }));
    assert('health reports the D1 binding state', body.d1 === false);
    assert('health reports the Turnstile state', body.turnstile === 'off');

    body = await (await worker.fetch(req('/health'),
        Object.assign({}, env, { RESEND_API_KEY: 're_test' }), {})).json();
    assert('health reports resend once the key exists',
        body.emailChannel === 'resend' && body.email === true, body.emailChannel);

    body = await (await worker.fetch(req('/health'),
        Object.assign({}, env, { BREVO_API_KEY: 'x', RESEND_API_KEY: 're_test' }), {})).json();
    assert('health prefers resend when both keys exist', body.emailChannel === 'resend', body.emailChannel);

    body = await (await worker.fetch(req('/health'),
        Object.assign({}, env, { BREVO_API_KEY: 'x' }), {})).json();
    assert('health falls back to brevo alone', body.emailChannel === 'brevo', body.emailChannel);

    // 13c. Telegram notifier (zero-DNS notification path) -------------------------
    let telegramCalls = [];
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (url, init) => {
        if (typeof url === 'string' && url.includes('api.telegram.org')) {
            telegramCalls.push({ url, body: init && init.body });
            return new Response(JSON.stringify({ ok: true }), { status: 200 });
        }
        return originalFetch(url, init);
    };

    body = await (await worker.fetch(req('/health'), env, {})).json();
    assert('health reports telegram=off without secrets', body.telegram === 'off', body.telegram);
    assert('health leaves verification null unless asked', body.telegramVerified === null);

    const tgEnv = Object.assign({}, env, {
        TELEGRAM_BOT_TOKEN: '123:TEST',
        TELEGRAM_CHAT_ID: '-100123'
    });
    body = await (await worker.fetch(req('/health'), tgEnv, {})).json();
    assert('health reports telegram=on with secrets', body.telegram === 'on', body.telegram);
    assert('on is not a validity claim', body.telegramVerified === null);

    body = await (await worker.fetch(req('/health?deep=1'), tgEnv, {})).json();
    assert('deep mode fills telegramVerified', typeof body.telegramVerified === 'boolean',
        String(body.telegramVerified));

    body = await (await worker.fetch(req('/notify/check'), tgEnv, {})).json();
    assert('/notify/check reports configured and a boolean ok',
        body.configured === true && typeof body.ok === 'boolean');

    telegramCalls = [];
    res = await worker.fetch(req('/lead', {
        method: 'POST',
        ip: '7.7.7.7',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            clientName: 'Telegram Probe',
            phone: '+31600000001',
            notes: 'ping'
        })
    }), tgEnv, {});
    assert('lead accepted with telegram configured', res.status === 200, `got ${res.status}`);
    assert('telegram was called exactly once', telegramCalls.length === 1, `calls=${telegramCalls.length}`);
    assert('telegram payload carries the phone number',
        (telegramCalls[0] || {}).body && telegramCalls[0].body.includes('+31600000001'));
    assert('telegram payload never leaks the token in the body',
        (telegramCalls[0] || {}).body && !telegramCalls[0].body.includes('123:TEST'));

    globalThis.fetch = originalFetch;

    // 14. VAT calculator (replaces the dead api.coresync.eu) ----------------------
    res = await worker.fetch(req('/tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: 100, rate: 21 })
    }), env, {});
    body = await res.json();
    assert('POST /tax exclusive returns 200', res.status === 200, `got ${res.status}`);
    assert('exclusive: net 100 -> vat 21 -> gross 121',
        body.net === 100 && body.vat === 21 && body.gross === 121,
        JSON.stringify(body));

    res = await worker.fetch(req('/tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: 121, rate: 21, mode: 'inclusive' })
    }), env, {});
    body = await res.json();
    assert('inclusive: gross 121 -> net 100 / vat 21',
        body.net === 100 && body.vat === 21 && body.gross === 121,
        JSON.stringify(body));

    res = await worker.fetch(req('/tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: 1234.56, rate: 9 })
    }), env, {});
    body = await res.json();
    assert('9% rate rounds to cents (1234.56 -> 111.11 vat)',
        body.vat === 111.11 && body.gross === 1345.67, JSON.stringify(body));

    res = await worker.fetch(req('/tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: -5 })
    }), env, {});
    assert('negative amount is rejected with 422', res.status === 422, `got ${res.status}`);

    res = await worker.fetch(req('/tax', { method: 'GET' }), env, {});
    assert('GET /tax returns 405', res.status === 405, `got ${res.status}`);

    // 15. Payment webhook ---------------------------------------------------------
    res = await worker.fetch(req('/pay/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: 'tr_123456' })
    }), env, {});
    assert('Mollie webhook without a key returns 503', res.status === 503, `got ${res.status}`);

    const stripeEnv = Object.assign({}, env, { STRIPE_WEBHOOK_SECRET: 'whsec_test_secret' });
    const goodPayload = JSON.stringify({ id: 'evt_1', type: 'payment_intent.succeeded',
        data: { object: { id: 'pi_1', amount_total: 5455, currency: 'eur' } } });
    const ts = Math.floor(Date.now() / 1000);
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode('whsec_test_secret'),
        { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const mac = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(ts + '.' + goodPayload));
    const sig = Array.from(new Uint8Array(mac)).map(b => b.toString(16).padStart(2, '0')).join('');

    res = await worker.fetch(req('/pay/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Stripe-Signature': `t=${ts},v1=deadbeef` },
        body: goodPayload
    }), stripeEnv, {});
    assert('Stripe webhook with a bad signature returns 401', res.status === 401, `got ${res.status}`);

    res = await worker.fetch(req('/pay/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Stripe-Signature': `t=${ts},v1=${sig}` },
        body: goodPayload
    }), stripeEnv, {});
    body = await res.json();
    assert('Stripe webhook with a valid signature returns 200', res.status === 200, `got ${res.status}`);
    assert('valid Stripe event is recorded in KV',
        [...kvStore.keys()].some(k => k === 'payment:stripe:evt_1'));

    const staleTs = ts - 900;
    const staleMac = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(staleTs + '.' + goodPayload));
    const staleSig = Array.from(new Uint8Array(staleMac)).map(b => b.toString(16).padStart(2, '0')).join('');
    res = await worker.fetch(req('/pay/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Stripe-Signature': `t=${staleTs},v1=${staleSig}` },
        body: goodPayload
    }), stripeEnv, {});
    assert('replayed Stripe event (>5 min) is rejected', res.status === 400, `got ${res.status}`);

    console.log('='.repeat(64));
    console.log(`RESULT: ${passed} passed, ${failed} failed`);
    console.log('='.repeat(64));
    process.exit(failed ? 1 : 0);
}

run().catch(err => {
    console.error('Test harness crashed:', err);
    process.exit(1);
});
