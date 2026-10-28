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

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const projectDir = path.resolve(__dirname, '..');

function startServer(port) {
    const mimeTypes = {
        '.html': 'text/html; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml'
    };

    const server = http.createServer((req, res) => {
        let reqPath = decodeURI(req.url.split('?')[0]);
        if (reqPath === '/' || reqPath === '') reqPath = '/index.html';
        const filePath = path.join(projectDir, reqPath);

        if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            const ext = path.extname(filePath).toLowerCase();
            res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
            fs.createReadStream(filePath).pipe(res);
        } else {
            res.writeHead(404);
            res.end('Not found');
        }
    });

    return new Promise(resolve => server.listen(port, '127.0.0.1', () => resolve(server)));
}

async function run() {
    const srvPort = 9574;
    const server = await startServer(srvPort);
    const dbgPort = 9893;
    const userDataDir = path.join(process.env.TEMP, 'edge_insp3_' + Date.now());

    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + dbgPort,
        '--user-data-dir=' + userDataDir,
        '--window-size=375,812',
        `http://127.0.0.1:${srvPort}/index.html`
    ]);

    try {
        await new Promise(r => setTimeout(r, 2200));
        const pages = await new Promise((res, rej) => {
            http.get(`http://127.0.0.1:${dbgPort}/json`, r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => res(JSON.parse(d)));
            }).on('error', rej);
        });

        const page = pages.find(p => p.url && p.url.includes(`127.0.0.1:${srvPort}`));
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
        await call('Runtime.enable');
        await call('Emulation.setDeviceMetricsOverride', {
            width: 375,
            height: 812,
            deviceScaleFactor: 2,
            mobile: true
        });

        await new Promise(r => setTimeout(r, 1200));

        const result = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const copy = document.querySelector('.hero-reference__copy');
                const items = copy ? Array.from(copy.children).map(c => ({
                    tag: c.tagName,
                    cls: c.className,
                    text: c.innerText.slice(0, 30),
                    scrollW: c.scrollWidth,
                    offsetW: c.offsetWidth,
                    whiteSpace: window.getComputedStyle(c).whiteSpace
                })) : [];
                return items;
            })()
            `,
            returnByValue: true
        });

        const val = result.result?.result?.value ?? result.result?.value ?? result;
        console.log('Parent chain:', JSON.stringify(val, null, 2));

    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

run();
