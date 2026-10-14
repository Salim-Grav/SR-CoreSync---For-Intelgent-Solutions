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

async function debugEl() {
    const srvPort = 9568;
    const server = await startServer(srvPort);
    const dbgPort = 9896;
    const userDataDir = path.join(process.env.TEMP, 'edge_dbg_' + Date.now());

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
                const el = document.querySelector('.section-software-hub .container') || document.querySelector('.software-filter-bar');
                if (!el) return 'element not found';
                const s = window.getComputedStyle(el);
                const parent = el.parentElement;
                const ps = window.getComputedStyle(parent);
                return {
                    tag: el.tagName,
                    cls: el.className,
                    width: s.width,
                    minWidth: s.minWidth,
                    maxWidth: s.maxWidth,
                    boxSizing: s.boxSizing,
                    parentCls: parent.className,
                    parentWidth: ps.width,
                    parentDisplay: ps.display,
                    heroActions: (function() {
                        const h = document.querySelector('.hero-reference__actions');
                        if (!h) return 'no hero actions';
                        const hs = window.getComputedStyle(h);
                        const firstBtn = h.querySelector('.tf-btn');
                        const bs = firstBtn ? window.getComputedStyle(firstBtn) : null;
                        return {
                            hWidth: hs.width,
                            hDisplay: hs.display,
                            hFlexWrap: hs.flexWrap,
                            btnWidth: bs ? bs.width : '',
                            btnMinW: bs ? bs.minWidth : '',
                            btnRect: firstBtn ? firstBtn.getBoundingClientRect() : null
                        };
                    })()
                };
            })()
            `,
            returnByValue: true
        });

        console.log('Inspection:', JSON.stringify(result.result.value, null, 2));

    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

debugEl();
