# مثال تشغيل وكيل Antigravity محلي

هذا المستند يوضح كيفية تشغيل السكربت `example_agent.py` الذي يستخدم حزمة **Google Antigravity SDK** لإرسال طلب إلى نموذج Gemini وعرض النتيجة.

---

## 1️⃣ تثبيت المتطلبات
```powershell
pip install -r requirements.txt
```
> **ملاحظة:** ملف `requirements.txt` يحتوي على:
> ```
> google-antigravity==0.1.23
> python-dotenv>=1.0
> ```

---

## 2️⃣ إعداد ملف البيئة `.env`
أنشئ ملف `.env` في جذر المشروع وأضف مفتاح API الخاص بـ Gemini:
```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```
> **تنبيه:** لا تشارك المفتاح مع أي أحد. الملف مُدرج في `.gitignore`.

---

## 3️⃣ تشغيل السكربت

### التشغيل الأساسي (بالطلب الافتراضي)
```powershell
python -u "d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\example_agent.py"
```

### تمرير طلب مخصص
```powershell
python -u "d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\example_agent.py" "ما هو أحدث نموذج Gemini؟"
```

### مثال على الإخراج المتوقع
```
جارٍ إرسال الطلب للوكيل: ما هو أحدث نموذج Gemini؟
✅ تم فتح جلسة الوكيل
✅ تم استلام الاستجابة

استجابة الوكيل:
أحدث نموذج من عائلة نماذج جوجل هو Gemini 3.6 Flash (ضمن جيل Gemini 3).
...
```

---

## 4️⃣ تعديل النموذج
النموذج الافتراضي هو `gemini-3.5-flash`. يمكن تغييره في السكربت:
```python
config = LocalAgentConfig(
    model="gemini-3.5-flash",   # يمكن تغييره إلى gemini-3.6-flash مثلاً
    api_key=api_key,
    timeout=60.0
)
```

---

## 5️⃣ ضبط مهلة التنفيذ
```python
config = LocalAgentConfig(
    model="gemini-3.5-flash",
    api_key=api_key,
    timeout=60.0   # المهلة بالثواني داخل LocalAgentConfig
)
# وأيضاً داخل asyncio.wait_for
response = await asyncio.wait_for(agent.chat(prompt), timeout=60.0)
```

---

## 6️⃣ ملاحظات تقنية مهمة
- **`agent.chat(prompt)`** يُعيد كائن `ChatResponse`؛ لاستخراج النص يجب `await` على `response.text()`.
- **`async with Agent(config) as agent`** يفتح جلسة الوكيل ويُغلقها تلقائيًا.
- **`await response.text()`** يجب استدعاؤه داخل نفس كتلة `async with` قبل إغلاق الجلسة.
- الاستيراد الصحيح هو `from google.antigravity import LocalAgentConfig, Agent` (وليس `google_antigravity`).
