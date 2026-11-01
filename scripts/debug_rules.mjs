import { spawn } from 'node:child_process';
import http from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';

const PORT = 8115;
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

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
    const filepath = join(process.cwd(), p);
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
        '--remote-debugging-port=9228',
        '--no-sandbox',
        '--disable-gpu',
        '--user-data-dir=' + join(process.cwd(), '.chrome-test-profile-5')
    ]);

    await sleep(2500);

    try {
        const listRes = await fetch('http://127.0.0.1:9228/json/list');
        const list = await listRes.json();
        const page = list.find(t => t.type === 'page') || list[0];
        const ws = new globalThis.WebSocket(page.webSocketDebuggerUrl);

        ws.onopen = async () => {
            let id = 1;
            function send(method, params = {}) {
                const curId = id++;
                ws.send(JSON.stringify({ id: curId, method, params }));
                return curId;
            }

            send('Runtime.enable');
            send('Console.enable');

            ws.onmessage = async (evt) => {
                const msg = JSON.parse(evt.data);
                if (msg.params && msg.params.exceptionDetails) {
                    console.error('[EXCEPTION DETAILS]', msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
                }
                if (msg.result && msg.result.result) {
                    console.log('[DEBUG RESULT]', JSON.stringify(msg.result.result.value || msg.result.result, null, 2));
                }
            };

            send('Page.navigate', { url: `http://127.0.0.1:${PORT}/index.html` });
            await sleep(4000);

            send('Runtime.evaluate', {
                expression: `
                try {
                    const btn = document.getElementById('floatingFollowChatBtn');
                    btn.click();
                    const win = document.getElementById('sr-agent-window');
                    ({
                        linkTagExists: Boolean(document.querySelector('link[href*="sr-agent-widget.css"]')),
                        winClassName: win ? win.className : null,
                        computedOpacity: win ? window.getComputedStyle(win).opacity : null,
                        computedVisibility: win ? window.getComputedStyle(win).visibility : null,
                        computedDisplay: win ? window.getComputedStyle(win).display : null,
                        computedZIndex: win ? window.getComputedStyle(win).zIndex : null
                    });
                } catch(e) {
                    ({ error: e.message, stack: e.stack });
                }
                `,
                returnByValue: true
            });

            await sleep(3000);
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
