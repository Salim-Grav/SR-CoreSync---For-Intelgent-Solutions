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

async function findClipped() {
    const srvPort = 9556;
    const server = await startServer(srvPort);
    const dbgPort = 9897;
    const userDataDir = path.join(process.env.TEMP, 'edge_clip_' + Date.now());

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

        // Test mobile portrait (375x812 - standard iPhone)
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
                const clippedList = [];
                const winW = window.innerWidth;

                // Scan all text containers
                const candidates = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, button, li, dt, dd, td, th, div');

                candidates.forEach(el => {
                    const style = window.getComputedStyle(el);
                    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;

                    // Condition 1: Horizontal text clipping (scrollWidth > clientWidth)
                    const isHorizClipped = (el.scrollWidth - el.clientWidth > 4) && (style.overflow === 'hidden' || style.overflowX === 'hidden' || style.textOverflow === 'ellipsis');
                    
                    // Condition 2: Vertical text clipping (scrollHeight > clientHeight with fixed height)
                    const isVertClipped = (el.scrollHeight - el.clientHeight > 8) && (style.overflow === 'hidden' || style.overflowY === 'hidden') && (style.maxHeight !== 'none' || style.height.includes('px'));

                    // Condition 3: Text with -webkit-line-clamp
                    const hasLineClamp = style.webkitLineClamp && style.webkitLineClamp !== 'none';

                    // Condition 4: White-space nowrap causing element to push outside viewport
                    const rect = el.getBoundingClientRect();
                    const isOutsideViewport = rect.right > winW + 2 || rect.left < -2;

                    const text = (el.innerText || '').trim();
                    if (!text || text.length < 3) return;

                    // Avoid duplicate logging of parent containers if children are already logged
                    if (isHorizClipped || isVertClipped || isOutsideViewport || (hasLineClamp && el.scrollHeight > el.clientHeight)) {
                        clippedList.push({
                            tag: el.tagName,
                            id: el.id || '',
                            class: el.className || '',
                            isHorizClipped,
                            isVertClipped,
                            isOutsideViewport,
                            hasLineClamp: !!hasLineClamp,
                            scrollW: el.scrollWidth,
                            clientW: el.clientWidth,
                            rect: { left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) },
                            text: text.slice(0, 80)
                        });
                    }
                });

                return {
                    winW,
                    count: clippedList.length,
                    items: clippedList.slice(0, 30)
                };
            })()
            `,
            returnByValue: true
        });

        console.log(JSON.stringify(result, null, 2));

    } catch (e) {
        console.error('Error:', e);
    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

findClipped();
