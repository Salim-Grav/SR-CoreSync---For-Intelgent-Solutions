# الانتقال الجذري إلى Cloudflare — دليل التنفيذ

> ## ⚠️ قرار مالك المشروع (2026-10-24): **لا نقل للنطاق**
> Nameservers تبقى عند Hostinger. لذلك هذا الدليل ينقسم إلى قسمين:
>
> **ما يعمل بدون أي تغيير في DNS (منفَّذ ومُختبَر):**
> - الـ Worker على `*.workers.dev` → استفسارات محفوظة + بريد + إشعارات حقيقية + `/pay/webhook` + `/tax`.
> - ربط الموقع به: `python scripts/configure_api_base.py --base https://<worker>.<sub>.workers.dev`
>
> **ما لا يمكن بدون نقل النطاق:** رؤوس الأمان الحقيقية (CSP/HSTS)، 301 على GitHub Pages،
> والنطاق `api.sr-coresync.com`. البديل الوحيد بلا نقل NS هو استضافة تدعم `_headers`
> وتُربط بسجل **CNAME واحد** (Netlify/Vercel) — انظر القسم 8.

> الغاية: إنهاء حالة «موقع بلا خادم». بعد هذا الدليل تصبح الاستفسارات محفوظة،
> والإشعارات حقيقية، والدفع مُتحقَّقًا منه خادميًا، والرؤوس مُطبَّقة، والروابط
> القديمة تُحوَّل بـ 301 حقيقي.

**الزمن:** 20 دقيقة بيدك + 20 دقيقة بيدي.
**التكلفة:** صفر (الخطة المجانية تغطي حركة أضعاف هذا الموقع).

---

## 0. قبل البدء — نقطة الرجوع
```powershell
git status                     # يجب أن تكون الشجرة نظيفة
git checkout -b deploy/cloudflare
```
سجّل الحالة الحالية للسجلات كي تقارن بعد النقل:
```powershell
Resolve-DnsName sr-coresync.com -Type MX
Resolve-DnsName sr-coresync.com -Type TXT
Resolve-DnsName _dmarc.sr-coresync.com -Type TXT
```

---

## 1. بيدك — الحساب والصلاحيات (20 دقيقة)

1. **أنشئ حساب Cloudflare** وأضف النطاق `sr-coresync.com`.
2. عند **استيراد DNS**، تأكّد أن هذه السجلات بقيت كما هي:
   - `MX 10 mx1.improvmx.com` و `20 mx2.improvmx.com`
   - `TXT @ v=spf1 include:spf.improvmx.com ~all`
   > لو حُذفت سجلات MX، يتوقف استقبال البريد فورًا. راجعها قبل المتابعة.
3. أنشئ **API Token** بصلاحيات: `Zone.DNS Edit` + `Workers Scripts Edit` + `Account: Cloudflare Pages Edit`.
4. أنشئ مفتاح **Resend** (أو Brevo) وأضف النطاق `send.sr-coresync.com` داخله.

---

## 2. بيدي — الـ Worker (بدون انتظار)

```powershell
cd workers/sr-lead-capture
npm ci
npx wrangler login

# D1 (السجل الدائم)
npx wrangler d1 create sr-coresync
#   → انسخ database_id وضعه في wrangler.toml ثم أزل التعليق عن [[d1_databases]]
npx wrangler d1 execute sr-coresync --remote --file=migrations/0001_init.sql

# الأسرار
npx wrangler secret put NOTIFY_EMAIL          # info@sr-coresync.com
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put STRIPE_WEBHOOK_SECRET # إن كنت تستخدم Stripe
npx wrangler secret put MOLLIE_API_KEY        # إن كنت تستخدم Mollie
npx wrangler secret put TURNSTILE_SECRET      # لاحقًا عند إضافة الودجة

npx wrangler deploy
```

**النطاق المخصّص:** أزل التعليق في `wrangler.toml` ثم `npx wrangler deploy`:
```toml
routes = [
  { pattern = "api.sr-coresync.com", custom_domain = true }
]
```

**تحقّق:**
```powershell
Invoke-RestMethod https://api.sr-coresync.com/health
Invoke-RestMethod -Method Post https://api.sr-coresync.com/tax `
  -ContentType 'application/json' -Body '{"amount":100,"rate":21}'
