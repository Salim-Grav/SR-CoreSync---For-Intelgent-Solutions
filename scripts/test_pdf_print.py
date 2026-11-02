import asyncio
import websockets
import json
import subprocess
import urllib.request
import os
import sys
import base64

sys.stdout.reconfigure(encoding='utf-8')

PDF_OUT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\blueprint_test_output.pdf'
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_launchpad_profile'

async def test_pdf_print():
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
            await asyncio.sleep(4.0)

            # Generate Web / CLGID plan for Salim
            user_idea = "تطوير وإعادة بناء المنظومة الرقمية لمركز CLGID للدراسات والحوكمة في لاهاي"
            await send_cdp('Runtime.evaluate', {
                'expression': f'window.fillHeroPromptSample("{user_idea}");',
                'returnByValue': True
            })
            await asyncio.sleep(2.5)

            # Open A4 Blueprint modal
            await send_cdp('Runtime.evaluate', {
                'expression': 'window.openBlueprintPreviewModal();',
                'returnByValue': True
            })
            await asyncio.sleep(1.5)

            # Execute Page.printToPDF
            pdf_res = await send_cdp('Page.printToPDF', {
                'paperWidth': 8.27,  # A4 width in inches
                'paperHeight': 11.69, # A4 height in inches
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4,
                'printBackground': True,
                'preferCSSPageSize': True
            })

            pdf_b64 = pdf_res['result']['data']
            pdf_bytes = base64.b64decode(pdf_b64)
            with open(PDF_OUT_PATH, 'wb') as f:
                f.write(pdf_bytes)
            
            print(f"Generated PDF File: {len(pdf_bytes)} bytes written to {PDF_OUT_PATH}")

            # Verify PDF size is healthy (> 50KB indicates rich graphics, tables, texts, seals)
            if len(pdf_bytes) > 50000:
                print("✓ SUCCESS: PDF is rich and populated (NOT blank)!")
            else:
                print("⚠️ Warning: PDF file size is suspiciously small:", len(pdf_bytes))

    finally:
        proc.terminate()
        try: proc.wait(timeout=2)
        except: proc.kill()

if __name__ == '__main__':
    asyncio.run(test_pdf_print())
