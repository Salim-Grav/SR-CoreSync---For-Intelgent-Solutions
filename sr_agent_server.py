import os
import sys
import json
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Query, Path
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
from sr_rag_engine import SovereignRAGDatabase, build_or_update_knowledge_index, query_rag_knowledge
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

    print("=" * 70)
    print("  🏛️ خادم S&R CoreSync Sovereign Agent API قيد التشغيل والجاهزية")
    print(f"  🧠 ذاكرة المتجهات (RAG): {stats.get('total_documents', 0)} مستنداً و {stats.get('total_chunks', 0)} قطعة دلالية.")
    print("  🛡️ الوكيل الفرعي للتدقيق الذاتي (Subagent Monitor): نشط وجاهز.")
    print(f"  🤖 النموذج النشط: {app.state.config.model}")
    print("  📚 توثيق Swagger التفاعلي متاح على: http://127.0.0.1:8000/docs")
    print("  💾 ذاكرة الجلسات المستمرة (SQLite): نشطة وجاهزة")
    print("=" * 70)
    yield
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sr_agent_server:app", host="127.0.0.1", port=8000, reload=False)
