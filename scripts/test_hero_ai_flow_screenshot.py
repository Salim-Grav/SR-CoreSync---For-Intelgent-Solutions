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

            file_url = 'file:' + urllib.request.pathname2url(os.path.abspath('index.html'))
            await send_cdp('Page.navigate', {'url': file_url})
            await asyncio.sleep(3.0)

            # Trigger ERP Blueprint generation directly
            await send_cdp('Runtime.evaluate', {
                'expression': 'window.fillHeroPromptSample("نظام CoreSync ERP لإدارة المحاسبة والضرائب الأوروبية BTW وسلاسل الإمداد");',
                'returnByValue': True
            })
            
            # Wait for AI blueprint generation and animation
            await asyncio.sleep(2.0)

            # Now open the A4 Blueprint Preview Modal featuring Option 1 (Live QR), Option 2 (JSON spec button), Option 3 (Dispatch button)
            await send_cdp('Runtime.evaluate', {
                'expression': 'if (typeof openBlueprintPreviewModal === "function") openBlueprintPreviewModal();',
                'returnByValue': True
            })

            await asyncio.sleep(1.5)

            # Check if modal is active, verify QR code, seal and toolbar buttons
            audit_state = await send_cdp('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const modal = document.getElementById("srBlueprintPreviewModal");
                    const qrImg = modal ? modal.querySelector(".sr-a4-qr-img") : null;
                    const qrLink = modal ? modal.querySelector(".sr-a4-qr-badge-link") : null;
                    const jsonBtn = modal ? modal.querySelector(".sr-a4-btn-json") : null;
                    const dispatchBtn = modal ? modal.querySelector(".sr-a4-btn-dispatch") : null;
                    const founderSign = modal ? modal.querySelector(".sr-a4-founder-sign-name") : null;
                    const seal = modal ? modal.querySelector(".sr-a4-official-seal") : null;
                    const docRef = modal ? modal.querySelector(".sr-a4-doc-ref") : null;

                    // Scroll the endorsement and QR section into nice view inside modal wrapper
                    const endorsement = modal ? modal.querySelector(".sr-a4-endorsement-strip") : null;
                    if (endorsement) {
                        endorsement.scrollIntoView({ behavior: 'instant', block: 'center' });
                    }

                    return {
                        modalActive: modal ? modal.classList.contains("active") : false,
                        docRef: docRef ? docRef.innerText : "",
                        qrSrc: qrImg ? qrImg.getAttribute("src") : "",
                        qrHref: qrLink ? qrLink.getAttribute("href") : "",
                        jsonBtnText: jsonBtn ? jsonBtn.innerText : "",
                        dispatchBtnText: dispatchBtn ? dispatchBtn.innerText : "",
                        founderSignName: founderSign ? founderSign.innerText : "",
                        hasSeal: !!seal
                    };
                })()
                ''',
                'returnByValue': True
            })
            print("A4 Dossier Audit State (Option 1+2+3):", json.dumps(audit_state['result']['result'].get('value', {}), ensure_ascii=False))

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
        try:
            proc.wait(timeout=2)
        except:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(capture())
