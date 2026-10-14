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

async function verifyAll() {
    const srvPort = 9580;
    const server = await startServer(srvPort);
    const dbgPort = 9891;
    const userDataDir = path.join(process.env.TEMP, 'edge_multi_' + Date.now());

    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + dbgPort,
        '--user-data-dir=' + userDataDir,
        '--window-size=1920,1080',
        `http://127.0.0.1:${srvPort}/index.html`
    ]);

    const viewports = [
        { name: 'Ultra-Narrow Phone Portrait (320px)', width: 320, height: 640, mobile: true },
        { name: 'Samsung Galaxy Portrait (360px)', width: 360, height: 800, mobile: true },
        { name: 'iPhone 15 Pro Portrait (393px)', width: 393, height: 852, mobile: true },
        { name: 'iPhone Max Portrait (428px)', width: 428, height: 926, mobile: true },
        { name: 'Mobile Landscape (844px)', width: 844, height: 390, mobile: true },
        { name: 'iPad Portrait (768px)', width: 768, height: 1024, mobile: true },
        { name: 'iPad Landscape (1024px)', width: 1024, height: 768, mobile: false },
        { name: 'Desktop Full HD (1920px)', width: 1920, height: 1080, mobile: false },
        { name: 'Large 4K UHD TV Display (3840px)', width: 3840, height: 2160, mobile: false }
    ];

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

        const results = [];

        for (const vp of viewports) {
            await call('Emulation.setDeviceMetricsOverride', {
                width: vp.width,
                height: vp.height,
                deviceScaleFactor: vp.width > 2000 ? 1 : 2,
                mobile: vp.mobile
            });

            await new Promise(r => setTimeout(r, 800));

            const evalRes = await call('Runtime.evaluate', {
                expression: `
                (function() {
                    const winW = window.innerWidth;
                    const docW = document.documentElement.scrollWidth;
                    const bodyW = document.body.scrollWidth;
                    const hasPageHScroll = docW > winW + 1 || bodyW > winW + 1;

                    let overflowCount = 0;
                    const overflows = [];

                    document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, a, button, li, label, .tf-btn, .tf-btn-tab').forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;
                        if (el.closest('.brand-marquee') || el.closest('.tech-marquee') || el.closest('.marquee')) return;

                        const r = el.getBoundingClientRect();
                        const isOutRight = r.right > winW + 2;
                        const isOutLeft = r.left < -2;
                        const isHorizClipped = (el.scrollWidth - el.clientWidth > 4) && (style.overflow === 'hidden' || style.overflowX === 'hidden');
                        const isVertClipped = (el.scrollHeight - el.clientHeight > 6) && (style.overflow === 'hidden' || style.overflowY === 'hidden') && (style.maxHeight !== 'none' || (style.height && style.height.includes('px')));

                        const text = (el.innerText || '').trim();
                        if (!text || text.length < 2) return;

                        if (isOutRight || isOutLeft || isHorizClipped || isVertClipped) {
                            overflowCount++;
                            if (overflows.length < 5) {
                                overflows.push({
                                    tag: el.tagName,
                                    cls: (el.className || '').slice(0, 30),
                                    id: el.id,
                                    isOutRight,
                                    isOutLeft,
                                    isHorizClipped,
                                    isVertClipped,
                                    rect: { l: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width) },
                                    text: text.slice(0, 40).replace(/\\s+/g, ' ')
                                });
                            }
                        }
                    });

                    return {
                        winW,
                        docW,
                        hasPageHScroll,
                        overflowCount,
                        overflows
                    };
                })()
                `,
                returnByValue: true
            });

            const data = evalRes.result?.result?.value || evalRes.result?.value;
            results.push({
                device: vp.name,
                width: vp.width,
                height: vp.height,
                hasPageHScroll: data?.hasPageHScroll,
                overflowCount: data?.overflowCount,
                sampleOverflows: data?.overflows
            });
        }

        console.log('=== MULTI-VIEWPORT VERIFICATION RESULTS ===');
        console.table(results.map(r => ({
            Device: r.device,
            Dimensions: `${r.width}x${r.height}`,
            'Horizontal Scroll': r.hasPageHScroll ? '❌ YES' : '✅ CLEAN',
            'Text Clipping Count': r.overflowCount === 0 ? '✅ 0' : `❌ ${r.overflowCount}`
        })));

        // Capture live mobile portrait screenshots for the final response
        console.log('\nCapturing live mobile portrait screenshots...');
        await call('Emulation.setDeviceMetricsOverride', {
            width: 390,
            height: 844,
            deviceScaleFactor: 2,
            mobile: true
        });
        await new Promise(r => setTimeout(r, 1000));

        // 1. Hero Mobile View
        const heroSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_mobile_hero_portrait.png'), Buffer.from(heroSS.result.data, 'base64'));
        console.log('Saved: live_mobile_hero_portrait.png');

        // 2. Work Section with 2x2 Tabs Mobile View
        await call('Runtime.evaluate', {
            expression: `document.getElementById('work').scrollIntoView({ behavior: 'instant', block: 'start' });`
        });
        await new Promise(r => setTimeout(r, 600));
        const workSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_mobile_work_tabs.png'), Buffer.from(workSS.result.data, 'base64'));
        console.log('Saved: live_mobile_work_tabs.png');

        // 3. Instant Project Estimator Mobile View
        await call('Runtime.evaluate', {
            expression: `document.getElementById('estimator-section')?.scrollIntoView({ behavior: 'instant', block: 'start' }) || document.getElementById('pricing')?.scrollIntoView({ behavior: 'instant', block: 'start' });`
        });
        await new Promise(r => setTimeout(r, 600));
        const estSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_mobile_estimator.png'), Buffer.from(estSS.result.data, 'base64'));
        console.log('Saved: live_mobile_estimator.png');

        // 4. Software Hub Section Mobile View
        await call('Runtime.evaluate', {
            expression: `document.getElementById('software-hub')?.scrollIntoView({ behavior: 'instant', block: 'start' });`
        });
        await new Promise(r => setTimeout(r, 600));
        const swSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_mobile_software_hub.png'), Buffer.from(swSS.result.data, 'base64'));
        console.log('Saved: live_mobile_software_hub.png');

        // 5. 4K Television View (3840x2160)
        console.log('\nCapturing 4K TV landscape screenshot...');
        await call('Emulation.setDeviceMetricsOverride', {
            width: 1920,
            height: 1080,
            deviceScaleFactor: 2,
            mobile: false
        });
        await call('Runtime.evaluate', {
            expression: `window.scrollTo({ top: 0, behavior: 'instant' });`
        });
        await new Promise(r => setTimeout(r, 800));
        const tvSS = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(artifactDir, 'live_desktop_4k_hero.png'), Buffer.from(tvSS.result.data, 'base64'));
        console.log('Saved: live_desktop_4k_hero.png');

        console.log('\nAll tests and snapshots completed successfully!');

    } finally {
        edge.kill();
        server.close();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

verifyAll();
