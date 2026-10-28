/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

const { spawn } = require('child_process');
const http = require('http');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = process.env.TEMP + '\\edge_all_identity_' + Date.now();
const port = 9561;

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

        // Switch to identity
        await call('Runtime.evaluate', { expression: `switchWorkTab('identity')` });
        await new Promise(r => setTimeout(r, 500));

        // Test each of the 4 projects
        const testRes = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const results = [];
                const projects = projectsDB['identity'];
                for (let i = 0; i < projects.length; i++) {
                    currentWorkProjectIdx = i;
                    renderActiveWork();
                    openCurrentProjectModal();
                    const modal = document.getElementById('projectModal');
                    const title = document.getElementById('projectModalTitle').textContent;
                    const imgs = document.querySelectorAll('.project-gallery-item img');
                    results.push({
                        idx: i,
                        id: projects[i].id,
                        titleSet: title,
                        isActive: modal.classList.contains('active'),
                        isOpen: modal.classList.contains('is-open'),
                        imagesCount: imgs.length,
                        firstImgSrc: imgs[0] ? imgs[0].src : null
                    });
                    closeProjectModal();
                }
                return results;
            })()
            `,
            returnByValue: true
        });

        console.log('RESULTS ARABIC:', JSON.stringify(testRes.result.value, null, 2));

        // Now test on NL
        await call('Page.navigate', { url: 'http://localhost:8000/nl/index.html' });
        await new Promise(r => setTimeout(r, 2000));

        await call('Runtime.evaluate', { expression: `switchWorkTab('identity')` });
        await new Promise(r => setTimeout(r, 500));

        const testResNL = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const results = [];
                const projects = projectsDB['identity'];
                for (let i = 0; i < projects.length; i++) {
                    currentWorkProjectIdx = i;
                    renderActiveWork();
                    openCurrentProjectModal();
                    const modal = document.getElementById('projectModal');
                    const title = document.getElementById('projectModalTitle').textContent;
                    const imgs = document.querySelectorAll('.project-gallery-item img');
                    results.push({
                        idx: i,
                        id: projects[i].id,
                        titleSet: title,
                        isActive: modal.classList.contains('active'),
                        isOpen: modal.classList.contains('is-open'),
                        imagesCount: imgs.length,
                        firstImgSrc: imgs[0] ? imgs[0].src : null
                    });
                    closeProjectModal();
                }
                return results;
            })()
            `,
            returnByValue: true
        });

        console.log('RESULTS DUTCH:', JSON.stringify(testResNL.result.value, null, 2));

        edge.kill();
    } catch(e) {
        console.error(e);
        edge.kill();
    }
}, 3000);
