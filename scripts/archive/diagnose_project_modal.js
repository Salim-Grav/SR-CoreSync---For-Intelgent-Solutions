const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = path.join(process.env.TEMP, 'edge_diag_' + Date.now());
const port = 9444;

console.log('Starting Edge headless...');
const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://localhost:8000/index.html'
]);

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getWsUrl() {
    for (let i = 0; i < 20; i++) {
        await wait(500);
        try {
            const data = await new Promise((resolve, reject) => {
                http.get(`http://127.0.0.1:${port}/json`, res => {
                    let d = '';
                    res.on('data', c => d += c);
                    res.on('end', () => resolve(d));
                }).on('error', reject);
            });
            const pages = JSON.parse(data);
            const page = pages.find(p => p.url && p.url.includes('localhost:8000'));
            if (page && page.webSocketDebuggerUrl) {
                return page.webSocketDebuggerUrl;
            }
        } catch (e) {}
    }
    throw new Error('Could not find page in CDP list');
}

async function run() {
    try {
        const wsUrl = await getWsUrl();
        console.log('Connected to WS:', wsUrl);

        const ws = new WebSocket(wsUrl);
        let msgId = 1;
        const pending = new Map();

        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.id && pending.has(msg.id)) {
                pending.get(msg.id)(msg);
                pending.delete(msg.id);
            }
        };

        function send(method, params = {}) {
            return new Promise((resolve) => {
                const id = msgId++;
                pending.set(id, resolve);
                ws.send(JSON.stringify({ id, method, params }));
            });
        }

        await new Promise(r => ws.onopen = r);
        await send('Runtime.enable');
        await send('Page.enable');

        await wait(2000);

        console.log('Inspecting rules causing visibility hidden and opacity 0...');
        const cssRes = await send('Runtime.evaluate', {
            expression: `
            (function() {
                openCurrentProjectModal();

                const getMatched = (el) => {
                    const matched = [];
                    for (let sIdx = 0; sIdx < document.styleSheets.length; sIdx++) {
                        const sheet = document.styleSheets[sIdx];
                        try {
                            const rules = sheet.cssRules || [];
                            for (let rIdx = 0; rIdx < rules.length; rIdx++) {
                                const rule = rules[rIdx];
                                if (rule.selectorText && el.matches(rule.selectorText)) {
                                    matched.push({
                                        sheet: sheet.href ? sheet.href.split('/').pop() : 'inline-style-tag',
                                        selector: rule.selectorText,
                                        cssText: rule.cssText
                                    });
                                }
                            }
                        } catch(e) {}
                    }
                    return matched;
                };

                const details = document.querySelector('.project-modal__details');
                const media = document.querySelector('.project-modal__media');
                const closeBtn = document.querySelector('.project-modal__close');

                return JSON.stringify({
                    detailsRules: getMatched(details),
                    mediaRules: getMatched(media),
                    closeRules: getMatched(closeBtn)
                });
            })()
            `,
            returnByValue: true
        });

        console.log('CSS RULES:', JSON.stringify(JSON.parse(cssRes.result.value), null, 2));

        ws.close();
    } catch (err) {
        console.error('DIAG ERROR:', err);
    } finally {
        edge.kill();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e){}
    }
}

run();
