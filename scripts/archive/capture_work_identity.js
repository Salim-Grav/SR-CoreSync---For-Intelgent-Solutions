const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

async function testWorkSection(url, outShot) {
    const port = Math.floor(Math.random() * 1000) + 9850;
    const userDataDir = process.env.TEMP + '\\edge_work_sec_' + port;
    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + port,
        '--user-data-dir=' + userDataDir,
        '--window-size=1440,960',
        url
    ]);

    try {
        await new Promise(r => setTimeout(r, 2200));
        const pages = await new Promise((res, rej) => {
            http.get('http://127.0.0.1:' + port + '/json', r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => res(JSON.parse(d)));
            }).on('error', rej);
        });
        const page = pages.find(p => p.url && p.url.includes('localhost:8000'));
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

        await new Promise(r => setTimeout(r, 1500));

        // Switch to identity
        await call('Runtime.evaluate', {
            expression: `
            (function() {
                const btn = document.getElementById('tab-btn-identity');
                if (btn) btn.click();
                const workSec = document.getElementById('work');
                if (workSec) workSec.scrollIntoView({ behavior: 'instant', block: 'start' });
            })()
            `
        });

        await new Promise(r => setTimeout(r, 1000));

        const shot = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(outShot, Buffer.from(shot.result.data, 'base64'));
        console.log('Saved work snapshot to:', outShot);

    } catch(e) {
        console.error(e);
    } finally {
        edge.kill();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e){}
    }
}

async function run() {
    await testWorkSection('http://localhost:8000/index.html', 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_work_identity_ar.png');
    await testWorkSection('http://localhost:8000/nl/index.html', 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_work_identity_nl.png');
}

run();
