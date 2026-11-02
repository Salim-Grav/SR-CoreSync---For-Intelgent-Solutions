"""
Comprehensive Test Script for Triple Upgrade:
1. Option 1: Multilingual Voice Planner & Speech in European/Arabic language
2. Option 2: Executive VIP Booking Modal Audio Greeting (Salim & Raed personal audio)
3. Option 3: Sovereign Executive A4 Blueprint Preview Modal & Official Stamping
"""
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
PROFILE_DIR = r'C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_launchpad_profile_triple'

async def test_suite():
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless=new',
        '--remote-debugging-port=9280',
        '--no-sandbox',
        '--disable-gpu',
        '--window-size=1440,900',
        f'--user-data-dir={PROFILE_DIR}'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.0)

    try:
        list_url = 'http://127.0.0.1:9280/json/list'
        req = urllib.request.urlopen(list_url, timeout=5)
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next((t for t in targets if t.get('type') == 'page'), targets[0])
        ws_url = page_target['webSocketDebuggerUrl']

        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cur = msg_id
                msg_id += 1
                payload = {'id': cur, 'method': method, 'params': params or {}}
                await ws.send(json.dumps(payload))
                while True:
                    raw = await ws.recv()
                    data = json.loads(raw)
                    if data.get('id') == cur:
                        return data

            await send('Page.enable')
            await send('DOM.enable')

            file_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
            await send('Page.navigate', {'url': file_url})
            await asyncio.sleep(2.5)

            # -------------------------------------------------------------
            # TEST 1: Option 2 - VIP Executive Booking Modal Audio Greeting
            # -------------------------------------------------------------
            print("--- Testing Option 2: VIP Executive Booking Modal Audio Greeting ---")
            await send('Runtime.evaluate', {
                'expression': 'openExecutiveBookingModal("salim");'
            })
            await asyncio.sleep(0.8)

            greeting_audit_salim = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const strip = document.getElementById("bookingAudioGreetingStrip");
                    const avatar = document.getElementById("bookingAudioAvatar");
                    const name = document.getElementById("bookingAudioAdvisorName");
                    const sub = document.getElementById("bookingAudioAdvisorSubtitle");
                    const playBtn = document.getElementById("bookingAudioPlayBtn");
                    return {
                        stripPresent: !!strip,
                        avatarSrc: avatar ? avatar.getAttribute("src") : "",
                        nameText: name ? name.innerText : "",
                        subText: sub ? sub.innerText : "",
                        playBtnPresent: !!playBtn
                    };
                })()''',
                'returnByValue': True
            })
            print("Salim Booking Audio Bar:", json.dumps(greeting_audit_salim['result']['result']['value'], ensure_ascii=False))

            # Switch advisor to Raed
            await send('Runtime.evaluate', {
                'expression': 'selectBookingAdvisor("raed");'
            })
            await asyncio.sleep(0.5)

            greeting_audit_raed = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const avatar = document.getElementById("bookingAudioAvatar");
                    const name = document.getElementById("bookingAudioAdvisorName");
                    const sub = document.getElementById("bookingAudioAdvisorSubtitle");
                    return {
                        avatarSrc: avatar ? avatar.getAttribute("src") : "",
                        nameText: name ? name.innerText : "",
                        subText: sub ? sub.innerText : ""
                    };
                })()''',
                'returnByValue': True
            })
            print("Raed Booking Audio Bar:", json.dumps(greeting_audit_raed['result']['result']['value'], ensure_ascii=False))

            # Close booking modal
            await send('Runtime.evaluate', {
                'expression': 'closeExecutiveBookingModal();'
            })
            await asyncio.sleep(0.5)

            # -------------------------------------------------------------
            # TEST 2: Option 1 & 3 - Hero AI Chip -> Blueprint -> A4 Modal
            # -------------------------------------------------------------
            print("--- Testing Option 1 & 3: Hero AI Chip -> Blueprint -> A4 Modal ---")
            # Click FinTech Chip (chip 0)
            await send('Runtime.evaluate', {
                'expression': 'document.querySelectorAll(".hero-ai-chip")[0].click();'
            })
            await asyncio.sleep(2.5)

            blueprint_audit = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const player = document.getElementById("blueprintAudioPlayer");
                    const previewBtn = document.querySelector(".sr-btn-preview-a4");
                    return {
                        hasPlayer: !!player,
                        founderType: player ? player.getAttribute("data-founder-type") : "",
                        hasPreviewBtn: !!previewBtn,
                        previewBtnText: previewBtn ? previewBtn.innerText : ""
                    };
                })()''',
                'returnByValue': True
            })
            print("Blueprint & Preview Btn Audit:", json.dumps(blueprint_audit['result']['result']['value'], ensure_ascii=False))

            # Open Sovereign A4 Blueprint Preview Modal
            await send('Runtime.evaluate', {
                'expression': 'openBlueprintPreviewModal();'
            })
            await asyncio.sleep(1.0)

            a4_modal_audit = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const modal = document.getElementById("srBlueprintPreviewModal");
                    const sheet = document.getElementById("srA4SheetContent");
                    const refEl = sheet ? sheet.querySelector(".sr-a4-doc-ref") : null;
                    const signName = sheet ? sheet.querySelector(".sr-a4-founder-sign-name") : null;
                    const sealTitle = sheet ? sheet.querySelector(".sr-a4-seal-title") : null;
                    return {
                        modalActive: modal ? modal.classList.contains("active") : false,
                        docRef: refEl ? refEl.innerText : "",
                        signer: signName ? signName.innerText : "",
                        seal: sealTitle ? sealTitle.innerText : ""
                    };
                })()''',
                'returnByValue': True
            })
            print("A4 Blueprint Modal Audit:", json.dumps(a4_modal_audit['result']['result']['value'], ensure_ascii=False))

            # Capture live visual snapshot of the Sovereign A4 Preview Modal!
            ss = await send('Page.captureScreenshot', {
                'format': 'jpeg',
                'quality': 90
            })
            img_b64 = ss['result']['data']
            img_data = base64.b64decode(img_b64)
            with open(SNAPSHOT_PATH, 'wb') as f:
                f.write(img_data)
            print(f"Captured live visual snapshot ({len(img_data)} bytes) to {SNAPSHOT_PATH}")

            # -------------------------------------------------------------
            # TEST 3: Multilingual in European Page (en/index.html)
            # -------------------------------------------------------------
            print("--- Testing Multilingual Hero AI in en/index.html ---")
            en_url = 'file:///' + os.path.abspath('en/index.html').replace('\\', '/')
            await send('Page.navigate', {'url': en_url})
            await asyncio.sleep(2.5)

            en_chip_click = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const chips = document.querySelectorAll(".hero-ai-chip");
                    if (chips && chips.length > 1) {
                        chips[1].click(); // Click ERP chip
                        return { clicked: true, text: chips[1].innerText };
                    }
                    return { clicked: false };
                })()''',
                'returnByValue': True
            })
            print("EN Chip Click:", json.dumps(en_chip_click['result']['result']['value'], ensure_ascii=False))
            await asyncio.sleep(2.5)

            en_audit = await send('Runtime.evaluate', {
                'expression': '''(() => {
                    const player = document.getElementById("blueprintAudioPlayer");
                    const previewBtn = document.querySelector(".sr-btn-preview-a4");
                    return {
                        hasPlayer: !!player,
                        founderType: player ? player.getAttribute("data-founder-type") : "",
                        lead: player ? decodeURIComponent(player.getAttribute("data-founder-lead") || "") : "",
                        hasPreviewBtn: !!previewBtn
                    };
                })()''',
                'returnByValue': True
            })
            print("EN Modal & Blueprint Audit:", json.dumps(en_audit['result']['result']['value'], ensure_ascii=False))

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(test_suite())
