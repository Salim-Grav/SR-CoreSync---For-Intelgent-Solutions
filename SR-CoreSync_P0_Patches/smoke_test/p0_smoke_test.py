"""
==============================================================================
P0 Smoke Test — حزمة إصلاحات أمان S&R CoreSync
==============================================================================
يختبر ملفات الحزمة في full_files/ مقابل وحدات المستودع الحقيقية، داخل الذاكرة
(TestClient) مع محاكاة google-antigravity (بلا شبكة ولا استدعاء Gemini).

الاستخدام (من جذر المستودع، سواء طُبقت الرقع أم لا):
    python <مسار الحزمة>/smoke_test/p0_smoke_test.py

المتطلبات: fastapi, uvicorn, httpx, python-dotenv
==============================================================================
"""
import os
import sys
import json
import shutil
import tempfile
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent          # جذر الحزمة
FULL_FILES = PACKAGE_DIR / "full_files"
STUBS_DIR = PACKAGE_DIR / "smoke_test" / "stubs"
SRC_DIR = Path(os.environ.get("CORESYNC_REPO_DIR", os.getcwd()))  # جذر المستودع

PATCHED_FROM_PACKAGE = ["sr_auth.py", "sr_agent_server.py", "sr_session_db.py"]
FROM_REPO = ["sr_rag_engine.py", "sr_subagent_monitor.py", "sr_alert_dispatcher.py", "sr_agent_core.py"]

missing = [f for f in FROM_REPO if not (SRC_DIR / f).is_file()]
if missing:
    print(f"❌ لم أجد وحدات المستودع في {SRC_DIR}: {missing}")
    print("   شغّل الاختبار من جذر المستودع أو اضبط CORESYNC_REPO_DIR.")
    sys.exit(2)

TEST_DIR = tempfile.mkdtemp(prefix="coresync_p0_smoke_")
(APP := Path(TEST_DIR) / "app").mkdir(parents=True)
for f in PATCHED_FROM_PACKAGE:
    shutil.copy(FULL_FILES / f, APP / f)
for f in FROM_REPO:
    shutil.copy(SRC_DIR / f, APP / f)
sys.path.insert(0, str(APP))
sys.path.insert(0, str(STUBS_DIR))
os.chdir(APP)

KEYS = "ops-console:admin-secret-key-123:admin,widget-a:client-a-key:client,widget-b:client-b-key:client"
os.environ["CORESYNC_API_KEYS"] = KEYS
os.environ["GEMINI_API_KEY"] = "dummy-for-smoke-test"
os.environ["CORESYNC_RATE_LIMIT"] = "1000/min"
os.environ["CORESYNC_CHAT_RATE_LIMIT"] = "6/min"

results = []

def record(name, ok, detail=""):
    results.append((name, ok))
    print(f"  {'✅' if ok else '❌'} {name} {detail}")

print("=" * 70)
print("Phase 1 — server WITH configured API keys")
print("=" * 70)

import sr_agent_server  # noqa: E402
from starlette.testclient import TestClient  # noqa: E402

