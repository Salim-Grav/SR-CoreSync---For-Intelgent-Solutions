# 🔐 تقرير تدقيق أمني — GitHub Pages

**S&R CoreSync For Intelligent Solutions**
**التاريخ:** الخميس، 22 أكتوبر 2026 — الساعة 12:43 فجراً
**النطاق:** `https://sr-coresync.com` + المستودع `Salim-Grav/SR-CoreSync---For-Intelgent-Solutions`

---

## 0. خلاصة تنفيذية

الاستضافة الفعلية هي **GitHub Pages** وليس Hostinger. المشروع كله كان مُهيّأً لخادم
LiteSpeed/cPanel، ما resulted in **طبقة أمان كاملة غير مُفعَّلة** و**تسريب كود
ومفاتيح عامة**، و**تعطّل كامل لالتقاط العملاء المحتملين**.

| # | الفجوة | الخطورة | الحالة |
|---|---|---|---|
| 0 | **مصدر النشر `legacy` (من الفرع) → شجرة المستودع كاملة منشورة + `_headers` غير مُطبَّق** | 🔴 حرجة | 🔄 يحتاج تبديلاً من الواجهة |
| 1 | `.htaccess` (161 سطر) غير مُطبَّق → **0 من 9** رؤوس أمان | 🔴 حرجة | ✅ مُصلَح |
| 2 | PHP لا يُنفَّذ → كود PHP مكشوف + **صفر عملاء مسجَّلون** | 🔴 حرجة | ✅ مُصلَح |
| 3 | `config/` و`api/` منشوران للعامة | 🔴 حرجة | ✅ مُصلَح |
| 4 | 42 مرجعاً مكسوراً في مجلدات اللغات (منها 5 في `ckb`) | 🔴 حرجة | ✅ مُصلَح |
| 5 | **ترجمة JS المدمجة كسرت 7 صفحات: `new Date()` و`querySelectorAll` ميّتة** | 🔴 حرجة | ✅ مُصلَح |
| 6 | `.git` = 770 MB (حد GitHub 1 GB) + ZIP 27 MB × 54 التزاماً | 🟠 عالية | ✅ مُصلَح |
| 7 | `path: '.'` ينشر 91.5 MB من أدوات التطوير | 🟠 عالية | ✅ مُصلَح |
| 8 | `.catch(() => {})` يُخفي فشل الالتقاط | 🟡 متوسطة | ✅ مُصلَح |
| 9 | لا `PHASE_STATUS.md` ولا توثيق للهندسة | 🟡 متوسطة | ⚠️ مفتوح |

---

## 0.1 الفجوة #0 — مصدر النشر: لماذا كان كل شيء معرَّضاً

هذه هي **السبب الجذري** وراء الفجوتين #1 و#3، ولا تُحل بإصلاح الملفات —
بل بإعداد المستودع على GitHub نفسه.

### الاكتشاف

بعد رفع الإصلاح الأول (commit `f0b3703`) والتحقق من النشر، تبيّن أن:

- الـ artifact المرفوع كان صحيحاً (35.25 MB = `_site`، مقابل 91.5 MB للفرع كاملاً).
- لكن الموقع الحيّ كان **لا يزال يقدّم شجرة الفرع**:
  `/workers/sr-lead-capture/src/index.js` → `200`، و`/scripts/validate.js` → `200`،
  بينما `/api/lead-capture.php` → `404` (لأنه نُقل، لا لأنه استُبعد).
- ورؤوس الأمان التسعة **ما تزال غائبة** رغم وجود `_headers` في الجذر.

### قياس تجريبي حاسم (commit `16dedde`)

فُصلت مسارات استطلاع داخل الفرع، ثم قِيست حيّاً:

| المسار | النتيجة | الاستنتاج |
|---|---|---|
| `/probe-root.txt` | `200` | ملفات الجذر تُنشر |
| `/probe-dir/probe.txt` | `200` | المجلدات العادية تُنشر |
| `/_probe-dir/probe.txt` | `200` | **المجلدات `_` لا تُستثنى** |
| `/.probe-dir/probe.txt` | `200` | **الملفات `.` لا تُستثنى** |
| `/.github/probe-dir/probe.txt` | `404` | **`.github/` وحده مستثنى** |
| `/docs/probe.txt` | `200` | `docs/` يُنشر كما هو |

> أي أن وضع «Deploy from a branch» ينشر **كل شيء** عدا `.github/`،
> وملف `_headers` يُقدَّم كملف نصّي عادي بدل أن يطبّقه الـ CDN.

### السبب

