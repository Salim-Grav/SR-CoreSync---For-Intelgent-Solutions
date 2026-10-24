# نشر الـ Worker — الخطوات التنفيذية

> كل ما سبق (الإشعارات الحقيقية، وصول الاستفسارات، بريد التنبيه) متوقف على هذه الخطوة.
> `api.sr-coresync.com` لا يُحلّ حاليًا، لذلك نموذج العملاء يُحفظ في متصفح الزائر فقط.

## المتطلبات
| # | المطلوب | لماذا |
|---|---|---|
| 1 | حساب Cloudflare (Free) | الاستضافة + النطاق المخصّص |
| 2 | `sr-coresync.com` مُدار من Cloudflare | لازم للنطاق `api.` ولتفعيل رؤوس الأمان |
| 3 | مفتاح **Resend** أو **Brevo** | إرسال بريد التنبيه (الـ Worker يستخدم أيهما وُجد) |
| 4 | Node 18+ و npx | تشغيل wrangler |

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
