import os
import sys
import json
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

# ضبط الترميز لدعم العربية في الطرفية
sys.stdout.reconfigure(encoding="utf-8")

from sr_agent_core import (
    create_sovereign_agent_config,
    SOVEREIGN_SYSTEM_INSTRUCTIONS,
    tool_get_service_details,
    tool_list_project_portals
)
from google.antigravity import Agent

class ChatRequest(BaseModel):
    message: str
    channel: Optional[str] = "web_portal"
    session_id: Optional[str] = "default"

class ConciergeRequest(BaseModel):
    message: str
    channel: Optional[str] = "whatsapp_cloud_api"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = create_sovereign_agent_config()
    print("=" * 65)
    print("  🚀 خادم S&R CoreSync Sovereign Agent API قيد التشغيل الآن")
    print(f"  🤖 النموذج النشط: {app.state.config.model}")
    print("  🌐 الواجهة متوافقة مع ai-concierge-simulator.html وتدعم SSE")
    print("=" * 65)
    yield
    print("🛑 إيقاف خادم الوكيل الذكي.")

app = FastAPI(
    title="S&R CoreSync Sovereign Agent Micro-API",
    description="خادم الويب والـ API المصغر للوكيل الذكي المحلي لمنظومة S&R CoreSync",
    version="1.0.0",
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

@app.get("/")
async def root():
    return {
        "service": "S&R CoreSync Sovereign Agent API",
        "status": "online",
        "model": app.state.config.model,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "endpoints": {
            "chat": "POST /api/chat",
            "ai_concierge": "POST /api/ai-concierge",
            "chat_stream": "GET /api/chat/stream?message=...",
            "portals": "GET /api/workspace/portals"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": True}

@app.get("/api/workspace/portals")
async def get_portals():
    return {"portals_summary": tool_list_project_portals()}

@app.post("/api/ai-concierge")
async def ai_concierge_endpoint(req: ConciergeRequest):
    """
    نقطة النهاية المتوافقة بنسبة 100% مع واجهة ai-concierge-simulator.html
    """
    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="رسالة فارغة")

    reply_text = ""
    source = "google_antigravity_agent"

    try:
        async with Agent(app.state.config) as agent:
            resp = await asyncio.wait_for(agent.chat(user_msg), timeout=60.0)
            reply_text = await resp.text()
    except Exception as e:
        # صمود سيادي: إذا حدث ضغط حصة مؤقت 429، يتم الرد من قاعدة المعرفة السيادية المعتمدة
        print(f"⚠️ تنبيه الوكيل (استخدام الرد السيادي الاحتياطي): {e}")
        reply_text = tool_get_service_details(user_msg)
        source = "sovereign_knowledge_engine"

    # صياغة الإجراءات الذكية المناسبة
    actions = [
        {"label": "💬 محادثة واتساب VIP المباشرة", "url": "https://wa.me/31618111116"},
        {"label": "📋 طلب عرض سعر مخصص (RFQ)", "action": "open_rfq"}
    ]

    return {
        "reply": reply_text,
        "actions": actions,
        "intent": "sovereign_executive_advisory",
        "confidence": 0.99,
        "channel": req.channel or "whatsapp_cloud_api",
        "source": source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """
    نقطة نهاية المحادثة العامة
    """
    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="رسالة فارغة")

    reply_text = ""
    source = "google_antigravity_agent"

    try:
        async with Agent(app.state.config) as agent:
            resp = await asyncio.wait_for(agent.chat(user_msg), timeout=60.0)
            reply_text = await resp.text()
    except Exception as e:
        reply_text = tool_get_service_details(user_msg)
        source = "sovereign_knowledge_engine"

    return {
        "reply": reply_text,
        "source": source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/chat/stream")
async def chat_stream_endpoint(message: str = Query(...)):
    """
    نقطة نهاية البث اللحظي للكلمات بنظام Server-Sent Events (SSE)
    """
    async def sse_generator():
        try:
            full_text = ""
            try:
                async with Agent(app.state.config) as agent:
                    resp = await asyncio.wait_for(agent.chat(message), timeout=60.0)
                    full_text = await resp.text()
            except Exception:
                full_text = tool_get_service_details(message)

            words = full_text.split(" ")
            for w in words:
                payload = json.dumps({"chunk": w + " "}, ensure_ascii=False)
                yield f"data: {payload}\n\n"
                await asyncio.sleep(0.02)
            yield "data: [DONE]\n\n"
        except Exception as e:
            err_payload = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {err_payload}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # التشغيل الافتراضي على المنفذ 8000
    uvicorn.run("sr_agent_server:app", host="127.0.0.1", port=8000, reload=False)

