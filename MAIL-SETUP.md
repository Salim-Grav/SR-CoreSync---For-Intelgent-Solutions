# تشغيل البريد الثلاثي (info@ · support@ · billing@) — استقبال وإرسال

> **الحالة المقيسة الآن (2026-10-24):**
> ```
> MX     : mx1.improvmx.com, mx2.improvmx.com
> SPF    : v=spf1 include:spf.improvmx.com ~all
> DKIM   : لا يوجد
> DMARC  : لا يوجد
> ```
> **ImprovMX = تحويل فقط**: لا صناديق، لا IMAP/SMTP، ولا إرسال من النطاق.
> أي ردّ ترسله اليوم يخرج من بريدك الشخصي باسمك لا باسم الشركة.

**الخلاصة:** «كل الميزات» تعني الانتقال إلى مزوّد **صناديق بريد حقيقية**.
وهذا **لا يحتاج نقل النطاق** — فقط تعديل سجلات DNS في hPanel، تمامًا كما رفضتَ سابقًا.

---

## الخيارات الثلاثة

| | **Zoho Mail** | **Hostinger Email** | **Google Workspace / M365** |
|---|---|---|---|
| صناديق حقيقية | ✅ 3 (خطة مجانية: 5 صناديق) | ✅ 3 | ✅ 3 |
| IMAP/SMTP/Webmail | ✅ | ✅ | ✅ |
| DKIM + DMARC | ✅ | ✅ | ✅ |
| مركز بيانات أوروبي | ✅ (zoho.eu) | ✅ (LT/NL) | ✅ |
| التكلفة | **مجاني** (5 صناديق، 5GB) | منخفضة/صندوق (غالبًا ضمن استضافتك) | ~€6–7 لكل مستخدم شهريًا |
| الأفضل لـ | 3 عناوين بميزانية صفر | من يريد مزوّدًا واحدًا مع الاستضافة | تكامل Gmail/Office الكامل |

**توصيتي:** **Zoho Mail (EU)** — ثلاث صناديق كاملة بميزانية صفر، ودعم DKIM/DMARC،
ولا يمسّ ملكية النطاق. إن كنت تدفع لـ Hostinger hosting، فـ **Hostinger Email**
أبسط (مزوّد واحد ولن تنسى تجديدًا).

---

## 1) Zoho Mail — الخطوات والسجلات

**أ) في Zoho:** أنشئ حسابًا → `Mail Admin → Domains → Add Domain` → `sr-coresync.com`
→ اختر数据中心 **EU (zoho.eu)** → سيطلب سجل تحقق TXT/CNAME → أنشئ الصناديق الثلاثة.

**ب) في Hostinger (DNS Zone Editor):**

| النوع | الاسم | القيمة | ملاحظة |
|---|---|---|---|
| `TXT` | `@` | `zoho-verification=...` | من لوحة Zoho (تحقّق الملكية) |
| `MX` | `@` | `mx.zoho.eu` أولوية **10** | أساسي |
| `MX` | `@` | `mx2.zoho.eu` أولوية **20** | احتياطي |
| `MX` | `@` | `mx3.zoho.eu` أولوية **50** | احتياطي |
| `TXT` | `@` | `v=spf1 include:zoho.eu ~all` | **استبدل** SPF الحالي |
| `TXT` | `zoho._domainkey` | القيمة من لوحة Zoho | DKIM (أنشئها في Mail Admin) |
| `TXT` | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@sr-coresync.com; pct=100` | ابدأ بالمراقبة |

> ⚠️ **الترتيب مهم:** أنشئ سجلات DKIM والتحقق **قبل** حذف MX القديمة.
> أبقِ `mx1.improvmx.com` بأولوية **90** كشبكة أمان لأسبوع — البريد يذهب للأولوية الأقل
> أولًا، فإن قبلها Zoho لا يصل شيء إلى ImprovMX، وإن تعطّل يعود التحويل.

**ج) بعد التحقق:** أضف توقيعات المؤسسين في Zoho، وفعّل `SPF` و`DKIM` ثم ارفع DMARC
إلى `quarantine` بعد 2–4 أسابيع من تقارير نظيفة.

---

## 2) Hostinger Email

| النوع | الاسم | القيمة |
|---|---|---|
| `MX` | `@` | `mx1.hostinger.com` (5) · `mx2.hostinger.com` (10) |
| `TXT` | `@` | `v=spf1 include:_spf.mail.hostinger.com ~all` |
| `CNAME` | `hostingermail-a._domainkey` | `hostingermail-a._domainkey.hostinger.com` |
| `CNAME` | `hostingermail-b._domainkey` | `hostingermail-b._domainkey.hostinger.com` |
| `CNAME` | `autodiscover` | `autodiscover.mail.hostinger.com` |
| `TXT` | `_dmarc` | كما أعلاه |

الصناديق تُنشأ من hPanel → **Emails**. (هذه هي القيم التي كان المستودع يوثّقها كأنها حيّة.)

---

## 3) Google Workspace / Microsoft 365

- **Google:** `MX aspmx.l.google.com (1)` + `alt1–4.asp...` · `SPF include:_spf.google.com`
  · DKIM من Admin Console → Apps → Gmail → Authenticate email (`google._domainkey`).
- **Microsoft:** `MX <tenant>.mail.protection.outlook.com` · `SPF include:spf.protection.outlook.com`
  · DKIM: `CNAME selector1._domainkey` و`selector2._domainkey` (القيم من مركز الإدارة).

---

## التحقق (بعد أي خيار)

```powershell
python scripts/check_mail_setup.py
```
يقيس: MX · SPF · DKIM · DMARC ويقول أين أنت بالضبط.

ثم اختبار وظيفي حقيقي:
1. أرسل **إلى** `info@` و`support@` و`billing@` من بريد خارجي → يجب أن تظهر في الويبميل.
2. أرسل **من** كل عنوان إلى Gmail → افحص ترويسة `Authentication-Results`:
   يجب `spf=pass dkim=pass dmarc=pass`.

---

## علاقة ذلك ببريد الموقع (الـ Worker)

مساران مختلفان يجب الفصل بينهما:

| المسار | من يرسل | يحتاج |
|---|---|---|
| **بريد البشر** (ردود، فواتير يدوية) | الصناديق الثلاثة | مزوّد صناديق (Zoho/Hostinger/Google) |
| **بريد الموقع الآلي** (تنبيه استفسار، عرض سعر) | الـ Worker | مفتاح Resend/Brevo أو Send binding |

تفعيل أحدهما لا يفعّل الآخر. تنبيه الاستفسارات يعمل اليوم عبر **Telegram**،
ويحتاج Resend ليصل بالبريد أيضًا.
