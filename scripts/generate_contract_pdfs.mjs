#!/usr/bin/env node
/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

/**
 * Render the two official contract pages to real PDF files (vector text, A4).
 * Output: <outDir>/OF-2026-1021.pdf and <outDir>/OF-2026-1022-FIN.pdf
 *
 * Usage: node scripts/generate_contract_pdfs.mjs <outDir>
 */
import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const PORT = 9336;
const BROWSERS = [
    process.env.SR_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
].filter(Boolean);

const outDir = process.argv[2] || '.';
mkdirSync(outDir, { recursive: true });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const getJson = async (p, method = 'GET') => JSON.parse(await (await fetch(`http://127.0.0.1:${PORT}${p}`, { method })).text());

const browser = BROWSERS.find((p) => existsSync(p));
if (!browser) { console.error('No Chromium/Edge binary found.'); process.exit(3); }

const profile = mkdtempSync(join(tmpdir(), 'sr-pdf-'));
const child = spawn(browser, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--no-first-run',
    '--disable-extensions', '--remote-debugging-port=' + PORT,
    '--user-data-dir=' + profile, '--window-size=1240,1754', 'about:blank',
], { stdio: 'ignore' });

for (let i = 0; i < 80; i++) { try { await getJson('/json/version'); break; } catch { await sleep(300); } }

const jobs = [
    ['OF-2026-1021', 'https://sr-coresync.com/contract-of2026-pdf.html?client=mudar&contract=OF-2026-1021'],
    ['OF-2026-1022-FIN', 'https://sr-coresync.com/contract-of2026-fin-pdf.html?client=mudar&contract=OF-2026-1022-FIN'],
];

for (const [ref, url] of jobs) {
    const target = await getJson('/json/new?' + encodeURIComponent(url), 'PUT');
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    let id = 0;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((res, rej) => {
        const n = ++id; pending.set(n, { res, rej }); ws.send(JSON.stringify({ id: n, method, params }));
    });
    ws.addEventListener('message', (ev) => {
        const m = JSON.parse(ev.data);
        if (m.id && pending.has(m.id)) {
            const { res, rej } = pending.get(m.id); pending.delete(m.id);
            m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
        }
    });
    await new Promise((res, rej) => { ws.addEventListener('open', res, { once: true }); ws.addEventListener('error', rej, { once: true }); });
    await send('Page.enable');
    await send('Page.navigate', { url });
    await sleep(4000);
    const pdf = await send('Page.printToPDF', {
        printBackground: true,
        preferCSSPageSize: true,
        paperWidth: 8.27,
        paperHeight: 11.69,
        marginTop: 0.3,
        marginBottom: 0.3,
        marginLeft: 0.3,
        marginRight: 0.3,
    });
    const out = join(outDir, ref + '.pdf');
    writeFileSync(out, Buffer.from(pdf.data, 'base64'));
    console.log('saved', out);
    ws.close();
}

child.kill();

