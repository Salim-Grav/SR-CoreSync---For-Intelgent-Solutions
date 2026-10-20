# دليل نشر الإنتاج المعتمد — خوادم Hostinger cPanel
### مشروع: S&R CoreSync Solutions B.V. (Enterprise Edition v2.0)
**تاريخ وموعد الاعتماد:** الثلاثاء، 20 أكتوبر 2026 - الساعة 06:25 صباحاً

---

## 📦 تفاصيل حزمة النشر الرقمية (Production Package Metadata)
- **اسم الحزمة:** `SR-CoreSync-Solutions-Production-v2.0.zip`
- **الحجم المضغوط (ZIP):** `27.04 MB` (توفير ضغط بنسبة 14.4%)
- **الحجم بعد فك الضغط:** `31.61 MB`
- **إجمالي الملفات المضمنة:** `175 ملفاً نظيفاً ومفحوصاً`
- **بصمة التحقق التشفيرية (SHA-256 Checksum):**
  ```
  9a072f0d5430f710cd2fdd5a3fe7503f49064b85454d7c98d6784eac59c27b32
  ```

---

## 🚀 خطوات النشر السريع عبر Hostinger cPanel (Quick Steps)

### 1. الرفع عبر مدير الملفات (File Manager):
1. افتح لوحة تحكم **Hostinger hPanel / cPanel**.
2. توجه إلى **File Manager** ثم افتح مجلد الجذر `public_html`.
3. اضغط على زر **Upload** وارفع الملف:
   `dist/SR-CoreSync-Solutions-Production-v2.0.zip`.

### 2. فك الضغط (Extract):
1. انقر بزر الفأرة الأيمن على الملف المرفوع واختر **Extract**.
2. حدد مسار الاستخراج إلى `public_html/`.
3. تأكد من ظهور ملف `.htaccess` وملف `index.html` في المجلد الرئيسي مباشرة.

### 3. إعداد البيئة الآمنة (.env):
1. انسخ ملف `.env.example` إلى `.env`.
2. أدخل مفاتيح بوابات الدفع الرسمية (Mollie & Stripe) وكلمة مرور بريد Hostinger Webmail:
   ```env
   GATEWAY_ENVIRONMENT=production
   SMTP_HOST=smtp.hostinger.com
   SMTP_PORT=465
   SMTP_USER=billing@sr-coresync.com
   SMTP_PASS=YourRealSecurePasswordHere
   ```
3. ملف `.htaccess` مجهز مسبقاً لحجب ملف `.env` وقواعد البيانات عن الوصول العام نهائياً.

### 4. التحقق من أذونات الملفات (Permissions):
- المجلدات: `755`
- الملفات: `644`

---

## 🛡️ فحوصات الأمان المنجزة مسبقاً (Pre-flight Verifications)
- ✅ ترويسات الأمان المصرفية (CSP, COOP, CORP, HSTS) مفعلة بالكامل.
- ✅ حظر مباشر لملفات `.env`, `.git`, `package.json`, `.sql`, `.bak`.
- ✅ تشغيل وضع عدم الاتصال (Service Worker & Cache API) بنسبة 100%.
- ✅ محرك التراخيص المشفرة والمحاكي السحابي جاهز فورياً.
