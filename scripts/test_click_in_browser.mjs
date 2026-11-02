import { spawn } from 'node:child_process';
import http from 'node:http';
import { readFileSync, writeFileSync, existsSync, statSync, rmSync } from 'node:fs';
import { join, extname } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';

const PORT = 8099;
const CHROME_PATH = process.env.SR_BROWSER || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const MIME = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.woff2': 'font/woff2',
    '.vcf': 'text/vcard'
};

const server = http.createServer((req, res) => {
    let p = req.url.split('?')[0];
    if (p === '/') p = '/index.html';
    const filepath = join(process.cwd(), '_site', p);
    if (existsSync(filepath) && statSync(filepath).isFile()) {
        const ext = extname(filepath).toLowerCase();
        res.writeHead(200, {
            'Content-Type': MIME[ext] || 'application/octet-stream',
            'Cache-Control': 'no-store, no-cache, must-revalidate'
        });
        res.end(readFileSync(filepath));
    } else {
        res.writeHead(404);
        res.end('Not found: ' + req.url);
    }
});

const profileDir = join(process.cwd(), '.chrome-audit-fresh');
if (existsSync(profileDir)) {
    try { rmSync(profileDir, { recursive: true, force: true }); } catch(e) {}
}

server.listen(PORT, async () => {
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        '--remote-debugging-port=9232',
        '--no-sandbox',
        '--disable-gpu',
        '--disk-cache-size=1',
        '--media-cache-size=1',
        '--disable-application-cache',
        '--user-data-dir=' + profileDir
    ]);

    await sleep(2500);

    try {
        const listRes = await fetch('http://127.0.0.1:9232/json/list');
        const list = await listRes.json();
        const page = list.find(t => t.type === 'page') || list[0];
        const ws = new globalThis.WebSocket(page.webSocketDebuggerUrl);

        ws.onopen = async () => {
            let id = 1;
            function send(method, params = {}) {
                return new Promise((resolve) => {
                    const curId = id++;
                    const handler = (evt) => {
                        const m = JSON.parse(evt.data);
                        if (m.id === curId) {
                            ws.removeEventListener('message', handler);
                            resolve(m.result);
                        }
                    };
                    ws.addEventListener('message', handler);
                    ws.send(JSON.stringify({ id: curId, method, params }));
                });
            }

            await send('Runtime.enable');
            await send('Page.enable');
            await send('Network.enable');
            await send('Network.clearBrowserCache');
            await send('Emulation.setDeviceMetricsOverride', {
                width: 1366,
                height: 768,
                deviceScaleFactor: 1,
                mobile: false
            });
            await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/index.html?lang=ar&noredirect=1&ts=${Date.now()}` });

            for (let i = 0; i < 20; i++) {
                await sleep(300);
                const r = await send('Runtime.evaluate', { expression: 'document.readyState', returnByValue: true });
                if (r && r.result && r.result.value === 'complete') break;
            }
            await sleep(2000);

            // Measure title lines and emblem geometry
            const geoRes = await send('Runtime.evaluate', {
                expression: `
                (function() {
                    const emblem = document.querySelector('.hero-emblem-card-3d');
                    const emblemRect = emblem.getBoundingClientRect();
                    const lines = Array.from(document.querySelectorAll('.hero-reference__title .hero-title-line__text')).map(el => {
                        const r = el.getBoundingClientRect();
                        return {
                            text: el.innerText,
                            left: r.left,
                            right: r.right,
                            width: r.width,
                            collidesWithEmblem: r.left < emblemRect.right
                        };
                    });

                    const heroActions = document.querySelector('.hero-reference__actions');
                    const heroActionBtns = Array.from(heroActions ? heroActions.querySelectorAll('.tf-btn') : []).map(b => ({
                        text: b.innerText.trim(),
                        className: b.className,
                        width: b.getBoundingClientRect().width,
                        height: b.getBoundingClientRect().height
                    }));

                    const headerAgentBtn = document.querySelector('.btn-partner-portal-header');

                    return {
                        emblem: {
                            left: emblemRect.left,
                            right: emblemRect.right,
                            width: emblemRect.width
                        },
                        lines: lines,
                        heroActionBtns: heroActionBtns,
                        headerAgentBtnExists: !!headerAgentBtn
                    };
                })()
                `,
                returnByValue: true
            });

            console.log('GEOMETRY & BUTTONS INSPECTION:', JSON.stringify(geoRes.result.value, null, 2));

            // Test opening Header Support Dropdown
            const testDropdownRes = await send("Runtime.evaluate", {
                expression: `
                (function() {
                    const btn = document.getElementById("headerSupportBtn");
                    const wrap = document.getElementById("headerSupportDropdownWrap");
                    const menu = document.getElementById("headerSupportMenu");
                    if (!btn || !wrap || !menu) return { success: false, reason: "elements missing", btn: !!btn, wrap: !!wrap, menu: !!menu };

                    btn.click();
                    const menuRect = menu.getBoundingClientRect();
                    const style = window.getComputedStyle(menu);
                    return {
                        success: true,
                        hasActive: wrap.classList.contains("is-active"),
                        display: style.display,
                        opacity: style.opacity,
                        rect: {
                            left: menuRect.left,
                            right: menuRect.right,
                            top: menuRect.top,
                            bottom: menuRect.bottom,
                            width: menuRect.width,
                            height: menuRect.height
                        },
                        clippedLeft: menuRect.left < 0,
                        clippedRight: menuRect.right > window.innerWidth,
                        itemsCount: menu.querySelectorAll(".support-menu-item").length
                    };
                })()
                `,
                returnByValue: true
            });
            console.log("HEADER SUPPORT DROPDOWN TEST:", JSON.stringify(testDropdownRes.result.value, null, 2));
            await sleep(500);

            const screenshotRes = await send('Page.captureScreenshot', {
                format: 'jpeg',
                quality: 85
            });

            if (screenshotRes && screenshotRes.data) {
                const buf = Buffer.from(screenshotRes.data, 'base64');
                const outPath = 'C:\\Users\\msali\\.gemini\\antigravity\\brain\\bf4ab143-8aba-421c-91f9-24d1a1f376a3\\live_terminal_snapshot.jpg';
                writeFileSync(outPath, buf);
                console.log('LIVE SCREENSHOT SAVED TO:', outPath);
            }

            await sleep(1000);
            chrome.kill();
            server.close();
            process.exit(0);
        };
    } catch(e) {
        console.error(e);
        chrome.kill();
        server.close();
        process.exit(1);
    }
});
