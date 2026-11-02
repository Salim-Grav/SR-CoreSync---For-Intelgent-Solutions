import asyncio, websockets, json, subprocess, os, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

async def test_en():
    profile = r"C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\chrome_launchpad_profile_en_debug2"
    cmd = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--remote-debugging-port=9282", "--no-sandbox", "--disable-gpu", "--window-size=1440,900", f"--user-data-dir={profile}"]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2.0)
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9282/json/list", timeout=5)
        ws_url = json.loads(req.read().decode("utf-8"))[0]["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            mid = 1
            async def send(m, p=None):
                nonlocal mid; c = mid; mid += 1
                await ws.send(json.dumps({"id": c, "method": m, "params": p or {}}))
                while True:
                    d = json.loads(await ws.recv())
                    if d.get("id") == c: return d

            await send("Page.enable"); await send("DOM.enable"); await send("Runtime.enable")
            
            # Listen to console
            file_url = "file:///" + os.path.abspath("en/index.html").replace("\\\\", "/")
            await send("Page.navigate", {"url": file_url})
            await asyncio.sleep(2.5)

            # Check if fillHeroPromptSample is available
            eval_res = await send("Runtime.evaluate", {
                "expression": '''(() => {
                    const btn = document.querySelectorAll(".hero-ai-chip")[1];
                    btn.click();
                    return {
                        inputVal: document.getElementById("heroAiIdeaInput") ? document.getElementById("heroAiIdeaInput").value : null,
                        transcriptVal: document.getElementById("voicePlannerTranscript") ? document.getElementById("voicePlannerTranscript").value : null,
                        modalClasses: document.getElementById("aiVoicePlannerModal") ? document.getElementById("aiVoicePlannerModal").className : null,
                        statusText: document.getElementById("voicePlannerStatus") ? document.getElementById("voicePlannerStatus").innerText : null
                    };
                })()''',
                "returnByValue": True
            })
            print("Immediate click eval raw:", json.dumps(eval_res, ensure_ascii=False))

            await asyncio.sleep(2.0)

            result_eval = await send("Runtime.evaluate", {
                "expression": '''(() => {
                    const res = document.getElementById("voicePlannerResult");
                    return {
                        hasResult: !!res,
                        resultHtmlLength: res ? res.innerHTML.length : 0,
                        hasPlayer: !!document.getElementById("blueprintAudioPlayer")
                    };
                })()''',
                "returnByValue": True
            })
            print("After 2s eval:", json.dumps(result_eval["result"]["result"]["value"], ensure_ascii=False))

    finally:
        proc.terminate()
        try: proc.wait(timeout=2)
        except: proc.kill()

if __name__ == '__main__':
    asyncio.run(test_en())
