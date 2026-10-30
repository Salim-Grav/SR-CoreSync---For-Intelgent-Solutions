import asyncio
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.antigravity import LocalAgentConfig

# ضبط الترميز لدعم الطباعة باللغة العربية في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

# تحميل المتغيّرات من ملف .env (expects GEMINI_API_KEY)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)

# تكوين الوكيل المحلي مع تحديد مهلة زمنية للتنفيذ (مثلاً 30 ثانية)
config = LocalAgentConfig(
    model="gemini-2.5-flash",
    api_key=api_key,
    timeout=30.0
)

async def main():
    prompt = "قل لي التحية باللغة العربية واشرح بإيجاز كيف نعمل محلياً"
    print(f"جارٍ إرسال الطلب للوكيل: {prompt}")
    
    try:
        # الانتظار حتى استجابة الوكيل بالكامل ضمن المهلة المحددة (30 ثانية)
        response = await asyncio.wait_for(config.send_message(prompt), timeout=30.0)
        print(f"\nاستجابة الوكيل:\n{response}")
    except asyncio.TimeoutError:
        print("تنبيه: استغرق الوكيل وقتاً أطول من المتوقع، وانتهت مهلة الـ 30 ثانية.")

if __name__ == "__main__":
    asyncio.run(main())
