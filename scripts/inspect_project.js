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
    const srvPort = 9570;
    const server = await startServer(srvPort);
    const dbgPort = 9895;
    const userDataDir = path.join(process.env.TEMP, 'edge_insp_' + Date.now());

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
                const el = document.querySelector('.section-software-hub .container');
                const heroActions = document.querySelector('.hero-reference__actions');
                const heroCopy = document.querySelector('.hero-reference__copy');
                const heroGrid = document.querySelector('.hero-reference__grid');

                // Inspect heroCopy and heroGrid widths
                return {
                    containerWidth: el ? el.offsetWidth : null,
                    containerInlineStyle: el ? el.getAttribute('style') : null,
                    heroGridWidth: heroGrid ? heroGrid.offsetWidth : null,
                    heroCopyWidth: heroCopy ? heroCopy.offsetWidth : null,
                    heroActionsWidth: heroActions ? heroActions.offsetWidth : null,
                    heroCopyMargin: heroCopy ? window.getComputedStyle(heroCopy).margin : null,
                    heroCopyPadding: heroCopy ? window.getComputedStyle(heroCopy).padding : null,
                    heroGridStyle: heroGrid ? {
                        width: window.getComputedStyle(heroGrid).width,
                        display: window.getComputedStyle(heroGrid).display,
                        gridTemplateColumns: window.getComputedStyle(heroGrid).gridTemplateColumns
                    } : null
                };
            })()
            `,
            returnByValue: true
        });

        console.log('Result:', JSON.stringify(result));

    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

run();