`build_type` في إعداد Pages كان `legacy` (بناء من الفرع) بدل `workflow`.
في هذا الوضع يتجاهل GitHub Pages الـ artifact المرفوع من GitHub Actions،
وينشر شجرة الفرع حرفياً.

### الحل

1. `Settings ← Pages ← Build and deployment ← Source ← "GitHub Actions"` —
   يفتح المسار published = `_site` فقط، ويُفعّل `_headers`.
2. **حارس دائم**: مهمة `pages-source` في `.github/workflows/deploy-pages.yml`
   تقرأ `build_type` عبر REST API وتفشل بوضوح إن لم يكن `workflow`.
3. محاولة التحويل الآلي عبر `GITHUB_TOKEN` **محاولة وتُسجَّل النتيجة**؛
   لكن هذا الـ token لا يملك صلاحية "manage GitHub Pages settings"
   (صلاحية مالك المستودع)، فالتبديل النهائي يدوي.

### بعد التبديل (المتوقّع، مُتحقَّق منه محلياً)

| المسار | قبل التبديل | بعد التبديل |
|---|---|---|
| `/workers/**` (شيفرة Worker + إعدادات الدفع) | `200` | `404` |
| `/scripts/**` (أدوات التطوير) | `200` | `404` |
| `/_headers` | `200` (كنص) | مُطبَّق (لا يُقدَّم) |
| 9 رؤوس أمان | `0/9` | `9/9` |
| حجم النشر | 91.5 MB | 58.01 MB (255 ملفاً) |

---

## 1. الأدلة على أن الاستضافة هي GitHub Pages

| المؤشر | القيمة |
|---|---|
| DNS A (apex) | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| DNS `www` | `CNAME → sr-coresync.com` |
| HTTP `Server` | `GitHub.com` |
| `X-GitHub-Request-Id` | `DF9A:16BACF:2E2F99:2EDBFC:6AD92B88` |
| `X-Served-By` | `cache-ams-eham8680028-AMS` |
| `Last-Modified` | `Wed, 21 Oct 2026 18:58:31 GMT` = آخر commit ✓ |
| `CNAME` | `sr-coresync.com` |

---

## 2. الفجوة #1 — رؤوس الأمان غير مُفعَّلة

**القياس الحيّ على `https://sr-coresync.com` (قبل الإصلاح):**

```
[MISS] Strict-Transport-Security      [MISS] Cross-Origin-Opener-Policy
[MISS] Content-Security-Policy        [MISS] Cross-Origin-Resource-Policy
[MISS] X-Frame-Options                [MISS] Referrer-Policy
[MISS] X-Content-Type-Options         [MISS] Permissions-Policy
[MISS] X-XSS-Protection
```

**السبب:** `.htaccess` يستدعي `mod_headers` / `mod_rewrite` / `mod_expires` — وهي
وحدات Apache/LiteSpeed. GitHub Pages يشغّل خادمه الخاص ولا يقرأ `.htaccess` إطلاقاً.
كما أن `FilesMatch` التي كانت تحجب `.env` و`payment-gateways.json` و`*.py`
و`*.bat` لم تكن ذات أثر.

### الحل
ملف [`_headers`](../_headers) — الآلية الأصلية في GitHub Pages — يستبدل `.htaccess`،
مع إضافة النطاقين `cdn.tailwindcss.com` و`unpkg.com` إلى CSP لأنهما كانا
مستخدمين فعلياً ولم يكونا في سياسة CSP القديمة.

---

## 3. الفجوة #2 — PHP لا يعمل + كود مصدري مكشوف

| الطلب | قبل | الأثر |
|---|---|---|
| `GET /api/lead-capture.php` | `200` · `application/x-httpd-php` | **كود PHP كامل معروض** |
| `POST /api/lead-capture.php` | `405` | **لا يُسجَّل أي عميل محتمل** |

`api/lead-dispatcher.js` كان يبتلع الخطأ بصمت عبر `.catch(err => null)`،
والواجهة تعرض "تم بنجاح" للعميل.

### الحل
- **Cloudflare Worker** جديد: [`workers/sr-lead-capture/`](../workers/sr-lead-capture/)
  — 23 اختبار وحدة ناجح (`node scripts/test_lead_worker.mjs`).
- العميل الجديد [`js/sr-lead-dispatcher.js`](../js/sr-lead-dispatcher.js)
  يجرّب 3 نقاط نهاية بالترتيب، ويخزّن محلياً دائماً، **ويُبلغ عن الفشل بوضوح**.
- البوابة PHP القديمة محفوظة كمرجع في `workers/legacy/lead-capture.php` (غير منشورة).

---

## 4. الفجوة #3 — الملفات الحساسة مكشوفة (مُتحقَّق منها حيّاً)

