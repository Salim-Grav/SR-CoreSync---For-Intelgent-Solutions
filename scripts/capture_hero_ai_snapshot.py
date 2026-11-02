import os
import subprocess
import json
import base64
import urllib.request
import asyncio
import websockets

SNAPSHOT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\live_terminal_snapshot.jpg'
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_launchpad_profile'

async def capture():
    # Kill any lingering chrome on 9277
    try:
        urllib.request.urlopen('http://127.0.0.1:9277/json/version', timeout=1)
    except:
        pass

    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--remote-debugging-port=9277',
        '--no-sandbox',
        '--disable-gpu',
        '--window-size=1440,900',
        f'--user-data-dir={PROFILE_DIR}'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.0)

    try:
        list_url = 'http://127.0.0.1:9277/json/list'
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
                    raw = await ws.recv()
                    data = json.loads(raw)
                    if data.get('id') == cur:
                        return data

            await send_cdp('Page.enable')
            await send_cdp('DOM.enable')

            file_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
            await send_cdp('Page.navigate', {'url': file_url})
            await asyncio.sleep(2.0)

            # Ensure Hero AI Bar is in view
            await send_cdp('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const el = document.getElementById("heroAiIdeaBar");
                    if (el) {
                        el.scrollIntoView({block: "center", behavior: "instant"});
                    }
                })()
                '''
            })
            await asyncio.sleep(0.5)

            # Capture screenshot
            ss = await send_cdp('Page.captureScreenshot', {
                'format': 'jpeg',
                'quality': 90
            })
            img_b64 = ss['result']['data']
            img_data = base64.b64decode(img_b64)
            with open(SNAPSHOT_PATH, 'wb') as f:
                f.write(img_data)
            print(f"Captured live snapshot: {len(img_data)} bytes saved to {SNAPSHOT_PATH}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(capture())
