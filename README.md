# 🏛️ منظومة الوكيل الذكي المحلي لشركة S&R CoreSync (Google Antigravity SDK)

توثيق شامل لبناء وتشغيل منظومة الوكلاء الأذكياء التنفيذيين محلياً باستخدام حزمة **Google Antigravity SDK** ونماذج **Gemini** المتقدمة، مع الربط الكامل بأدوات استكشاف مساحة العمل وخادم الويب المصغر وبوابات المشروع.

---

## 📁 هيكلية ملفات منظومة الذكاء الاصطناعي

```text
Project/
├── sr_agent_core.py            # المحرك الأساسي: ميثاق الهوية، أدوات مساحة العمل (Workspace Tools)، ودالة التهيئة
├── sr_agent_server.py          # خادم الويب المصغر (FastAPI / Uvicorn / SSE) ونقاط نهاية ai-concierge
├── interactive_agent.py        # واجهة المحادثة التفاعلية الحية عبر سطر الأوامر (CLI Terminal)
├── example_agent.py            # سكربت الإطلاق السريع لطلب واحد
├── ai-concierge-simulator.html # المحاكي التفاعلي المربوط تلقائياً بخادم الوكيل المحلي
├── requirements.txt            # الاعتماديات الرسمية (google-antigravity, fastapi, uvicorn, python-dotenv)
└── chat_history.txt            # سجل المحادثات المؤرخ تلقائياً
```

---

## 1️⃣ تثبيت الاعتماديات
```powershell
pip install -r requirements.txt
```

---

## 2️⃣ إعداد مفتاح الاتصال `.env`
تأكد من وجود المتغير في ملف `.env`:
```text
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 3️⃣ التشغيل التفاعلي عبر التيرمينال (CLI)
لبدء محادثة مباشرة مع المستشار التنفيذي الذكي:
```powershell
python -u interactive_agent.py
```
**المميزات:**
- محادثة متعددة الأدوار (Multi-turn Chat) باللغة العربية الفصحى الراقية.
- كتابة `بوابات` لاستعراض صفحات ومحاور المشروع مباشرة.
- كتابة `خروج` لإنهاء الجلسة وحفظ السجل المؤرخ في `chat_history.txt`.

---

## 4️⃣ تشغيل خادم الويب المصغر (FastAPI & SSE)
لتشغيل الخادم المحلي وربطه بالواجهات الرسومية:
```powershell
python sr_agent_server.py
```
أو عبر Uvicorn:
```powershell
python -m uvicorn sr_agent_server:app --host 127.0.0.1 --port 8000
```

### نقاط النهاية المتاحة (API Endpoints):
- **`GET /`**: فحص حالة الخادم ومعلومات النموذج والخدمات.
- **`POST /api/ai-concierge`**: متوافق تماماً مع محاكي [`ai-concierge-simulator.html`](ai-concierge-simulator.html) ويعيد الرد مصحوباً بإجراءات واتساب السريعة وروابط الـ RFQ.
- **`POST /api/chat`**: نقطة نهاية برمجية عامة لاستقبال الأسئلة وإرجاع الإجابات.
- **`GET /api/chat/stream?message=...`**: بث الكلمات لحظياً بتقنية **Server-Sent Events (SSE)**.
- **`GET /api/workspace/portals`**: ملخص فوري لصفحات وبوابات المشروع.

---

## 5️⃣ التكامل مع محاكي المتصفح (`ai-concierge-simulator.html`)
عند فتح صفحة `ai-concierge-simulator.html` في المتصفح وتشغيل خادم `sr_agent_server.py` محلياً، تقوم الواجهة تلقائياً بتوجيه الرسائل إلى `http://127.0.0.1:8000/api/ai-concierge`، ليجيب الوكيل التنفيذي بذكاء فائق بناءً على ميثاق المنظمة وأدواتها. وفي حال توقف الخادم المحلي، تتحول الواجهة تلقائياً وسلساً إلى السحابة أو المحرك الداخلي بدون أي انقطاع.

---

## 6️⃣ أدوات مساحة العمل (Workspace Tools المدمجة)
1. **`tool_list_project_portals()`**: فحص وقراءة بوابات وصفحات المشروع HTML.
2. **`tool_get_service_details(service_name)`**: جلب تفاصيل الخدمات التسع والباقات السعرية المعتمدة (€890 للسوشيال، €1,450 للموقع، €1,490 للباقة المتكاملة).
3. **`tool_read_project_overview(file_name)`**: قراءة مقتطفات من وثائق ومخططات المشروع.
## File Attachment Support

The platform now supports uploading PDF and DOCX documents for on‑the‑fly RAG indexing.

- **Endpoint**: `POST /api/upload`
- **Accepted file types**: `.pdf`, `.docx`
- **Maximum file size**: **5 MB** per file (larger files will be rejected with HTTP 413).
- **Response**: `{ "status": "ok", "files_processed": <int> }`

You can test the endpoint with `curl`:
```bash
curl -X POST http://127.0.0.1:8000/api/upload \
  -F "files=@path/to/document.pdf" \
  -F "files=@path/to/another.docx"
```

The uploaded content is extracted, added to the local RAG knowledge base, and becomes searchable by the agent.


---

## 7️⃣ Multi-Channel Alert & Webhook Dispatcher (`sr_alert_dispatcher.py`)

The platform includes an automated sovereign watchdog and multi-channel notification engine for operational alerts and security monitoring:

### Supported Notification Channels:
1. **External Webhooks (Non-blocking):**
   - **Slack Webhook**: Set `SLACK_WEBHOOK_URL` in `.env` (receives markdown alert cards).
   - **Discord Webhook**: Set `DISCORD_WEBHOOK_URL` in `.env` (receives embedded messages).
   - **Generic Webhook**: Set `ALERT_WEBHOOK_URL` in `.env` (works with Zapier, n8n, Make, or custom HTTP APIs).
   - **Telegram Bot API**: Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`.
2. **Native Desktop Alerts (Windows GUI):**
   - Non-blocking `ctypes MessageBoxW` modal notification.
   - Cross-platform system tray balloon notifications (`plyer` / `win10toast`).
   - Resilient `sys.stderr` console fallback.

### CLI Usage:
```powershell
# Send alert across all configured channels:
python sr_alert_dispatcher.py "High CPU utilization detected on RAG cluster"

# Test specific webhook directly:
python sr_alert_dispatcher.py "Test Alert" --webhook "https://hooks.slack.com/services/..."
```
