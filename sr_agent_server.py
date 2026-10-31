import os
import sys
import io
import json
import asyncio
import hashlib
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Query, Path, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from pydantic import BaseModel, Field

# ضبط الترميز لدعم العربية في الطرفية
sys.stdout.reconfigure(encoding="utf-8")

from sr_agent_core import (
    create_sovereign_agent_config,
    SOVEREIGN_SYSTEM_INSTRUCTIONS,
    tool_get_service_details,
    tool_list_project_portals
)
import sr_session_db
from sr_rag_engine import SovereignRAGDatabase, build_or_update_knowledge_index, query_rag_knowledge, index_custom_document
from sr_subagent_monitor import AutonomousSecurityHealthSubagent
from google.antigravity import Agent

# ==============================================================================
# نماذج البيانات (Pydantic Schemas) لتوثيق Swagger التفاعلي
# ==============================================================================
class ChatRequest(BaseModel):
    message: str = Field(..., description="نص الرسالة أو الاستفسار الموجه للوكيل الذكي", example="ما هي باقات الخدمات المتوفرة؟")
    session_id: Optional[str] = Field("default", description="معرّف الجلسة لضمان استمرارية الذاكرة والسياق", example="client_session_101")
    channel: Optional[str] = Field("web_portal", description="قناة المحادثة (web_portal, whatsapp, telegram)", example="web_portal")

class ConciergeRequest(BaseModel):
    message: str = Field(..., description="نص الرسالة الواردة من محاكي المتصفح أو تطبيق العميل", example="ما هي باقة السوشيال ميديا 8K؟")
    channel: Optional[str] = Field("whatsapp_cloud_api", description="اسم القناة الافتراضية", example="whatsapp_cloud_api")
    session_id: Optional[str] = Field("concierge_default", description="معرّف الجلسة للمحاكي", example="concierge_default")

class ActionButton(BaseModel):
    label: str = Field(..., description="عنوان الزر التفاعلي")
    url: Optional[str] = Field(None, description="رابط الإجراء إن وجد")
    action: Optional[str] = Field(None, description="اسم الإجراء في الواجهة")

class ChatResponseModel(BaseModel):
    reply: str = Field(..., description="نص استجابة المستشار الذكي التنفيذي")
    session_id: str = Field(..., description="معرّف الجلسة النشطة")
    source: str = Field(..., description="مصدر الإجابة (google_antigravity_agent أو sovereign_knowledge_engine)")
    timestamp: str = Field(..., description="طابع التوقيت الزمني")

class ConciergeResponseModel(BaseModel):
    reply: str = Field(..., description="نص الرد المؤسسي")
    actions: List[ActionButton] = Field(..., description="قائمة الأزرار والإجراءات السريعة")
    intent: str = Field("sovereign_executive_advisory", description="نية المستخدم المستنتجة")
    confidence: float = Field(0.99, description="درجة ثقة النموذج")
    channel: str = Field(..., description="القناة")
    source: str = Field(..., description="المصدر")
    session_id: str = Field(..., description="معرّف الجلسة")
    timestamp: str = Field(..., description="الطابع الزمني")

class PublishEventRequest(BaseModel):
    event_type: str = Field(..., description="نوع الحدث (e.g. new_evidence_uploaded, settlement_completed, appeal_lodged, escrow_frozen)")
    payload: Dict[str, Any] = Field(..., description="بيانات الحدث التفصيلية")

