"""
S&R CoreSync - Direct Test Suite for Mission 110 (SSE Live Pulse), 111 (Counsel WORM), 112 (Appeals)
"""
import sys
import os
import json
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding="utf-8")

from sr_agent_server import (
    app,
    verify_worm_evidence,
    list_certified_arbitral_awards,
    publish_sovereign_event,
    lodge_appeal,
    list_appeals,
    PublishEventRequest,
    AppealRequest
)

async def run_suite():
    print("=" * 70)
    print("🚀 بدء فحص المنطق التشغيلي للمهام 110 (SSE Live Pulse) و 111 (Counsel) و 112 (Appeals)")
    print("=" * 70)

    # 1. فحص التحقق من مستند WORM الجنائي (Mission 111)
    valid_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    res_valid = await verify_worm_evidence(hash=valid_hash)
    assert res_valid["status"] == "VERIFIED_IMMUTABLE", "WORM hash should be verified immutable"
    assert res_valid["iso_27037_compliant"] is True, "Must be ISO/IEC 27037 compliant"
    assert res_valid["is_tampered"] is False, "Document must not be tampered"
    print("  [✓] فحص WORM للمستند المعتمد EVD-2026-901: سليم 100% (ISO/IEC 27037 Verified)")

    # فحص كشف التلاعب للمستندات غير المعتمدة
    tampered_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    res_invalid = await verify_worm_evidence(hash=tampered_hash)
    assert res_invalid["status"] == "UNREGISTERED_OR_TAMPERED", "Expected tamper detection"
    assert res_invalid["is_tampered"] is True
    print("  [✓] فحص كشف التلاعب WORM: تم رصد البصمة غير المطابقة بنجاح (Tamper Detected)")

    # 2. فحص استرجاع قائمة أحكام التحكيم المعتمدة (Mission 111)
    awards = await list_certified_arbitral_awards()
    assert len(awards) >= 4, "Should have at least 4 certified awards"
    assert any(a["case_id"] == "ARB-2026-0418" for a in awards), "ARB-2026-0418 must be present"
    print(f"  [✓] فحص استرجاع أحكام التحكيم المعتمدة: تم استرجاع {len(awards)} أحكام تحكيمية متوافقة مع اتفاقية نيويورك 1958")

    # 3. فحص نشر حدث لحظي في SSE (Mission 110)
    pub_req = PublishEventRequest(
        event_type="evidence_uploaded",
        payload={
            "evidence_id": "EVD-2026-905",
            "case_ref": "ARB-2026-0418",
            "standard": "ISO/IEC 27037:2012"
        }
    )
    pub_res = await publish_sovereign_event(pub_req)
    assert pub_res["status"] == "ok"
    assert pub_res["event_published"] == "evidence_uploaded"
    print("  [✓] فحص نشر الأحداث اللحظية (/api/events/publish): سليم 100%")

    # 4. فحص قيد استئناف تحكيمي ذاتي وتجميد الضمان (Mission 112)
    appeal_req = AppealRequest(
        case_id="ARB-2026-0418",
        appellant="Rotterdam Logistics B.V.",
        respondent="Gulf Trade Holding LLC",
        grounds="اكتشاف مستند بوليصة شحن بحرية أصلي EVD-2026-901 في خزانة WORM ينفي واقعة التأخير",
        evidence_worm_hash=valid_hash,
        counsel_signature="Counsel Hendrik Van Der Berg (NAI Netherlands)"
    )
    appeal_res = await lodge_appeal(appeal_req)
    assert appeal_res["status"] == "ok"
    docket = appeal_res["docket"]
    assert "APP-2026-0418" in docket["appeal_id"]
    assert len(docket["seal_sha256"]) == 64
    assert docket["escrow_action"] == "ESCROW_LOCKED_PENDING_APPELLATE_RULING"
    print(f"  [✓] فحص قيد الاستئناف الذاتي ({docket['appeal_id']}): تم التوثيق والختم بـ SHA-256 وتجميد الضمان")

    # 5. فحص استرجاع قائمة ملفات الاستئناف النشطة (Mission 112)
    appeals_list = await list_appeals()
    assert appeals_list["total_appeals"] >= 2
    assert any(a["appeal_id"] == docket["appeal_id"] for a in appeals_list["appeals"])
    print(f"  [✓] فحص سجل الاستئنافات: إجمالي {appeals_list['total_appeals']} ملفات استئناف نشطة ومؤرشفة في RAG")

    print("=" * 70)
    print("🎉 كافة الفحوصات الـ 5 للمهام 110 و 111 و 112 اجتازت بنجاح تام بنسبة 100%!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_suite())
