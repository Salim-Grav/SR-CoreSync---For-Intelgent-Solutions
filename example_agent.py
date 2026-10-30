import argparse
import asyncio
import os
import sys
from dotenv import load_dotenv
from google.antigravity import LocalAgentConfig, Agent

# ضبط الترميز لدعم الطباعة باللغة العربية في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

# تحميل المتغيّرات من ملف .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)

config = LocalAgentConfig(
    model="gemini-3.5-flash",
    api_key=api_key,
    timeout=60.0
)

async def main():
    parser = argparse.ArgumentParser(description="تشغيل وكيل Antigravity محلي")
    parser.add_argument(
        "prompt", nargs="*",
        default=["قل لي التحية باللغة العربية واشرح بإيجاز كيف نعمل محلياً"]
    )
    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    print(f"جارٍ إرسال الطلب للوكيل: {prompt}")

    try:
        async with Agent(config) as agent:
            print("✅ تم فتح جلسة الوكيل")
            response = await asyncio.wait_for(agent.chat(prompt), timeout=60.0)
            print("✅ تم استلام الاستجابة")
            # استخراج النص داخل نفس الجلسة
            text = await response.text()
            print(f"\nاستجابة الوكيل:\n{text}")
    except asyncio.TimeoutError:
        print("تنبيه: استغرق الوكيل وقتاً أطول من المتوقع (60 ث).")
    except Exception as e:
        print(f"خطأ أثناء التواصل مع الوكيل: {e}")

if __name__ == "__main__":
    asyncio.run(main())
