/**
 * S&R CoreSync For Intelligent Solutions - live browser console audit
 * -----------------------------------------------------------------------------
 * Loads every published page in headless Microsoft Edge via the DevTools
 * Protocol and reports uncaught exceptions, failed network requests and
 * console errors. This is the check that proves the pages actually run -
 * a page can be perfectly valid HTML and still be dead in the browser.
 *
 * Usage: node scripts/browser_console_audit.mjs [--pages=10]
 */
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync, existsSync, readFileSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, extname, resolve } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';
import http from 'node:http';
import net from 'node:net';

const BROWSER_CANDIDATES = [
    process.env.SR_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/usr/bin/microsoft-edge'
].filter(Boolean);

const EDGE = BROWSER_CANDIDATES.find(p => existsSync(p));

// --csp[=policy] serves every page with Content-Security-Policy-Report-Only and
// reports the violations instead of auditing handlers. GitHub Pages cannot send
// headers, so this is the only honest way to measure what a strict policy would
// block tonight.
const CSP_ARG = process.argv.find(a => a.startsWith('--csp'));
const CSP_MODE = Boolean(CSP_ARG);
// The target policy: same host allowlist the live _headers file declares, but
// with 'unsafe-inline' removed from script-src and style-src. Anything reported
// here is therefore a genuine blocker, not a missing allowlist entry.
const DEFAULT_CSP = [
    "default-src 'self'",
    "script-src 'self' https://cdn.jsdelivr.net https://cdn.tailwindcss.com https://unpkg.com https://js.stripe.com",
    "style-src 'self' https://fonts.googleapis.com https://cdn.tailwindcss.com",
    "img-src 'self' data: blob:",
    "font-src 'self' data: https://fonts.gstatic.com",
    "connect-src 'self' https://sr-lead-capture.sr-coresync.workers.dev https://fonts.googleapis.com",
    "object-src 'none'",
    "base-uri 'self'"
].join('; ');
const CSP_POLICY = CSP_ARG && CSP_ARG.includes('=') ? CSP_ARG.slice(CSP_ARG.indexOf('=') + 1) : DEFAULT_CSP;

let PORT = 9222;
let HTTP_PORT = 8099;
const SITE = resolve(process.env.SR_SITE_DIR || join(process.cwd(), '_site'));

// The DevTools port must be free before the browser is started. If another
// browser already owns it, the launch silently attaches to that foreign
// instance and the audit hangs on /json/new.
async function findFreePort(preferred) {
    const candidates = [preferred, 0].filter(v => v !== undefined);
    for (const wanted of candidates) {
        const port = await new Promise(resolve => {
            const probe = net.createServer();
            probe.once('error', () => resolve(-1));
            probe.listen(wanted, '127.0.0.1', () => {
                const found = probe.address().port;
                probe.close(() => resolve(found));
            });
        });
        if (port > 0) return port;
    }
    throw new Error('No free DevTools port available.');
}

const MIME = {
    '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif',
    '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2',
    '.mp4': 'video/mp4', '.webm': 'video/webm', '.txt': 'text/plain; charset=utf-8',
    '.xml': 'application/xml', '.zip': 'application/zip'
};

function startServer() {
    const server = http.createServer((req, res) => {
        let p = decodeURIComponent(req.url.split('?')[0]);
        if (p.endsWith('/')) p += 'index.html';
        const file = join(SITE, p);
        if (!file.startsWith(SITE) || !existsSync(file) || !statSync(file).isFile()) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('not found');
            return;
        }
        const headers = { 'Content-Type': MIME[extname(file).toLowerCase()] || 'application/octet-stream' };
        if (CSP_MODE) headers['Content-Security-Policy-Report-Only'] = CSP_POLICY;
        res.writeHead(200, headers);
        res.end(readFileSync(file));
    });
    return new Promise(r => server.listen(HTTP_PORT, '127.0.0.1', () => r(server)));
}

const args = process.argv.slice(2);
const limitArg = args.find(a => a.startsWith('--pages='));
const LIMIT = limitArg ? parseInt(limitArg.split('=')[1], 10) : Infinity;

const LANGUAGES = ['/', '/en/', '/ckb/', '/de/', '/tr/', '/ku/', '/nl/', '/fr/', '/es/',
    '/it/', '/no/', '/sv/', '/pl/', '/ro/', '/bg/', '/cs/', '/da/', '/el/', '/et/',
    '/fi/', '/ga/', '/hr/', '/hu/', '/lt/', '/lv/', '/mt/', '/pt/', '/sk/', '/sl/', '/hr/'];

async function getJson(path) {
    const res = await fetch(`http://127.0.0.1:${PORT}${path}`);
    return res.json();
}
async function launchBrowser(profile, extraArgs = []) {
    const base = [
        '--disable-gpu',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-extensions',
        '--disable-background-networking',
        '--remote-debugging-port=' + PORT,
        '--user-data-dir=' + profile,
        ...extraArgs,
        'about:blank'
    ];
    const child = spawn(EDGE, base, { stdio: 'ignore' });
    for (let i = 0; i < 40; i++) {
        try { await getJson('/json/version'); return child; }
        catch { await sleep(250); }
    }
    child.kill();
    return null;
}