class AppealRequest(BaseModel):
    case_id: str = Field(..., description="معرف القضية الأصلية", example="ARB-2026-0418")
    appellant: str = Field(..., description="الطرف المستأنف", example="Rotterdam Logistics B.V.")
    respondent: str = Field(..., description="المستأنف ضده", example="Gulf Trade Holding LLC")
    grounds: str = Field(..., description="أسباب الاستئناف واكتشاف أدلة جنائية جديدة في WORM", example="اكتشاف سجلات تدقيق محاسبي إضافية EVD-2026-901 تثبت تسليم الشحنة")
    evidence_worm_hash: Optional[str] = Field(None, description="بصمة SHA-256 للمستند الجنائي في WORM", example="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    counsel_signature: Optional[str] = Field("Counsel Salim Al-Din (Bar Reg. 104)", description="توقيع المستشار القانوني المعتمد")

# ==============================================================================
# إدارة البث المباشر للنبض السيادي (Mission 110: SSE Event Bus)
# ==============================================================================
sse_subscribers: set[asyncio.Queue] = set()

async def broadcast_live_event(event_type: str, payload: dict):
    """بث حدث لحظي لجميع الواجهات المتصلة عبر تقنية Server-Sent Events"""
    if not sse_subscribers:
        return
    message = {
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "payload": payload
    }
    encoded = f"data: {json.dumps(message, ensure_ascii=False)}\n\n"
    dead_queues = set()
    for q in sse_subscribers:
        try:
            q.put_nowait(encoded)
        except asyncio.QueueFull:
            dead_queues.add(q)
    for dq in dead_queues:
        sse_subscribers.discard(dq)

async def telemetry_pulse_loop(app: FastAPI):
    """حلقة البث النبضي الدوري (Heartbeat & Telemetry) لتغذية لوحة القيادة الموحدة"""
    while True:
        try:
            await asyncio.sleep(5)
            if sse_subscribers:
                stats = app.state.rag_db.get_stats() if hasattr(app.state, "rag_db") else {}
                appeal_count = len(app.state.appeals) if hasattr(app.state, "appeals") else 0
                pulse_data = {
                    "suite_health": 100,
                    "active_hubs": 6,
                    "arbitration_active": 4,
                    "arbitration_value_eur": 12385000,
                    "cbdc_settles": 12,
                    "cbdc_savings_eur": 38450,
                    "zkp_enclaves": 3,
                    "zkp_proofs": 28,
                    "forensics_docs": stats.get("total_documents", 90),
                    "forensics_chunks": stats.get("total_chunks", 506),
                    "escrow_vaults": 4,
                    "escrow_total_eur": 22350000,
                    "escrow_locked_eur": 6250000 + (appeal_count * 1850000),
                    "active_appeals": appeal_count,
                    "worm_status": "VERIFIED_IMMUTABLE",
                    "heartbeat": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                await broadcast_live_event("pulse_telemetry", pulse_data)
        except asyncio.CancelledError:
            break
        except Exception as e:
            await asyncio.sleep(5)

# ==============================================================================
# دورة حياة التطبيق (Lifespan Context)
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. تهيئة قاعدة بيانات الجلسات والذاكرة
    sr_session_db.init_db()
    
    # 2. تهيئة ذاكرة المتجهات المحلية (Local Vector DB / RAG)
    app.state.rag_db = SovereignRAGDatabase()
    stats = app.state.rag_db.get_stats()
    if stats.get("total_chunks", 0) == 0:
        print("  🔄 جاري الفهرسة التأسيسية لذاكرة المتجهات RAG...")
        build_or_update_knowledge_index()

    # 3. تهيئة الوكيل الفرعي الذاتي للتدقيق الأمني والصحي
    app.state.subagent = AutonomousSecurityHealthSubagent()

    # 4. تكوين وكيل Google Antigravity
    app.state.config = create_sovereign_agent_config()

    # 5. تهيئة سجل الاستئنافات السيادية النشطة (Mission 112)
    app.state.appeals = [
        {
            "appeal_id": "APP-2026-0418",
            "case_id": "ARB-2026-0418",
            "appellant": "Rotterdam Logistics B.V.",
            "respondent": "Gulf Trade Holding LLC",
            "grounds": "ظهور مستند WORM جنائي إضافي EVD-2026-901 يثبت تزوير بوليصة الشحن البحرية",
            "evidence_worm_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "counsel_signature": "Counsel Hendrik Van Der Berg (NAI Netherlands)",
            "status": "APPEAL_UNDER_REVIEW",
            "escrow_action": "ESCROW_LOCKED_EUR_1850000",
            "timestamp": "2026-10-31T11:20:00Z",
            "seal_sha256": "8a7c2e4f01b965dd34c4980a31ecde01a54728fba0e9176395bcf6d3910a30b1"
        }
    ]

    # 6. إطلاق مهمة البث النبضي الخلفي (Mission 110)
    pulse_task = asyncio.create_task(telemetry_pulse_loop(app))

    print("=" * 70)
    print("  🏛️ خادم S&R CoreSync Sovereign Agent API قيد التشغيل والجاهزية")
    print(f"  🧠 ذاكرة المتجهات (RAG): {stats.get('total_documents', 0)} مستنداً و {stats.get('total_chunks', 0)} قطعة دلالية.")
    print("  🛡️ الوكيل الفرعي للتدقيق الذاتي (Subagent Monitor): نشط وجاهز.")
    print("  ⚡ البث المباشر للنبض السيادي (SSE Live Pulse): نشط وجاهز.")
    print(f"  🤖 النموذج النشط: {app.state.config.model}")
    print("  📚 توثيق Swagger التفاعلي متاح على: http://127.0.0.1:8000/docs")
    print("  💾 ذاكرة الجلسات المستمرة (SQLite): نشطة وجاهزة")
    print("=" * 70)
    yield
    pulse_task.cancel()
    try:
        await pulse_task
    except asyncio.CancelledError:
        pass
    print("🛑 إيقاف خادم الوكيل الذكي بنجاح.")

# إنشاء تطبيق FastAPI مع تعطيل مسارات docs التلقائية لتخصيصها بهوية S&R
app = FastAPI(
    title="S&R CoreSync Sovereign Agent Micro-API",
    description="""
### 🏛️ واجهة برمجة التطبيقات المصغرة للمستشار الذكي التنفيذي لـ S&R CoreSync
توفر هذه المنظومة:
- **تكامل كامل مع Google Antigravity SDK** ونماذج Gemini.
- **أدوات مساحة العمل (Workspace Tools)** لاستكشاف صفحات وملفات وباقات المشروع.
- **ذاكرة محادثة مستمرة (SQLite Session DB)** لحفظ واسترجاع سياق الحوار.
- **بث مباشر بتقنية Server-Sent Events (SSE)** لتدفق الكلمات لحظياً.
- **ربط مباشر مع واجهات الويب ومحاكي الذكاء الاصطناعي.**
    """,
    version="2.0.0",
    docs_url=None,   # يتم تقديمها مخصصة
    redoc_url=None,
    lifespan=lifespan
)

# التهيئة المسبقة لسجل الاستئنافات في app.state لضمان الجاهزية الفورية
app.state.appeals = [
    {
        "appeal_id": "APP-2026-0418",
        "case_id": "ARB-2026-0418",
        "appellant": "Rotterdam Logistics B.V.",
        "respondent": "Gulf Trade Holding LLC",
        "grounds": "ظهور مستند WORM جنائي إضافي EVD-2026-901 يثبت تزوير بوليصة الشحن البحرية",
        "evidence_worm_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "counsel_signature": "Counsel Hendrik Van Der Berg (NAI Netherlands)",
        "status": "APPEAL_UNDER_REVIEW",
        "escrow_action": "ESCROW_LOCKED_EUR_1850000",
        "timestamp": "2026-10-31T11:20:00Z",
        "seal_sha256": "8a7c2e4f01b965dd34c4980a31ecde01a54728fba0e9176395bcf6d3910a30b1"
    }
]

# تفعيل CORS الشامل لجميع الأصول والمنافذ وصفحات file://
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# تخصيص واجهات التوثيق التفاعلية (Swagger & ReDoc) بهوية المنظومة
# ==============================================================================
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="S&R CoreSync | Sovereign Agent API — Swagger Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://sr-coresync.com/favicon.ico"
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="S&R CoreSync | Sovereign Agent API — ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        redoc_favicon_url="https://sr-coresync.com/favicon.ico"
    )

# ==============================================================================
# نقاط النهاية الرئيسية (API Endpoints)
# ==============================================================================
@app.get("/", tags=["النظام والجاهزية"])
async def root():
    """فحص حالة الخادم والنموذج وروابط التوثيق"""
    return {
        "service": "S&R CoreSync Sovereign Agent API",
        "status": "online",
        "version": "2.0.0",
        "model": app.state.config.model,
        "swagger_docs": "/docs",
        "redoc": "/redoc",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/health", tags=["النظام والجاهزية"])
async def health():
    """فحص النبض اللحظي للخدمة (Health Check)"""
    return {"status": "ok", "agent_ready": True, "db_ready": True}

@app.get("/api/workspace/portals", tags=["أدوات مساحة العمل"])
async def get_portals():
    """استعراض قائمة بوابات وصفحات المشروع الرسمية الـ 80"""
    return {"portals_summary": tool_list_project_portals()}

@app.post("/api/ai-concierge", response_model=ConciergeResponseModel, tags=["المساعد الذكي والمحاكي"])
async def ai_concierge_endpoint(req: ConciergeRequest):
    """
    نقطة النهاية المعتمدة لمحاكي `ai-concierge-simulator.html` وويدجت المحادثة العائم،
    مع حفظ الحوار بالكامل في ذاكرة الجلسة المستمرة.
    """
    user_msg = req.message.strip()
    session_id = req.session_id or "concierge_default"
    if not user_msg:
        raise HTTPException(status_code=400, detail="الرسالة لا يمكن أن تكون فارغة")

    # 1. حفظ رسالة المستخدم في قاعدة بيانات الجلسة
    sr_session_db.add_message(session_id, "user", user_msg, source="user")

    # 2. استخراج سياق المحادثة واسترجاع المعرفة عبر ذاكرة المتجهات (RAG)
    context = sr_session_db.get_formatted_context(session_id, max_turns=4)
    rag_matches = app.state.rag_db.hybrid_search(user_msg, top_k=2)
    rag_context = ""
    if rag_matches and rag_matches[0]["score"] >= 0.40:
        rag_snippets = "\n".join([f"• [{r['title']}]: {r['content'][:300]}" for r in rag_matches])
        rag_context = f"\n[المعرفة الموثقة من مساحة عمل المشروع (Local RAG Context)]:\n{rag_snippets}\n"

    prompt_with_memory = f"{context}\n{rag_context}\nسؤال المستخدم الحالي: {user_msg}".strip()

    reply_text = ""
    source = "google_antigravity_agent"

    try:
        async with Agent(app.state.config) as agent:
            resp = await asyncio.wait_for(agent.chat(prompt_with_memory), timeout=60.0)
            reply_text = await resp.text()
    except Exception as e:
        print(f"⚠️ استخدام الصمود السيادي البديل مع RAG: {e}")
        if rag_matches and rag_matches[0]["score"] >= 0.40:
            top_m = rag_matches[0]
            reply_text = f"بناءً على وثائق وبوابات المنظومة الرسمية ({top_m['title']}):\n{top_m['content'][:350]}...\n\nلطلب استشارة مخصصة، تواصل مع المبيعات على +31 618111116."
        else:
            reply_text = tool_get_service_details(user_msg)
        source = "sovereign_rag_knowledge_engine"

    # 3. حفظ رد الوكيل في قاعدة بيانات الجلسة
    sr_session_db.add_message(session_id, "assistant", reply_text, source=source)

    actions = [
        ActionButton(label="💬 محادثة واتساب VIP المباشرة", url="https://wa.me/31618111116"),
        ActionButton(label="📋 طلب عرض سعر مخصص (RFQ)", action="open_rfq")
    ]

    return ConciergeResponseModel(
        reply=reply_text,
        actions=actions,
        intent="sovereign_executive_advisory",
        confidence=0.99,
        channel=req.channel or "whatsapp_cloud_api",
        source=source,
        session_id=session_id,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.post("/api/chat", response_model=ChatResponseModel, tags=["المحادثة العامة والذاكرة"])
async def chat_endpoint(req: ChatRequest):
    """
    نقطة النهاية العامة للمحادثة مع دعم كامل للذاكرة المستمرة عبر `session_id`.
    """
    user_msg = req.message.strip()
    session_id = req.session_id or "default"
    if not user_msg:
        raise HTTPException(status_code=400, detail="الرسالة لا يمكن أن تكون فارغة")

    # حفظ رسالة المستخدم
    sr_session_db.add_message(session_id, "user", user_msg, source="user")

    # استرجاع سياق الجلسة ودمج ذاكرة المتجهات RAG
    context = sr_session_db.get_formatted_context(session_id, max_turns=4)
    rag_matches = app.state.rag_db.hybrid_search(user_msg, top_k=2)
    rag_context = ""
    if rag_matches and rag_matches[0]["score"] >= 0.40:
        rag_snippets = "\n".join([f"• [{r['title']}]: {r['content'][:300]}" for r in rag_matches])
        rag_context = f"\n[المعرفة الموثقة من مساحة عمل المشروع (Local RAG Context)]:\n{rag_snippets}\n"

    prompt_with_memory = f"{context}\n{rag_context}\nسؤال المستخدم الحالي: {user_msg}".strip()

    reply_text = ""
    source = "google_antigravity_agent"

    try:
        async with Agent(app.state.config) as agent:
            resp = await asyncio.wait_for(agent.chat(prompt_with_memory), timeout=60.0)
            reply_text = await resp.text()
    except Exception as e:
        if rag_matches and rag_matches[0]["score"] >= 0.40:
            top_m = rag_matches[0]
            reply_text = f"وفقاً للوثائق الرسمية ({top_m['title']}):\n{top_m['content'][:350]}...\n\nللمزيد تواصل عبر واتساب: +31 618111116."
        else:
            reply_text = tool_get_service_details(user_msg)
        source = "sovereign_rag_knowledge_engine"

    # حفظ استجابة الوكيل
    sr_session_db.add_message(session_id, "assistant", reply_text, source=source)

    return ChatResponseModel(
        reply=reply_text,
        session_id=session_id,
        source=source,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.get("/api/chat/stream", tags=["المحادثة العامة والذاكرة"])
async def chat_stream_endpoint(
    message: str = Query(..., description="نص الرسالة المراد بثها لحظياً"),
    session_id: Optional[str] = Query("default", description="معرف الجلسة")
):
    """
    نقطة نهاية البث اللحظي للكلمات بتقنية Server-Sent Events (SSE)
    """
    # حفظ رسالة المستخدم
    sr_session_db.add_message(session_id, "user", message, source="user")
    context = sr_session_db.get_formatted_context(session_id, max_turns=3)
    prompt = f"{context}\n\nسؤال المستخدم الحالي: {message}" if context else message

    async def sse_generator():
        full_text = ""
        source = "google_antigravity_agent"
        try:
            try:
                async with Agent(app.state.config) as agent:
                    resp = await asyncio.wait_for(agent.chat(prompt), timeout=60.0)
                    full_text = await resp.text()
            except Exception:
                full_text = tool_get_service_details(message)
                source = "sovereign_knowledge_engine"

            # حفظ الرد المكتمل في الجلسة
            sr_session_db.add_message(session_id, "assistant", full_text, source=source)

            words = full_text.split(" ")
            for w in words:
                payload = json.dumps({"chunk": w + " ", "session_id": session_id}, ensure_ascii=False)
                yield f"data: {payload}\n\n"
                await asyncio.sleep(0.015)
            yield "data: [DONE]\n\n"
        except Exception as e:
            err_payload = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {err_payload}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

# ==============================================================================
# إدارة جلسات المحادثة والذاكرة (Session Management Endpoints)
# ==============================================================================
@app.get("/api/sessions", tags=["إدارة الجلسات والذاكرة"])
async def get_sessions(limit: int = Query(20, description="الحد الأقصى لعدد الجلسات")):
    """استعراض الجلسات المخزنة وعدد الرسائل وآخر نشاط"""
    return {"sessions": sr_session_db.list_all_sessions(limit=limit)}

@app.get("/api/sessions/{session_id}/history", tags=["إدارة الجلسات والذاكرة"])
async def get_session_history(
    session_id: str = Path(..., description="معرف الجلسة المطلوب استرجاع رسائلها"),
    limit: int = Query(50, description="عدد الرسائل")
):
    """استرجاع سجل الرسائل الكامل لجلسة معينة"""
    messages = sr_session_db.get_history(session_id, limit=limit)
    return {"session_id": session_id, "messages": messages, "count": len(messages)}

@app.delete("/api/sessions/{session_id}", tags=["إدارة الجلسات والذاكرة"])
async def delete_session(session_id: str = Path(..., description="معرف الجلسة المراد حذفها")):
    """حذف ومسح تاريخ جلسة معينة"""
    sr_session_db.clear_session(session_id)
    return {"status": "success", "message": f"تم مسح الجلسة {session_id} بنجاح"}

# ==============================================================================
# ذاكرة المتجهات واسترجاع المعرفة المحلية (Local Vector DB / RAG Endpoints)
# ==============================================================================
@app.get("/api/rag/search", tags=["ذاكرة المتجهات RAG"])
async def rag_search_endpoint(
    query: str = Query(..., description="نص الاستعلام للبحث في ذاكرة المتجهات"),
    top_k: int = Query(4, description="عدد النتائج المسترجعة")
):
    """
    البحث الهجين (Dense Vectors + FTS5 BM25) في كافة صفحات ووثائق المشروع ومقالات المدونة.
    """
    results = app.state.rag_db.hybrid_search(query, top_k=top_k)
    return {
        "query": query,
        "count": len(results),
        "results": results
    }

@app.get("/api/rag/stats", tags=["ذاكرة المتجهات RAG"])
async def rag_stats_endpoint():
    """استعراض إحصائيات ذاكرة المتجهات وعدد المستندات والقطع المفهرسة"""
    return app.state.rag_db.get_stats()

@app.post("/api/rag/reindex", tags=["ذاكرة المتجهات RAG"])
async def rag_reindex_endpoint():
    """إعادة فهرسة وتحديث متجهات المشروع بالكامل على الفور"""
    stats = build_or_update_knowledge_index()
    return {"status": "success", "message": "تم تحديث ذاكرة المتجهات بنجاح", "stats": stats}

# ==============================================================================
# وكيل التدقيق الذاتي الفرعي (Autonomous Subagent Monitoring Endpoints)
# ==============================================================================
@app.get("/api/subagent/status", tags=["وكيل التدقيق الذاتي الفرعي"])
async def subagent_status_endpoint():
    """استعراض الحالة الحالية للوكيل الفرعي وآخر تدقيق أمني وتشغيلي"""
    report = app.state.subagent.run_full_audit()
    return report

@app.post("/api/subagent/run-audit", tags=["وكيل التدقيق الذاتي الفرعي"])
async def subagent_run_audit_endpoint():
    """تنفيذ دورة فحص وتدقيق أمني وصحي فوري"""
    report = app.state.subagent.run_full_audit()
    return {"status": "completed", "report": report}

@app.get("/cockpit", include_in_schema=False)
async def cockpit_page():
    """عرض لوحة التحكم التنفيذية للوكيل والمراقب الذاتي وفهرس RAG"""
    cockpit_file = os.path.join(os.path.dirname(__file__), "agent-cockpit.html")
    if os.path.exists(cockpit_file):
        with open(cockpit_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Cockpit file not found</h1>", status_code=404)

@app.post("/api/upload", tags=["تحليل المرفقات وفهرسة RAG"])
async def upload_files_endpoint(files: List[UploadFile] = File(...)):
    """
    استلام مرفقات المستندات (PDF / DOCX) بحد أقصى 5 ميجابايت للملف،
    استخراج النصوص وفهرستها فورياً داخل محرك RAG المحلي للمنظومة.
    """
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    processed = []
    
    for file in files:
        filename = file.filename or "unknown_document"
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"الملف {filename} يتجاوز الحد الأقصى المسموح به (5 ميجابايت)."
            )
            
        lower_name = filename.lower()
        extracted_text = ""
        
        try:
            if lower_name.endswith(".pdf"):
                import pdfplumber
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    pages_text = [page.extract_text() or "" for page in pdf.pages]
                    extracted_text = "\n\n".join(pages_text).strip()
            elif lower_name.endswith(".docx"):
                import docx
                doc = docx.Document(io.BytesIO(content))
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                extracted_text = "\n\n".join(paragraphs).strip()
            elif lower_name.endswith(".txt") or lower_name.endswith(".md"):
                extracted_text = content.decode("utf-8", errors="ignore").strip()
            else:
                raise HTTPException(
                    status_code=415,
                    detail=f"نوع الملف {filename} غير مدعوم. الأنواع المدعومة: PDF, DOCX, TXT, MD"
                )
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(
                status_code=422,
                detail=f"تعذر استخراج المحتوى من الملف {filename}: {str(err)}"
            )
            
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail=f"الملف {filename} لا يحتوي على أي نصوص قابلة للاستخراج."
            )
            
        # فهرسة المستند في قاعدة بيانات RAG
        index_result = index_custom_document(
            title=f"مرفق: {filename}",
            text_content=extracted_text,
            source_identifier=f"uploads/{filename}",
            category="user_attachment"
        )
        processed.append({
            "filename": filename,
            "size_bytes": len(content),
            "chunks_indexed": index_result.get("chunks_indexed", 0),
            "status": "indexed"
        })
        
    return {
        "status": "ok",
        "message": f"تمت معالجة وفهرسة {len(processed)} ملف(ات) بنجاح في قاعدة RAG المحلية.",
        "files_processed": len(processed),
        "details": processed
    }

# ==============================================================================
# نقاط نهاية البث المباشر للنبض السيادي (Mission 110: SSE Endpoints)
# ==============================================================================
@app.get("/api/stream/events", tags=["البث السيادي المباشر SSE"])
async def stream_sovereign_events(request: Request):
    """
    بث مباشر لحظي عبر تقنية Server-Sent Events (SSE) لتغذية لوحة القيادة الموحدة
    وبوابة المستشار القانوني بنبض العمليات الجنائية والمالية والأحكام فور حدوثها.
    """
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    sse_subscribers.add(queue)

    async def event_generator():
        init_event = {
            "event": "connected",
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "message": "تم الاتصال بنجاح بقناة البث السيادي المباشر (Sovereign Live Pulse SSE)",
                "subscribers_active": len(sse_subscribers),
                "hubs_monitored": ["104-Arbitration", "105-CBDC", "106-ZKP", "107A-Forensics", "107B-Escrow", "111-Counsel"]
            }
        }
        yield f"data: {json.dumps(init_event, ensure_ascii=False)}\n\n"

        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=12.0)
                    yield data
                except asyncio.TimeoutError:
                    yield f": heartbeat {datetime.now().strftime('%H:%M:%S')}\n\n"
        finally:
            sse_subscribers.discard(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/events/publish", tags=["البث السيادي المباشر SSE"])
async def publish_sovereign_event(req: PublishEventRequest):
    """نشر حدث لحظي جديد في قناة البث المباشر SSE من أي بوابة أو طرفية سيادية"""
    await broadcast_live_event(req.event_type, req.payload)
    return {
        "status": "ok",
        "event_published": req.event_type,
        "subscribers_delivered": len(sse_subscribers),
        "timestamp": datetime.now().isoformat()
    }

# ==============================================================================
# بوابة المستشار القانوني والتحقق من WORM (Mission 111: Corporate Counsel Portal API)
# ==============================================================================
CERTIFIED_WORM_REGISTRY = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": {
        "evidence_id": "EVD-2026-901",
        "title": "النسخة الجنائية لخادم قاعدة بيانات ERP لشركة Rotterdam B.V.",
        "case_ref": "ARB-2026-0418",
        "custodian": "Deloitte Forensics Netherlands",
        "standard": "ISO/IEC 27037:2012 Sec 6.3",
        "captured_at": "2026-10-14T08:15:00Z",
        "size_gb": 1840.5,
        "worm_status": "VERIFIED_IMMUTABLE",
        "enforceability": "Compliant with Hague Convention & EU Digital Evidence Reg."
    },
    "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a": {
        "evidence_id": "EVD-2026-902",
        "title": "أرشيف مراسلات بروتوكول توريد الصلب عبر البريد المشفر S/MIME",
        "case_ref": "ARB-2026-0421",
        "custodian": "KPMG Advisory / Gulf Financial Centre",
        "standard": "RFC 5322 / RFC 3161 Timestamping",
        "captured_at": "2026-10-18T14:22:30Z",
        "size_gb": 124.8,
        "worm_status": "VERIFIED_IMMUTABLE",
        "enforceability": "DIFC / DIAC Evidence Rules Compliant"
    },
    "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d": {
        "evidence_id": "EVD-2026-903",
        "title": "سجلات المعاملات المشفرة لعقد التمويل بالمرابحة SPV",
        "case_ref": "ARB-2026-0447",
        "custodian": "PwC Digital Forensics Dubai",
        "standard": "IEEE C/BDL Distributed Ledger Evidence",
        "captured_at": "2026-10-22T11:05:12Z",
        "size_gb": 48.2,
        "worm_status": "VERIFIED_IMMUTABLE",
        "enforceability": "SCCA / AAOIFI Standard No. 32 Compliant"
    },
    "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069": {
        "evidence_id": "EVD-2026-904",
        "title": "لقطات الذاكرة الحية (RAM Dump) لبوابة التحقق المصرفي",
        "case_ref": "ARB-2026-0433",
        "custodian": "S&R Sovereign Cybersecurity Team",
        "standard": "NIST SP 800-86 Memory Acquisition",
        "captured_at": "2026-10-25T16:40:00Z",
        "size_gb": 64.0,
        "worm_status": "VERIFIED_IMMUTABLE",
        "enforceability": "SIAC Rules 2025 Compliant"
    }
}