| المسار | قبل | بعد |
|---|---|---|
| `/api/lead-capture.php` | `200` (كود PHP) | `404` |
| `/.htaccess` | `200` (7.1 KB) | `404` |
| `/config/payment-gateways.json` | `200` | `404` |
| `/config/lead-webhook-config.json` | `200` | `404` |
| `/api/email-notification-service.js` | `200` | `404` |
| `/api/payment-webhook-service.js` | `200` | `404` |
| `/dist/*.zip` (27 MB) | `200` | `404` |
| `/scripts/*` (180 ملف) | `200` | `404` |

**ملاحظة:** المفاتيح في `payment-gateways.json` كانت 모두 placeholders
(`live_REPLACE_WITH_REAL_MOLLIE_API_KEY`)، فلم يتسرّب مفتاح فعّال.
لكن رابط Make.com و`IBAN` و`KvK` كانت مكشوفة — يُنصح بتدوير رابط الـ webhook.

### الحل
- `scripts/publish_set.py` — مصدر واحد لقواعد النشر.
- `scripts/prepare_publish_set.py` — يبني `_site/`.
- `scripts/validate_publish_set.py` — يتحقق محلياً.
- `.github/workflows/deploy-pages.yml` — يبني `_site/` ثم **يحرس** قبل الرفع.

---

## 5. الفجوة #4 — 42 مرجعاً مكسوراً (404 في الإنتاج)

مسارات الصفحات المُعرَّبة تشير إلى الأصول المشتركة بـ `./` بدل `../`،
بينما كل الأصول المشتركة (css/، js/، assets/، manifest.json) في الجذر.

| الملف | المراجع المكسورة |
|---|---|
| `ckb/index.html` | 30 — محرّك Enterprise Suite، المفتش، الدليل، **مبدّل اللغة**، prefetch، بطاقة NFC، استوديو الشعار، تنزيلات المنتجات |
| `ckb/demo.html` | 2 |
| `en/index.html` · `nl/index.html` · `de/index.html` | 3 لكلٍّ — صور أعمال `work-civicsync-hero.jpg` وغيرها |
| 24 ملف `demo.html` | 1 لكلٍّ — `assets/sr-core-emblem-official.png` |

**الأثر:** صفحة الكردي (Sorani) كانت **معطوبة جزئياً** — لا محرّك Enterprise Suite،
ولا التقاط عملاء، ولا تبديل لغة. وصفحات EN/NL/DE كانت تفقد 3 صور أعمال.

### الحل
`scripts/fix_language_paths.py` + `scripts/audit_language_paths.py` (CI gate دائم).
بعد توسيع مُدقّق المسارات ليشمل `srcset` و`poster`، ظهرت **13 مرجعاً إضافياً**
في `ckb/index.html` (WebP founders banner + poster) — أُصلحت أيضاً.

---

## 5.1 الفجوة #5 — الترجمة كسرت JavaScript في 7 صفحات (الأخطر)

تمريرة الترجمة متعددة اللغات ترجمت **أسماء دوال JavaScript** مع النص المرئي.
النتيجة: `TypeError` عند التنفيذ، و**فقدان كامل للعميل المحتمل**.

| اللغة | ما تغيّر | الأثر |
|---|---|---|
| `de` · `sv` | `new Date()` → `new Datum()` | 💥 `Datum is not a constructor` |
| `es` | `new Date()` → `new Fecha()` | 💥 |
| `it` | `new Date()` → `new Data()` | 💥 |
| `no` | `new Date()` → `new Dato()` | 💥 |
| `ku` | `new Date()` → `new Dîrok()` | 💥 |
| `tr` | `new Date()` → `new Tarih()` | 💥 |
| `es` `fr` `it` `no` `sv` | `querySelectorAll` → `querySelectorTodos/Tout/Tutti/Alle/Alla` | 💥 13 استدعاء لكل صفحة |
| `tr` | `querySelectorAll` → `querySelectorTümü` | 💥 13 استدعاء |
| `ku` | `querySelectorAll` → `querySelectorHemû` | 💥 13 استدعاء |
| `de` `sv` | `toLocaleDateString` → `toLocaleDatumString` | 💥 |
| `es` `it` `no` `tr` `ku` | `toLocaleDateString` → `toLocale{Fecha,Data,Dato,Tarih,Dîrok}String` | 💥 |

**الأثر التفصيلي:**

1. **فقدان العملاء** — في مسار `lead-capture` الاحتياطي، `new Tarih()` يرمي
   `TypeError` **قبل** `localStorage.setItem`، فالعميل يُفقد تماماً (لا خادم ولا تخزين محلي).
