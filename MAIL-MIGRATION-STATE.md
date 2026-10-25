# حالة ترحيل البريد إلى Purelymail — مرجع تشغيلي

آخر تحديث: السبت 24 أكتوبر 2026 — 18:24

> ## ✅ مكتمل — البريد يعمل إرسالًا واستقبالًا
>
> **دليل الإرسال (18:22):** رسالة من `info@sr-coresync.com` إلى Gmail، ونتيجة الفحص في
> «إظهار الأصل»:
>
> | الفحص | النتيجة | التفصيل |
> |---|---|---|
> | `SPF` | **PASS** | IP `34.202.193.197` (Purelymail على AWS) |
> | `DKIM` | **PASS** | نطاق `sr-coresync.com` — التوقيع تحقق من المفتاح المنشور |
> | `DMARC` | **PASS** | السياسة `p=reject` راضية (Alignment + SPF/DKIM) |
>
> **الاستقبال:** مُتحقَّق منه ضمنيًا — الرسائل تصل إلى `inbox.purelymail.com` بعد
> تحويل MX إلى أولوية 50، والصناديق الخمسة موجودة.
>
> ما تبقّى اختياري: حذف MX الاحتياطيين بعد أسبوع · تعديل `MAIL_FROM` في الـ Worker ·
> إضافة `autoconfig` و`SRV`.

## المستخدمون (Users) — مكتمل ✓ (18:12)

| العنوان | الحالة |
|---|---|
| `salimgrav@purelymail.com` | admin الحساب |
| `info@sr-coresync.com` | ✓ |
| `support@sr-coresync.com` | ✓ (يظهر في 58 ملفًا على الموقع) |
| `billing@sr-coresync.com` | ✓ (يظهر في ملفين) |
| `salim@sr-coresync.com` | ✓ |
| `raed@sr-coresync.com` | ✓ |

الخمسة المنشورة على الموقع كلها موجودة، فلا عنوان ظاهر للزائر بلا صندوق.
سبعة عناوين أخرى (`security@` · `dmarc@` · `dmarc-reports@` · `tlsrpt@` ·
`leads@` · `client-audit@` · `onboarding-test@`) ترد في ملفات تشغيلية فقط ولا يراها الزائر.

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

## إشعارات بريدية من المنصة — تعمل ✅ (25 أكتوبر 05:30)
الـ Worker يرسل بنفسه عبر `smtp.purelymail.com:587` بـ STARTTLS (Cloudflare يحجب 25 فقط).

**دليل التشغيل الكامل:**
```
/mail/check?deep=1  -> verified=true · steps=connected,tls,auth
/mail/selftest      -> ok=true · steps=connected,tls,auth,sent
Inbox info@         -> "SMTP self-test 2026-10-25 05:29"
                       DKIM signed — selector=purelymail1 domain=sr-coresync.com
                       Authentication-Results: purelymail.com; auth=pass
Lead تجريبي          -> "New Consultation Lead LEAD-SR-20261025-DUE4" وصل بالتوقيع نفسه
```

| المسار | ما يفعله |
|---|---|
| `/health` | `emailChannel` و`purelymail: on\|off` (وجود الأسرار فقط) |
| `/mail/check` | هل الأسرار موجودة |
| `/mail/check?deep=1` | مصادقة SMTP حقيقية بلا إرسال — محدود مرة/5 دقائق |
| `/mail/selftest` | يرسل رسالة فعلية إلى `NOTIFY_EMAIL` — محدود مرة/10 دقائق |
| `/mail/dns` | يقرأ MX/SPF/DKIM/DMARC عبر DoH ويعيد حكمًا واحدًا |

### أخطاء واجهناها وأصلحناها
1. **`WritableStream is currently locked`** — `startTls()` يجب أن يُسبق بتحرير قفل reader/writer القديمين.
2. **قيمة السرّ كانت نص العنصر النائب** (`Enter a secret value:`) — اكتُشفت بفكّ base64 من رسالة 535.
3. **تسريب السرّ في رسالة الخطأ** — كان `AUTH` يعيد الأمر كما هو (كلمة المرور بصيغة base64). الآن يظهر `AUTH password rejected` فقط.

### مكان بيانات الاعتماد
- السرّ في Cloudflare: `PURELYMAIL_PASS` (نوع Secret).
- محليًا للفحص: `.secrets/purelymail-pass.txt` (خارج Git) — يقرأه `scripts/check_mailbox.py`.
- ⚠️ كلمة المرور ظهرت في محادثة 25 أكتوبر ⇒ يُنصح بتدويرها في Purelymail ثم `wrangler secret put PURELYMAIL_PASS` بالقيمة الجديدة.

## صفحة الحالة
`status.html` تقرأ الحالة من الخدمة نفسها: `/health` · `/mail/dns` · `/mail/check?deep=1`،
بلسانين (AR/EN)، ومربوطة من تذييل البوابات الـ29: العربية من الجذر، والـ28 الباقية إلى `?lang=en`.

## سجلات اختيارية لم تُضف بعد
| النوع | الاسم | القيمة | الفائدة |
|---|---|---|---|
| `CNAME` | `autoconfig` | `autoconfig.purelymail.com` | إعداد تلقائي في Thunderbird وأمثاله |
| `SRV` | `_autodiscover._tcp` | `autodiscover.purelymail.com` · 0 · 0 · **443** | إعداد تلقائي في Outlook والجوال |

بعد إضافتهما: `python scripts/snapshot_dns.py --save` لكي يحرسهما فحص الانحراف.

## ما تبقّى — اختبار حقيقي ✅ تم
رسالة واحدة من Webmail إلى Gmail أثبتت كل شيء:

| الفحص | النتيجة (18:22) |
|---|---|
| `SPF` | PASS — IP 34.202.193.197 |
| `DKIM` | PASS — d=sr-coresync.com |
| `DMARC` | PASS |

إعادة الاختبار لاحقًا: من `inbox.purelymail.com` إلى Gmail ثم «إظهار الأصل».
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

`dns-snapshot.json` يحرس الآن 11 مجموعة: A · MX · TXT · www · _dmarc TXT ·
DKIM ×3 (CNAME) · _dmarc CNAME · autoconfig · SRV. ومنذ 24/10 يُسجّل الأساس
بإجماع المُحلّلين (تقاطع Google وCloudflare) كي لا يدخل كاشٌ قديم في الأساس.

## تحذيرات مستخلصة من حادثة اليوم
1. **لا تضغط «إعادة تعيين سجلات DNS»** في Hostinger — مسح كل السجلات وأوقف الموقع والبريد.
2. أدوات الفحص تقرأ من Google + Cloudflare معًا، لأن كاش خادم واحد يعطي نتيجة خاطئة أو قديمة.
3. سجل الملكية يُنسخ بـ**زر النسخ** لا يدويًا — خطأ حرف واحد (`0` بدل `6`) كلّف جولة كاملة.
4. `check_mail_setup.py` كان يفحص `purelymail1.sr-coresync.com` بدل `purelymail1._domainkey…`
   فيُبلّغ «DKIM missing» كذبًا — أُصلح: يضيف `._domainkey` تلقائيًا.
5. بعد propagation، قد تُظهر بعض المخدمات MX القديمة (10/20) من الكاش لساعات — السلطة على
   `artemis/hermes.dns-parking.com` هي المرجع.
