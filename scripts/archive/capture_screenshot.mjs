#!/usr/bin/env node
/**
 * Live screenshot capture over the Chrome DevTools Protocol.
 *
 * Usage:
 *   node scripts/capture_screenshot.mjs <url> <output.png> [width] [height] [fullPage]
 *
 * The tool reuses the same browser discovery as scripts/browser_console_audit.mjs
 * so a single machine can verify the production site without extra tooling.
 */
import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const PORT = Number(process.env.SR_CDP_PORT || 9222);

const BROWSERS = [
    process.env.SR_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/usr/bin/microsoft-edge',
].filter(Boolean);

const [url, output, widthArg, heightArg, fullArg] = process.argv.slice(2);
if (!url || !output) {
    console.error('Usage: node scripts/capture_screenshot.mjs <url> <output.png> [width] [height] [fullPage]');
    process.exit(2);
}

const width = Number(widthArg || 1440);
const height = Number(heightArg || 900);
const fullPage = String(fullArg || 'false').toLowerCase() === 'true';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function findBrowser() {
    for (const candidate of BROWSERS) {
        if (existsSync(candidate)) return candidate;
    }
    return null;
}

async function getJson(path, method = 'GET') {
    const res = await fetch(`http://127.0.0.1:${PORT}${path}`, { method });
    const text = await res.text();
    try {
        return JSON.parse(text);
    } catch {
        throw new Error(`Unexpected DevTools response: ${text.slice(0, 120)}`);
    }
}

async function launch(browser, profile) {
    const args = [
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-extensions',
        '--hide-scrollbars',
        '--remote-debugging-port=' + PORT,
        '--user-data-dir=' + profile,
        '--window-size=' + width + ',' + height,
        'about:blank',
    ];
    const child = spawn(browser, args, { stdio: 'ignore' });
    for (let i = 0; i < 60; i++) {
        try { await getJson('/json/version'); return child; }
        catch { await sleep(250); }
    }
    child.kill();
    return null;
}

async function main() {
    const browser = findBrowser();
    if (!browser) {
        console.error('No Chromium/Edge binary found. Set SR_BROWSER to the executable path.');
        process.exit(3);
    }
    if (typeof WebSocket === 'undefined') {
        console.error('A global WebSocket is required (Node 22+).');
        process.exit(3);
    }

    const profile = mkdtempSync(join(tmpdir(), 'sr-shot-'));
    const child = await launch(browser, profile);
    if (!child) {
        console.error('The browser did not expose a DevTools endpoint.');
        process.exit(3);
    }

    try {
        const target = await getJson('/json/new?' + encodeURIComponent(url), 'PUT');
        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let id = 0;
        const pending = new Map();
        const events = [];

        const send = (method, params = {}) => new Promise((resolve, reject) => {
            const msgId = ++id;
            pending.set(msgId, { resolve, reject });
            ws.send(JSON.stringify({ id: msgId, method, params }));
        });

        ws.addEventListener('message', (event) => {
            const msg = JSON.parse(event.data);
            if (msg.id && pending.has(msg.id)) {
                const { resolve, reject } = pending.get(msg.id);
                pending.delete(msg.id);
                if (msg.error) reject(new Error(JSON.stringify(msg.error)));
                else resolve(msg.result);
            } else if (msg.method) {
                events.push(msg);
            }
        });

        await new Promise((resolve, reject) => {
            ws.addEventListener('open', resolve, { once: true });
            ws.addEventListener('error', reject, { once: true });
        });

        await send('Page.enable');
        await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', {
            width, height, deviceScaleFactor: 1, mobile: false,
        });

        await send('Page.navigate', { url });
        await sleep(3500);

        const errors = events
            .filter((e) => e.method === 'Runtime.exceptionThrown')
            .map((e) => e.params.exceptionDetails.text);

        const shot = await send('Page.captureScreenshot', {
            format: 'png',
            captureBeyondViewport: fullPage,
        });
        writeFileSync(output, Buffer.from(shot.data, 'base64'));

        const title = await send('Runtime.evaluate', {
            expression: 'document.title', returnByValue: true,
        });

        console.log(`Saved ${output}`);
        console.log(`Title: ${title.result.value}`);
        console.log(`JS errors: ${errors.length}${errors.length ? ' -> ' + errors.join(' | ') : ''}`);
        ws.close();
    } finally {
        child.kill();
    }
}

main().catch((err) => {
    console.error('Screenshot failed:', err.message);
    process.exit(1);
});
