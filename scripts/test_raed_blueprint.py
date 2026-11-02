import asyncio
import websockets
import json
import subprocess
import urllib.request
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    cmd = [r'C:\Program Files\Google\Chrome\Application\chrome.exe', '--headless=new', '--remote-debugging-port=9292', '--no-sandbox']
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.0)
    try:
        req = urllib.request.urlopen('http://127.0.0.1:9292/json/list')
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next((t for t in targets if t.get('type') == 'page' and not t.get('url', '').startswith('chrome-extension://')), targets[0])
        ws_url = page_target['webSocketDebuggerUrl']
        print("Connected to target:", page_target.get('title'), page_target.get('url'))
        async with websockets.connect(ws_url) as ws:
            mid = 1
            async def send(m, p=None):
                nonlocal mid; c = mid; mid += 1
                await ws.send(json.dumps({'id': c, 'method': m, 'params': p or {}}))
                while True:
                    d = json.loads(await ws.recv())
                    if d.get('id') == c: return d
            await send('Page.enable')
            file_url = 'file:' + urllib.request.pathname2url(os.path.abspath('index.html'))
            print("Navigating to:", file_url)
            await send('Page.navigate', {'url': file_url})
            await asyncio.sleep(2.5)

            # Click chip 1: ERP
            await send('Runtime.evaluate', {'expression': 'document.querySelectorAll(".hero-ai-chip")[1].click();'})
            await asyncio.sleep(2.5)

            res = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const p = document.getElementById("blueprintAudioPlayer");
                    const title = p ? p.querySelector(".sr-blueprint-audio-title").innerText : "";
                    const badge = p ? p.querySelector(".sr-blueprint-audio-badge").innerText : "";
                    const lead = p ? decodeURIComponent(p.getAttribute("data-founder-lead") || "") : "";
                    const type = p ? p.getAttribute("data-founder-type") : "";
                    return { type, title, badge, lead };
                })()''',
                'returnByValue': True
            })
            print('Raed Blueprint State:', json.dumps(res['result']['result']['value'], ensure_ascii=False))
    finally:
        proc.terminate()
        try: proc.wait(timeout=2)
        except: proc.kill()

if __name__ == '__main__':
    asyncio.run(test())
