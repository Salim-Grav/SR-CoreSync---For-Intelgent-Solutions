const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const projectDir = path.resolve(__dirname, '..');
const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\17be0c82-0a87-4d01-bb34-f04959091305';

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

async function verifyAndCapture() {
    const srvPort = 9595;
    const server = await startServer(srvPort);
    const dbgPort = 9893;
    const userDataDir = path.join(process.env.TEMP, 'edge_zoom_' + Date.now());

    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + dbgPort,
        '--user-data-dir=' + userDataDir,
        '--window-size=390,844',
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
            width: 390,
            height: 844,
            deviceScaleFactor: 2,
            mobile: true
        });

        // Hide GDPR banner for clean snapshots
        await call('Runtime.evaluate', {
            expression: `
                const b = document.getElementById('esGdprBanner');
                if (b) { b.classList.remove('active'); b.style.display = 'none'; }
            `
        });

        console.log('Testing font zooming at 125% on 390px mobile...');
        await call('Runtime.evaluate', {
            expression: `window.srApplyFontSize(125, true);`
        });
        await new Promise(r => setTimeout(r, 800));

        // 1. Capture Hero scaled at 125%
        const heroSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_mobile_scaled_125.png'), Buffer.from(heroSS.result.data, 'base64'));
        console.log('Saved: live_mobile_scaled_125.png');

        // Check horizontal scroll at 125%
        const scrollCheck = await call('Runtime.evaluate', {
            expression: `
                ({
                    winW: window.innerWidth,
                    docW: document.documentElement.scrollWidth,
                    hasScroll: document.documentElement.scrollWidth > window.innerWidth + 1
                })
            `,
            returnByValue: true
        });
        console.log('Scroll check at 125% zoom:', scrollCheck.result?.value);

        // 2. Open Mobile Offcanvas Menu to show the resizer box inside the drawer
        console.log('Opening offcanvas mobile menu...');
        await call('Runtime.evaluate', {
            expression: `
                const m = document.getElementById('mobileMenu');
                if (m) {
                    m.classList.add('active');
                    m.scrollTop = m.scrollHeight; // scroll to bottom where resizer is
                }
            `
        });
        await new Promise(r => setTimeout(r, 800));
        const menuSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_mobile_menu_resizer.png'), Buffer.from(menuSS.result.data, 'base64'));
        console.log('Saved: live_mobile_menu_resizer.png');

        // Close mobile menu completely
        await call('Runtime.evaluate', {
            expression: `
                const m = document.getElementById('mobileMenu');
                if (m) {
                    m.classList.remove('active');
                    m.style.display = 'none';
                }
            `
        });
        await new Promise(r => setTimeout(r, 600));

        // 3. Scroll to Footer to show the footer accessibility text resizer
        console.log('Scrolling to footer bottom bar...');
        await call('Runtime.evaluate', {
            expression: `
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'instant' });
            `
        });
        await new Promise(r => setTimeout(r, 800));
        const footerSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_footer_accessibility_resizer.png'), Buffer.from(footerSS.result.data, 'base64'));
        console.log('Saved: live_footer_accessibility_resizer.png');

        console.log('\nAll accessibility snapshots captured successfully!');

    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

verifyAndCapture();
