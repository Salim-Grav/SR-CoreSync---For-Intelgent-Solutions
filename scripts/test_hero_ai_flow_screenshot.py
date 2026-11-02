import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import subprocess
import json
import base64
import urllib.request
import asyncio
import websockets

SNAPSHOT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\live_terminal_snapshot.jpg'
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_launchpad_profile'

async def capture():
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--remote-debugging-port=9288',
        '--no-sandbox',
        '--disable-gpu',
        '--window-size=1440,1050',
        f'--user-data-dir={PROFILE_DIR}'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.0)

    try:
        list_url = 'http://127.0.0.1:9288/json/list'
        req = urllib.request.urlopen(list_url, timeout=5)
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next((t for t in targets if t.get('type') == 'page' and not t.get('url', '').startswith('chrome-extension://')), targets[0])
        ws_url = page_target['webSocketDebuggerUrl']

        async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
            mid = 1
            async def send_cdp(method, params=None):
                nonlocal mid; c = mid; mid += 1
                payload = {'id': c, 'method': method}
                if params: payload['params'] = params
                await ws.send(json.dumps(payload))
                while True:
                    raw = await ws.recv()
                    data = json.loads(raw)
                    if data.get('id') == c: return data

            await send_cdp('Page.enable')
            await send_cdp('DOM.enable')

            file_url = 'file:' + urllib.request.pathname2url(os.path.abspath('index.html'))
            await send_cdp('Page.navigate', {'url': file_url})
            await asyncio.sleep(3.5)

            # Trigger CLGID / Web Governance Plan -> Salim Aziza
            prompt = "تطوير وإعادة بناء المنظومة الرقمية لمركز CLGID للدراسات والحوكمة في لاهاي وبناء موقع ويبسايت سحابي سيادي"
            await send_cdp('Runtime.evaluate', {
                'expression': f'window.fillHeroPromptSample("{prompt}");',
                'returnByValue': True
            })
            await asyncio.sleep(2.5)

            # Center the generated blueprint card in the viewport
            await send_cdp('Runtime.evaluate', {
                'expression': '''(() => {
                    const player = document.getElementById("blueprintAudioPlayer");
                    if (player) {
                        player.scrollIntoView({ behavior: 'instant', block: 'center' });
                    }
                })()'''
            })
            await asyncio.sleep(1.0)

            # Capture live modal & blueprint snapshot
            ss = await send_cdp('Page.captureScreenshot', {
                'format': 'jpeg',
                'quality': 95
            })
            img_b64 = ss['result']['data']
            img_data = base64.b64decode(img_b64)
            with open(SNAPSHOT_PATH, 'wb') as f:
                f.write(img_data)
            print(f"Captured live simulation snapshot ({len(img_data)} bytes) to {SNAPSHOT_PATH}")

    finally:
        proc.terminate()
        try: proc.wait(timeout=2)
        except: proc.kill()

if __name__ == '__main__':
    asyncio.run(capture())
