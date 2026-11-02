# حزمة إصلاحات P0 — خادم الوكيل السيادي S&R CoreSync

هذه الحزمة هي التنفيذ العملي لبنود الأولوية القصوى (P0) الواردة في تقرير التدقيق الأمني، وتعالج أيضاً عدداً من النتائج مرتفعة الخطورة. تتكون من 4 رقع Git متتابعة + ملفات كاملة جاهزة للنسخ + حزمة اختبار دخاني أثبتت نجاح **16/16 فحصاً**.

## 1. خريطة الرقع مقابل نتائج التدقيق

| الرقعة | العنوان | النتائج المعالجة | الملفات |
|---|---|---|---|
| `0001` | طبقة المصادقة السيادية والحد من المعدل | **A1** (حرج)، جزء من **A8** | `sr_auth.py` جديد، `scripts/generate_auth_keys.py` جديد |
| `0002` | فرض المصادقة، تقييد CORS، تحصين الرفع، ملكية الجلسات | **A1، A3، A4** (مرتفع)، **A8** (متوسط) | `sr_agent_server.py`، `sr_session_db.py`، `.env.example` |
| `0003` | سياق بناء Docker بقائمة بيضاء | **P1** (حرج)، **P5** (متوسط) | `Dockerfile`، `.dockerignore`، `docker-compose.yml` |
| `0004` | وقف إيداع مخلفات التشغيل + تنظيف التاريخ | **P2، P3** (مرتفع) | `.gitignore`، `scripts/git_history_purge.sh` جديد |

الأثر الإجمالي: 11 ملفاً، ‎+1001 سطراً / −49 سطراً.

## 2. التطبيق — الطريقة الأولى (موصى بها): عبر Git

من جذر مستودع نظيف على الفرع `main` (نفس الالتزام الأساس `638ea47` أو أحدث):

```bash
git am patches/0001-security-a1-add-sovereign-API-key-auth-layer-rate-li.patch
git am patches/0002-security-a1-a3-a4-a8-enforce-auth-restrict-CORS-hard.patch
git am patches/0003-security-p1-p5-whitelist-build-context-defense-in-de.patch
git am patches/0004-security-p2-p3-stop-committing-runtime-artifacts-his.patch
```

وإن فضّلت التطبيق دون إنشاء التزامات (يبقى التغيير في منطقة الـ staging):

```bash
git apply --index patches/*.patch
```

> ملاحظة: الرقع مُختبرة ضد التزام الأساس `638ea472` ("perf(index): extract 3 heavy inline scripts…"). إن تقدّم `main` عنه، فإن `git am` عادةً يعالج الفروقات البسيطة تلقائياً؛ وعند التعارض استخدم `git am --3way`.

## 3. التطبيق — الطريقة الثانية: نسخ الملفات الكاملة

انسخ محتويات مجلد `full_files/` إلى جذر المستودع (مع الحفاظ على البنية):

```
full_files/
├── sr_auth.py                     ← جديد
├── sr_agent_server.py             ← يستبدل الموجود
├── sr_session_db.py               ← يستبدل الموجود
├── .env.example                   ← يستبدل الموجود
├── .gitignore                     ← يستبدل الموجود
├── Dockerfile                     ← يستبدل الموجود
├── .dockerignore                  ← يستبدل الموجود
├── docker-compose.yml             ← يستبدل الموجود
├── scripts/generate_auth_keys.py  ← جديد
├── scripts/git_history_purge.sh   ← جديد (chmod +x)
└── web/coresync-auth.js           ← جديد (جسر الواجهة الأمامية)
```

## 4. التهيئة بعد التطبيق (إلزامية — الخادم مُغلق افتراضياً)

بعد الرقعة، **لا يعمل أي مسار محمي حتى تُعرَّف المفاتيح** (يرد الخادم بـ 503 `auth_not_configured`). ولأن كل نقاط النهاية الـ 24 كانت مكشوفة سابقاً، هذه هي النتيجة المرغوبة.

