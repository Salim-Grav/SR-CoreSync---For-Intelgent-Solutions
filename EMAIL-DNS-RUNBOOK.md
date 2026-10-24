# دليل مصادقة البريد — `sr-coresync.com`

> **قياس مباشر من DNS يوم السبت 24 أكتوبر 2026 (10:05 صباحاً):**

| السجل | المتوقع في `workers/config/dns-records.json` | **الواقع على DNS** |
|---|---|---|
| MX | `mx1/mx2.hostinger.com` | `mx1/mx2.improvmx.com` |
| SPF | `include:_spf.mail.hostinger.com` + `include:sendgrid.net` | `v=spf1 include:spf.improvmx.com ~all` |
| DMARC | `p=quarantine` + تقارير | **غير موجود** |
| DKIM | مُنتقِيان `hostingermail-a/b` | **غير موجود** |
| BIMI | `default._bimi` | **غير موجود** |

**النتيجة العملية:** أي رسالة تُرسل من النطاق عبر مزوّد معاملات (Resend/Brevo) —
وهو المزوّد الذي يستخدمه الـ Worker فعلًا — **تفشل في SPF وDMARC**، فتذهب
للسبام أو تُرفض. ولا يوجد أي شيء يمنع انتحال النطاق (Spoofing) في بريد المديرين.

---

## 1. لماذا نبدأ بالنطاق الفرعي

لا ترسل من `@sr-coresync.com` مباشرة. أرسل من:

```
send.sr-coresync.com      ← البريد المعاملاتي (فواتير، ترحيب، إشعارات)
sr-coresync.com           ← بريد البشر فقط (info@، support@، billing@)
```

السبب: بريد البشر يمرّ عبر ImprovMX (تحويل)، والبريد الآلي يمرّ عبر مزوّد
معاملات. فصل السمعة يمنع أن تؤثر شكاوى الآلي على وصول رسائل المؤسسين، ويسمح
بتشديد DMARC على النطاق الفرعي (`adkim=s; aspf=s`) دون كسر التحويل.

---

## 2. السجلات المطلوبة (بالترتيب)

### أ) SPF — النطاق الرئيسي (يبقى للتحويل)
```
Type: TXT     Name: @     Value: v=spf1 include:spf.improvmx.com ~all
```
لا تُضِف مزوّد المعاملات هنا إذا استخدمت النطاق الفرعي.

### ب) SPF — النطاق الفرعي للإرسال
```
Type: TXT     Name: send     Value: v=spf1 include:<provider-spf> ~all
```
> انسخ قيمة `include:` من لوحة المزوّد (Resend / Brevo) — وهي ثابتة لكل مزوّد،
> لكن تأكيدها من اللوحة يمنع خطأ نسخ قديم.

### ج) DKIM — إلزامي، وقيمه خاصة بحسابك
```
Type: CNAME (أو TXT حسب المزوّد)
Name:  <selector>._domainkey.send
Value: <القيمة التي يعرضها المزوّد بعد إضافة النطاق>
```
- **Resend:** يعرض CNAME باسم `resend._domainkey` — الصق القيمة كما هي.
- **Brevo:** يعرض TXT باسم `mail._domainkey` — الصق القيمة كما هي.

> ⚠️ لا تخترع قيمة DKIM. المفتاح عام/خاص ويُولَّد في حساب المزوّد؛ نسخ قيمة
> خاطئة يعني فشل التوقيع بصمت.

### د) DMARC — ابدأ مراقبةً ثم شدّد
```dns
Type: TXT   Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@sr-coresync.com; ruf=mailto:security@sr-coresync.com; fo=1; pct=100
```
بعد 2–4 أسابيع من التقارير النظيفة:
```dns
v=DMARC1; p=quarantine; sp=quarantine; adkim=s; aspf=s; rua=mailto:dmarc@sr-coresync.com; pct=100
```
ثم عند التأكد التام:
```dns
v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s; rua=mailto:dmarc@sr-coresync.com; pct=100
```

> **إلزامي لـ Google/Yahoo** (منذ فبراير 2024): نطاق يرسل أكثر من 5,000 رسالة
> يوميًا يجب أن يملك SPF **و** DKIM **و** DMARC. المشروع اليوم لا يملك أيًّا منها
> عمليًا.

### هـ) TLS-RPT (اختياري لكنه مجاني)
```
Type: TXT   Name: _smtp._tls
Value: v=TLSRPTv1; rua=mailto:tlsrpt@sr-coresync.com
```

### و) BIMI — ليس الآن
BIMI يتطلب: DMARC على `p=quarantine/reject` **+ شهادة VMC** (تُشترى سنويًا) + شعار
بصيغة **SVG Tiny PS**. الشعار الحالي `sr-core-emblem.svg` ليس بصيغة Tiny PS،
وشعار SVG وحده **لا يظهر في Gmail**. أزِل سجل BIMI الحالي من الملف الوثائقي حتى
تتوفر الشهادة.

