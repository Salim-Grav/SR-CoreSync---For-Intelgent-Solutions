# ☁️ Cloudflare Worker — التقاط العملاء (Lead Capture)

> **S&R CoreSync For Intelligent Solutions — Sovereign Lead Capture**
> بديل بوابة `/api/lead-capture.php` التي لم تكن قابلة للتنفيذ على GitHub Pages.

---

## 1. لماذا هذا الـ Worker؟

الموقع الإنتاجي مستضاف على **GitHub Pages** (سجلات DNS تشير إلى
`185.199.108-111.153` والخادم `GitHub.com`). GitHub Pages **استضافة ثابتة
بالكامل** ولا تُنفِّذ PHP ولا Node.

النتيجة قبل هذا الإصلاح (مُتحقَّق منها حيّاً على `https://sr-coresync.com`):

| الطلب | السلوك السابق |
|---|---|
| `GET /api/lead-capture.php` | `200` + `Content-Type: application/x-httpd-php` → **كود PHP كامل معروض للمتصفح** |
| `POST /api/lead-capture.php` | `405 Method Not Allowed` → **لم يُسجَّل أي عميل محتمل إطلاقاً** |

كما أن `.htaccess` (161 سطراً مهيّأً لـ LiteSpeed/Apache) **لا يُطبَّق إطلاقاً**
على GitHub Pages، فكانت كل رؤوس الأمان (CSP، HSTS، COOP، CORP) **مفقودة**،
كانت ملفات `config/` و`api/` **قابلة للتحميل العام**.

---

## 2. ما الذي يفعله هذا الـ Worker؟

1. يستقبل طلب `POST` مع JSON يحتوي بيانات العميل المحتمل.
2. ينظّف كل حقل (إزالة HTML، تحديد الطول القصوى).
3. يرفض حركة الروبوتات (honeypot + تحديد معدّل).
4. يحفظ في Cloudflare KV (اختياري، اسم الربط `LEADS`).
5. يوزّع البيانات على webhooks التشغيل (Make / n8n / Google Sheets).
6. يُشعر صندوق البريد التنفيذي عبر ربط Email أو webhook.
7. يعيد استجابة JSON واضحة `{status, leadId, recorded, dispatched}`.

---

## 3. المسارات المدعومة

| الطريقة | المسار | الوظيفة |
|---|---|---|
| `GET` | `/health` | فحص الحياة (JSON) |
| `POST` | `/lead` | التقاط العميل المحتمل |
| `POST` | `/v1/lead` | مرادف |
| `POST` | `/api/lead` | مرادف (يُستخدم كمسار احتياطي على نفس النطاق) |
| `OPTIONS` | أي مسار | CORS preflight → `204` |

---

## 4. النشر

### 4.1 المتطلبات
- حساب Cloudflare (الطبقة المجانية تكفي).
- Node.js 20+ محلياً.

### 4.2 الخطوات

```bash
cd workers/sr-lead-capture
npm install

# 1) تسجيل الدخول
npx wrangler login

# 2) نشر الـ Worker
npx wrangler deploy
```

سيطبع Wrangler عنواناً مثل:
`https://sr-lead-capture.<subdomain>.workers.dev`

> **مهم:** هذا العنوان مؤقت. لأن رابط العملاء في `js/sr-lead-dispatcher.js`
> يشير إلى `https://api.sr-coresync.com/lead`، نضبط النطاق التالي.

### 4.3 الأسرار (Secrets)

```bash
npx wrangler secret put NOTIFY_EMAIL         # بريد استقبال التنبيهات
npx wrangler secret put RESEND_API_KEY       # تنبيه بريدي عبر Resend (اختر واحداً)
npx wrangler secret put BREVO_API_KEY        # تنبيه بريدي عبر Brevo  (اختر واحداً)
npx wrangler secret put LEAD_WEBHOOK_URLS    # اختياري: روابط Make / n8n / Sheets
npx wrangler secret put EMAIL_WEBHOOK_URL    # اختياري: endpoint يرسل البريد
```

ترتيب إرسال البريد: `SEND_EMAIL` (Cloudflare Email Routing) ← `RESEND_API_KEY`
← `BREVO_API_KEY` ← `EMAIL_WEBHOOK_URL`. أول خيار متاح يُستخدم فقط.

**متى يعمل `SEND_EMAIL`؟** بعد نقل النطاق إلى Cloudflare وتفعيل Email Routing؛
وقتها لا تحتاج أي مزوّد خارجي ولا أي مفتاح API.

### 4.4 مساحة تخزين KV (موصى به)

```bash
npx wrangler kv namespace create LEADS
```

ثم ضع المعرّف المُعاد في `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "LEADS"
id = "<YOUR_KV_NAMESPACE_ID>"
```

### 4.5 نطاق مخصص (api.sr-coresync.com)

**الخيار (أ) — نطاق فرعي (موصى به، لا يلمس Pages):**

1. في لوحة Cloudflare ← `Workers & Pages` ← `sr-lead-capture` ← `Settings` ← `Triggers`
2. `Add Custom Domain` ← `api.sr-coresync.com`
3. فعّل Auto DNS.

**الخيار (ب) — نفس النطاق (يتطلب Cloudflare أمام Pages):**