const HANDLER_AUDIT = `(() => {
    const names = new Set();
    const attrs = ['onclick','oninput','onchange','onsubmit','onload','onfocus',
                   'onblur','onkeydown','onkeyup','onerror','onmouseover',
                   'onmouseenter','onmouseleave','oncontextmenu','ondragend',
                   'onanimationend','ontoggle','onwheel'];
    document.querySelectorAll('*').forEach(el => {
        attrs.forEach(a => {
            const raw = el.getAttribute(a);
            if (!raw) return;
            // Drop string literals first: a caption such as
            // openFoundersLightbox('... S&R CoreSync (For ...)') must not be
            // mistaken for a call to a global named CoreSync.
            const v = raw.replace(/'[^']*'/g, "''").replace(/"[^"]*"/g, '""');
            const re = /(^|[^.\\w$])([A-Za-z_$][\\w$]*)\\s*\\(/g;
            let m;
            while ((m = re.exec(v)) !== null) names.add(m[2]);
        });
    });
    const blocked = new Set(['if','for','while','switch','catch','return','typeof',
        'function','new','await','async','delete','void','in','of','do','else','try',
        'finally','throw','case','default','break','continue','class','extends',
        'super','this','import','export','let','const','var','yield','instanceof']);
    const missing = [];
    Array.from(names).forEach(n => {
        if (blocked.has(n)) return;
        try {
            if (new Function('return typeof ' + n)() === 'undefined') missing.push(n);
        } catch (e) { /* not resolvable - ignore */ }
    });
    return missing.sort().join(',');
})()`;

