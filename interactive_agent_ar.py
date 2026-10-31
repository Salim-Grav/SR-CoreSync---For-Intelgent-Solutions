import asyncio
import os
import sys
import logging
from datetime import datetime
from google import genai
from google_antigravity import LocalAgentConfig, Agent

# إخفاء تحذيرات النظام المؤقتة للحفاظ على نظافة التيرمينال
logging.disable(logging.WARNING)

# ضبط الترميز لدعم الطباعة باللغة العربية بسلاسة
sys.stdout.reconfigure(encoding="utf-8")

# تحميل مفتاح الاتصال من ملف البيئة المحلي
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)

# تكوين الوكيل المحلي مع مهلة زمنية 60 ثانية
config = LocalAgentConfig(
    model="gemini-2.5-flash",
    api_key=api_key,
    timeout=60.0,
)

async def chat_loop():
    print("==================================================")
    print(" مرحباً بك في واجهة الوكيل الذكي لـ S&R CoreSync ")
    print(" اكتب سؤالك أو خطتك، أو اكتب 'خروج' لإنهاء الجلسة. ")
    print("==================================================\n")

    async with Agent(config) as agent:
        while True:
            try:
                user_input = input("\nأنت: ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ["خروج", "exit", "quit"]:
                    print("إغلاق الجلسة. مع السلامة!")
                    break

                print("الوكيل: ", end="", flush=True)

                response = await asyncio.wait_for(
                    agent.chat(user_input, timeout=60.0),
                    timeout=60.0,
                )

                full_response = ""
                async for chunk in response.chunks:
                    chunk_text = getattr(chunk, "text", str(chunk))
                    print(chunk_text, end="", flush=True)
                    full_response += chunk_text

                print()

                # تسجيل الحوارات والملخصات تلقائياً لتكون جاهزة لبرنامج الإدارة
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                bridge_entry = (
                    f"### جلسة تخطيط بتاريخ: {timestamp}\n\n"
                    "**المهمة / السؤال:**\n"
                    f"{user_input}\n\n"
                    "**الرد والملخص النظيف:**\n"
                    f"{full_response}\n\n"
                    + "-" * 50
                    + "\n\n"
                )

                # حفظ السجل العام وملف الجسر المخصص لبرنامج إدارة المهام
                with open("chat_history.txt", "a", encoding="utf-8") as f:
                    f.write(bridge_entry)

                with open("verity_bridge.md", "a", encoding="utf-8") as f:
                    f.write(bridge_entry)

            except asyncio.TimeoutError:
                print("\n[تنبيه]: استغرق الوكيل وقتاً أطول من المتوقع وانتهت المهلة.")
            except Exception as e:
                print(f"\n[خطأ]: {e}")

if __name__ == "__main__":
    asyncio.run(chat_loop())
