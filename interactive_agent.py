import asyncio
import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from google.antigravity import LocalAgentConfig, Agent

# كتم تحذيرات إعادة المحاولة الداخلية للحفاظ على نظافة واجهة المستخدم
logging.getLogger().setLevel(logging.ERROR)

# ضبط الترميز لدعم الطباعة باللغة العربية بسلاسة في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

# تحميل مفتاح الاتصال من ملف .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)

# تكوين الوكيل المحلي مع مهلة زمنية للتنفيذ
config = LocalAgentConfig(
    model="gemini-3.5-flash",   # نموذج موثوق وسريع ويدعم العربية باحترافية
    api_key=api_key,
    timeout=60.0
)

# مسار ملف سجل المحادثة
CHAT_HISTORY_FILE = os.path.join(
    os.path.dirname(__file__), "chat_history.txt"
)

async def main():
    print("=" * 60)
    print("  مرحباً بك في واجهة الوكيل الذكي التفاعلي لـ S&R CoreSync")
    print("  اكتب رسالتك أو سؤالك بحرية، أو اكتب 'خروج' لإنهاء الجلسة.")
    print("=" * 60)

    # فتح جلسة محادثة متواصلة ومتعددة الأدوار (Multi-turn Chat)
    async with Agent(config) as agent:
        while True:
            try:
                # قراءة المدخلات بطريقة async دون حظر حلقة الأحداث
                user_input = await asyncio.to_thread(input, "\nأنت: ")
                if not user_input.strip():
                    continue
                if user_input.strip().lower() in ["خروج", "exit", "quit", "q"]:
                    print("\nإغلاق الجلسة. إلى اللقاء! 👋")
                    break

                print("الوكيل: ", end="", flush=True)

                # إرسال الرسالة للوكيل واستلام الرد
                response = await asyncio.wait_for(
                    agent.chat(user_input.strip()),
                    timeout=90.0
                )

                # استخراج النص الصافي والمرتب من الوكيل
                full_response = await response.text()
                print(full_response)

                # حفظ المحادثة في ملف chat_history.txt مع الطابع الزمني
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = (
                    f"[{timestamp}]\n"
                    f"المستخدم: {user_input.strip()}\n"
                    f"الوكيل:\n{full_response}\n"
                    + "-" * 50 + "\n"
                )
                with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as log_file:
                    log_file.write(log_entry)

            except asyncio.TimeoutError:
                print("\n⚠️ استغرق الوكيل وقتاً أطول من المتوقع. حاول مرة أخرى.")
            except KeyboardInterrupt:
                print("\n\nتم الإيقاف يدوياً. إلى اللقاء! 👋")
                break
            except Exception as e:
                print(f"\n[خطأ أثناء التفاعل مع الوكيل]: {e}")

if __name__ == "__main__":
    asyncio.run(main())
