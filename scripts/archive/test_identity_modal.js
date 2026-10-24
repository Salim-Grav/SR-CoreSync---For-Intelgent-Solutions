const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = process.env.TEMP + '\\edge_identity_test_' + Date.now();
const port = 9559;

const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://localhost:8000/index.html'
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

        await new Promise(r => setTimeout(r, 2000));

        // Listen for console errors
        ws.addEventListener('message', (evt) => {
            const m = JSON.parse(evt.data);
            if (m.method === 'Runtime.consoleAPICalled' || m.method === 'Runtime.exceptionThrown') {
                console.log('BROWSER EVENT:', JSON.stringify(m));
            }
        });

        // 1. Switch to Identity tab (الهويات والشعارات)
        const switchRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const btn = document.getElementById('tab-btn-identity');
                if (btn) {
                    btn.click();
                    return { clickedIdentityTab: true };
                }
                return { clickedIdentityTab: false };
            })()
            `,
            returnByValue: true
        });
        console.log('Switch to identity result:', switchRes.result.value);

        await new Promise(r => setTimeout(r, 1000));

        // 2. Click the preview trigger
        const clickRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const trigger = document.getElementById('work-main-card-trigger');
                if (trigger) {
                    trigger.click();
                    return { clickedTrigger: true };
                }
                return { clickedTrigger: false };
            })()
            `,
            returnByValue: true
        });
        console.log('Click trigger result:', clickRes.result.value);

        await new Promise(r => setTimeout(r, 1500));

        // 3. Inspect Modal state
        const inspectRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const modal = document.getElementById('projectModal');
                const title = document.getElementById('projectModalTitle');
                const gallery = document.getElementById('projectModalGallery');
                const imgs = gallery ? Array.from(gallery.querySelectorAll('img')).map(i => ({ src: i.src, naturalWidth: i.naturalWidth, display: window.getComputedStyle(i).display, opacity: window.getComputedStyle(i).opacity })) : [];
                return {
                    modalClass: modal ? modal.className : null,
                    modalDisplay: modal ? window.getComputedStyle(modal).display : null,
                    modalOpacity: modal ? window.getComputedStyle(modal).opacity : null,
                    modalVisibility: modal ? window.getComputedStyle(modal).visibility : null,
                    title: title ? title.textContent : null,
                    imgsCount: imgs.length,
                    imgs: imgs
                };
            })()
            `,
            returnByValue: true
        });
        console.log('Inspect result:', JSON.stringify(inspectRes.result.value, null, 2));

        const screenshotRes = await call('Page.captureScreenshot', { format: 'png' });
        const screenshotPath = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_identity_modal_test.png';
        fs.writeFileSync(screenshotPath, Buffer.from(screenshotRes.result.data, 'base64'));
        console.log('Saved screenshot to:', screenshotPath);

        edge.kill();
    } catch(e) {
        console.error(e);
        edge.kill();
    }
}, 3000);
