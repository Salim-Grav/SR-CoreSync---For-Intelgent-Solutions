# 🛡️ إرشادات وضوابط حماية الفرع الرئيسي السيادي (Sovereign Branch Protection Guide)

**المنصة المؤسسية:** S&R CoreSync For Intelligent Solutions  
**الفرع السيادي:** `main`  
**تاريخ الاعتماد:** الأربعاء، 28 أكتوبر 2026

---

## 🔒 القواعد الإلزامية لحماية الفرع الرئيسي (GitHub Branch Protection Rules)

لضمان عدم تسريب أي أسرار، وعدم دمج أي شيفرة دون تدقيق سيادي صارم، يتم تفعيل القواعد التالية على فرع `main` في إعدادات المستودع (`Settings -> Branches -> Branch protection rules`):

### 1. إلزامية طلبات السحب والمراجعة (Require a pull request before merging)
- **Require approvals:** طلب موافقة إلزامية واحدة على الأقل قبل الدمج.
- **Dismiss stale pull request approvals when new commits are pushed:** إلغاء الموافقة تلقائياً عند دفع commits جديدة لضمان إعادة المراجعة.
- **Require review from Code Owners:** فرض موافقة المالك المعين في `.github/CODEOWNERS` (`@Salim-Grav`).

### 2. إلزامية اجتياز الفحوصات الأمنية (Require status checks to pass before merging)
- **Require branches to be up to date before merging:** إلزام تحديث الفرع بآخر إصدار قبل الدمج.
- **Status Checks الإلزامية:**
  - `S&R CoreSync CI & Quality Assurance / validate`
  - `Sovereign Secret Scanning & IP Protection / Audit Repository Credentials & Private Keys`

### 3. إلزامية التواقيع الرقمية المشفرة (Require signed commits)
- رفض أي Commit غير موقع بمفتاح GPG أو SSH مسجل وموثق، لضمان أصالة الناشر وعدم انتحال الهوية.

### 4. إلزامية التاريخ الخطي (Require linear history)
- منع دمج الـ Merge Commits الفوضوية وفرض `Squash and merge` أو `Rebase and merge` للمحافظة على نظافة سجل الـ Git.

### 5. عدم السماح بالاستثناءات حتى لمدراء النظام (Do not allow bypassing the above settings)
- تطبيق القواعد على الجميع بما فيهم مسؤولو وملاك المستودع (Enforce for Administrators) لمنع أي تجاوز غير مقصود.
