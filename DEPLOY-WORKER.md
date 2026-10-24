# نشر الـ Worker — الخطوات التنفيذية

> كل ما سبق (الإشعارات الحقيقية، وصول الاستفسارات، بريد التنبيه) متوقف على هذه الخطوة.
> `api.sr-coresync.com` لا يُحلّ حاليًا، لذلك نموذج العملاء يُحفظ في متصفح الزائر فقط.

## المتطلبات
| # | المطلوب | لماذا |
|---|---|---|
| 1 | حساب Cloudflare (Free) | الاستضافة + النطاق المخصّص |
| 2 | `sr-coresync.com` مُدار من Cloudflare | لازم للنطاق `api.` ولتفعيل رؤوس الأمان |
| 3 | صندوق Purelymail (info@) | إرسال بريد التنبيه من نطاقنا نفسه، بلا مزوّد إضافي |
| 4 | Node 18+ و npx | تشغيل wrangler |

> لم تعد هناك حاجة إلى Resend أو Brevo: الـ Worker يرسل عبر SMTP الخاص بصندوقنا
> (`smtp.purelymail.com:587` + STARTTLS). Cloudflare يحجب المنفذ 25 فقط، والمنفذ 587 مسموح.
> تبقى القنوات القديمة مدعومة تلقائيًا إن أضفت مفاتيحها لاحقًا.

## 0. أسرار البريد (مطلوب لتفعيل الإشعارات)
المتغيّران العاديان `PURELYMAIL_USER` و`NOTIFY_EMAIL` صارا في `wrangler.toml` (ليسا سرّين)،
فلم يبقَ إلا كلمة مرور الصندوق:
```powershell
cd "workers/sr-lead-capture"
npx wrangler secret put PURELYMAIL_PASS    # كلمة مرور info@sr-coresync.com
```
أو من لوحة Cloudflare: Workers → sr-lead-capture → Settings → Variables and Secrets
→ أضف `PURELYMAIL_PASS` بنوع **Secret** (وإن أضفت `PURELYMAIL_USER` هناك فالقيمة نفسها).

### التحقق بعد الإضافة
```powershell
# هل الأسرار موجودة؟
Invoke-RestMethod "https://sr-lead-capture.sr-coresync.workers.dev/health"
# هل كلمة المرور تعمل فعلًا؟ (مصادقة حقيقية، بلا إرسال رسالة)
Invoke-RestMethod "https://sr-lead-capture.sr-coresync.workers.dev/mail/check?deep=1"
# هل سجلات DNS صحيحة كما تراها الخدمة؟
Invoke-RestMethod "https://sr-lead-capture.sr-coresync.workers.dev/mail/dns"
```
`/health` يعطي `purelymail: on|off` للوجود فقط، و`/mail/check?deep=1` هو ما يثبت الصلاحية
(محدود مرة كل 5 دقائق عبر KV لكيلا يُستنزف الصندوق).


## 1. التحضير
```powershell
cd "workers/sr-lead-capture"
npm ci
npx wrangler login        # يفتح المتصفح لتفويض الحساب
```

## 2. KV — مُعدّ مسبقًا
`wrangler.toml` يحتوي بالفعل رابط KV:
```toml
[[kv_namespaces]]
binding = "LEADS"
id = "d23f177169fb4501b854056e67d21ed5"
```
تحقّق فقط:
```powershell
npx wrangler kv namespace list
```
> لو أنشأت مساحة جديدة، أنشئها بـ `npx wrangler kv namespace create LEADS` ثم ضع المعرّف الناتج مكان القديم.

## 3. الأسرار
```powershell
npx wrangler secret put RESEND_API_KEY     # أو BREVO_API_KEY
npx wrangler secret put NOTIFY_EMAIL       # info@sr-coresync.com
```
المتغيّرات غير السرية موجودة في `[vars]` داخل `wrangler.toml`:

| المتغيّر | القيمة الحالية | ملاحظة |
|---|---|---|
| `MAIL_FROM` | `leads@sr-coresync.com` | **بعد** إعداد DKIM بدّل إلى `leads@send.sr-coresync.com` |
| `ALLOWED_ORIGINS` | نطاقات الموقع | يجب أن تضم `https://sr-coresync.com` |
| `EVENTS_PUBLIC` | غير موجود | أضِفه `= "1"` فقط عندما تريد إظهار الأحداث العامة |

لإضافة `EVENTS_PUBLIC` إلى `wrangler.toml`:
```toml
[vars]
EVENTS_PUBLIC = "1"
```

## 4. النشر
```powershell
npx wrangler deploy
```
سيطبع رابطًا مثل `https://sr-lead-capture.<account>.workers.dev`.

## 5. النطاق المخصّص `api.sr-coresync.com`
افتح `wrangler.toml` وأزل التعليق:
```toml
routes = [
  { pattern = "api.sr-coresync.com", custom_domain = true }
]
```
ثم:
```powershell
npx wrangler deploy
```
أو من اللوحة: Workers → `sr-lead-capture` → Settings → Domains & Routes → Add Custom Domain.

