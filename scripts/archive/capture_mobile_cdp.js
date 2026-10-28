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

const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const dbgPort = 9893;
const userDataDir = path.join(process.env.TEMP, 'edge_cdp_' + Date.now());
const outPath = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\f3799c46-c9cb-4e3a-902f-f85603d0aae5\\nfc_card_mobile_perfect.png';

async function captureMobile() {
    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + dbgPort,
        '--user-data-dir=' + userDataDir,
        '--window-size=600,1000',
        'http://localhost:3000/card.html'
    ]);

    await new Promise(r => setTimeout(r, 2000));

    try {
        const pages = await new Promise((res, rej) => {
            http.get(`http://127.0.0.1:${dbgPort}/json`, r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => res(JSON.parse(d)));
            }).on('error', rej);
        });

        const page = pages.find(p => p.url && p.url.includes('card.html'));
        if (!page) throw new Error('Page not found in Edge debug list');

        const ws = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise(r => ws.onopen = r);

        let curId = 1;
        const call = (method, params = {}) => new Promise(res => {
            const id = curId++;
            const handler = (evt) => {
                const m = JSON.parse(evt.data);
                if (m.id === id) {
                    ws.removeEventListener('message', handler);
                    res(m);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id, method, params }));
        });

        await call('Page.enable');
        await call('Emulation.setDeviceMetricsOverride', {
            width: 390,
            height: 844,
            deviceScaleFactor: 2,
            mobile: true
        });

        await new Promise(r => setTimeout(r, 800));

        const snap = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(outPath, Buffer.from(snap.result.data, 'base64'));
        console.log('Mobile screenshot captured via CDP successfully:', outPath);

        ws.close();
    } catch (err) {
        console.error('CDP error:', err);
    } finally {
        edge.kill();
        setTimeout(() => {
            try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
        }, 1000);
    }
}

captureMobile();
