# حالة ترحيل البريد إلى Purelymail — مرجع تشغيلي

آخر تحديث: السبت 24 أكتوبر 2026 — 17:15

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
> تم التحقق من تطابقه (155 حرفًا) على Google DNS و Cloudflare DNS في 16:55.

## السجلات المطلوبة من Purelymail

### أ) منشورة ومتحقَّق منها ✅
| النوع | الاسم | القيمة |
|---|---|---|
| `TXT` | `@` | سجل الملكية أعلاه |

### ب) يجب إضافتها (لا تمسّ الاستقبال الحالي)
| النوع | الاسم في Hostinger | القيمة |
|---|---|---|
| `CNAME` | `purelymail1._domainkey` | `key1.dkimroot.purelymail.com` |
| `CNAME` | `purelymail2._domainkey` | `key2.dkimroot.purelymail.com` |
| `CNAME` | `purelymail3._domainkey` | `key3.dkimroot.purelymail.com` |
| `CNAME` | `_dmarc` | `dmarcroot.purelymail.com` |
| `CNAME` | `autoconfig` (اختياري) | `autoconfig.purelymail.com` |
| `SRV` | `_autodiscover._tcp` (اختياري) | `autodiscover.purelymail.com` · 0 · 0 · 443 |

### ج) تحويل الاستقبال (المرحلة الأخيرة)
| النوع | الاسم | القيمة | الأولوية |
|---|---|---|---|
| `MX` | `@` | `mailserver.purelymail.com` | **50** |
| `MX` | `@` | `mx1.improvmx.com` (موجود — يُخفَّض) | **90** |
| `TXT` | `@` | `v=spf1 include:_spf.purelymail.com ~all` (يستبدل SPF الحالي) | — |

## حالة DNS الحالية (سليمة — لا تمسّها إلا بالخطوات أعلاه)
```
A      : 185.199.108.153 · .109.153 · .110.153 · .111.153   (GitHub Pages)
CNAME  : www → salim-grav.github.io
MX     : 10 mx1.improvmx.com · 20 mx2.improvmx.com            (تحويل البريد الحالي)
TXT    : v=spf1 include:spf.improvmx.com ~all
TXT    : سجل ملكية Purelymail
DMARC  : غير موجود
```
أسماء النواقل: `artemis.dns-parking.com` · `hermes.dns-parking.com` (Hostinger)

## كيف تُدخل السجل في لوحة Hostinger (نموذج "إضافة سجل")

النموذج فيه أربعة حقول بهذا الترتيب، واللوحة تضيف النطاق تلقائيًا بجانب حقل الاسم:

| الحقل في اللوحة | ماذا تكتب | ملاحظة |
|---|---|---|
| **النوع** | `CNAME` (أو `TXT` / `MX` حسب السجل) | من القائمة المنسدلة |
| **الاسم** | `purelymail1._domainkey` | بلا `@` وبلا `.sr-coresync.com` — اللوحة تعرض النطاق بجانب الحقل بلون رمادي |
| **القيمة** | `key1.dkimroot.purelymail.com` | أو ما يطلبه السجل |
| **TTL** | `3600` | أو اتركه |

قيم حقل الاسم للسجلات الأربعة:

| السجل | الاسم الذي تكتبه | القيمة |
|---|---|---|
| DKIM 1 | `purelymail1._domainkey` | `key1.dkimroot.purelymail.com` |
| DKIM 2 | `purelymail2._domainkey` | `key2.dkimroot.purelymail.com` |
| DKIM 3 | `purelymail3._domainkey` | `key3.dkimroot.purelymail.com` |
| DMARC | `_dmarc` | `dmarcroot.purelymail.com` |
| AutoConfig | `autoconfig` | `autoconfig.purelymail.com` |

> استثناء واحد فقط: سجلات MX وSPF التابعة للنطاق نفسه تُكتب باسم `@` (كما فُعل مع سجلات A).
> السجلات أعلاه كلها أسماء فرعية، فلا `@` فيها.

## إعدادات الأجهزة بعد إنشاء الصناديق
| الخدمة | الخادم | المنفذ |
|---|---|---|
| IMAP | `imap.purelymail.com` | 993 (SSL) |
| SMTP | `smtp.purelymail.com` | 587 (STARTTLS) |
| POP3 | `pop3.purelymail.com` | 995 (SSL) |

## تحذيرات مستخلصة من حادثة اليوم
1. **لا تضغط «إعادة تعيين سجلات DNS»** في لوحة Hostinger — مسح كل السجلات في 16:20 وأوقف الموقع (صفحة Parking) والبريد.
2. أدوات الفحص تقرأ من Google + Cloudflare معًا، لأن كاش خادم واحد أعطى نتيجة خاطئة.
3. `python scripts/snapshot_dns.py --verbose` يكشف أي اختفاء للسجلات؛ اللقطة محفوظة في `dns-snapshot.json`.
4. سجل الملكية يجب أن يُنسخ بـ**زر النسخ** لا يدويًا — خطأ حرف واحد (0 بدل 6) كلّف جولة كاملة.

## الأوامر المرجعية
```powershell
python scripts/check_mail_setup.py --profile purelymail --dkim-selector purelymail1
python scripts/snapshot_dns.py --verbose
python scripts/check_mail_setup.py --guide purelymail
```
