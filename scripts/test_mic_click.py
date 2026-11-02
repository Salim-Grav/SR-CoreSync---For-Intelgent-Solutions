import asyncio
import websockets
import json
import subprocess
import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    cmd = [r'C:\Program Files\Google\Chrome\Application\chrome.exe', '--headless=new', '--remote-debugging-port=9289', '--no-sandbox', '--allow-file-access-from-files']
    proc = subprocess.Popen(cmd)
    await asyncio.sleep(2)
    try:
        req = urllib.request.urlopen('http://127.0.0.1:9289/json/list')
        ts = json.loads(req.read().decode())
        t = next(x for x in ts if x['type']=='page' and not x['url'].startswith('chrome-extension'))
        async with websockets.connect(t['webSocketDebuggerUrl']) as ws:
            mid = 1
            async def send(m, p=None):
                nonlocal mid; c = mid; mid += 1
                await ws.send(json.dumps({'id': c, 'method': m, 'params': p or {}}))
                while True:
                    d = json.loads(await ws.recv())
                    if d.get('id')==c: return d
            await send('Page.enable')
            f = 'file:' + urllib.request.pathname2url(os.path.abspath('index.html'))
            await send('Page.navigate', {'url': f})
            await asyncio.sleep(4)

            # Open modal
            await send('Runtime.evaluate', {'expression': 'window.openAiVoicePlannerModal();'})
            await asyncio.sleep(0.5)

            # Click mic button
            r = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const micBtn = document.getElementById("voicePlannerMicBtn");
                    const statusBefore = document.getElementById("voicePlannerStatus").innerText;
                    micBtn.click();
                    const statusAfter = document.getElementById("voicePlannerStatus").innerText;
                    return { statusBefore, statusAfter };
                })()''',
                'returnByValue': True
            })
            print('Mic Click Result:', json.dumps(r['result']['result']['value'], ensure_ascii=False))
    finally:
        proc.terminate()
        try: proc.wait(timeout=2)
        except: proc.kill()

if __name__ == '__main__':
    asyncio.run(test())