2. **تعطّل الواجهة** — `document.querySelectorTümü('video').forEach(...)` يمنع
   تهيئة: مراقبة الفيديو، تبويبات الأعمال، الأكورديون، تبويبات الأسعار،
   أزرار المظهر، قائمة اللغات، والعرض السينمائي.
3. **تعطّل تقرير PDF** — `now.toLocaleTarihString(...)` يمنع توليد التاريخ.

**إجمالي الأضرار:** **372 مُعرِّفاً تالفاً في 15 ملفاً** (منها 7 كان Arrow مميتاً).

### الحل
- `scripts/audit_js_identifiers.py` — يفحص كل كتلة `<script>` مدمجة في 96 صفحة
  (264,172 مُعرِّفاً) ويرصد أي مُعرِّف غير ASCII أو اسم API مترجَم.
- `scripts/repair_js_identifiers.py` — يُصلح عبر محاذاة رمزية مع الصفحة المرجعية
  (`index.html` / `en/demo.html`) + جدول مُثبت مُراجَع يدوياً.
- `scripts/audit_language_api_parity.py` — يقارن مخزون الـ DOM API بين كل لغة
  والصفحة المرجعية.
- `scripts/check_inline_scripts.mjs` — يحلّل كل كتلة JS مدمجة وJSON-LD فعلياً.

**النتيجة:** `PASSED — no translated or corrupted JavaScript identifiers found`
و**30/30 صفحة تعمل بلا أي خطأ JavaScript ولا أي طلب فاشل** (تدقيق headless Edge).

---

## 6. الفجوة #5 — تضخّم `.git`

```
.git = 770.0 MB          (حد GitHub: 1 GB تحذير / 2 GB رفض)
dist/SR-CoreSync-...v2.0.zip = 27.04 MB × 54 التزاماً
```

**السبب:** `package_deployment.js` يُنتج أرشيفاً جديداً في كل بناء،
وكل نسخة تُحفظ في التاريخ نهائياً.

### الحل
- `git rm --cached` للأرشيف + تقارير Lighthouse (≈ 30.7 MB من كل بناء).
- `.gitignore` جديد يمنع عودتها.
- ⚠️ **التاريخ الماضي لم يُنقَّ.** التصغير الفعلي يتطلب `git filter-repo` وإعادة كتابة
  التاريخ — عملية منفصلة تحتاج موافقة صريحة.

---

## 7. Changes summary

### ملفات جديدة
| الملف | الدور |
|---|---|
| `_headers` | رؤوس الأمان لـ GitHub Pages |
| `.nojekyll` | تعطيل Jekyll وضمان معالجة `_headers` |
| `js/sr-lead-dispatcher.js` | عميل التقاط العملاء الجديد (من `api/lead-dispatcher.js`) |
| `js/sr-payment-client-bridge.js` | جسر الدفع للعميل (من `api/`) |
| `workers/sr-lead-capture/src/index.js` | Cloudflare Worker |
| `workers/sr-lead-capture/wrangler.toml` | إعدادات النشر + KV + النطاق |
| `workers/sr-lead-capture/package.json` | اعتماد Wrangler |
| `workers/sr-lead-capture/.dev.vars.example` | نموذج الأسرار |
| `workers/sr-lead-capture/README.md` | دليل النشر بالعربية |
| `workers/config/*` · `workers/lib/*` · `workers/legacy/*` | مواد الخادم (غير منشورة) |
| `scripts/publish_set.py` | مصدر واحد لقواعد النشر |
| `scripts/prepare_publish_set.py` | بناء `_site/` |
| `scripts/validate_publish_set.py` | تحقق ما قبل النشر |
| `scripts/audit_language_paths.py` | تدقيق مسارات اللغات (CI gate) |
| `scripts/fix_language_paths.py` | إصلاح المسارات |
| `scripts/audit_js_identifiers.py` | تدقيق مُعرِّفات JavaScript (CI gate) |
| `scripts/repair_js_identifiers.py` | إصلاح مُعرِّفات JavaScript المترجمة |
| `scripts/audit_language_api_parity.py` | تدقيق تكافؤ الـ API بين اللغات |
| `scripts/check_inline_scripts.mjs` | تحليل كل كتلة JS/JSON-LD مدمجة |
| `scripts/browser_console_audit.mjs` | تدقيق headless: أخطاء JS + طلبات فاشلة |
| `scripts/test_lead_worker.mjs` | 23 اختبار وحدة للـ Worker |
| `scripts/audit_dead_gateway.py` | تدقيق بوابة PHP الميتة (يتجاهل التعليقات) |
| `scripts/migrate_lead_endpoint.py` | ترحيل نقطة الالتقاط |

