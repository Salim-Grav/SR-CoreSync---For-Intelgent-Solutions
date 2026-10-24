const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

async function testPage(url, outShot, pageName) {
    const port = Math.floor(Math.random() * 1000) + 9800;
    const userDataDir = process.env.TEMP + '\\edge_verify_' + port;
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

        // 1. Switch to identity
        const switchRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const btn = document.getElementById('tab-btn-identity');
                if (btn) btn.click();
                return { hasBtn: !!btn };
            })()
            `,
            returnByValue: true
        });

        await new Promise(r => setTimeout(r, 800));

        // 2. Click preview button or trigger
        const clickRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const previewBtn = document.getElementById('work-live-preview-btn');
                const trigger = document.getElementById('work-main-card-trigger');
                if (previewBtn && previewBtn.style.display !== 'none') {
                    previewBtn.click();
                    return { clicked: 'previewBtn', text: previewBtn.textContent.trim() };
                }
                if (trigger) {
                    trigger.click();
                    return { clicked: 'trigger' };
                }
                return { clicked: false };
            })()
            `,
            returnByValue: true
        });

        await new Promise(r => setTimeout(r, 1200));

        // 3. Inspect modal
        const modalRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const modal = document.getElementById('projectModal');
                const title = document.getElementById('projectModalTitle');
                const gallery = document.getElementById('projectModalGallery');
                const imgs = gallery ? Array.from(gallery.querySelectorAll('img')).map(i => i.src) : [];
                return {
                    modalExists: !!modal,
                    modalActive: modal ? modal.classList.contains('active') : false,
                    title: title ? title.textContent : null,
                    imgsCount: imgs.length,
                    firstImg: imgs[0] || null
                };
            })()
            `,
            returnByValue: true
        });

        console.log(pageName, 'Modal Inspection:', JSON.stringify(modalRes.result ? modalRes.result.value : modalRes, null, 2));

        const shot = await call('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(outShot, Buffer.from(shot.result.data, 'base64'));
        console.log(pageName, 'Saved snapshot to:', outShot);

    } catch(e) {
        console.error(pageName, e);
    } finally {
        edge.kill();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e){}
    }
}

async function main() {
    await testPage(
        'http://localhost:8000/work.html',
        'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_preview_work_identity.png',
        'PREVIEW-WORK'
    );
    await testPage(
        'http://localhost:8000/index.html',
        'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_index_identity.png',
        'INDEX-AR'
    );
    await testPage(
        'http://localhost:8000/nl/index.html',
        'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_nl_identity.png',
        'INDEX-NL'
    );
}

main();
