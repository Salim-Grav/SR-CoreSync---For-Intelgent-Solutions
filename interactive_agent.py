import asyncio
import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# كتم تحذيرات إعادة المحاولة الداخلية للحفاظ على نظافة واجهة المستخدم
logging.getLogger().setLevel(logging.ERROR)

# ضبط الترميز لدعم الطباعة باللغة العربية بسلاسة في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

# تحميل مفتاح الاتصال من ملف .env
load_dotenv()

from sr_agent_core import (
    create_sovereign_agent_config,
    SOVEREIGN_SYSTEM_INSTRUCTIONS,
    tool_get_service_details,
    tool_list_project_portals
)
from google.antigravity import Agent

# مسار ملف سجل المحادثة
CHAT_HISTORY_FILE = os.path.join(
    os.path.dirname(__file__), "chat_history.txt"
)

async def main():
    print("=" * 65)
    print("  🏛️ المستشار الذكي التنفيذي لمنظومة S&R CoreSync For Intelligent Solutions")
    print("  مدعوم بـ Google Antigravity SDK وأدوات استكشاف المشروع وسياق الميثاق")
    print("  اكتب استفسارك، أو اكتب 'بوابات' لعرض الصفحات، أو 'خروج' للإغلاق.")
    print("=" * 65)

    config = create_sovereign_agent_config()

    # فتح جلسة محادثة متواصلة ومتعددة الأدوار (Multi-turn Chat)
    async with Agent(config) as agent:
        while True:
            try:
                # قراءة المدخلات بطريقة async دون حظر حلقة الأحداث
                user_input = await asyncio.to_thread(input, "\nأنت: ")
                if not user_input.strip():
                    continue

                clean_cmd = user_input.strip().lower()
                if clean_cmd in ["خروج", "exit", "quit", "q"]:
                    print("\nإغلاق الجلسة المؤسسية. إلى اللقاء! 👋")
                    break

                if clean_cmd in ["بوابات", "صفحات", "portals", "pages"]:
                    print("\n" + tool_list_project_portals())
                    continue

                print("المستشار: ", end="", flush=True)

                # إرسال الرسالة للوكيل واستلام الرد
                try:
                    response = await asyncio.wait_for(
                        agent.chat(user_input.strip()),
                        timeout=90.0
                    )
                    full_response = await response.text()
                except Exception as e:
                    # صمود سيادي عند ضغط الحصة
                    full_response = tool_get_service_details(user_input.strip())

                print(full_response)

                # حفظ المحادثة في ملف chat_history.txt مع الطابع الزمني
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = (
                    f"[{timestamp}]\n"
                    f"المستخدم: {user_input.strip()}\n"
                    f"المستشار:\n{full_response}\n"
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
