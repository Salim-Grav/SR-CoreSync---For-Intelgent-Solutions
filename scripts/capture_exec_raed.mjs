import { spawn } from 'node:child_process';
import { existsSync, writeFileSync } from 'node:fs';

const PORT = 9333;
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
    const proc = spawn(CHROME, [
        `--remote-debugging-port=${PORT}`,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--window-size=1440,900',
        'http://localhost:3000/#leadership'
    ]);

    await sleep(2500);

    try {
        const listRes = await fetch(`http://127.0.0.1:${PORT}/json/list`);
        const pages = await listRes.json();
        const page = pages.find((p) => p.type === 'page') || pages[0];
        if (!page) throw new Error('No page found');

        const ws = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise((res, rej) => {
            ws.onopen = res;
            ws.onerror = rej;
        });

        let id = 1;
        const send = (method, params = {}) => new Promise((resolve) => {
            const curId = id++;
            const handler = (evt) => {
                const data = JSON.parse(evt.data);
                if (data.id === curId) {
                    ws.removeEventListener('message', handler);
                    resolve(data.result);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id: curId, method, params }));
        });

        // Click on execBtnRaed and wait for transition
        await send('Runtime.evaluate', {
            expression: `
                const btn = document.getElementById('execBtnRaed');
                if (btn) btn.click();
            `
        });

        await sleep(1200);

        const snap = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync('live_exec_stage_raed.png', Buffer.from(snap.data, 'base64'));
        console.log('Successfully captured live_exec_stage_raed.png');

        ws.close();
    } catch (e) {
        console.error(e);
    } finally {
        proc.kill();
    }
}

main();
