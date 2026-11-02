import os
import subprocess
import time
import json
import base64
import urllib.request
import asyncio
import websockets

PDF_PATH = r'd:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\CLGID_The_Hague_Modernization_Proposal_2026.pdf'
SNAPSHOT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\live_terminal_snapshot.jpg'
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_snapshot_profile2'

async def capture():
    # Kill any dangling chrome processes on 9288 if any
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--remote-debugging-port=9288',
        '--no-sandbox',
        '--disable-gpu',
        f'--user-data-dir={PROFILE_DIR}'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.5)

    try:
        list_url = 'http://127.0.0.1:9288/json/list'
        req = urllib.request.urlopen(list_url, timeout=5)
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next((t for t in targets if t.get('type') == 'page'), targets[0])
        ws_url = page_target['webSocketDebuggerUrl']

        async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
            msg_id = 1
            async def send_cdp(method, params=None):
                nonlocal msg_id
                cur = msg_id
                msg_id += 1
                payload = {'id': cur, 'method': method}
                if params:
                    payload['params'] = params
                await ws.send(json.dumps(payload))
                while True:
                    resp_raw = await ws.recv()
                    resp = json.loads(resp_raw)
                    if resp.get('id') == cur:
                        return resp.get('result', {})

            await send_cdp('Page.enable')
            await send_cdp('Emulation.setDeviceMetricsOverride', {
                'width': 1366,
                'height': 800,
                'deviceScaleFactor': 1,
                'mobile': False
            })

            file_url = 'file:///' + os.path.abspath('clgid-prototype.html').replace('\\', '/')
            await send_cdp('Page.navigate', {'url': file_url})
            await asyncio.sleep(2.0)

            # Scroll down to the pricing table
            scroll_script = "window.scrollTo(0, document.body.scrollHeight * 0.65);"
            await send_cdp('Runtime.evaluate', {'expression': scroll_script})
            await asyncio.sleep(1.0)

            # Capture visual live snapshot
            shot = await send_cdp('Page.captureScreenshot', {
                'format': 'jpeg',
                'quality': 85
            })

            data_b64 = shot.get('data')
            if data_b64:
                img_bytes = base64.b64decode(data_b64)
                with open(SNAPSHOT_PATH, 'wb') as f:
                    f.write(img_bytes)
                print(f'SUCCESS: Live screenshot saved to {SNAPSHOT_PATH} ({len(img_bytes)} bytes)')

            # Generate full PDF with backgrounds printed
            pdf_res = await send_cdp('Page.printToPDF', {
                'printBackground': True,
                'paperWidth': 8.27,
                'paperHeight': 11.69,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
                'preferCSSPageSize': True
            })

            pdf_b64 = pdf_res.get('data')
            if pdf_b64:
                pdf_bytes = base64.b64decode(pdf_b64)
                with open(PDF_PATH, 'wb') as f:
                    f.write(pdf_bytes)
                print(f'SUCCESS: PDF saved to {PDF_PATH} ({len(pdf_bytes)} bytes)')
            else:
                print('WARNING: Page.printToPDF returned empty data')

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(capture())