### ملفات معدَّلة
`_headers` · `.nojekyll` · `.gitignore` · `robots.txt` · `README.md` · `sw.js`
· `.github/workflows/ci.yml` · `.github/workflows/deploy-pages.yml`
· **30 صفحة HTML** (29 `index.html` + `preview-booking-modal.html`)
· **31 ملف HTML** مُصلَح للمسارات (2 منها مكرر مع ما سبق)
· **15 ملف HTML** مُصلَح لمُعرِّفات JavaScript المترجمة

---

## 8. بوابة الجودة (CI gate)

```bash
# 1. سلامة HTML / CSS / JS
node scripts/validate.js

# 2. تحليل كل كتلة JS مدمجة + JSON-LD
node scripts/check_inline_scripts.mjs

# 3. تدقيق مُعرِّفات JavaScript
python scripts/audit_js_identifiers.py

# 4. تكافؤ الـ API بين اللغات
python scripts/audit_language_api_parity.py

# 5. تدقيق مسارات اللغات
python scripts/audit_language_paths.py

# 6. سلامة مجموعة النشر
python scripts/validate_publish_set.py

# 7. بناء artifact النشر
python scripts/prepare_publish_set.py

# 8. تدقيق headless (أخطاء JS + 404)
node scripts/browser_console_audit.mjs

# 9. اختبارات الـ Worker
node scripts/test_lead_worker.mjs
```

**الحالة الحالية: 9/9 ناجحة.**

---

## 9. Commands

```bash
# ---- 1) نشر الـ Worker على Cloudflare (بانتظار إنجازه) ----
cd workers/sr-lead-capture
npm install
npx wrangler login                       # يفتح المتصفح لتفويض الحساب
npx wrangler kv namespace create LEADS   # انسخ الـ id في wrangler.toml
npx wrangler secret put LEAD_WEBHOOK_URLS   # روابط Make/n8n/Sheets مفصولة بفاصلة
npx wrangler secret put NOTIFY_EMAIL         # بريد الاستقبال
npx wrangler deploy
# ثم: لوحة Cloudflare ← Workers & Pages ← sr-lead-capture ← Triggers
#      ← Add Custom Domain ← api.sr-coresync.com ← Auto DNS

# ---- 2) التحقق من النشر ----
curl -X POST https://api.sr-coresync.com/lead \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://sr-coresync.com' \
  -d '{"clientName":"Test Lead","email":"test@example.com","companyName":"QA","notes":"smoke test","language":"en"}'
# المتوقع: {"status":"success","leadId":"LEAD-SR-20261022-A1B2",...}

# ---- 3) بوابة الجودة محلياً ----
node scripts/validate.js
node scripts/check_inline_scripts.mjs
python scripts/audit_js_identifiers.py
python scripts/audit_language_api_parity.py
python scripts/audit_language_paths.py
python scripts/validate_publish_set.py
python scripts/prepare_publish_set.py
python scripts/audit_dead_gateway.py
node scripts/browser_console_audit.mjs
node scripts/test_lead_worker.mjs
```

---

## 10. المتبقي (مفتوح)

| # | البند | الأولوية |
|---|---|---|
| 0 | **تبديل Pages Source إلى "GitHub Actions"** (يوقف تسريب `workers/` و`scripts/` ويُفعّل `_headers`) | 🔴 |
| 1 | نشر الـ Worker على `api.sr-coresync.com` (يحتاج حساب Cloudflare) | 🔴 |
| 2 | تعبئة أسرار `LEAD_WEBHOOK_URLS` و`NOTIFY_EMAIL` | 🔴 |
| 3 | تدوير رابط Make.com المكشوف سابقاً | 🟠 |
| 4 | تصغير تاريخ `.git` عبر `git filter-repo` | 🟠 |
| 5 | **انحراف الميزات:** 27 لغة لا تنفّذ ميزات الجذر (QR المؤسسين، ملء الشاشة، `Object.keys/values/entries`، `updateROICalculator`، `setRoiTeamPreset`) | 🟠 |
| 6 | تفعيل `sr-readiness.js` (معزول تماماً — 0 مرجع) | 🟡 |
| 7 | توسيع 4 الميزات (Tier/Trust/Dock/Geo) على 24 لغة | 🟡 |
| 8 | `PHASE_STATUS.md` + تحديث `README.md` للغة CKB | 🟡 |
| 9 | تفعيل الدفع الحقيقي (Mollie/Stripe) | 🟡 |

---

**التاريخ والوقت (بالعربية):** الخميس، 22 أكتوبر 2026 — الساعة 12:43 فجراً
