"""
==============================================================================
S&R CoreSync For Intelligent Solutions — Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

interactive_agent.py — واجهة المحادثة الذكية التفاعلية (Terminal CLI)
تعمل بمحرك Google Antigravity SDK مع RAG محلي وأدوات مساحة العمل.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# إخفاء تحذيرات النظام المؤقتة للحفاظ على نظافة التيرمينال
logging.getLogger().setLevel(logging.ERROR)

# ضبط الترميز لدعم الطباعة باللغة العربية بسلاسة في أي بيئة Windows
sys.stdout.reconfigure(encoding="utf-8")

# تحميل مفتاح الاتصال من ملف البيئة المحلي (.env)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️  تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)

# استيراد مكونات المنصة الذاتية السيادية
from sr_agent_core import (
    create_sovereign_agent_config,
    tool_get_service_details,
    tool_list_project_portals,
)
from google.antigravity import Agent

# مسارات ملفات السجل
_DIR = os.path.dirname(__file__)
CHAT_HISTORY_FILE  = os.path.join(_DIR, "chat_history.txt")
VERITY_BRIDGE_FILE = os.path.join(_DIR, "verity_bridge.md")


def _save_log(user_input: str, full_response: str) -> None:
    """حفظ الحوار في ملفي السجل العام وجسر التكامل."""
    timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry   = (
        f"[{timestamp}]\n"
        f"المستخدم: {user_input.strip()}\n"
        f"الوكيل:\n{full_response}\n"
        + "-" * 50 + "\n"
    )
    bridge_entry = (
        f"### جلسة تخطيط بتاريخ: {timestamp}\n\n"
        f"**المهمة / السؤال:**\n{user_input.strip()}\n\n"
        f"**الرد والملخص النظيف:**\n{full_response}\n\n"
        + "-" * 50 + "\n\n"
    )
    for path, content in ((CHAT_HISTORY_FILE, log_entry), (VERITY_BRIDGE_FILE, bridge_entry)):
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)


async def main() -> None:
    print("=" * 65)
    print("  🎯 المستشار الذكي التنفيذي لمنظومة S&R CoreSync")
    print("  مدعوم بـ Google Antigravity SDK + RAG محلي + أدوات مساحة العمل")
    print("  اكتب سؤالك، أو 'بوابات' لعرض الصفحات، أو 'خروج' للإنهاء.")
    print("=" * 65)

    config = create_sovereign_agent_config()

    # فتح جلسة محادثة متواصلة ومتعددة الأدوار (Multi-turn Chat)
    async with Agent(config) as agent:
        while True:
            try:
                # قراءة المدخلات بشكل async لتجنب تعطيل حلقة الأحداث
                user_input = await asyncio.to_thread(input, "\nأنت: ")
                if not user_input.strip():
                    continue

                clean_cmd = user_input.strip().lower()

                # أوامر التنقل السريع
                if clean_cmd in ["خروج", "exit", "quit", "q"]:
                    print("\nإغلاق الجلسة. مع السلامة! 👋")
                    break

                if clean_cmd in ["بوابات", "صفحات", "portals", "pages"]:
                    print("\n" + tool_list_project_portals())
                    continue

                print("الوكيل: ", end="", flush=True)

                # إرسال الرسالة للوكيل مع مهلة زمنية 90 ثانية
                try:
                    response = await asyncio.wait_for(
                        agent.chat(user_input.strip()),
                        timeout=90.0,
                    )
                    full_response = await response.text()
                except asyncio.TimeoutError:
                    full_response = (
                        "⏱️  استغرق الوكيل وقتاً أطول من المتوقع وانتهت المهلة. "
                        "حاول مرة أخرى أو تحقق من اتصالك."
                    )
                except Exception:
                    # Fallback: استخدام قاعدة المعرفة المحلية كبديل
                    full_response = tool_get_service_details(user_input.strip())

                print(full_response)

                # حفظ الحوار تلقائياً في ملفي السجل والجسر
                _save_log(user_input, full_response)

            except KeyboardInterrupt:
                print("\n\nتم الإيقاف يدوياً. مع السلامة! 👋")
                break
            except Exception as e:
                print(f"\n[خطأ غير متوقع من الوكيل]: {e}")


if __name__ == "__main__":
    asyncio.run(main())
