# تفعيل رؤوس الأمان على `sr-coresync.com`

> **الخلاصة:** GitHub Pages لا يطبّق ملف `_headers` إطلاقًا. الملف موجود في المستودع
> لكنه يُقدَّم كنص عادي (`https://sr-coresync.com/_headers` → 200) ولا يُترجم إلى
> رؤوس HTTP. لذلك الموقع المباشر اليوم **بلا HSTS وبلا CSP وبلا X-Content-Type-Options**،
> رغم أن تقرير `SECURITY-AUDIT-GITHUB-PAGES.md` يذكر «9/9 رؤوس مُطبَّقة».
>
> هذا الملف يشرح المسارين الممكنين لتفعيلها فعليًا، مع القيم الجاهزة للصق.

---

## المسار أ — Cloudflare أمام GitHub Pages (الأسرع، بلا نقل استضافة)

DNS الحالي: سجلات `A` تشير إلى `185.199.108–111.153` (GitHub Pages).
الخطوات:

1. أضف النطاق إلى Cloudflare (خطة Free تكفي) واستورد سجلات DNS الحالية.
2. بدّل سجلات `A` الأربعة إلى **Proxied** (السحابة البرتقالية) بدل DNS only.
   - تحقّق أولًا أن `CNAME` = `salim-grav.github.io` (أو ما يعادله) موجود،
     وإلا سيتوقف GitHub Pages عن التعرّف على النطاق المخصّص.
3. في Cloudflare → **Rules → Transform Rules → Modify Response Header** أنشئ
   قاعدة واحدة: *When incoming requests match: All incoming requests*،
   ثم أضف الرؤوس التالية بالضبط (Set / Set / …):

| Header | Value |
|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `SAMEORIGIN` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), payment=(), usb=(), browsing-topics=()` |
| `Cross-Origin-Opener-Policy` | `same-origin-allow-popups` |
| `Content-Security-Policy` | القيمة الكاملة في [_headers](../_headers) (سطر `Content-Security-Policy`) |

4. **تحقّق** بعد النشر:

```powershell
Invoke-WebRequest -Uri 'https://sr-coresync.com/' -Method Head |
  Select-Object -ExpandProperty Headers
```

يجب أن ترى `strict-transport-security` و`content-security-policy` في المخرجات.
وللتحقق الآلي المستمر: المهمة المجدولة `sr-coresync-live-guard` في هذا المشروع
تفحص ذلك أسبوعيًا.

> **ملاحظة CSP:** لا تُضِف `includeSubDomains` إلى HSTS قبل التأكد أن كل
> النطاقات الفرعية (`api.`, `www.`) تعمل على HTTPS، وإلا ستصبح غير قابلة للوصول.

---

## المسار ب — نقل الاستضافة إلى Cloudflare Pages (أنظف على المدى الطويل)

Cloudflare Pages **يطبّق** ملف `_headers` كما هو (نفس صيغة Netlify). الفائدة:
لا حاجة لقواعد Transform، ويصبح ملف `_headers` هو المصدر الوحيد للحقيقة.

1. أنشئ مشروع Pages واربطه بمستودع GitHub.
2. إعدادات البناء: **Framework preset = None**، **Build command = فارغ**،
   **Build output directory = `_site`** (نفس مخرجات `scripts/prepare_publish_set.py`).
3. أو استخدم الأمر:
   `python scripts/prepare_publish_set.py && echo "build ok"`.
4. أضف النطاق المخصّص، وبعد التحقق من عمله حوّل سجلات DNS من GitHub إلى Pages.

الميزة الإضافية: على Cloudflare Pages يمكن تنفيذ **تحويلات 301 حقيقية** لصفحات
`preview-*.html` القديمة (انظر `REDIRECTS-PLAN.md`)، وهو ما لا يدعمه GitHub Pages.

---

## ما تغيّر فعليًا في CSP (وهو أضيق من السابق)

| البند | قبل | بعد | السبب |
|---|---|---|---|
| `unsafe-eval` | مسموح | **محذوف** | لا يوجد أي `eval(`/`new Function(` في الصفحات، و`jszip` محمي بـ try/catch — تم اختباره فعليًا |
| `default-src` | `'self' https: data: blob:` | **`'self'`** | القائمة البيضاء الصريحة أدق من السماح لكل https |
| `connect-src` | `https: wss:` | نطاقات محددة | `api.coresync.eu`، `api.coresync.solutions`، `api.sr-coresync.com`، `api.telegram.org`، `api.mollie.com` |
| `form-action` | `'self' https:` | `'self' https://wa.me` | النماذج لا تُرسل خارج الموقع عدا واتساب |
| `object-src` | `'none'` | `'none'` | كما هو |
| `unsafe-inline` (scripts) | مسموح | **مسموح (مؤقتًا)** | 429 كتلة `<script>` داخلية و**11,909** معالج حدث داخلي — إزالته تتطلب refactor كامل |

### الطريق إلى CSP صارم فعليًا
`'unsafe-inline'` يعني أن أي حقن HTML سيستطيع تنفيذ سكربت. للإزالة التدريجية:

1. استبدال `onclick=`/`oninput=`… بـ `addEventListener` + **event delegation** على مستوى المستند.
   العدد الحالي: 10,943 `onclick`، 450 `oninput`، 213 `onsubmit`، 182 `onchange`.
2. بعد ذلك: `script-src 'self'` + `nonce` للقليل المتبقي، ثم `style-src` بلا `unsafe-inline`
   بعد تحويل أنماط `style="…"` إلى أصناف.
3. قياس التقدّم: `python scripts/audit_inline_csp_readiness.py` (يضاف مع الدفعة القادمة).

---

## التحقق المحلي قبل التفعيل

```powershell
# يبني _site ثم يقدّمه مع رؤوس _headers لفحص أي تعارض CSP
python scripts/prepare_publish_set.py
python dist/_tmp_csp_server.py   # خادم اختبار مؤقت
```

الفحص المُنفَّذ في هذه الجلسة على النسخة الحقيقية:

- 31 طلبًا، لا موارد محجوبة، `document.styleSheets` = 12، الخطوط المحمّلة = 53.
- `JSZip` يُحمَّل ويُنشئ ملفًا (110 بايت) **دون `unsafe-eval`**.
- `Chart.js` يُحمَّل بنجاح.
- لا صور مكسورة.
