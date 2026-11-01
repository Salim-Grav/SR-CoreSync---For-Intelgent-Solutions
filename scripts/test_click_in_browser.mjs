import { spawn } from 'node:child_process';
import http from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
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
        res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
        res.end(readFileSync(filepath));
    } else {
        res.writeHead(404);
        res.end('Not found: ' + req.url);
    }
});

server.listen(PORT, async () => {
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        '--remote-debugging-port=9231',
        '--no-sandbox',
        '--disable-gpu',
        '--user-data-dir=' + join(process.cwd(), '.chrome-audit-profile-2')
    ]);

    await sleep(2500);

    try {
        const listRes = await fetch('http://127.0.0.1:9231/json/list');
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
            await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/index.html` });

            for (let i = 0; i < 20; i++) {
                await sleep(300);
                const r = await send('Runtime.evaluate', { expression: 'document.readyState', returnByValue: true });
                if (r && r.result && r.result.value === 'complete') break;
            }
            await sleep(1500);

            // Click button
            const clickRes = await send('Runtime.evaluate', {
                expression: `
                (function() {
                    const btn = document.getElementById('floatingFollowChatBtn');
                    btn.click();
                    const win = document.getElementById('sr-agent-window');
                    
                    // Let's inspect all style sheets matching win
                    let matchedRules = [];
                    for (const sheet of document.styleSheets) {
                        try {
                            for (const rule of sheet.cssRules || []) {
                                if (rule.selectorText && (rule.selectorText.includes('sr-agent-window') || rule.selectorText.includes('sr-open'))) {
                                    matchedRules.push({
                                        sheet: sheet.href ? sheet.href.split('/').pop() : 'inline',
                                        selector: rule.selectorText,
                                        cssText: rule.cssText
                                    });
                                }
                            }
                        } catch(e) {}
                    }

                    return {
                        classList: win.className,
                        matchedRules: matchedRules,
                        computedOpacity: window.getComputedStyle(win).opacity,
                        computedVisibility: window.getComputedStyle(win).visibility
                    };
                })()
                `,
                returnByValue: true
            });

            console.log('CLICK RESULT INSPECTION:', JSON.stringify(clickRes.result.value, null, 2));

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
