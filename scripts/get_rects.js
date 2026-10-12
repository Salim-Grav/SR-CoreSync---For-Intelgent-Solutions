const http = require('http');
const { spawn } = require('child_process');

const edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const proc = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--window-size=390,844',
    'http://127.0.0.1:3000/index.html'
]);

setTimeout(async () => {
    try {
        const getTargets = () => new Promise((res, rej) => {
            http.get('http://127.0.0.1:9222/json', r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => res(JSON.parse(d)));
            }).on('error', rej);
        });

        const targets = await getTargets();
        const page = targets.find(t => t.type === 'page');
        if (!page) {
            console.log('No page found');
            proc.kill();
            return;
        }

        // Connect to WebSocket using native node net or https?
        // Wait, CDP HTTP has /json/version or we can use WebSocket.
        // Node 22 has built-in WebSocket!
        const ws = new WebSocket(page.webSocketDebuggerUrl);
        ws.onopen = () => {
            ws.send(JSON.stringify({
                id: 1,
                method: "Runtime.evaluate",
                params: {
                    expression: `(() => {
                        const brand = document.querySelector('.header-col-brand');
                        const logo = document.querySelector('.brand-logo-site');
                        const emblem = document.querySelector('.brand-emblem-img');
                        const sr = document.querySelector('.brand-sr-text');
                        const sub = document.querySelector('.brand-sub-text');
                        return {
                            windowWidth: window.innerWidth,
                            brand: brand ? brand.getBoundingClientRect() : null,
                            logo: logo ? logo.getBoundingClientRect() : null,
                            emblem: emblem ? emblem.getBoundingClientRect() : null,
                            sr: sr ? sr.getBoundingClientRect() : null,
                            sub: sub ? sub.getBoundingClientRect() : null,
                            subComputed: sub ? {
                                display: getComputedStyle(sub).display,
                                visibility: getComputedStyle(sub).visibility,
                                opacity: getComputedStyle(sub).opacity,
                                color: getComputedStyle(sub).color,
                                width: getComputedStyle(sub).width
                            } : null
                        };
                    })()`,
                    returnByValue: true
                }
            }));
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.id === 1) {
                console.log('DOM_METRICS:', JSON.stringify(data.result.value, null, 2));
                ws.close();
                proc.kill();
            }
        };
    } catch (e) {
        console.error(e);
        proc.kill();
    }
}, 2500);
