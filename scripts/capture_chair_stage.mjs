import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const PORT = 9335;
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
    const proc = spawn(CHROME, [
        `--remote-debugging-port=${PORT}`,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--window-size=1600,1050',
        'http://localhost:3000/'
    ]);

    await sleep(3000);

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

        // 1. Scroll section-executive-stage into view and ensure Salim is active
        await send('Runtime.evaluate', {
            expression: `
                const sec = document.querySelector('.section-executive-stage');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
                const btnSalim = document.getElementById('execBtnSalim');
                if (btnSalim) btnSalim.click();
            `
        });

        await sleep(1500);

        // Capture Salim
        const snapSalim = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync('live_exec_stage_leadership.png', Buffer.from(snapSalim.data, 'base64'));
        writeFileSync('C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\c2846371-b1e6-4b8f-9fee-01dda36014e9\\live_exec_stage_leadership.png', Buffer.from(snapSalim.data, 'base64'));
        console.log('Successfully captured Salim view');

        // 2. Switch to Raed
        await send('Runtime.evaluate', {
            expression: `
                const btnRaed = document.getElementById('execBtnRaed');
                if (btnRaed) btnRaed.click();
            `
        });

        await sleep(1500);

        // Capture Raed
        const snapRaed = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync('live_exec_stage_raed.png', Buffer.from(snapRaed.data, 'base64'));
        writeFileSync('C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\c2846371-b1e6-4b8f-9fee-01dda36014e9\\live_exec_stage_raed.png', Buffer.from(snapRaed.data, 'base64'));
        console.log('Successfully captured Raed view');

        ws.close();
    } catch (e) {
        console.error(e);
    } finally {
        proc.kill();
    }
}

main();
