import argparse
import asyncio
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.antigravity import LocalAgentConfig, Agent

# ضبط الترميز لدعم الطباعة باللغة العربية في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

# تحميل المتغيّرات من ملف .env (expects GEMINI_API_KEY)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)

# تكوين LocalAgentConfig (استخدام نموذج موثوق)
config = LocalAgentConfig(
    model="gemini-3.5-flash",   # أو gemini-3.8-flash إذا رغبت
    api_key=api_key,
    timeout=45.0                # مهلة أوسع
)

# إنشاء وكيل من الإعدادات (تم إلغاء الإنشاء هنا؛ سيُنشأ داخل async with)


async def main():
    # يمكن تمرير نص من سطر الأوامر (اختياري)
    parser = argparse.ArgumentParser(
        description="تشغيل وكيل Antigravity محلي"
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        default=["قل لي التحية باللغة العربية واشرح بإيجاز كيف نعمل محلياً"]
    )
    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    print(f"جارٍ إرسال الطلب للوكيل: {prompt}")

    try:
        # انتظار الرد مع مهلة 45 ثانية داخل جلسة الوكيل
        async with Agent(config) as agent:
            print("✅ تم فتح جلسة الوكيل")
            response = await asyncio.wait_for(
                agent.chat(prompt),
                timeout=30.0
            )
            print("✅ تم استلام الاستجابة")
        # طباعة النص الفعلي إذا كان متاحًا
        try:
            # معظم إصدارات ChatResponse توفر طريقة `text()` أو الخاصية `text`
            # استخراج النص: `response.text()` يُعيد coroutine يحتاج await
            printed = None
            try:
                printed = await response.text()
            except Exception as e_txt:
                # إذا فشل text() جرّب تجميع الـ chunks
                try:
                    printed = "".join([c.text async for c in response.chunks])
                except Exception:
                    printed = None
            if printed is not None:
                print(f"\nاستجابة الوكيل:\n{printed}")
            else:
                print(f"\nاستجابة الوكيل (كائن):\n{response}")
            if printed is not None:
                print(f"\nاستجابة الوكيل:\n{printed}")
            else:
                print(f"\nاستجابة الوكيل (كائن):\n{response}")
        except Exception as exc:
            print(f"\nخطأ أثناء استخراج النص من الاستجابة: {exc}")
    except asyncio.TimeoutError:
        print("تنبيه: استغرق الوكيل وقتاً أطول من المتوقع (45 ث).")
    except Exception as e:
        print(f"خطأ أثناء التواصل مع الوكيل: {e}")

if __name__ == "__main__":
    asyncio.run(main())
