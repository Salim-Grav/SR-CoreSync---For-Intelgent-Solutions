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

    console.log('='.repeat(64));
    console.log(`RESULT: ${passed} passed, ${failed} failed`);
    console.log('='.repeat(64));
    process.exit(failed ? 1 : 0);
}

run().catch(err => {
    console.error('Test harness crashed:', err);
    process.exit(1);
});
