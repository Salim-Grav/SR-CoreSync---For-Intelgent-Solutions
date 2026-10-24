const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = process.env.TEMP + '\\edge_verify_' + Date.now();
const port = 9557;

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

        // Click on the laptop trigger directly
        const clickRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const trigger = document.getElementById('work-main-card-trigger');
                if (trigger) {
                    trigger.click();
                    return { clicked: true };
                }
                return { clicked: false, err: 'trigger not found' };
            })()
            `,
            returnByValue: true
        });

        console.log('Trigger click result:', clickRes.result.value);

        await new Promise(r => setTimeout(r, 1200));

        // Inspect state
        const stateRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const modal = document.getElementById('projectModal');
                const panel = document.querySelector('.project-modal__panel');
                const details = document.querySelector('.project-modal__details');
                const media = document.querySelector('.project-modal__media');
                const galleryImgs = Array.from(document.querySelectorAll('.project-gallery-item img'));
                const closeBtn = document.querySelector('.project-modal__close');
                const expandBtn = document.getElementById('projectModalExpandBtn');

                return {
                    modalClass: modal ? modal.className : null,
                    modalVisible: modal ? (window.getComputedStyle(modal).display !== 'none' && window.getComputedStyle(modal).opacity === '1') : false,
                    detailsVisible: details ? (window.getComputedStyle(details).visibility === 'visible' && window.getComputedStyle(details).opacity === '1') : false,
                    mediaVisible: media ? (window.getComputedStyle(media).visibility === 'visible' && window.getComputedStyle(media).opacity === '1') : false,
                    closeBtnVisible: closeBtn ? (window.getComputedStyle(closeBtn).visibility === 'visible' && window.getComputedStyle(closeBtn).opacity === '1') : false,
                    expandBtnVisible: expandBtn ? (window.getComputedStyle(expandBtn).visibility === 'visible') : false,
                    galleryImagesCount: galleryImgs.length,
                    galleryImagesLoaded: galleryImgs.map(img => ({ src: img.src, naturalWidth: img.naturalWidth, opacity: window.getComputedStyle(img).opacity }))
                };
            })()
            `,
            returnByValue: true
        });

        console.log('VERIFIED STATE:', JSON.stringify(stateRes.result.value, null, 2));

        const screenshotRes = await call('Page.captureScreenshot', { format: 'png' });
        const screenshotPath = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_project_modal_verified.png';
        fs.writeFileSync(screenshotPath, Buffer.from(screenshotRes.result.data, 'base64'));
        console.log('Saved verified screenshot to:', screenshotPath);

        edge.kill();
    } catch(e) {
        console.error(e);
        edge.kill();
    }
}, 3000);
