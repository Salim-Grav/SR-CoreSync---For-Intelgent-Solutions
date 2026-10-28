# 🔐 دليل الخزينة السيادية لتشفير المتغيرات والأسرار (Sovereign Secret Vault Runbook)

**المنصة:** S&R CoreSync For Intelligent Solutions  
**معيار التشفير:** AES-256-GCM (Authenticated Encryption with Associated Data)  
**خوارزمية اشتقاق المفاتيح:** PBKDF2-HMAC-SHA256 (600,000 دورة اشتقاق مع Salt 128-bit عشوائي)  
**تاريخ التوثيق:** الأربعاء، 28 أكتوبر 2026

---

## 🎯 الهدف والأهمية الأمنية
توفير منظومة عزل وحماية سيادية لكافة ملفات البيئة والمتغيرات الحساسة (`.env` وما يرتبط بها من مفاتيح Stripe، Cloudflare Tokens، قواعد البيانات، والشهادات الرقمية)، بحيث:
1. يظل الملف الصريح `.env` مستبعداً بشكل قطعي من Git (`.gitignore`).
2. يتم تشفير محتواه وتحويله إلى صيغة خزينة مشفرة وآمنة `.env.vault` قابلة للتخزين الآمن والمزامنة دون أي خوف من تسريب الأسرار.
3. لا يمكن فك التشفير إلا بامتلاك مفتاح السيادة المشفر `SOVEREIGN_VAULT_KEY` أو الملف العتادي `.secrets/master.key`.

---

## 🛠️ أوامر التشغيل والتحكم (CLI Commands)

### 1. توليد مفتاح سيادي جديد (Master Key Generation):
```bash
python scripts/sovereign_vault.py keygen
```
*يقوم بتوليد مفتاح عالي العشوائية 256-bit ويحفظه في `.secrets/master.key` (المستبعد تماماً من Git).*

### 2. تشفير ملف البيئة (.env -> .env.vault):
```bash
python scripts/sovereign_vault.py encrypt
```
*يقوم بقراءة `.env` وتوليد Salt و Nonce عشوائيين وتشفيره بـ AES-256-GCM وكتابة `.env.vault` مع بصمة SHA-256 للتحقق.*

### 3. فك تشفير الخزينة (.env.vault -> .env):
```bash
python scripts/sovereign_vault.py decrypt
```
*يتحقق من صحة المفتاح وبصمة التشفير ويعيد إنشاء ملف `.env` مع أخذ نسخة احتياطية تلقائية `.env.bak`.*

### 4. فحص حالة المزامنة والأمان (Vault Audit & Status):
```bash
python scripts/sovereign_vault.py status
```
*يفحص وجود المفتاح، حالة المزامنة بين `.env` و `.env.vault`، ويتأكد من أن Git يتجاهل الملفات الصريحة.*

### 5. تدوير المفاتيح الدورية (Key Rotation):
```bash
python scripts/sovereign_vault.py rotate
```
*يفك تشفير الخزينة بالمفتاح القديم، يولد مفتاحاً سيادياً جديداً، ويعيد التشفير فورياً.*

---

## ☁️ الاستخدام في بيئات النشر السحابي (CI/CD & Cloud Deployments)
في خوادم الإنتاج أو GitHub Actions، قم بتعيين المفتاح كمتغير بيئي سري:
```bash
export SOVEREIGN_VAULT_KEY="<مفتاح_السيادة_256_بت>"
python scripts/sovereign_vault.py decrypt
```
ثم تشغيل الخدمات بأمان تام.
