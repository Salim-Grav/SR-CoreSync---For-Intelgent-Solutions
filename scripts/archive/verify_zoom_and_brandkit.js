const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

async function testZoomAndBrandKit() {
    const port = Math.floor(Math.random() * 1000) + 9860;
    const userDataDir = process.env.TEMP + '\\edge_zoom_test_' + port;
    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=' + port,
        '--user-data-dir=' + userDataDir,
        '--window-size=1440,960',
        'http://localhost:8000/index.html'
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

        // 1. Switch to Identity tab and open SARLOR modal
        const openResult = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const tab = document.getElementById('tab-btn-identity');
                if (tab) tab.click();
                
                // Open current project modal
                if (typeof openCurrentProjectModal === 'function') {
                    openCurrentProjectModal();
                } else if (typeof openProjectModal === 'function') {
                    openProjectModal('sarlor');
                }
                
                const modal = document.getElementById('projectModal');
                const brandKit = document.getElementById('projectModalBrandKit');
                return {
                    modalActive: modal ? modal.classList.contains('active') : false,
                    brandKitVisible: brandKit ? getComputedStyle(brandKit).display : 'none',
                    galleryCount: document.querySelectorAll('.project-gallery-item').length
                };
            })()
            `,
            returnByValue: true
        });

        console.log('Project Modal State:', openResult.result.value);
        await new Promise(r => setTimeout(r, 1200));

        // Capture Project Modal with Brand Kit widget
        const shotModal = await call('Page.captureScreenshot', { format: 'png' });
        const modalPath = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_project_modal_brandkit.png';
        fs.writeFileSync(modalPath, Buffer.from(shotModal.result.data, 'base64'));
        console.log('Saved project modal snapshot to:', modalPath);

        // 2. Click the first gallery item to open 4K Zoom & Pan Inspector
        const zoomResult = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const firstItem = document.querySelector('.project-gallery-item');
                if (firstItem) {
                    firstItem.click();
                } else if (typeof openImageZoom === 'function') {
                    openImageZoom('./assets/work-3.webp', 'SARLOR • فحص تفاصيل الشعار والعرض بدقة 4K');
                }
                // Zoom in twice for 4K magnification
                if (typeof zoomIn === 'function') {
                    zoomIn(0.6);
                    zoomIn(0.4);
                }
                const zoomModal = document.getElementById('srImageZoomModal');
                return {
                    zoomActive: zoomModal ? zoomModal.classList.contains('active') : false,
                    levelText: document.getElementById('srZoomLevelText') ? document.getElementById('srZoomLevelText').textContent : ''
                };
            })()
            `,
            returnByValue: true
        });

        console.log('Zoom Inspector State:', zoomResult.result.value);
        await new Promise(r => setTimeout(r, 1200));

        // Capture 4K Zoom Inspector
        const shotZoom = await call('Page.captureScreenshot', { format: 'png' });
        const zoomPath = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\1778519a-9b5a-4358-b8ed-35a118f691af\\live_4k_zoom_inspector.png';
        fs.writeFileSync(zoomPath, Buffer.from(shotZoom.result.data, 'base64'));
        console.log('Saved 4K zoom snapshot to:', zoomPath);

    } catch (e) {
        console.error(e);
    } finally {
        edge.kill();
        try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }
}

testZoomAndBrandKit();
