import os
import subprocess
import time
import json
import base64
import urllib.request
import asyncio
import websockets

SNAPSHOT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\live_terminal_snapshot.jpg'
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_snapshot_profile'

async def capture():
    # Start Chrome
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--remote-debugging-port=9266',
        '--no-sandbox',
        '--disable-gpu',
        f'--user-data-dir={PROFILE_DIR}'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.5)

    try:
        # Get target websocket URL
        list_url = 'http://127.0.0.1:9266/json/list'
        req = urllib.request.urlopen(list_url, timeout=5)
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next((t for t in targets if t.get('type') == 'page'), targets[0])
        ws_url = page_target['webSocketDebuggerUrl']

        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
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
                'height': 768,
                'deviceScaleFactor': 1,
                'mobile': False
            })

            # Load local file
            index_file_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
            await send_cdp('Page.navigate', {'url': index_file_url})
            await asyncio.sleep(2.0)

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
    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(capture())
