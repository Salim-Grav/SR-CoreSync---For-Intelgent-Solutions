const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = process.env.TEMP + '\\edge_test_' + Date.now();
const port = 9556;

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

        await call('Runtime.evaluate', {
            expression: `
            (function() {
                openCurrentProjectModal();
                const modal = document.getElementById('projectModal');
                modal.classList.add('is-open');
                
                // Also add robust CSS override
                const s = document.createElement('style');
                s.textContent = \`
                    .project-modal.active, .project-modal.is-open {
                        top: 0 !important;
                        opacity: 1 !important;
                        visibility: visible !important;
                        display: block !important;
                    }
                    .project-modal.active .project-modal__close,
                    .project-modal.active .project-modal__media,
                    .project-modal.active .project-modal__details,
                    .project-modal.is-open .project-modal__close,
                    .project-modal.is-open .project-modal__media,
                    .project-modal.is-open .project-modal__details {
                        opacity: 1 !important;
                        visibility: visible !important;
                        transform: none !important;
                    }
                    .project-gallery-item img {
                        opacity: 1 !important;
                        visibility: visible !important;
                        display: block !important;
                        width: 100% !important;
                        height: auto !important;
                        border-radius: 16px;
                    }
                \`;
                document.head.appendChild(s);
            })()
            `
        });

        await new Promise(r => setTimeout(r, 1200));

        const screenshotRes = await call('Page.captureScreenshot', { format: 'png' });
        const screenshotPath = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_project_modal_fixed_test.png';
        fs.writeFileSync(screenshotPath, Buffer.from(screenshotRes.result.data, 'base64'));
        console.log('Saved fixed screenshot to:', screenshotPath);

        edge.kill();
    } catch(e) {
        console.error(e);
        edge.kill();
    }
}, 3000);
