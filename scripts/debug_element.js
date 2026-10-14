const { spawn } = require('child_process');
const http = require('http');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = process.env.TEMP + '\\edge_test_' + Date.now();
const port = 9555;

const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
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
        await call('DOM.enable');
        await call('CSS.enable');

        await call('Runtime.evaluate', { expression: 'openCurrentProjectModal()' });

        const res = await call('Runtime.evaluate', {
            expression: `
            (function() {
                const el = document.querySelector('.project-modal__details');
                const cs = window.getComputedStyle(el);
                
                // Also check if any element has animation or transition or inline style
                return {
                    opacity: cs.opacity,
                    visibility: cs.visibility,
                    classes: el.className,
                    inlineStyle: el.getAttribute('style'),
                    parentOpacity: window.getComputedStyle(el.parentElement).opacity,
                    parentVisibility: window.getComputedStyle(el.parentElement).visibility,
                    parentClass: el.parentElement.className,
                    grandParentOpacity: window.getComputedStyle(el.parentElement.parentElement).opacity,
                    grandParentVisibility: window.getComputedStyle(el.parentElement.parentElement).visibility,
                    grandParentClass: el.parentElement.parentElement.className,
                    // Check closeBtn
                    closeBtnInlineStyle: document.querySelector('.project-modal__close').getAttribute('style'),
                    closeBtnClass: document.querySelector('.project-modal__close').className,
                    closeBtnOpacity: window.getComputedStyle(document.querySelector('.project-modal__close')).opacity,
                    closeBtnVisibility: window.getComputedStyle(document.querySelector('.project-modal__close')).visibility
                };
            })()
            `,
            returnByValue: true
        });

        console.log('DETAILS STYLE INFO:', JSON.stringify(res.result.value, null, 2));

        // Now let's find matched CSS rules for .project-modal__details using CSS domain
        const doc = await call('DOM.getDocument');
        const node = await call('DOM.querySelector', { nodeId: doc.result.root.nodeId, selector: '.project-modal__details' });
        if (node && node.result && node.result.nodeId) {
            const matched = await call('CSS.getMatchedStylesForNode', { nodeId: node.result.nodeId });
            console.log('MATCHED CSS RULES:');
            for (const r of matched.result.matchedCSSRules || []) {
                const decls = r.rule.style.cssProperties.filter(p => ['opacity', 'visibility', 'display'].includes(p.name));
                if (decls.length) {
                    console.log('Rule:', r.rule.selectorList.text, decls.map(p => `${p.name}: ${p.value} (${p.important ? '!important' : ''})`));
                }
            }
        }

        // Also for .project-modal__close
        const closeNode = await call('DOM.querySelector', { nodeId: doc.result.root.nodeId, selector: '.project-modal__close' });
        if (closeNode && closeNode.result && closeNode.result.nodeId) {
            const matchedClose = await call('CSS.getMatchedStylesForNode', { nodeId: closeNode.result.nodeId });
            console.log('MATCHED CLOSE RULES:');
            for (const r of matchedClose.result.matchedCSSRules || []) {
                const decls = r.rule.style.cssProperties.filter(p => ['opacity', 'visibility', 'display'].includes(p.name));
                if (decls.length) {
                    console.log('Rule:', r.rule.selectorList.text, decls.map(p => `${p.name}: ${p.value} (${p.important ? '!important' : ''})`));
                }
            }
        }

        edge.kill();
    } catch(e) {
        console.error(e);
        edge.kill();
    }
}, 3000);
