const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const projectDir = path.resolve(__dirname, '..');

// Static server
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
            res.writeHead(200, {
                'Content-Type': mimeTypes[ext] || 'application/octet-stream',
                'Cache-Control': 'no-store'
            });
            fs.createReadStream(filePath).pipe(res);
        } else {
            res.writeHead(404);
            res.end('Not found');
        }
    });

    return new Promise(resolve => {
        server.listen(port, '127.0.0.1', () => resolve(server));
    });
}

async function runAudit() {
    const srvPort = 9555;
    const server = await startServer(srvPort);
    const dbgPort = 9896;
    const userDataDir = path.join(process.env.TEMP, 'edge_diag_' + Date.now());

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

        const testViewports = [
            { name: 'iPhone 13/14/15 Portrait', width: 390, height: 844 },
            { name: 'Small Mobile Portrait (Galaxy/iPhone SE)', width: 360, height: 740 },
            { name: 'Narrow Mobile (320px)', width: 320, height: 600 },
            { name: 'iPad Portrait (768px)', width: 768, height: 1024 },
            { name: 'iPad Landscape (1024px)', width: 1024, height: 768 },
            { name: 'Desktop Full HD (1920px)', width: 1920, height: 1080 }
        ];

        for (const vp of testViewports) {
            console.log(`\n=== Testing Viewport: ${vp.name} (${vp.width}x${vp.height}) ===`);
            await call('Emulation.setDeviceMetricsOverride', {
                width: vp.width,
                height: vp.height,
                deviceScaleFactor: 2,
                mobile: vp.width <= 768
            });

            await new Promise(r => setTimeout(r, 800));

            const diagResult = await call('Runtime.evaluate', {
                expression: `
                (function() {
                    const docWidth = document.documentElement.offsetWidth;
                    const scrollWidth = document.documentElement.scrollWidth;
                    const winWidth = window.innerWidth;
                    const hasHorizontalOverflow = scrollWidth > winWidth;

                    const overflowingElements = [];
                    const allEls = document.querySelectorAll('*');
                    for (const el of allEls) {
                        const rect = el.getBoundingClientRect();
                        // Check if element overflows window boundaries horizontally
                        if (rect.right > winWidth + 1 || rect.left < -1) {
                            // ignore fixed background overlays or offscreen hidden modals
                            const style = window.getComputedStyle(el);
                            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') continue;
                            if (style.position === 'fixed' && rect.width >= winWidth) continue;

                            overflowingElements.push({
                                tag: el.tagName,
                                id: el.id,
                                class: el.className,
                                textSnippet: (el.innerText || '').slice(0, 50).trim(),
                                rect: { left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) },
                                overflowAmount: Math.round(Math.max(rect.right - winWidth, -rect.left))
                            });
                        }
                    }

                    // Sort by largest overflow amount
                    overflowingElements.sort((a, b) => b.overflowAmount - a.overflowAmount);

                    return {
                        winWidth,
                        docWidth,
                        scrollWidth,
                        hasHorizontalOverflow,
                        overflowCount: overflowingElements.length,
                        topOverflows: overflowingElements.slice(0, 8)
                    };
                })()
                `,
                returnByValue: true
            });

            console.log(JSON.stringify(diagResult, null, 2));
        }

    } catch (e) {
        console.error('Audit Error:', e);
    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

runAudit();