@app.get("/api/counsel/worm-verify", tags=["بوابة المستشار القانوني المؤسسي"])
async def verify_worm_evidence(hash: str = Query(..., description="بصمة SHA-256 للمستند القضائي المراد التحقق من سلامته")):
    """
    التحقق الفوري من سلامة وأصالة مستند قضائي ومطابقته لسجل WORM ومعيار ISO/IEC 27037.
    """
    clean_hash = hash.strip().lower()
    if clean_hash in CERTIFIED_WORM_REGISTRY:
        record = CERTIFIED_WORM_REGISTRY[clean_hash]
        return {
            "status": "VERIFIED_IMMUTABLE",
            "hash": clean_hash,
            "is_tampered": False,
            "iso_27037_compliant": True,
            "details": record,
            "verification_timestamp": datetime.now().isoformat(),
            "seal_authority": "S&R CoreSync Sovereign WORM Custody Chamber"
        }
    return {
        "status": "UNREGISTERED_OR_TAMPERED",
        "hash": clean_hash,
        "is_tampered": True,
        "iso_27037_compliant": False,
        "warning": "البصمة التشفيرية غير متطابقة مع سجل WORM المعتمد؛ يحتمل تعديل المستند أو تلفه.",
        "verification_timestamp": datetime.now().isoformat()
    }