## 6. التحقق (بالترتيب)
```powershell
# 1) صحة الخدمة
Invoke-RestMethod https://api.sr-coresync.com/health

# 2) الإحصاءات (بلا بيانات شخصية)
Invoke-RestMethod https://api.sr-coresync.com/stats

# 3) الأحداث العامة (تُرجع enabled=false ما لم تُضبط EVENTS_PUBLIC)
Invoke-RestMethod https://api.sr-coresync.com/events/recent

# 4) استفسار تجريبي حقيقي
$body = @{ name='Test Client'; email='test@example.com'; phone='+31600000000'; source='contact'; message='deployment smoke test' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri https://api.sr-coresync.com/lead -ContentType 'application/json' -Body $body
```
النتيجة المتوقعة: `status: success` + وصول بريد إلى `NOTIFY_EMAIL`.

> لو ظهر `403 Origin not allowed` فالطلب جاء من أصل غير مسجّل — أضفه إلى `ALLOWED_ORIGINS`.

## 7. تفعيل الإشعارات على الموقع
```powershell
python scripts/enable_live_feed.py
```
يضيف سطرًا واحدًا قبل الوحدة في **30 صفحة**:
```html
<script>window.SR_FEED_BASE = 'https://api.sr-coresync.com';</script>
```
للتراجع: `python scripts/enable_live_feed.py --disable`.

## 8. بعد النشر — تحقق نهائي
```powershell
node scripts/verify_dns_records.js   # يجب أن يتحوّل FAIL (DMARC) إلى PASS بعد إضافة السجل
node scripts/browser_console_audit.mjs
```
> مع `EVENTS_PUBLIC="1"` ستظهر بطاقتان أو ثلاث للزائر. المحتوى **مجموع بلا هوية**:
> تصنيف + وقت فقط، ولا اسم/بريد/هاتف/مدينة.

## ما لا يفعله الـ Worker
- لا يخزّن بيانات بطاقات (الدفع عبر Mollie/Stripe في المتصفح).
- لا يرسل بيانات شخصية إلى المتصفح: `/stats` و`/events/recent` محسوبان من فهرس
  KV ويحتويان عددًا وطابعًا زمنيًا فقط.
- لا يعمل بلا `LEADS`: عند غياب الرابط يظل يرسل البريد لكن دون تخزين.

---

## تنبيه Telegram (القناة الفعّالة حاليًا)

بدل انتظار مزوّد بريد وسجلات DKIM على نطاق فرعي، يعمل التنبيه الفوري عبر بوت
تيليجرام — **بلا DNS وبلا مزوّد خارجي**.

```powershell
# مرة واحدة: @BotFather -> /newbot -> انسخ التوكن، ثم أرسل للبوت أي رسالة
python scripts/setup_telegram.py --apply      # يكتشف chat_id ويكتب السرّين وينشر
python scripts/setup_telegram.py --test       # يجب أن يطبع True
```

التحقق الحقيقي:
```powershell
cd workers/sr-lead-capture
node node_modules/wrangler/bin/wrangler.js tail --format json   # راقب سجلات الـ Worker
# في نافذة أخرى أرسل استفسارًا؛ يجب أن يظهر: "telegram=sent"
```

آخر تحقق (2026-10-24 10:30): استفسار `LEAD-SR-20261024-T3TX` → `telegram=sent`.

> **أمان:** التوكن يُدخَل مخفيًا ولا يُكتب في أي ملف، ويُستخدم في رابط الـ API فقط.
> إن ظهر التوكن في أي محادثة أو سجل، أبطله من BotFather (`/revoke`) وأعد التنفيذ.

---

## القناة الثانية المستقلة (relay)

Telegram قناة واحدة؛ لو تعطّلت (توكن مبطَل، حجب، انقطاع) يبقى الاستفسار محفوظًا
بلا تنبيه. `LEAD_WEBHOOK_URLS` هو المسار المستقل: يستقبل كل استفسار ويحوّله إلى
أي خدمة (Make / n8n / Slack / بريد عبر خدمة أخرى) — بلا كود إضافي.

**تفعيله بأمر واحد:**
```powershell
python scripts/configure_lead_webhook.py --url https://hook.eu1.make.com/xxxxxxxx
# عدة وجهات: --url "https://a..., https://b..."
python scripts/configure_lead_webhook.py --show     # الحالة الحالية
python scripts/configure_lead_webhook.py --remove   # التعطيل
```

الأمر يكتب المتغيّر في `wrangler.toml`، يعيد النشر، ويطبع `webhooks=N` من `/health`.

**كيف يظهر أثره:**
- إذا نجح Telegram → `announced: "sent"`.
- إذا فشل Telegram ونجح الـ relay → `announced: "sent:webhook"` (لا يُحتسب متأخرًا).
- إذا فشل الاثنان → `announced: "failed:<السبب>"` ويظهر في عدّاد `NOT ALERTED`.

استجابة `POST /lead` تحتوي الآن `announced` صراحةً، فيمكن لأي مراقب معرفة ما حدث
دون قراءة سجلات.
