import os
import sys
import asyncio
from dotenv import load_dotenv
from google import antigravity
from google_antigravity import LocalAgentConfig

# Ensure UTF‑8 output for Arabic characters
sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env (expects GEMINI_API_KEY)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("تنبيه: لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")
    sys.exit(1)
else:
    print("تم تحميل مفتاح الاتصال بنجاح!")

# Configure the local Antigravity agent
config = LocalAgentConfig(model="gemini-3.5-flash", api_key=api_key)
print("تم تكوين الوكيل الذكي المحلي (LocalAgentConfig) بنجاح وجاهز للإرسال.")

async def main():
    # Simple prompt to demonstrate the agent
    prompt = "قل لي التحية باللغة العربية."
    response = await config.send_message(prompt)
    print("استجابة الوكيل:", response)

if __name__ == "__main__":
    asyncio.run(main())
