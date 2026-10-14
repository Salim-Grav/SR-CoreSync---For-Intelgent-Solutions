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
    const srvPort = 9562;
    const server = await startServer(srvPort);
    const dbgPort = 9899;
    const userDataDir = path.join(process.env.TEMP, 'edge_clip_all_' + Date.now());

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
                const clipped = [];
                const winW = window.innerWidth;
                let totalChecked = 0;
                document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, button, li, label, div').forEach(el => {
                    totalChecked++;
                    const style = window.getComputedStyle(el);
                    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;
                    const r = el.getBoundingClientRect();
                    const text = (el.innerText || '').trim();
                    if (!text || text.length < 2) return;

                    // Exclude marquee tracks and tickers which are intentionally animating
                    if (el.closest('.brand-marquee') || el.closest('.marquee') || el.closest('.ticker')) return;

                    const isOutRight = r.right > winW + 2;
                    const isOutLeft = r.left < -2;
                    const isHorizClipped = (el.scrollWidth - el.clientWidth > 4) && (style.overflow === 'hidden' || style.overflowX === 'hidden');
                    const isVertClipped = (el.scrollHeight - el.clientHeight > 4) && (style.overflow === 'hidden' || style.overflowY === 'hidden') && (style.maxHeight !== 'none' || (style.height && style.height.includes('px')));

                    if (isOutRight || isOutLeft || isHorizClipped || isVertClipped) {
                        clipped.push({
                            tag: el.tagName,
                            cls: (el.className || '').slice(0, 40),
                            id: el.id,
                            isOutRight,
                            isOutLeft,
                            isHorizClipped,
                            isVertClipped,
                            rect: { l: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width) },
                            text: text.slice(0, 50).replace(/\s+/g, ' ')
                        });
                    }
                });
                return { winW, totalChecked, clipped };
            })()
            `,
            returnByValue: true
        });

        if (result.exceptionDetails) {
            console.error('JS Exception:', result.exceptionDetails);
        } else {
            const data = result.result?.value;
            console.log('Result data:', JSON.stringify(data, null, 2));
        }
    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

run();