### أ) توليد المفاتيح

```bash
# مفتاح إدارة (admin) — احفظ المخرج في مدير أسرار فوراً؛ يُعرض مرة واحدة
python scripts/generate_auth_keys.py --name ops-console --role admin

# مفاتيح عملاء (client) للواجهات والويدجت
python scripts/generate_auth_keys.py --client site-widget
python scripts/generate_auth_keys.py --client mobile-app
```

ينتج ذلك ملف `auth_keys.json` يضم بصمات SHA-256 فقط بصلاحيات 600 (وهو مُستثنى من Git عبر `.gitignore` الجديد).

### ب) بدائل عبر متغيرات البيئة (انظر `.env.example` المحدث)

```bash
export CORESYNC_API_KEYS="ops-console:$ADMIN_PLAIN_KEY:admin,site-widget:$CLIENT_PLAIN_KEY:client"
export CORESYNC_CORS_ORIGINS="https://sr-coresync.com,https://www.sr-coresync.com,http://127.0.0.1:8000"
export CORESYNC_RATE_LIMIT="120/min"
export CORESYNC_CHAT_RATE_LIMIT="10/min"
# للتطوير المحلي فقط على 127.0.0.1:
# export CORESYNC_AUTH_DISABLED=1
```

### ج) التشغيل والتحقق السريع

```bash
python -m uvicorn sr_agent_server:app --host 127.0.0.1 --port 8000
```

| الفحص | الأمر المتوقع |
|---|---|
| الصحة العامة (بلا مفتاح) | `curl -s http://127.0.0.1:8000/health` → `200` |
| حماية عامة | `curl -s http://127.0.0.1:8000/api/rag/stats` → `401` |
| مصادقة سليمة | `curl -s -H 'X-API-Key: ...' http://127.0.0.1:8000/api/rag/stats` → `200` |
| فرض الدور | `curl -H 'X-API-Key: <client>' /api/sessions` → `403` |
| التوثيق محمي | `curl -s http://127.0.0.1:8000/docs` → `401` (للوصول: `/docs?api_key=...`) |

## 5. تكامل الواجهة الأمامية

صفحات الموقع (المحاكي، لوحة القيادة، الويدجت) تستدعي `/api/` عبر `fetch` دون ترويسات، فستتوقف بعد تفعيل الحماية — هذا متعمد. الحل:

1. ضع مفتاح **client** (وليس admin) في `localStorage` للأجهزة الموثوقة:
   ```js
   localStorage.setItem('CORESYNC_API_KEY', 'srk_...');
   ```
2. أدرج `full_files/web/coresync-auth.js` قبل سكربتات المحادثة في الصفحات ذات الصلة:
   ```html
   <script src="/coresync-auth.js"></script>
   ```
   يضيف الجسر ترويسة `X-API-Key` تلقائياً لكل نداء `/api/`، ويتيح `coresyncEventSource(url)` لقنوات SSE.

> للحماية من تمرير مفتاح admin عبر صفحات عامة: استخدم مفاتيح client في الواجهات، واحتفظ بمفاتيح admin للسطر المؤمّن (ops).

## 6. الاختبار الدخاني المرفق (16/16 ناجح)

`smoke_test/p0_smoke_test.py` يشغّل التطبيق داخل الذاكرة (مع محاكاة SDK في `smoke_test/stubs/`، بلا شبكة ولا Gemini) ويتحقق من:

- **T1–T7، T14**: الصحة العامة 200، الرفض 401 بلا/بمفتاح خاطئ، منع client من مسارات admin بـ 403، حماية `/docs`.
- **T8–T9**: ملكية الجلسات (A8) — المالك 200، عميل آخر 403، admin 200.
- **T10**: CORS — أصل خبيث بلا إذن، أصل موثوق يصله `access-control-allow-origin`.
- **T11**: حد معدل المحادثة — يظهر 429 بعد تجاوز السقف مع `Retry-After`.
- **T12**: رفع يتجاوز الحد الكلي عبر `Content-Length` → 413 قبل قراءة أي بايت.
- **T13**: الإغلاق الافتراضي — بلا مفاتيح: 503 للمحمي و200 للصحة.