في `wrangler.toml`:
```toml
routes = [
  { pattern = "sr-coresync.com/api/*", zone_name = "sr-coresync.com" }
]
```
> هذا الخيار يتطلّب أن يكون `sr-coresync.com` مُداراً عبر Cloudflare (برتقالي)
> مع إعادة توجيه GitHub Pages. **الأكثر تعقيداً — استخدم الخيار (أ).**

### 4.6 اختبار سريع

```bash
curl -X POST https://api.sr-coresync.com/lead \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://sr-coresync.com' \
  -d '{"clientName":"Test Lead","email":"test@example.com","companyName":"QA","notes":"smoke test","language":"en"}'
```

الاستجابة المتوقعة:
```json
{ "status": "success", "leadId": "LEAD-SR-20261021-A1B2", "recorded": true, "dispatched": 1 }
```

### 4.7 إرسال العقد بالبريد (`POST /contract`)

يرسل نص العقد كاملاً في جسم الرسالة **مع ملف PDF مرفق**، ويتجنّب رابط Gmail
الطويل الذي كان يجمّد المتصفح.

```bash
curl -X POST https://sr-lead-capture.sr-coresync.workers.dev/contract \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://sr-coresync.com' \
  -d '{"to":"mudar@nlbilarabi.nl","subject":"العقد OF-2026-1021","text":"<نص العقد>","contractRef":"OF-2026-1021","attach":true}'
```

- المستقبِل يجب أن يكون داخل `CONTRACT_RECIPIENTS` وإلا يُرفض بـ 403.
- ملف الـPDF يُقرأ من KV بالمفتاح `contract:<ref>` (Base64).
- لتوليد PDFs وتحديثها بعد أي تغيير في صفحات العقد:

```bash
node scripts/generate_contract_pdfs.mjs <outDir>
# ثم ارفع كل ملف بعد تحويله إلى Base64:
node "node_modules/wrangler/bin/wrangler.js" kv key put "contract:OF-2026-1021" \
  --path <outDir>/OF-2026-1021.b64 --namespace-id <ID> --remote
```

- يتطلب مزوّد بريد مُهيّأ (`SEND_EMAIL` أو `RESEND_API_KEY` أو `BREVO_API_KEY`)،
  وإلا يعيد `502` مع `reason: no-email-provider`.

---

## 5. سجل المراقبة

```bash
npx wrangler tail
```

---

## 6. متغيرات البيئة

| المتغير | النوع | الوصف |
|---|---|---|
| `ALLOWED_ORIGINS` | var | النطاقات المسموح لها بـ CORS (مفصولة بفاصلة) |
| `LEAD_WEBHOOK_URLS` | secret | روابط relay (Make / n8n / Sheets) |
| `NOTIFY_EMAIL` | secret | بريد الاستقبال |
| `MAIL_FROM` | var | مرسل البريد |
| `RESEND_API_KEY` | secret | مفتاح Resend لإرسال التنبيهات |
| `BREVO_API_KEY` | secret | مفتاح Brevo لإرسال التنبيهات |
| `EMAIL_WEBHOOK_URL` | secret | مُرحِّل بريد اختياري |
| `SEND_EMAIL` | binding | إرسال عبر Cloudflare Email Routing (بعد نقل النطاق) |
| `LEADS` | KV | تخزين العملاء المحتملين |

---

## 7. الحماية المطبَّقة

| الحماية | التفصيل |
|---|---|
| CORS | قائمة بيضاء صريحة للنطاقات + `Vary: Origin` |
| تحديد الحجم | 16 KB كحد أقصى للـ body |
| تحديد المعدّل | 8 طلبات / 10 دقائق لكل (IP + User-Agent)، مُخزَّن في KV |
| Honeypot | الحقل `website` — يُقبل بصمت دون تخزين إن كان ممتلئاً |
| التنقية | إزالة وسوم HTML، قطع النصوص الطويلة، رفض الروابط غير http(s) |
| عدم التسريب | لا تُعاد أي بيانات مدخلات في الاستجابة |
| التحقق | اسم (≥2 حرف) + قناة اتصال واحدة على الأقل (بريد أو هاتف) |

---

## 8. بنية المشروع

```
workers/
├── sr-lead-capture/          ← هذا الـ Worker
│   ├── src/index.js          ← المعالج الرئيسي
│   ├── wrangler.toml         ← إعدادات النشر
│   ├── package.json
│   └── .dev.vars.example     ← نموذج الأسرار للتطوير
├── config/                   ← إعدادات خادمية (غير منشورة)
│   ├── lead-webhook-config.json
│   ├── payment-gateways.json
│   ├── dns-records.json
│   └── BIND_ZONE_FILE.txt
├── lib/                      ← وحدات Node للجهة الخلفية (مرجعية)
│   ├── email-notification-service.js
│   └── payment-webhook-service.js
└── legacy/                   ← بوابة PHP القديمة (مرجعية، غير منشورة)
    └── lead-capture.php
```

> مجلد `workers/` بالكامل **مستبعَد من النشر** على GitHub Pages
> (انظر `.github/workflows/deploy-pages.yml`).

---

**التاريخ:** الخميس، 22 أكتوبر 2026 — الساعة 12:43 فجراً
