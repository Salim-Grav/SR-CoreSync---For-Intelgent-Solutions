# دليل ضبط سجلات الـ DNS وضمان وصول البريد الإلكتروني إلى صندوق الوارد (Inbox)
### مشروع: S&R CoreSync For Intelligent Solutions — منصة الأعمال والأنظمة المؤسسية
**النطاق الرسمي:** `sr-coresync.com` | **تاريخ الاعتماد:** الأربعاء، 14 أكتوبر 2026 - الساعة 06:55 صباحاً

---

## 🎯 الهدف التقني (Deliverability Objective)
ضمان وصول كافة رسائل البريد الإلكتروني الصادرة من `billing@sr-coresync.com` و `info@sr-coresync.com` (الفواتير الضريبية، عروض الأسعار، مفاتيح التراخيص، ورسائل الترحيب) إلى **صندوق الوارد الأساسي (Primary Inbox)** مباشرة لدى عملاء الشركات عبر Gmail، Microsoft Outlook، Apple Mail، وباقي المزودين، ومنع تصنيفها كرسائل غير مرغوب فيها (Spam / Junk) بنسبة 100%.

---

## 📋 جدول السجلات المطلوب إدخالها في لوحة Hostinger DNS Zone Editor

| النوع (Type) | الاسم / المضيف (Name / Host) | القيمة / الوجهة (Value / Points to) | الأولوية (Priority) | TTL | الوظيفة التقنية |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **MX** | `@` | `mx1.hostinger.com` | **5** | 3600 | خادم استقبال البريد الأساسي |
| **MX** | `@` | `mx2.hostinger.com` | **10** | 3600 | خادم استقبال البريد الاحتياطي |
| **TXT** | `@` | `v=spf1 include:_spf.mail.hostinger.com include:sendgrid.net ~all` | — | 3600 | **SPF:** تفويض خوادم Hostinger و SendGrid بالإرسال |
| **TXT** | `_dmarc` | `v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@sr-coresync.com; ruf=mailto:security@sr-coresync.com; sp=quarantine; aspf=r; adkim=r; fo=1; pct=100` | — | 3600 | **DMARC:** سياسة الحماية الصارمة من التزوير وجمع التقارير |
| **CNAME** | `hostingermail-a._domainkey` | `hostingermail-a._domainkey.hostinger.com` | — | 3600 | **DKIM A:** التوقيع التشفيري للرسائل الصادرة |
| **CNAME** | `hostingermail-b._domainkey` | `hostingermail-b._domainkey.hostinger.com` | — | 3600 | **DKIM B:** التوقيع التشفيري الاحتياطي للتدوير |
| **TXT** | `default._bimi` | `v=BIMI1; l=https://sr-coresync.com/assets/sr-core-emblem.svg;` | — | 3600 | **BIMI:** إظهار الشعار الرسمي في صور الملف الشخصي بصندوق الوارد |
| **CNAME** | `mail` | `mail.hostinger.com` | — | 3600 | رابط الولوج للويب ميل (`mail.sr-coresync.com`) |
| **CNAME** | `autodiscover` | `autodiscover.mail.hostinger.com` | — | 3600 | الضبط التلقائي لبرامج Outlook و Apple Mail |
| **CNAME** | `autoconfig` | `autoconfig.mail.hostinger.com` | — | 3600 | الضبط التلقائي لبرنامج Thunderbird |

---

## 🛠️ خطوات التنفيذ المباشرة عبر لوحة Hostinger (Step-by-Step)

### 1. الدخول إلى محرر المنطقة (DNS Zone Editor):
1. افتح لوحة تحكم الاستضافة **Hostinger hPanel**.
2. انتقل إلى قسم **Domains** واختر النطاق `sr-coresync.com`.
3. اضغط على القائمة الجانبية: **DNS / Nameservers** -> **DNS Records**.

### 2. إضافة / تعديل سجل الـ SPF:
- ابحث عن أي سجل TXT يبدأ بـ `v=spf1`.
- قم بتعديل قيمته لتصبح:
  ```text
  v=spf1 include:_spf.mail.hostinger.com include:sendgrid.net ~all
  ```
- اضغط **Save**.

### 3. إضافة سجل الـ DMARC:
- اضغط على **Add Record**:
  * **Type:** `TXT`
  * **Name:** `_dmarc`
  * **TXT Value:**
    ```text
    v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@sr-coresync.com; ruf=mailto:security@sr-coresync.com; sp=quarantine; aspf=r; adkim=r; fo=1; pct=100
    ```
  * **TTL:** `3600`
- اضغط **Add Record**.

### 4. إضافة سجل الـ BIMI (الشعار الرسمي):
- اضغط على **Add Record**:
  * **Type:** `TXT`
  * **Name:** `default._bimi`
  * **TXT Value:**
    ```text
    v=BIMI1; l=https://sr-coresync.com/assets/sr-core-emblem.svg;
    ```
  * **TTL:** `3600`
- اضغط **Add Record**.

---

## 🔍 أدوات الفحص والاختبار الموصى بها (Verification Tools):
- **فحص SPF / DKIM / DMARC:** [MXToolbox SuperTool](https://mxtoolbox.com/SuperTool.aspx?action=mx%3asr-coresync.com)
- **فحص وصول الرسائل ومعدل الـ Spam:** [Mail-Tester](https://www.mail-tester.com/) (النتيجة المتوقعة: 10/10).