# المتوقع: net=100 vat=21 gross=121
```

---

## 3. بيدي — الموقع على Pages

1. أنشئ مشروع Pages واربطه بمستودع GitHub.
2. الإعدادات: **Framework = None** · **Build command = فارغ** · **Output directory = `_site`**.
   أو استخدم أمرًا يبني المجموعة:
   ```
   python scripts/prepare_publish_set.py
   ```
3. ملفات التحكم تُقرأ تلقائيًا من `_site/`:
   - `_headers` → CSP/HSTS فعلية (أول مرة في تاريخ المشروع).
   - `_redirects` → 301 للصفحات الخمس المسمّاة سابقًا `preview-*`.
4. أضف النطاق المخصّص، واختبر على `*.pages.dev` قبل تحويل DNS.

---

## 4. البريد — التوقيع والتحقق

| السجل | القيمة |
|---|---|
| `TXT send` | `v=spf1 include:<provider-spf> ~all` |
| `CNAME resend._domainkey.send` أو `TXT mail._domainkey.send` | القيمة من لوحة المزوّد |
| `TXT _dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@sr-coresync.com; pct=100` |
| `TXT _smtp._tls` | `v=TLSRPTv1; rua=mailto:tlsrpt@sr-coresync.com` |

بعد 2–4 أسابيع من تقارير نظيفة: `p=quarantine` ثم `p=reject`.
التفاصيل الكاملة في [EMAIL-DNS-RUNBOOK.md](EMAIL-DNS-RUNBOOK.md).

---

## 5. الإشعارات — زر واحد

```powershell
python scripts/enable_live_feed.py
git add -A && git commit -m "feat(feed): enable live notifications" && git push
```
عندها تعرض الصفحات عدّادًا حقيقيًا («N استشارة خلال 30 يومًا») وأحداثًا مصنَّفة
بلا هوية. لو توقف الـ Worker، تصمت الوحدة بدل أن تختلق.

---

## 6. التحقق النهائي
```powershell
Invoke-WebRequest https://sr-coresync.com/ -Method Head | Select-Object -Expand Headers
# يجب: strict-transport-security · content-security-policy · x-content-type-options

Invoke-WebRequest https://sr-coresync.com/preview-software.html -Method Head -MaximumRedirection 0
# يجب: 301 → /software.html

node scripts/verify_dns_records.js     # DMARC/DKIM
node scripts/check_perf_budget.py
node scripts/test_lead_worker.mjs      # 34 اختبارًا
```

---

## 7. التراجع
| الطبقة | كيف ترجع |
|---|---|
| DNS | أعد سجلات `A` إلى `185.199.108–111.153` (GitHub) — التغيير ينتشر خلال TTL=3600 |
| الموقع | مشروع Pages يبقى، لكن DNS يعود إلى GitHub Pages |
| الـ Worker | `npx wrangler rollback` أو احذف النطاق المخصّص فقط |
| الإشعارات | `python scripts/enable_live_feed.py --disable` |

---

## ما يُغلق بعد التنفيذ

| الفجوة | الحالة قبل | بعد |
|---|---|---|
| حفظ الاستفسارات | localStorage فقط | D1 + KV + بريد |
| الإشعارات | مُصنَّعة | مجموعات حقيقية |
| تحقق الدفع | لا شيء | توقيع Stripe + تحقق Mollie |
| حاسبة الضريبة | نطاق ميت | `/tax` داخلي |
| رؤوس الأمان | غير مُطبَّقة | CSP/HSTS فعليان |
| 301 | meta refresh | تحويل حقيقي |
| حماية النموذج | honeypot فقط | + Turnstile |

---

## 8. إذا رفضت نقل النطاق (الوضع الحالي)

**يعمل اليوم بلا لمس DNS:**
```powershell
cd workers/sr-lead-capture && npx wrangler deploy
npx wrangler whoami      # يعطي subdomain الحساب
python scripts/configure_api_base.py --base https://sr-lead-capture.<sub>.workers.dev
```

**لا يعمل بدون نقل NS:**

| البند | السبب | البديل الوحيد |
|---|---|---|
| `api.sr-coresync.com` | Cloudflare يمنح Custom Domain للنطاقات الموجودة في حسابه فقط | استخدام رابط `workers.dev` مباشرة |
| HSTS / CSP حقيقية | GitHub Pages لا يقرأ `_headers` | استضافة تدعم `_headers` وتُربط بـ **CNAME واحد** (Netlify) |
| 301 حقيقي | GitHub Pages لا يدعم التحويلات | نفس البديل أعلاه عبر `_redirects` |
| `frame-ancestors` | لا يعمل في `<meta>` | لا بديل بلا رأس HTTP |

> **الفرق الجوهري:** نقل *النطاق* (Nameservers) شيء، وإضافة **سجل CNAME واحد** شيء آخر.
> الثاني لا يمسّ البريد ولا الحساب، ويكفي لإغلاق فجوة الرؤوس والـ301 عبر Netlify.

**ما يبقى متاحًا فورًا حتى بلا أي منهما:**
- صيغة CSP في `<meta http-equiv>`: تقيّد `default-src` و`connect-src` (تحدّ من تسريب
  البيانات) لكنها لا تغني عن الرأس في `frame-ancestors` ولا توفّر HSTS.
- إزالة `onclick` (مستمرة) — وهي المتطلب الحقيقي لأي CSP صارم لاحقًا.
