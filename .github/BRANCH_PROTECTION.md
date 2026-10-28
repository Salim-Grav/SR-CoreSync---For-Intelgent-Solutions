# 🛡️ إرشادات وضوابط حماية الفرع الرئيسي السيادي (Sovereign Branch Protection Guide)

**المنصة المؤسسية:** S&R CoreSync For Intelligent Solutions  
**المستودع السحابي:** `Salim-Grav/SR-CoreSync---For-Intelgent-Solutions`  
**الفرع السيادي:** `main`  
**تاريخ الاعتماد والتفعيل السحابي:** الأربعاء، 28 أكتوبر 2026 — الساعة 06:45 مساءً  
**الحالة السحابية في GitHub Cloud:** ✅ **مُفعّل ونشط رسمياً (`HTTP 200 OK — Protected: True`)**

---

## 🔒 القواعد الإلزامية المُفعّلة على الفرع الرئيسي (Active GitHub Branch Protection Rules)

لضمان عدم تسريب أي أسرار، وعدم دمج أي شيفرة دون تدقيق سيادي صارم، تم تفعيل القواعد التالية برمجياً وسحابياً على فرع `main` عبر أداة [`scripts/configure_branch_protection.py`](../scripts/configure_branch_protection.py) وملف القواعد القياسي [`deploy/github-main-branch-ruleset.json`](../deploy/github-main-branch-ruleset.json):

### 1. إلزامية طلبات السحب والمراجعة (Require a pull request before merging) — `ACTIVE`
- **Require approvals (`1`):** طلب موافقة إلزامية واحدة على الأقل قبل الدمج (`required_approving_review_count: 1`).
- **Dismiss stale pull request approvals when new commits are pushed (`True`):** إلغاء الموافقة تلقائياً عند دفع commits جديدة لضمان إعادة المراجعة.
- **Require review from Code Owners (`True`):** فرض موافقة المالك المعين في [`.github/CODEOWNERS`](./CODEOWNERS) (`@Salim-Grav`).
- **Require conversation resolution (`True`):** إلزام إغلاق كافة ملاحظات المراجعة قبل الدمج.

### 2. إلزامية اجتياز الفحوصات الأمنية (Require status checks to pass before merging) — `ACTIVE`
- **Require branches to be up to date before merging (`Strict: True`):** إلزام تحديث الفرع بآخر إصدار قبل الدمج.
- **Status Checks الإلزامية المُفعّلة:**
  - `validate` (يتضمن `Validate GitHub Pages Publish Set` + `Sovereign Secret Scanner`)
  - `Audit Repository Credentials & Private Keys`

### 3. إلزامية التواقيع الرقمية المشفرة (Require signed commits) — `ACTIVE`
- تم تفعيل `POST /repos/.../branches/main/protection/required_signatures -> HTTP 200` لرفض أي Commit غير موقع رقمياً.

### 4. إلزامية التاريخ الخطي ومنع التعديل القسري أو الحذف — `ACTIVE`
- **Require linear history (`True`):** منع دمج الـ Merge Commits الفوضوية وفرض `Squash` أو `Rebase`.
- **Allow force pushes (`False`):** حظر الدفع القسري (`git push --force`) نهائياً.
- **Allow deletions (`False`):** حظر حذف الفرع الرئيسي `main` نهائياً.

### 5. عدم السماح بالاستثناءات حتى لمدراء النظام (Enforce for Administrators) — `ACTIVE`
- **Enforce Admins (`True`):** تطبيق القواعد على الجميع بما فيهم مسؤولو وملاك المستودع لمنع أي تجاوز غير مقصود.

---

## ⚙️ أوامر الفحص وإعادة التطبيق الآلي (CLI Automation)

- **للتحقق من حالة الحماية السحابية الحية على GitHub:**
  ```powershell
  python scripts/configure_branch_protection.py --status
  ```
- **لإعادة تطبيق وتثبيت قواعد الحماية السحابية:**
  ```powershell
  python scripts/configure_branch_protection.py --apply
  ```