async function main() {
    if (typeof WebSocket === 'undefined') {
        console.log('='.repeat(72));
        console.log('SKIPPED - the DevTools client needs a global WebSocket (Node 22+).');
        console.log('='.repeat(72));
        return;
    }
    if (!EDGE) {
        console.log('='.repeat(72));
        console.log('SKIPPED - no Chromium based browser found on this machine.');
        console.log('='.repeat(72));
        return;
    }
    if (!existsSync(SITE)) {
        console.log('='.repeat(72));
        console.log('SKIPPED - publish set not built. Run: python scripts/prepare_publish_set.py');
        console.log('='.repeat(72));
        return;
    }
    PORT = await findFreePort(9222);
    HTTP_PORT = await findFreePort(8099);
    console.log(`DevTools port ${PORT}, site server port ${HTTP_PORT}`);
    const server = await startServer();
    const profile = mkdtempSync(join(tmpdir(), 'sr-edge-'));

    let child = await launchBrowser(profile, ['--headless=new']);
    if (!child) {
        child = await launchBrowser(profile, ['--headless']);
    }
    if (!child) {
        server.close();
        console.log('='.repeat(72));
        console.log('SKIPPED - the headless browser did not expose a DevTools endpoint.');
        console.log('='.repeat(72));
        return;
    }
    const pages = LANGUAGES.slice(0, LIMIT);
    const results = [];
const cspAll = [];
    let failed = 0;

    for (const route of pages) {
        const url = `http://127.0.0.1:${HTTP_PORT}${route}`;
        const target = await fetch(`http://127.0.0.1:${PORT}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' })
            .then(r => r.json());

        const errors = [];
        const failedRequests = [];
        const cspViolations = [];
        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let id = 0;
        const pending = new Map();

        const send = (method, params = {}) => new Promise(resolve => {
            const msgId = ++id;
            pending.set(msgId, resolve);
            ws.send(JSON.stringify({ id: msgId, method, params }));
        });

        await new Promise(resolve => ws.addEventListener('open', resolve));

        ws.addEventListener('message', ev => {
            const msg = JSON.parse(ev.data);
            if (msg.id && pending.has(msg.id)) {
                pending.get(msg.id)(msg.result);
                pending.delete(msg.id);
                return;
            }
            if (msg.method === 'Runtime.exceptionThrown') {
                const d = msg.params.exceptionDetails;
                errors.push((d.exception && d.exception.description) || d.text);
            }
            if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
                errors.push(msg.params.args.map(a => a.value ?? a.description ?? '').join(' '));
            }
            if (CSP_MODE && msg.method === 'Log.entryAdded') {
                const entry = msg.params.entry || {};
                if (entry.source === 'security') {
                    cspViolations.push((entry.text || '').replace(/\s+/g, ' ').trim().slice(0, 220));
                }
            }
            if (msg.method === 'Network.loadingFailed') {
                const reason = msg.params.errorText || '';
                // ERR_ABORTED means the request was cancelled (navigation,
                // tab close) - not a missing resource.
                if (/ERR_ABORTED/.test(reason)) return;
                failedRequests.push(reason + ' ' + (msg.params.type || ''));
            }
            if (msg.method === 'Network.responseReceived') {
                const r = msg.params.response;
                if (r.status >= 400) failedRequests.push(`${r.status} ${r.url}`);
            }
        });

        await send('Runtime.enable');
        await send('Network.enable');
        await send('Page.enable');
        if (CSP_MODE) await send('Log.enable');
        await send('Page.navigate', { url });
        await sleep(2600);

        // ---------------------------------------------------------------
        // Undefined inline event handlers.
        //
        // A localized page can keep the markup of a feature while losing
        // the function that backs it (e.g. the ROI sliders survived the
        // translation pass but updateROICalculator() never did). Nothing
        // breaks at load time - the control is simply dead until someone
        // drags it, and then it throws ReferenceError.
        // ---------------------------------------------------------------
        let deadHandlers = [];
        if (!CSP_MODE) try {
            const probe = await send('Runtime.evaluate', {
                expression: HANDLER_AUDIT,
                returnByValue: true,
            });
            const value = probe && probe.result && probe.result.value;
            if (value) deadHandlers = value.split(',').filter(Boolean);
        } catch (e) { /* evaluation failed - skip */ }

        ws.close();
        await fetch(`http://127.0.0.1:${PORT}/json/close/${target.id}`);

        const real = errors.filter(e => !/favicon/i.test(e));
        const req = failedRequests.filter(e => !/favicon/i.test(e));

        if (CSP_MODE) {
            const unique = [...new Set(cspViolations)];
            unique.forEach(v => cspAll.push({ route, text: v }));
            const ok = unique.length === 0;
            if (!ok) failed++;
            results.push({ route, ok, violations: unique });
            console.log(`${ok ? 'PASS' : 'FAIL'}  ${route.padEnd(8)} csp-violations=${unique.length}`);
            unique.slice(0, 3).forEach(v => console.log('        > ' + v.slice(0, 170)));
            continue;
        }

        const ok = real.length === 0 && req.length === 0 && deadHandlers.length === 0;
        if (!ok) failed++;
        results.push({ route, ok, errors: real, requests: req, deadHandlers });
        console.log(`${ok ? 'PASS' : 'FAIL'}  ${route.padEnd(8)} js-errors=${real.length} failed-requests=${req.length} dead-handlers=${deadHandlers.length}`);
        real.slice(0, 4).forEach(e => console.log('        ! ' + String(e).split('\n')[0].slice(0, 160)));
        req.slice(0, 4).forEach(e => console.log('        > ' + String(e).slice(0, 160)));
        if (deadHandlers.length) {
            console.log('        x undefined handlers: ' + deadHandlers.join(', ').slice(0, 400));
        }
    }

    child.kill();
    if (typeof server.closeAllConnections === 'function') server.closeAllConnections();
    server.close();
    try { rmSync(profile, { recursive: true, force: true }); } catch { }

    console.log('='.repeat(72));
    if (CSP_MODE) {
    // Group the violations so the next refactor targets causes, not symptoms.
    const byRule = {};
    const byBlocked = {};
    for (const item of cspAll) {
        const rule = (item.text.match(/violates the following Content Security Policy directive: "?([^"\s]+)/i) || [])[1]
            || (item.text.match(/(script-src|style-src|img-src|connect-src|font-src|default-src)/) || [])[1]
            || 'unknown';
        byRule[rule] = (byRule[rule] || 0) + 1;
        const blocked = (item.text.match(/blocked the (?:loading|execution) of (?:the )?([^\s.]+)/i) || [])[1] || 'inline';
        byBlocked[blocked] = (byBlocked[blocked] || 0) + 1;
    }
    console.log('-'.repeat(72));
    console.log('CSP report-only summary');
    console.log('policy: ' + CSP_POLICY);
    console.log('violations: ' + cspAll.length + ' across ' + new Set(cspAll.map(v => v.route)).size + ' route(s)');
    Object.entries(byRule).sort((a, b) => b[1] - a[1]).slice(0, 10)
        .forEach(([rule, count]) => console.log('  ' + String(count).padStart(5) + '  ' + rule));
    if (Object.keys(byBlocked).length) {
        console.log('blocked resources:');
        Object.entries(byBlocked).sort((a, b) => b[1] - a[1]).slice(0, 8)
            .forEach(([what, count]) => console.log('  ' + String(count).padStart(5) + '  ' + what));
    }
    console.log('-'.repeat(72));
}

console.log(`Pages audited: ${results.length}   passed: ${results.length - failed}   failed: ${failed}`);
    console.log('='.repeat(72));
    process.exit(failed ? 1 : 0);
}

main().catch(err => { console.error(err); process.exit(1); });

// Hard stop so a stuck browser connection can never hang CI.
setTimeout(() => { console.error('Browser audit timed out.'); process.exit(2); }, 15 * 60 * 1000).unref();