التشغيل:

```bash
pip install fastapi uvicorn httpx python-dotenv
python smoke_test/p0_smoke_test.py
```

## 7. P0-4 — تنظيف تاريخ Git وتدوير الأسرار (الأهم في الحزمة)

تحذير صريح: **إزالة الملفات من التاريخ لا "تلغي" تسريبها**. أي fork أو نسخة مستنسخة سابقة يملكها طرف آخر ما زالت تحوي `.env.vault` وقواعد بيانات الجلسات. لذا نفّذ الأمرين معاً وبالتوازي:

1. **تدوير كل الأسرار فوراً**: MOLLIE، STRIPE (المفتاح السري + سر الويب هوك)، SMTP، SENDGRID، POSTMARK، GEMINI، وكل ما داخل `.env.vault` مع إعادة توليد مفتاح master الخاص بها.
2. ثم نظّف التاريخ:

```bash
bash scripts/git_history_purge.sh --dry-run   # استعرض ما سيُزال أولاً
bash scripts/git_history_purge.sh             # نسخة احتياطية bundle + إعادة كتابة + إرشادات force-push
```

السكربت يزيل من كامل التاريخ: `.env.vault`، `chat_history.txt`، `sr_agent_sessions.db`، `sr_rag_knowledge.db`، سجلات الخادم الأربعة، `sr_subagent_audit.log`، ومجلد `uploads/` — ويطلب تأكيداً كتابياً (`PURGE`) قبل التنفيذ، ويحفظ نسخة احتياطية كاملة بصيغة bundle قبل أي تغيير.

## 8. حدود وملاحظات صادقة

- **حد المعدل في الذاكرة**: العدّاد لكل عملية worker على حدة. عند التشغيل بعمليات متعددة أو خلف موزع أحمال، طبّق حداً مركزياً (Redis أو قواعد الحد في الوكيل العكسي مثل nginx `limit_req`).
- **مفتاح الاستعلام `?api_key=`**: مدعوم لأن `EventSource` لا يقبل ترويسات؛ يظهر المفتاح في سجلات الوكيل العكسي. استخدمه عبر HTTPS فقط ويفضَّل التحويل إلى fetch-based SSE لاحقاً.
- **الجلسات القديمة**: الجلسات المخزنة قبل الرقعة بلا مالك (تُعلَّم `legacy`) وتتطلب مفتاح admin للوصول إليها — قرار مقصود لحماية بيانات قائمة.
- **`docs/` مُستبعدة من الـ webroot** في رقعة Docker لأنها وثائق تشغيل داخلية؛ لم يُرصد أي رابط عام يشير إليها في صفحات الموقع. إن كانت مطلوبة عمومية أضف `!/docs` و`!/docs/**` إلى `.dockerignore`.
- **نطاق الإصلاح**: هذه الحزمة تعالج بنود P0 فقط. بنود مثل A5 (البحث «الدلالي» الزائف)، A6 (SSE محاكى)، A7 (سجل WORM مزيّف)، P4 (SecureVault XOR) تبقى بنداً لتطوير لاحق وفق خارطة الطريق في التقرير.
- **رفع الملفات** أصبح مشدداً (5 ملفات × 5MB بقراءة تدفقية) لكن حقن المعرفة عبر `index_custom_document` يبقى محصوراً بمفاتيح admin فقط — راجع سياسة قبول المستندات عند فتح الرفع للعملاء.

## 9. محتويات الحزمة

```
SR-CoreSync_P0_Patches/
├── README_دليل_التطبيق.md   ← هذا الملف
├── patches/                 ← الرقع الأربع (git am / git apply)
├── full_files/              ← النسخ الكاملة لكل الملفات الجديدة والمعدلة
└── smoke_test/              ← الاختبار الدخاني + محاكاة SDK
```
