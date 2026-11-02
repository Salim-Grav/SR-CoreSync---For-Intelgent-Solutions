import os
import subprocess
import time
import json
import base64
import urllib.request
import asyncio
import websockets

PDF_OUTPUT_PATH = r'd:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\CLGID_The_Hague_Modernization_Proposal_2026.pdf'
SNAPSHOT_PATH = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\live_terminal_snapshot.jpg'
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_pdf_profile'

async def run_pdf_export():
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--remote-debugging-port=9277',
        '--no-sandbox',
        '--disable-gpu',
        f'--user-data-dir={PROFILE_DIR}'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.5)

    try:
        req = urllib.request.urlopen('http://127.0.0.1:9277/json/list', timeout=5)
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
            await send_cdp('DOM.enable')
            await send_cdp('CSS.enable')
            await send_cdp('Emulation.setDeviceMetricsOverride', {
                'width': 1200,
                'height': 900,
                'deviceScaleFactor': 1,
                'mobile': False
            })

            index_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
            await send_cdp('Page.navigate', {'url': index_url})
            await asyncio.sleep(2.0)

            # Trigger the AI blueprint generation for CLGID website
            trigger_script = """
            (() => {
                const transcript = document.getElementById("voicePlannerTranscript");
                if (transcript) {
                    transcript.value = "أريد تطوير وإعادة تصميم موقع مركز CLGID لاهاي للحوكمة بالواجهة العربية واستضافة آمنة";
                }
                if (typeof generateAiProjectBlueprint === "function") {
                    generateAiProjectBlueprint();
                }
            })()
            """
            await send_cdp('Runtime.evaluate', {'expression': trigger_script})
            await asyncio.sleep(1.5)

            # Open the A4 Preview Modal
            open_modal_script = """
            (() => {
                if (typeof openBlueprintPreviewModal === "function") {
                    openBlueprintPreviewModal();
                }
            })()
            """
            await send_cdp('Runtime.evaluate', {'expression': open_modal_script})
            await asyncio.sleep(1.0)

            # Capture visual screenshot of the A4 preview modal
            shot = await send_cdp('Page.captureScreenshot', {
                'format': 'jpeg',
                'quality': 90
            })
            b64_img = shot.get('data')
            if b64_img:
                img_data = base64.b64decode(b64_img)
                with open(SNAPSHOT_PATH, 'wb') as f:
                    f.write(img_data)
                print(f"SUCCESS: Captured live preview screenshot ({len(img_data)} bytes)")

            # Generate real print PDF
            pdf_res = await send_cdp('Page.printToPDF', {
                'printBackground': True,
                'paperWidth': 8.27,
                'paperHeight': 11.69,
                'marginTop': 0.3,
                'marginBottom': 0.3,
                'marginLeft': 0.3,
                'marginRight': 0.3,
                'preferCSSPageSize': True
            })

            b64_pdf = pdf_res.get('data')
            if b64_pdf:
                pdf_data = base64.b64decode(b64_pdf)
                with open(PDF_OUTPUT_PATH, 'wb') as f:
                    f.write(pdf_data)
                print(f"SUCCESS: Generated PDF report at {PDF_OUTPUT_PATH} ({len(pdf_data)} bytes)")
            else:
                print("WARNING: No PDF data returned from CDP")

    except Exception as e:
        print("Error during PDF export test:", e)
    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(run_pdf_export())
