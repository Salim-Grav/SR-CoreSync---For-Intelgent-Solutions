import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const PORT = 9337;
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

        // Open Voice Planner modal in fresh listening state
        await send('Runtime.evaluate', {
            expression: `
                openAiVoicePlannerModal();
            `
        });

        await sleep(1500);
        const snapMic = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync('live_voice_planner_mic_listening.png', Buffer.from(snapMic.data, 'base64'));
        writeFileSync('C:\\\\Users\\\\msali\\\\.gemini\\\\antigravity-ide\\\\brain\\\\c2846371-b1e6-4b8f-9fee-01dda36014e9\\\\live_voice_planner_mic_listening.png', Buffer.from(snapMic.data, 'base64'));
        console.log('Successfully captured mic listening stage');

        ws.close();
    } catch (e) {
        console.error(e);
    } finally {
        proc.kill();
    }
}

main();