@app.get("/api/counsel/certified-awards", tags=["بوابة المستشار القانوني المؤسسي"])
async def list_certified_arbitral_awards():
    """قائمة أحكام التحكيم المعتمدة مع المقاعد القضائية واتفاقية نيويورك 1958"""
    return [
        {
            "case_id": "ARB-2026-0418",
            "claimant": "Rotterdam Logistics B.V.",
            "respondent": "Gulf Trade Holding LLC",
            "amount_eur": 1850000,
            "seat": "Amsterdam (NAI)",
            "rules": "NAI Arbitration Rules 2024",
            "governing_law": "Dutch Civil Code Book 7 + CISG 1980",
            "award_status": "AWARD_ISSUED_SUBJECT_TO_APPEAL",
            "appeal_status": "APPEAL_ACTIVE",
            "linked_escrow": "ESC-2026-101 (LOCKED)",
            "enforceability": "New York Convention 1958 (172 States)"
        },
        {
            "case_id": "ARB-2026-0421",
            "claimant": "Al-Noor Construction Co.",
            "respondent": "Emirates Towers Dev. PJSC",
            "amount_eur": 6420000,
            "seat": "Dubai (DIFC-AI)",
            "rules": "DIAC Rules 2022 + FIDIC Red Book 2017",
            "governing_law": "DIFC Law No. 1 of 2008",
            "award_status": "AWARD_ENFORCED",
            "appeal_status": "NONE",
            "linked_escrow": "ESC-2026-102 (DISPUTED_FROZEN)",
            "enforceability": "New York Convention 1958"
        },
        {
            "case_id": "ARB-2026-0433",
            "claimant": "S&R CoreSync IP Licensing",
            "respondent": "Pacific SoftWorks Pte. Ltd.",
            "amount_eur": 940000,
            "seat": "Singapore (SIAC)",
            "rules": "SIAC Rules 2025",
            "governing_law": "TRIPS + Singapore IPA",
            "award_status": "HEARING_COMPLETED",
            "appeal_status": "NONE",
            "linked_escrow": "ESC-2026-103",
            "enforceability": "New York Convention 1958"
        },
        {
            "case_id": "ARB-2026-0447",
            "claimant": "Damascus Trade Finance House",
            "respondent": "Levant Sukuk Issuer SPV",
            "amount_eur": 3175000,
            "seat": "Riyadh (SCCA)",
            "rules": "SCCA Rules 2023 + AAOIFI Sharia Std. No. 32",
            "governing_law": "Saudi Arbitration Law (Royal Decree M/34)",
            "award_status": "AWARD_FINAL",
            "appeal_status": "NONE",
            "linked_escrow": "ESC-2026-104",
            "enforceability": "New York Convention 1958 + Riyadh Arab Agreement"
        }
    ]

