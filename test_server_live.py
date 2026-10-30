import time
import subprocess
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "sr_agent_server:app", "--port", "8000"])
print("Server process started with PID:", proc.pid)

try:
    time.sleep(4)
    # Test GET /
    req = urllib.request.Request("http://127.0.0.1:8000/")
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode())
        print("TEST 1 - GET / SUCCESS:", json.dumps(data, ensure_ascii=False, indent=2))

    # Test GET /api/workspace/portals
    req2 = urllib.request.Request("http://127.0.0.1:8000/api/workspace/portals")
    with urllib.request.urlopen(req2, timeout=5) as response2:
        data2 = json.loads(response2.read().decode())
        print("TEST 2 - GET /api/workspace/portals SUCCESS:", data2["portals_summary"][:120])

    # Test POST /api/ai-concierge with a query
    post_data = json.dumps({"message": "ما هي باقة السوشيال ميديا 8K؟"}).encode("utf-8")
    req3 = urllib.request.Request(
        "http://127.0.0.1:8000/api/ai-concierge",
        data=post_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req3, timeout=15) as response3:
        data3 = json.loads(response3.read().decode())
        print("TEST 3 - POST /api/ai-concierge SUCCESS:")
        print("Reply:", data3.get("reply"))
        print("Source:", data3.get("source"))
        print("Actions:", data3.get("actions"))

finally:
    proc.terminate()
    proc.wait()
    print("Server process terminated cleanly.")
