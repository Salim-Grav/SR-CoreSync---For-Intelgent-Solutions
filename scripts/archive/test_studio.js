const { spawn } = require('child_process');
const http = require('http');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = process.env.TEMP + '\\edge_studio_test_' + Date.now();
const port = 9562;

const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://localhost:8000/logo-studio.html'
]);

setTimeout(async () => {
    try {
        const pages = await new Promise((res, rej) => {
            http.get('http://127.0.0.1:' + port + '/json', r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => res(JSON.parse(d)));
            }).on('error', rej);
        });
        const page = pages.find(p => p.url && p.url.includes('logo-studio'));
        const ws = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise(r => ws.onopen = r);

        let id = 1;
        const call = (method, params = {}) => new Promise(res => {
            const curId = id++;
            const handler = (evt) => {
                const m = JSON.parse(evt.data);
                if (m.id === curId) {
                    ws.removeEventListener('message', handler);
                    res(m);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id: curId, method, params }));
        });

        await call('Runtime.enable');
        await call('Page.enable');

        const errors = [];
        ws.addEventListener('message', (evt) => {
            const m = JSON.parse(evt.data);
            if (m.method === 'Runtime.exceptionThrown') {
                errors.push(m.params);
            }
        });

        await new Promise(r => setTimeout(r, 2000));

        console.log('Errors on logo-studio.html:', JSON.stringify(errors, null, 2));
        edge.kill();
    } catch(e) {
        console.error(e);
        edge.kill();
    }
}, 3000);
