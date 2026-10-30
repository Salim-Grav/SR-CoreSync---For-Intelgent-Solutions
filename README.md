# مثال تشغيل وكيل Antigravity محلي

هذا المستند يوضح كيفية تشغيل السكربت `example_agent.py` الذي يستخدم حزمة **Google Antigravity SDK** لإرسال طلب إلى نموذج Gemini وعرض النتيجة.

---

## 1️⃣ تثبيت المتطلبات
```powershell
# من جذر المشروع
pip install -r requirements.txt
```
> **ملاحظة:** ملف `requirements.txt` يحتوي على:
> ```
> google-antigravity==0.1.23
> python-dotenv>=1.0
> ```

---

## 2️⃣ إعداد ملف البيئة `.env`
إنشاء ملف `.env` في جذر المشروع (إن لم يكن موجودًا) وضع فيه مفتاح API الخاص بـ Gemini:
```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```
> **تنبيه:** لا تشارك المفتاح مع أي أحد. الملف مُدرج في `.gitignore` تلقائيًا.

---

## 3️⃣ تشغيل السكربت الأساسي
```powershell
python -u "d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\example_agent.py"
```
سيظهر في الطرفية ما يلي (مثال):
```
تم تحميل مفتاح الاتصال بنجاح!
تم تكوين الوكيل الذكي المحلي (LocalAgentConfig) بنجاح وجاهز للإرسال.
جارٍ إرسال الطلب للوكيل: قل لي التحية باللغة العربية واشرح بإيجاز كيف نعمل محلياً

استجابة الوكيل:
مرحبًا! نحن نعمل محليًا باستخدام نموذج Gemini …
```

---

## 4️⃣ تعديل النموذج
النموذج الافتراضي في السكربت هو `gemini-2.5-flash`، وهو قد لا يكون متاحًا للمستخدمين الجدد. إذا تلقيت خطأ 503 أو 401، استبدله بأحد النماذج المتاحة مثل:
```python
config = LocalAgentConfig(
    model="gemini-3.5-flash",   # نموذج موثوق
    api_key=api_key,
    timeout=30.0
)
```
أو `gemini-3.8-flash` إذا رغبت في أداء أعلى (قد يتطلب مهلة أطول).

---

## 5️⃣ ضبط مهلة التنفيذ
القيمة الافتراضية للمهلة هي 30 ثانية. إذا استغرق الوكيل وقتًا أطول، يمكنك زيادة المهلة في كائن `LocalAgentConfig` أو في `asyncio.wait_for`:
```python
config = LocalAgentConfig(
    model="gemini-3.5-flash",
    api_key=api_key,
    timeout=45.0   # مهلة 45 ثانية
)

# وفي داخل الدالة async
response = await asyncio.wait_for(config.send_message(prompt), timeout=45.0)
```

---

## 6️⃣ تمرير نص الطلب عبر سطر الأوامر (اختياري)
لجعل السكربت أكثر مرونة، يمكنك استعمال `argparse` لتحديد النص المطلوب إرساله:
```python
import argparse
parser = argparse.ArgumentParser(description="تشغيل وكيل Antigravity محلي")
parser.add_argument("prompt", nargs="*", default=["قل لي التحية باللغة العربية واشرح بإيجاز كيف نعمل محلياً"])
args = parser.parse_args()
prompt = " ".join(args.prompt)
```
ثم تشغيله هكذا:
```powershell
python example_agent.py "ما هو أحدث نموذج Gemini؟"
```

---

## 7️⃣ مراجعة سجل التنفيذ (إن لزم)
إذا لم تظهر استجابة الوكيل أو ظهرت رسائل خطأ، راجع سجل المهمة في المسار:
```
C:\Users\msali\.gemini\antigravity\brain\bf4ab143-8aba-421c-91f9-24d1a1f376a3\.system_generated\tasks\
```
ستجد ملفات `task-XXX.log` التي تحتوي على مخرجات التشغيل.

---

**تم بنجاح** إضافة دليل التشغيل الكامل إلى `README.md`.
