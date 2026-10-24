# حالة ترحيل البريد إلى Purelymail — مرجع تشغيلي

آخر تحديث: السبت 24 أكتوبر 2026 — 17:40

> **الحالة: DNS مكتمل ✓** — `MX ✓ | SPF ✓ | DKIM ✓ | DMARC ✓`
> المُتحقَّق منه من الخادمين الرسميين (artemis/hermes.dns-parking.com) عبر Google + Cloudflare.
> المتبقي: **اختبار استقبال وإرسال حقيقي** (DNS لا يستطيع إثبات وجود صندوق).

## المستخدمون (Users)

| العنوان | الحالة |
|---|---|
| `salimgrav@purelymail.com` | admin الحساب |
| `info@sr-coresync.com` | ✓ منشأ |
| `salim@sr-coresync.com` | ✓ منشأ |
| `raed@sr-coresync.com` | ✓ منشأ |
| `support@sr-coresync.com` | يظهر 31 مرة في الموقع — تحقّق من وجوده |
| `billing@sr-coresync.com` | يظهر 11 مرة (الفواتير) — تحقّق من وجوده |

> بديل: `Routing rules` أو `catch-all` لتوجيه العناوين غير المنشأة إلى `info@`.

## الحساب
| البند | القيمة |
|---|---|
| حساب Purelymail | `salimgrav@purelymail.com` |
| معرّف النطاق في لوحتهم | `175728` (الرابط: /manage/domain/175728) |
| الخطة | Simple — $10/سنة رصيد، تعبئة تلقائية بسقف $11/سنة |
| Deliver Mail To | Purelymail (الافتراضي) |
| Allow Account Reset | مفعّل |

## سجل الملكية الصحيح (مهم — الحرف `6` لا `0`)
```
purelymail_ownership_proof=7cc6acfb76ed800e73c57f78eec7cea843de55ccd7ef579a3b80150ac82b805861c4634fd87d3683dfd9f91a875b54b1723c1557695dae1d761f117d91a9cff2
```
> تم التحقق من تطابقه (155 حرفًا) على Google DNS و Cloudflare DNS.

## DNS المنشور والمتحقَّق منه ✅ (17:40)

| النوع | الاسم | القيمة |
|---|---|---|
| `MX` | `@` | **50** `mailserver.purelymail.com` ← أساسي |
| `MX` | `@` | **90** `mx1.improvmx.com` ← احتياطي (احذفه بعد أسبوع) |
| `MX` | `@` | **100** `mx2.improvmx.com` ← احتياطي |
| `TXT` | `@` | `v=spf1 include:_spf.purelymail.com ~all` |
| `TXT` | `@` | سجل الملكية أعلاه |
| `CNAME` | `purelymail1._domainkey` | `key1.dkimroot.purelymail.com` |
| `CNAME` | `purelymail2._domainkey` | `key2.dkimroot.purelymail.com` |
| `CNAME` | `purelymail3._domainkey` | `key3.dkimroot.purelymail.com` |
| `CNAME` | `_dmarc` | `dmarcroot.purelymail.com` → يخدم `p=reject; ruf=mailto:dmarc@purelymail.com` |
| `A` | `@` | 185.199.108.153 · .109.153 · .110.153 · .111.153 (GitHub Pages) |
| `CNAME` | `www` | `salim-grav.github.io` |

اختياريان لم يُضافا بعد: `CNAME autoconfig → autoconfig.purelymail.com` ·
`SRV _autodiscover._tcp → autodiscover.purelymail.com (0 0 443)`.

### التحقق من DKIM (سلسلة CNAME ثم مفتاح عام حقيقي)
```
purelymail1._domainkey.sr-coresync.com → key1.dkimroot.purelymail.com.
   ثم TXT: v=DKIM1; k=rsa; t=s; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A…
```
> هذا يفيد أن التوقيع يعمل فعلًا، لا أن السجل موجود فقط.

## إعدادات الأجهزة
| الخدمة | الخادم | المنفذ |
|---|---|---|
| IMAP | `imap.purelymail.com` | 993 (SSL) |
| SMTP | `smtp.purelymail.com` | 587 (STARTTLS) |
| POP3 | `pop3.purelymail.com` | 995 (SSL) |
| Webmail | `https://inbox.purelymail.com` — **ليس** `purelymail.com/webmail` (يعطي 404) | — |

## ما تبقّى — اختبار حقيقي
DNS لا يثبت وجود صندوق. طريقتان:

1. **من Gmail** → أرسل إلى `info@sr-coresync.com` ثم افتح Webmail على **`https://inbox.purelymail.com`**.
   يجب أن يظهر في Inbox لا في Spam. (`purelymail.com/webmail` مسار غير موجود → 404؛
   وروابط الموقع العلوية «WEBMAIL» تشير إلى النطاق الفرعي `inbox`.)
2. **من Webmail** → أرسل إلى Gmail، ثم في Gmail: «إظهار الأصل» وتحقق من
   `SPF: PASS` · `DKIM: PASS` · `DMARC: PASS`.

`scripts/probe_recipients.py` يفحص وجود الصناديق على المنفذ 25 دون إرسال رسالة،
لكن مزوّد الإنترنت هنا يحجب المنفذ 25 (انتهى بمهلة) — يُشغَّل من VPS أو GitHub Action.

## أدوات
```powershell
python scripts/check_mail_setup.py --profile purelymail --dkim-selector purelymail1
python scripts/snapshot_dns.py            # يقارن مع dns-snapshot.json
python scripts/snapshot_dns.py --save     # يحدّث الأساس بعد تغيير مقصود
python scripts/probe_recipients.py --all-default
python scripts/check_mail_setup.py --guide purelymail
```

`dns-snapshot.json` يحرس الآن 9 مجموعات: A · MX · TXT · www · _dmarc TXT ·
DKIM ×3 (CNAME) · _dmarc CNAME.

## تحذيرات مستخلصة من حادثة اليوم
1. **لا تضغط «إعادة تعيين سجلات DNS»** في Hostinger — مسح كل السجلات وأوقف الموقع والبريد.
2. أدوات الفحص تقرأ من Google + Cloudflare معًا، لأن كاش خادم واحد يعطي نتيجة خاطئة أو قديمة.
3. سجل الملكية يُنسخ بـ**زر النسخ** لا يدويًا — خطأ حرف واحد (`0` بدل `6`) كلّف جولة كاملة.
4. `check_mail_setup.py` كان يفحص `purelymail1.sr-coresync.com` بدل `purelymail1._domainkey…`
   فيُبلّغ «DKIM missing» كذبًا — أُصلح: يضيف `._domainkey` تلقائيًا.
5. بعد propagation، قد تُظهر بعض المخدمات MX القديمة (10/20) من الكاش لساعات — السلطة على
   `artemis/hermes.dns-parking.com` هي المرجع.
