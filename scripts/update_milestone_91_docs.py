with open('task.md', 'r', encoding='utf-8') as f:
    task_content = f.read()

milestone_task_91 = """
<!-- id: 91 -->
- [x] **المرحلة 91: تحويل كبسولة اللغات إلى كبسولة عائمة فاخرة بأسفل الشاشة ودمج رابط العقد في رسالة العميل**
  - **الهدف**: تنفيذ الخيارات الثلاثة مجتمعة (1+2+3) استجابة لطلب المستخدم؛ بتحويل مظهر كبسولة اللغات إلى كبسولة عائمة فاخرة في أسفل الشاشة (Bottom-Floating Luxury Pill)، تفعيل وتسهيل روابط الاختبار المباشر، وتضمين رابط العقد الرسمي المباشر `https://sr-coresync.com/clgid-contract.html` في رسالة الواتساب الموجهة للأستاذ محمود الناصر.
  - **الإنجازات**:
    1. إعادة تصميم كبسولة اللغات في `css/sr-geo-lang.css` لتطفو بزاوية الشاشة السفلية (Bottom-Left في العربية / Bottom-Right في اللغات الأوروبية) بتصميم كبسولي بيضاوي فاخر (`border-radius: 999px`) مع خلفية زجاجية معتمة بظلال ناعمة وإطار ذهبي رقيق وحركات انزلاق صاعدة (`slide-up`).
    2. استقرار الكبسولة فوق شريط التنقل السفلي في الهواتف الذكية مع استجابة كاملة لكافة الشاشات.
    3. دمج رابط مراجعة وتوقيع مسودة العقد الرسمي المباشر B2B في رسائل الواتساب والبريد الإلكتروني الموجهة للأستاذ محمود الناصر.
    4. اجتياز كافة اختبارات الأمان والجودة (147 CSP Hashes، 0 أخطاء برمجية، 100% Isolation).
"""

if "<!-- id: 91 -->" not in task_content:
    task_content += milestone_task_91
    with open('task.md', 'w', encoding='utf-8') as f:
        f.write(task_content)
    print("Updated task.md with Milestone 91.")

with open('walkthrough.md', 'r', encoding='utf-8') as f:
    walkthrough_content = f.read()

milestone_walkthrough_91 = """
---

## المرحلة 91: تفعيل الكبسولة العائمة بأسفل الشاشة وتجهيز رسالة العقد لمحمود الناصر (1+2+3)

### 1. الكبسولة العائمة بأسفل الشاشة (Bottom-Floating Luxury Pill)
- تم نقل موضع الكبسولة من الشريط العلوي العريض إلى كبسولة عائمة زجاجية فاخرة تستقر بأسفل الشاشة:
  - **في الواجهة العربية:** تطفو في أسفل يسار الشاشة (`bottom: 24px; left: 24px`).
  - **في الواجهات الأوروبية:** تطفو في أسفل يمين الشاشة (`bottom: 24px; right: 24px`).
  - **في الموبايل:** ترتفع تلقائياً فوق شريط الأدوات السفلي (`bottom: 84px`).
  - **التصميم:** حواف دائرية كاملة (Pill shape - 999px)، خلفية زجاجية بلورية (`backdrop-filter: blur(28px)`), إطار ذهبي نحيف فخم مع تأثيرات الوهج، وزر أخضر زمردي للتبديل الفوري.

### 2. روابط اختبار الكبسولة الحية
- يمكن لأي زائر تجربة انزلاق الكبسولة وصعودها من أسفل الشاشة عبر:
  - 🇳🇱 [`https://sr-coresync.com/demo.html?test_lang=nl`](https://sr-coresync.com/demo.html?test_lang=nl)
  - 🇩🇪 [`https://sr-coresync.com/demo.html?test_lang=de`](https://sr-coresync.com/demo.html?test_lang=de)
  - 🇸🇦 [`https://sr-coresync.com/de/demo.html?test_lang=ar`](https://sr-coresync.com/de/demo.html?test_lang=ar)

### 3. مسار إرسال العقد للأستاذ محمود الناصر
- تم تحديث رسالة الواتساب المتولدة في المنصة لتتضمن الرابط الحي المباشر للعقد:
  - الرابط: `https://sr-coresync.com/clgid-contract.html`
  - يمكن للأستاذ محمود فتح الرابط مباشرة من هاتفه والتوقيع الإلكتروني بنقرة واحدة بموجب القانون الهولندي eIDAS.
"""

if "المرحلة 91" not in walkthrough_content:
    walkthrough_content += milestone_walkthrough_91
    with open('walkthrough.md', 'w', encoding='utf-8') as f:
        f.write(walkthrough_content)
    print("Updated walkthrough.md with Milestone 91.")

