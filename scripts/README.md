# `scripts/` — فهرس الأدوات

هذا المجلد يحتوي **أدوات نشطة** تُشغَّل في CI أو تُستخدم دوريًا.
كل ما كان سكربتًا لمرة واحدة (لقطات شاشة، إصلاحات سابقة، اختبارات تجريبية)
نُقل إلى [`archive/`](./archive) ولا يُشغَّل تلقائيًا.

## 🚦 بوابات الجودة (يعتمدها CI)

| الأداة | الدور |
|---|---|
| `validate.js` | توازن وسوم HTML/CSS/JS في كل الصفحات |
| `check_inline_scripts.mjs` | صحة كل كتلة `<script>` مضمّنة وكل JSON-LD |
| `check_site_links.py` | كل `href`/`src` محلي في مجموعة النشر يشير إلى ملف موجود |
| `audit_language_paths.py` | صحة بادئات `../` في كل الصفحات المترجمة |
| `audit_js_identifiers.py` | لا معرّفات JavaScript مترجمة/تالفة |
| `audit_language_api_parity.py` | تكافؤ واجهات JS بين اللغات |
| `audit_dead_gateway.py` | لا إشارة إلى بوابة PHP الميتة |
| `validate_publish_set.py` | لا مواد خادم داخل ما سيُنشر |
| `prepare_publish_set.py` | يبني `_site/` (نفس القواعد التي يتحقق منها CI) |
| `publish_set.py` | المصدر الوحيد لقواعد «ما يُنشر» |
| `browser_console_audit.mjs` | 30 صفحة في Chromium: أخطاء JS، طلبات فاشلة، معالجات ميتة |
| `test_lead_worker.mjs` | اختبار Cloudflare Worker لالتقاط العملاء |

## 🛠️ أدوات صيانة (تُشغَّل يدويًا)

| الأداة | الدور |
|---|---|
| `verify_dns_records.js` | فحص حقيقي لسجلات SPF/DKIM/DMARC/BIMI من DNS المباشر (`--strict` للفشل عند نقص) |
| `build_email_templates.py` | يبني رسائل المعاملات: CSS مضمّن + preheader + نسخة نصية + فحص حد Gmail |
| `optimize_images_webp.py` | يولّد نسخة WebP لكل صورة بطاقة/هيرو ويحوّل `<img src>` إليها |
| `extract_inline_css.py` | يستخرج CSS المضمّن إلى `css/inline-<lang>.css` |
| `apply_quick_package_fixes.py` | حزمة أداء/نظافة 2026-10 (مطبَّقة بالكامل — idempotent) |
| `rename_product_pages.py` | نقل `preview-*.html` إلى مسارات منتج نظيفة + كعب تحويل |
| `build_all_multilingual_portals.py` | توليد بوابات اللغات |
| `generate_international_sitemap.py` | توليد `sitemap.xml` (28 لغة + demos + صفحات المنتج) |
| `build_production.js` · `package_deployment.js` | تجهيز حزمة الإنتاج |

## 📦 `archive/`

118 سكربتًا لمرة واحدة (لقطات `capture_*`، إصلاحات `fix_*`/`clean_*`،
اختبارات `test_*`/`verify_*`، تحديثات `update_*`). محفوظة للمرجعية فقط:
لا يعتمد عليها CI ولا يستوردها أي سكربت نشط. لا تُضِف إليها؛ إن احتجت أداة
جديدة اجعلها في `scripts/` مع صف في هذا الفهرس.
