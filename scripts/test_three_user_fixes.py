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

async def test_fixes():
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

            # Test 1: Verify Voice Recording Button and window bindings
            test1 = await send_cdp('Runtime.evaluate', {
                'expression': '''(() => {
                    const micBtn = document.getElementById("voicePlannerMicBtn");
                    const hasToggle = typeof window.toggleVoiceRecording === "function";
                    const hasStart = typeof window.startVoiceRecording === "function";
                    const hasStop = typeof window.stopVoiceRecording === "function";
                    
                    // Simulate clicking mic button
                    let clickResult = "not clicked";
                    if (micBtn) {
                        micBtn.click();
                        clickResult = "clicked micBtn successfully";
                    }
                    return { hasToggle, hasStart, hasStop, clickResult };
                })()''',
                'returnByValue': True
            })
            print("Test 1 Result (Voice Button Bindings):", json.dumps(test1['result']['result'].get('value', {}), ensure_ascii=False))

            # Test 2: Route Web & CLGID Project -> Salim Aziza
            test2_prompt = "أريد تطوير ويبسايت وموقع لمنصة حوكمة واستشارات وإدارة وتطوير المشاريع CLGID"
            await send_cdp('Runtime.evaluate', {
                'expression': f'window.fillHeroPromptSample("{test2_prompt}");',
                'returnByValue': True
            })
            await asyncio.sleep(2.5)

            # Check Blueprint State for Salim
            test2 = await send_cdp('Runtime.evaluate', {
                'expression': '''(() => {
                    const player = document.getElementById("blueprintAudioPlayer");
                    const img = player ? player.querySelector(".sr-blueprint-audio-img") : null;
                    const badge = player ? player.querySelector(".sr-blueprint-audio-badge") : null;
                    const title = player ? player.querySelector(".sr-blueprint-audio-title") : null;
                    const lead = player ? decodeURIComponent(player.getAttribute("data-founder-lead") || "") : "";
                    const founderType = player ? player.getAttribute("data-founder-type") : "";
                    const projTitle = document.querySelector(".sr-blueprint-title");

                    // Scroll into view
                    if (player) {
                        player.scrollIntoView({ behavior: 'instant', block: 'center' });
                    }

                    return {
                        founderType,
                        avatarSrc: img ? img.getAttribute("src") : "",
                        badgeText: badge ? badge.innerText : "",
                        titleText: title ? title.innerText : "",
                        speechLead: lead,
                        projectTitle: projTitle ? projTitle.innerText : ""
                    };
                })()''',
                'returnByValue': True
            })
            print("Test 2 Result (Web/CLGID Routing to Salim):", json.dumps(test2['result']['result'].get('value', {}), ensure_ascii=False))

            # Test 3: Test A4 Preview Modal & PDF Generation
            await send_cdp('Runtime.evaluate', {
                'expression': 'if (typeof openBlueprintPreviewModal === "function") openBlueprintPreviewModal();',
                'returnByValue': True
            })
            await asyncio.sleep(1.5)

            test3 = await send_cdp('Runtime.evaluate', {
                'expression': '''(() => {
                    const modal = document.getElementById("srBlueprintPreviewModal");
                    const sheet = document.getElementById("srA4SheetContent");
                    const sheetHtmlLen = sheet ? sheet.innerHTML.length : 0;
                    const founderSign = modal ? modal.querySelector(".sr-a4-founder-sign-name") : null;
                    const qrImg = modal ? modal.querySelector(".sr-a4-qr-img") : null;
                    const docRef = modal ? modal.querySelector(".sr-a4-doc-ref") : null;

                    // Verify media print styles exist
                    const printStyles = Array.from(document.styleSheets).some(s => {
                        try {
                            return Array.from(s.cssRules || []).some(r => r.media && r.media.mediaText.includes("print"));
                        } catch(e) { return false; }
                    });

                    return {
                        modalActive: modal ? modal.classList.contains("active") : false,
                        sheetPopulated: sheetHtmlLen > 500,
                        sheetLength: sheetHtmlLen,
                        founderSignName: founderSign ? founderSign.innerText : "",
                        qrSrc: qrImg ? qrImg.getAttribute("src") : "",
                        docRef: docRef ? docRef.innerText : "",
                        hasPrintMediaRules: printStyles
                    };
                })()''',
                'returnByValue': True
            })
            print("Test 3 Result (A4 PDF Sheet Content & Print Media):", json.dumps(test3['result']['result'].get('value', {}), ensure_ascii=False))

            # Capture live screenshot of the updated view
            await asyncio.sleep(1.0)
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
    asyncio.run(test_fixes())
