import os
import sys
from dotenv import load_dotenv
from google import genai

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

candidates = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-flash-latest",
]

for model in candidates:
    try:
        resp = client.models.generate_content(
            model=model,
            contents="مرحبا"
        )
        print(f"AVAILABLE: {model} -> {resp.text.strip()}")
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "Quota" in err_msg:
            print(f"QUOTA EXCEEDED: {model}")
        else:
            print(f"FAILED: {model} -> {err_msg[:60]}")
