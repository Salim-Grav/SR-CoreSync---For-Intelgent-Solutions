import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const PORT = 9338;
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

        // 1. Switch to creative pricing tab and scroll into view
        await send('Runtime.evaluate', {
            expression: `
                const sec = document.getElementById('pricing');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
                const btn = document.getElementById('tab-btn-pricing-creative');
                if (btn) btn.click();
            `
        });

        await sleep(1500);
        const snapPricing = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync('live_pricing_social_8k_card.png', Buffer.from(snapPricing.data, 'base64'));
        writeFileSync('C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\c2846371-b1e6-4b8f-9fee-01dda36014e9\\live_pricing_social_8k_card.png', Buffer.from(snapPricing.data, 'base64'));
        console.log('Successfully captured creative pricing tab with 8K card');

        // 2. Switch to work identity tab and scroll into view
        await send('Runtime.evaluate', {
            expression: `
                const sec = document.getElementById('work');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
                const btn = document.getElementById('tab-btn-identity');
                if (btn) btn.click();
            `
        });

        await sleep(1500);
        const snapWork = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync('live_work_omnichannel_8k.png', Buffer.from(snapWork.data, 'base64'));
        writeFileSync('C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\c2846371-b1e6-4b8f-9fee-01dda36014e9\\live_work_omnichannel_8k.png', Buffer.from(snapWork.data, 'base64'));
        console.log('Successfully captured work identity tab with omnichannel 8K project');

        ws.close();
    } catch (e) {
        console.error(e);
    } finally {
        proc.kill();
    }
}

main();