with TestClient(sr_agent_server.app, raise_server_exceptions=False) as tc:
    admin = {"X-API-Key": "admin-secret-key-123"}
    wa = {"X-API-Key": "client-a-key"}
    wb = {"X-API-Key": "client-b-key"}

    r = tc.get("/health")
    record("T1 /health عام → 200", r.status_code == 200, f"[{r.status_code}]")

    r = tc.get("/api/rag/stats")
    record("T2 /api/rag/stats بلا مفتاح → 401", r.status_code == 401, f"[{r.status_code}]")

    r = tc.get("/api/rag/stats", headers=wa)
    record("T3 /api/rag/stats بمفتاح client → 200", r.status_code == 200, f"[{r.status_code}]")

    r = tc.get("/api/sessions", headers=wa)
    record("T4 GET /api/sessions بclient → 403", r.status_code == 403, f"[{r.status_code}]")

    r = tc.get("/api/sessions", headers=admin)
    record("T5 GET /api/sessions بadmin → 200", r.status_code == 200, f"[{r.status_code}]")

    r = tc.delete("/api/sessions/some-session", headers=wa)
    record("T6 DELETE جلسة بclient → 403", r.status_code == 403, f"[{r.status_code}]")

    r = tc.get("/api/rag/stats", headers={"X-API-Key": "wrong-key"})
    record("T7 مفتاح خاطئ → 401", r.status_code == 401, f"[{r.status_code}]")

    # ملكية الجلسات [A8] عبر مسار الصمود (RAG fallback، دون Gemini)
    r = tc.post("/api/chat", json={"message": "ما هي باقاتكم؟", "session_id": "sess-A"}, headers=wa)
    chat_ok = r.status_code == 200
    r2 = tc.get("/api/sessions/sess-A/history", headers=wa)
    record("T9 المالك يقرأ جلسته → 200", r2.status_code == 200 and chat_ok, f"[chat={r.status_code},hist={r2.status_code}]")
    r3 = tc.get("/api/sessions/sess-A/history", headers=wb)
    record("T8 عميل آخر يقرأ جلسة غيره → 403", r3.status_code == 403, f"[{r3.status_code}]")
    r4 = tc.get("/api/sessions/sess-A/history", headers=admin)
    record("T8b admin يقرأ أي جلسة → 200", r4.status_code == 200, f"[{r4.status_code}]")

    # CORS
    r = tc.options("/api/chat", headers={
        "Origin": "https://evil.example",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,x-api-key",
    })
    no_allow = "access-control-allow-origin" not in {k.lower() for k in r.headers.keys()}
    r = tc.options("/api/chat", headers={
        "Origin": "https://sr-coresync.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,x-api-key",
    })
    allow_ok = r.headers.get("access-control-allow-origin") == "https://sr-coresync.com"
    record("T10 CORS مقيّد (أصل خبيث محجوب، أصل موثوق مقبول)", no_allow and allow_ok)

    # حد معدل المحادثة (6/min)
    codes = []
    for i in range(12):
        rr = tc.post("/api/chat", json={"message": f"سؤال {i}", "session_id": "rl-test"}, headers=wa)
        codes.append(rr.status_code)
    record("T11 تجاوز حد المحادثة → 429", 429 in codes, f"[codes={set(codes)}]")

    # رفع يتجاوز السقف الكلي (content-length مزيف)
    r = tc.post(
        "/api/upload",
        files={"files": ("big.pdf", b"%PDF-1.4 tiny", "application/pdf")},
        headers={**admin, "content-length": str(6 * 5 * 1024 * 1024)},
    )
    record("T12 رفع بحجم إجمالي زائد → 413", r.status_code == 413, f"[{r.status_code}]")

    # التوثيق محمي
    r = tc.get("/docs")
    record("T14 /docs بلا مفتاح → 401", r.status_code == 401, f"[{r.status_code}]")

print()
print("=" * 70)
print("Phase 2 — fail-closed: NO keys configured")
print("=" * 70)

for mod in list(sys.modules):
    if mod.startswith(("sr_", "google")):
        del sys.modules[mod]
os.environ.pop("CORESYNC_API_KEYS", None)
os.environ.pop("CORESYNC_AUTH_DISABLED", None)

import sr_agent_server as srv2  # noqa: E402
from starlette.testclient import TestClient as TC2  # noqa: E402

with TC2(srv2.app, raise_server_exceptions=False) as tc2:
    r = tc2.get("/api/rag/stats")
    record("T13 بلا مفاتيح → 503 (إغلاق افتراضي)", r.status_code == 503, f"[{r.status_code}]")
    r = tc2.get("/health")
    record("T13b /health يبقى عاماً → 200", r.status_code == 200, f"[{r.status_code}]")

print()
shutil.rmtree(TEST_DIR, ignore_errors=True)
total_ok = sum(1 for _, ok in results if ok)
print(f"RESULT: {total_ok}/{len(results)} passed")
sys.exit(0 if total_ok == len(results) else 1)
