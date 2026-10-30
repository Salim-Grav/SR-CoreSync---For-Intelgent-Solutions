import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from google.antigravity import LocalAgentConfig, Agent

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
    model="gemini-3.5-flash",   # نموذج موثوق مع إعادة محاولة تلقائية عند 503
    api_key=api_key,
    timeout=60.0
)

# مسار ملف سجل المحادثة
CHAT_HISTORY_FILE = os.path.join(
    os.path.dirname(__file__), "chat_history.txt"
)

async def main():
    print("=" * 50)
    print("  مرحباً بك في واجهة الوكيل الذكي المحلي لـ S&R CoreSync")
    print("  اكتب رسالتك أو سؤالك، أو اكتب 'خروج' لإنهاء الجلسة.")
    print("=" * 50 + "\n")

    # فتح جلسة محادثة (Multi-turn Chat)
    async with Agent(config) as agent:
        while True:
            try:
                user_input = input("\nأنت: ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ["خروج", "exit", "quit"]:
                    print("\nإغلاق الجلسة. إلى اللقاء! 👋")
                    break

                print("الوكيل: ", end="", flush=True)
                full_response = ""

                # إرسال الرسالة والحصول على الاستجابة
                response = await asyncio.wait_for(
                    agent.chat(user_input),
                    timeout=60.0
                )

                # بث الرد كلمة بكلمة عبر chunks
                try:
                    async for chunk in response.chunks:
                        chunk_text = getattr(chunk, "text", str(chunk))
                        print(chunk_text, end="", flush=True)
                        full_response += chunk_text
                except TypeError:
                    # إذا لم تكن chunks async iterable، استخدم text() مباشرة
                    full_response = await response.text()
                    print(full_response, end="", flush=True)

                print()  # سطر جديد بعد اكتمال الرد

                # حفظ المحادثة في ملف chat_history.txt
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = (
                    f"[{timestamp}]\n"
                    f"المستخدم: {user_input}\n"
                    f"الوكيل: {full_response}\n"
                    + "-" * 40 + "\n"
                )
                with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as log_file:
                    log_file.write(log_entry)

            except asyncio.TimeoutError:
                print("\n⚠️ انتهت مهلة الانتظار (60 ث). حاول مرة أخرى.")
            except KeyboardInterrupt:
                print("\n\nتم الإيقاف يدوياً. إلى اللقاء! 👋")
                break
            except Exception as e:
                print(f"\n[خطأ أثناء التفاعل مع الوكيل]: {e}")

if __name__ == "__main__":
    asyncio.run(main())
