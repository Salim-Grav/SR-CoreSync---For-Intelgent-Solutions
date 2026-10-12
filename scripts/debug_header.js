const { execSync } = require('child_process');
const http = require('http');

// Start edge with debugging port
const edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const edgeProcess = require('child_process').spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--window-size=390,844',
    'http://127.0.0.1:3000/index.html'
]);

setTimeout(async () => {
    try {
        const fetchJson = () => new Promise((resolve, reject) => {
            http.get('http://127.0.0.1:9222/json', (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => resolve(JSON.parse(data)));
            }).on('error', reject);
        });

        const targets = await fetchJson();
        const page = targets.find(t => t.type === 'page');
        if (!page) {
            console.log('No page target found');
            edgeProcess.kill();
            return;
        }

        // Use CDP HTTP endpoint to evaluate JS
        // Or connect via basic WebSocket
        console.log('Page target:', page.url, page.webSocketDebuggerUrl);
        const WebSocket = require('net'); // simple check
    } catch (e) {
        console.error(e);
    } finally {
        edgeProcess.kill();
    }
}, 2000);
