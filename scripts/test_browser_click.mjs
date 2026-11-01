import { spawn } from 'node:child_process';
import http from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';

const PORT = 8111;
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
    console.log(`Server listening on http://127.0.0.1:${PORT}`);
    const chrome = spawn(CHROME_PATH, [
        '--headless=new',
        '--remote-debugging-port=9223',
        '--no-sandbox',
        '--disable-gpu',
        '--user-data-dir=' + join(process.cwd(), '.chrome-test-profile'),
        `http://127.0.0.1:${PORT}/index.html`
    ]);

    await sleep(2500);

    try {
        const listRes = await fetch('http://127.0.0.1:9223/json/list');
        const list = await listRes.json();
        console.log('Pages in Chrome:', list.length);
        const page = list[0];
        if (!page) {
            console.error('No page found');
            process.exit(1);
        }

        const wsUrl = page.webSocketDebuggerUrl;
        console.log('Connecting to DevTools WS:', wsUrl);

        const WebSocket = (await import('ws')).default;
        const ws = new WebSocket(wsUrl);

        ws.on('open', () => {
            console.log('Connected to Chrome DevTools WebSocket!');
            
            let id = 1;
            function send(method, params = {}) {
                ws.send(JSON.stringify({ id: id++, method, params }));
            }

            send('Runtime.enable');
            send('Console.enable');

            ws.on('message', async (data) => {
                const msg = JSON.parse(data.toString());
                if (msg.method === 'Runtime.consoleAPICalled') {
                    console.log('[BROWSER CONSOLE]', msg.params.type, msg.params.args.map(a => a.value || a.description).join(' '));
                }
                if (msg.method === 'Runtime.exceptionThrown') {
                    console.error('[BROWSER EXCEPTION]', msg.params.exceptionDetails.text, msg.params.exceptionDetails.exception?.description);
                }
            });

            setTimeout(async () => {
                console.log('--- Testing in Browser ---');
                // Check if srAgentWidget is defined
                send('Runtime.evaluate', {
                    expression: `
                    JSON.stringify({
                        hasWidget: Boolean(window.srAgentWidget),
                        hasToggle: Boolean(window.toggleAiChat),
                        widgetContainer: Boolean(document.getElementById('sr-agent-widget-container')),
                        widgetWindow: Boolean(document.getElementById('sr-agent-window')),
                        followChatBtn: Boolean(document.getElementById('floatingFollowChatBtn'))
                    })
                    `,
                    returnByValue: true
                });

                await sleep(1000);

                // Simulate clicking floatingFollowChatBtn
                console.log('Simulating click on #floatingFollowChatBtn...');
                send('Runtime.evaluate', {
                    expression: `
                    (function() {
                        const btn = document.getElementById('floatingFollowChatBtn');
                        if (!btn) return 'BUTTON NOT FOUND';
                        btn.click();
                        const win = document.getElementById('sr-agent-window');
                        return {
                            clicked: true,
                            windowExists: Boolean(win),
                            windowClasses: win ? win.className : null,
                            windowStyle: win ? window.getComputedStyle(win).display : null,
                            windowOpacity: win ? window.getComputedStyle(win).opacity : null,
                            windowVisibility: win ? window.getComputedStyle(win).visibility : null,
                            windowZIndex: win ? window.getComputedStyle(win).zIndex : null,
                            windowBBox: win ? win.getBoundingClientRect() : null
                        };
                    })()
                    `,
                    returnByValue: true
                });

                await sleep(2000);
                chrome.kill();
                server.close();
                process.exit(0);
            }, 3000);
        });

        ws.on('error', (err) => {
            console.error('WS Error:', err);
            chrome.kill();
            server.close();
            process.exit(1);
        });

    } catch (e) {
        console.error('Test error:', e);
        chrome.kill();
        server.close();
        process.exit(1);
    }
});