---

## 3. ترتيب التنفيذ الآمن

1. أضف نطاق الإرسال في لوحة المزوّد → خذ DKIM + SPF منه.
2. أنشئ سجلات (ب) و(ج) على `send.sr-coresync.com`.
3. أضف DMARC بـ `p=none` على النطاق الرئيسي (لا يكسر شيئًا).
4. أرسل رسالة اختبار إلى Gmail + Outlook + Yahoo، وافحص الرؤوس:
   `Authentication-Results: spf=pass dkim=pass dmarc=pass`.
5. بعد 2–4 أسابيع: `p=quarantine`، ثم `p=reject`.
6. اضبط `MAIL_FROM` في الـ Worker على `leads@send.sr-coresync.com`.

> **التراجع:** DMARC سجل DNS واحد؛ حذفه أو تخفيضه إلى `p=none` يوقف أي أثر فورًا
> (مع مراعاة TTL = 3600).

---

## 4. التحقق

```powershell
# SPF
Resolve-DnsName -Name send.sr-coresync.com -Type TXT | Select-Object Strings

# DMARC
Resolve-DnsName -Name _dmarc.sr-coresync.com -Type TXT | Select-Object Strings

# DKIM (اسم المُنتقي كما يعرضه المزوّد)
Resolve-DnsName -Name resend._domainkey.send.sr-coresync.com -Type CNAME
```

ثم أرسل رسالة فعلية وافحص ترويسة `Authentication-Results` في صندوق المستلم —
هذا هو الحكم النهائي، لا مجرد وجود السجل.

---

## 5. الوضع الحالي للعناوين

| العنوان | الاستخدام | ملاحظة |
|---|---|---|
| `info@sr-coresync.com` | 411 إشارة في الموقع — العنوان الرئيسي | يجب أن يكون صندوقًا حقيقيًا أو تحويلًا مُختبَرًا |
| `support@` | 29 إشارة | غير مؤكد وجوده |
| `billing@` | 7 إشارات + مستخدم SMTP في الكود القديم | غير مؤكد |
| `leads@` | `MAIL_FROM` في الـ Worker | يجب أن يكون على نطاق الإرسال |
| `security@` / `dmarc-reports@` / `tlsrpt@` | تقارير | يجب إنشاؤها قبل تفعيل DMARC، وإلا فقدت التقارير |

**قبل تفعيل DMARC:** تأكد أن كل عنوان من هذه العناوين يستقبل فعلًا (أرسل إليه
رسالة من خارج النطاق). تقارير DMARC المرسلة إلى صندوق غير موجود = صفر رؤية.

---

## 6. تشغيل بريد التنبيه عبر Resend — خطوة بخطوة (لبريدك أنت)

> الوضع الحالي: `emailChannel: none` — الاستفسار يُحفظ ولا يُبلَّغ أحد.

**أ) في لوحة Resend**
1. أنشئ حسابًا (Free) → **Domains → Add Domain** → اكتب `send.sr-coresync.com`
2. سيعرض لك ثلاثة سجلات. لا تنسخها من هنا — القيم خاصة بحسابك.

**ب) في Hostinger (hPanel → DNS Zone Editor)** — أضف ما يعرضه Resend، وبأسماء مضيف كما يلي:

| النوع | الاسم في Hostinger | القيمة |
|---|---|---|
| `TXT` | `send` | `v=spf1 include:amazonses.com ~all` |
| `TXT` أو `CNAME` | `resend._domainkey.send` | القيمة من لوحة Resend |
| `MX` (اختياري) | `send` | أولوية 10 → `feedback-smtp.eu-west-1.amazonses.com` |

> **مهم:** لا تلمس سجلات `MX` الحالية (`mx1/mx2.improvmx.com`) ولا SPF الجذر. هذه إضافات على النطاق الفرعي فقط.

**ج) في Resend:** اضغط **Verify** — يتحول إلى Verified خلال دقائق.

**د) خزّن المفتاح (بنفسك، ولا يظهر في أي محادثة)**
```powershell
cd "workers/sr-lead-capture"
node node_modules/wrangler/bin/wrangler.js secret put RESEND_API_KEY
# الصق المفتاح (re_...) ثم Enter
node node_modules/wrangler/bin/wrangler.js deploy
```

**هـ) تحقّق (أمران)**
```powershell
python scripts/verify_email_channel.py
# يجب أن يتحول emailChannel إلى resend

python scripts/verify_email_channel.py --send info@sr-coresync.com
# يرسل استفسارًا تجريبيًا حقيقيًا → افتح الصندوق
```

**و) بعد التأكد:** أضف DMARC تدريجيًا (القسم 2/د) — يبدأ `p=none` ثم `quarantine`.
