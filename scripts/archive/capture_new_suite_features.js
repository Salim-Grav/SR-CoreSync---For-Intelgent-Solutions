const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const brainDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\17be0c82-0a87-4d01-bb34-f04959091305';
const projectDir = path.resolve(__dirname, '..');

// 1. Simple local static server
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
        server.listen(port, '127.0.0.1', () => {
            console.log(`Static server running on http://127.0.0.1:${port}`);
            resolve(server);
        });
    });
}

async function captureAll() {
    const srvPort = 9444;
    const server = await startServer(srvPort);

    const dbgPort = 9892;
    const userDataDir = path.join(process.env.TEMP, 'edge_suite_cap_' + Date.now());

    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + dbgPort,
        '--user-data-dir=' + userDataDir,
        '--window-size=1440,960',
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

        const targets = [
            {
                name: 'live_3d_mockup_viewer.png',
                url: `http://127.0.0.1:${srvPort}/3d-mockup.html`,
                waitMs: 2200,
                action: null
            },
            {
                name: 'live_project_estimator.png',
                url: `http://127.0.0.1:${srvPort}/estimator.html`,
                waitMs: 1800,
                action: null
            },
            {
                name: 'live_client_portal_dashboard.png',
                url: `http://127.0.0.1:${srvPort}/preview-client-portal.html`,
                waitMs: 1800,
                action: null
            },
            {
                name: 'live_brandkit_with_3d_and_toast.png',
                url: `http://127.0.0.1:${srvPort}/index.html`,
                waitMs: 2500,
                action: `
                    (function() {
                        const tab = document.getElementById('tab-btn-identity');
                        if (tab) tab.click();
                        if (typeof openCurrentProjectModal === 'function') openCurrentProjectModal();
                        
                        setTimeout(() => {
                            const brandKit = document.getElementById('projectModalBrandKit');
                            if (brandKit) {
                                brandKit.scrollIntoView({ behavior: 'instant', block: 'center' });
                            }
                        }, 500);

                        const toast = document.getElementById('srSocialToast');
                        if (toast) {
                            toast.classList.add('is-visible');
                        }
                    })()
                `
            }
        ];

        for (const target of targets) {
            console.log(`Navigating to: ${target.url}...`);
            await call('Page.navigate', { url: target.url });
            await new Promise(r => setTimeout(r, target.waitMs));

            if (target.action) {
                await call('Runtime.evaluate', { expression: target.action });
                await new Promise(r => setTimeout(r, 1200));
            }

            const shot = await call('Page.captureScreenshot', { format: 'png' });
            const outPath = path.join(brainDir, target.name);
            fs.writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
            console.log(`✓ Captured ${target.name} (${fs.statSync(outPath).size} bytes)`);
        }

    } catch (err) {
        console.error('Error during capture:', err);
    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

captureAll();
