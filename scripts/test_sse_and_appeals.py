import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from sr_agent_server import app

def run():
    print("=" * 70)
    print("🚀 بدء فحص واجهات المهمة 110 (SSE Live Pulse) و 111 (Counsel) و 112 (Appeals)")
    print("=" * 70)

    with TestClient(app) as client:
        # 1. فحص التحقق من مستند WORM الجنائي
        valid_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        resp = client.get(f"/api/counsel/worm-verify?hash={valid_hash}")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert data["status"] == "VERIFIED_IMMUTABLE", "WORM hash should be verified immutable"
        assert data["iso_27037_compliant"] is True, "Must be ISO/IEC 27037 compliant"
        print("  [✓] فحص WORM للمستند المعتمد: سليم 100% (ISO/IEC 27037 Verified)")

        # فحص بصمة تالفة / معدلة
        tampered_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        resp = client.get(f"/api/counsel/worm-verify?hash={tampered_hash}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "UNREGISTERED_OR_TAMPERED", "Expected tamper detection"
        assert data["is_tampered"] is True
        print("  [✓] فحص كشف التلاعب WORM: تم رصد البصمة غير المطابقة بنجاح (Tamper Detected)")

        # 2. فحص قائمة أحكام التحكيم المعتمدة
        resp = client.get("/api/counsel/certified-awards")
        assert resp.status_code == 200
        awards = resp.json()
        assert len(awards) >= 4, "Should have at least 4 certified awards"
        print(f"  [✓] فحص استرجاع أحكام التحكيم المعتمدة: تم استرجاع {len(awards)} أحكام تحكيمية بنجاح")

        # 3. فحص نشر حدث لحظي في SSE
        pub_payload = {
            "event_type": "evidence_uploaded",
            "payload": {
                "evidence_id": "EVD-2026-905",
                "case_ref": "ARB-2026-0418",
                "standard": "ISO/IEC 27037:2012"
            }
        }
        resp = client.post("/api/events/publish", json=pub_payload)
        assert resp.status_code == 200
        print("  [✓] فحص نشر الأحداث اللحظية (/api/events/publish): ناجح")

        # 4. فحص قيد استئناف تحكيمي ذاتي (Mission 112)
        appeal_payload = {
            "case_id": "ARB-2026-0418",
            "appellant": "Rotterdam Logistics B.V.",
            "respondent": "Gulf Trade Holding LLC",
            "grounds": "ظهور مستند بوليصة شحن بحرية أصلي EVD-2026-901 في خزانة WORM ينفي واقعة التأخير",
            "evidence_worm_hash": valid_hash,
            "counsel_signature": "Counsel Hendrik Van Der Berg (NAI Netherlands)"
        }
        resp = client.post("/api/appeals/lodge", json=appeal_payload)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        appeal_res = resp.json()
        assert appeal_res["status"] == "ok"
        assert "APP-2026-0418" in appeal_res["docket"]["appeal_id"]
        assert len(appeal_res["docket"]["seal_sha256"]) == 64
        print(f"  [✓] فحص قيد الاستئناف الذاتي ({appeal_res['docket']['appeal_id']}): تم القيد والختم بـ SHA-256")

        # 5. فحص استرجاع قائمة ملفات الاستئناف
        resp = client.get("/api/appeals/list")
        assert resp.status_code == 200
        appeals_list = resp.json()
        assert appeals_list["total_appeals"] >= 2
        print(f"  [✓] فحص سجل الاستئنافات: إجمالي {appeals_list['total_appeals']} ملفات استئناف نشطة")

    print("=" * 70)
    print("🎉 كافة الفحوصات الـ 5 للمهام 110 و 111 و 112 اجتازت بنسبة 100% بنجاح!")
    print("=" * 70)

if __name__ == "__main__":
    run()