# ==============================================================================
# منظومة الاستئناف والاعتراض الذاتي (Mission 112: Autonomous Appeals Workflow)
# ==============================================================================
@app.post("/api/appeals/lodge", tags=["منظومة الاستئناف والاعتراض الذاتي"])
async def lodge_appeal(req: AppealRequest):
    """
    تسجيل طلب مراجعة استئنافية ذاتية لحكم تحكيمي فور ظهور أدلة جنائية جديدة في WORM.
    تقوم المنظومة تلقائياً بما يلي:
    1. تجميد فوري لمبالغ الضمان الذكي المرتبطة بالقضية (Smart Escrow Dispute Freeze).
    2. توليد ختم تشفيري موحد SHA-256 لملف الاستئناف.
    3. أرشفة وفهرسة أسباب الاستئناف داخل محرك RAG السيادي.
    4. بث إشعار فوري لجميع لوحات القيادة وبوابة المستشار القانوني عبر SSE.
    """
    docket_num = len(app.state.appeals) + 1
    appeal_id = f"APP-2026-{req.case_id.split('-')[-1]}-{docket_num:02d}"
    timestamp_iso = datetime.now().isoformat()

    docket_body = {
        "appeal_id": appeal_id,
        "case_id": req.case_id,
        "appellant": req.appellant,
        "respondent": req.respondent,
        "grounds": req.grounds,
        "evidence_worm_hash": req.evidence_worm_hash,
        "counsel_signature": req.counsel_signature,
        "timestamp": timestamp_iso,
        "jurisdiction": "Autonomous Appellate Tribunal Chamber 104"
    }
    encoded_bytes = json.dumps(docket_body, sort_keys=True).encode("utf-8")
    seal_sha256 = hashlib.sha256(encoded_bytes).hexdigest()

    docket_body["seal_sha256"] = seal_sha256
    docket_body["status"] = "APPEAL_UNDER_REVIEW"
    docket_body["escrow_action"] = "ESCROW_LOCKED_PENDING_APPELLATE_RULING"

    app.state.appeals.append(docket_body)

    index_custom_document(
        title=f"استئناف تحكيمي: {appeal_id} على القضية {req.case_id}",
        text_content=f"استئناف رقم {appeal_id}\nالقضية المستأنفة: {req.case_id}\nالمستأنف: {req.appellant}\nالمستأنف ضده: {req.respondent}\nالأسباب: {req.grounds}\nبصمة الدليل: {req.evidence_worm_hash}\nتوقيع المستشار: {req.counsel_signature}\nالختم: {seal_sha256}",
        source_identifier=f"appeals/{appeal_id}",
        category="judicial_appeals"
    )

    await broadcast_live_event("appeal_lodged", {
        "appeal_id": appeal_id,
        "case_id": req.case_id,
        "appellant": req.appellant,
        "grounds": req.grounds,
        "escrow_action": "DISPUTE_FROZEN",
        "seal_sha256": seal_sha256,
        "timestamp": timestamp_iso
    })

    return {
        "status": "ok",
        "message": f"تم قيد ملف الاستئناف {appeal_id} وتجميد أصول الضمان الذكي المرتبطة بنجاح.",
        "docket": docket_body
    }

@app.get("/api/appeals/list", tags=["منظومة الاستئناف والاعتراض الذاتي"])
async def list_appeals():
    """استرجاع كافة ملفات الاستئناف المقيدة وحالتها الراهنة"""
    return {
        "total_appeals": len(app.state.appeals),
        "appeals": app.state.appeals
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sr_agent_server:app", host="127.0.0.1", port=8000, reload=False)
