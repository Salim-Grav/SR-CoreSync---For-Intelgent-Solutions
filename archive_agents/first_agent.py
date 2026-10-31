"""أول وكيل حقيقي باستخدام Google Antigravity SDK.

يقرأ GEMINI_API_KEY من ملف .env، ويرسل رسالة إلى Gemini، ثم يطبع الرد.

التشغيل:
  python first_agent.py
"""

import asyncio
import sys

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

# ضبط الترميز لدعم الطباعة باللغة العربية في التيرمينال
sys.stdout.reconfigure(encoding="utf-8")

# تحميل GEMINI_API_KEY من ملف .env في جذر المشروع
load_dotenv()


async def main() -> None:
    # نموذج محدد صراحةً ومتاح لمفتاح المشروع
    config = LocalAgentConfig(model="gemini-3.5-flash")

    async with Agent(config) as agent:
        prompt = "عرّف بنفسك في جملة واحدة باللغة العربية."
        print(f"  المستخدم: {prompt}")

        response = await agent.chat(prompt)
        print(f"  الوكيل: {await response.text()}")


if __name__ == "__main__":
    asyncio.run(main())

