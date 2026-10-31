import sys
import os
import asyncio
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding="utf-8")

from sr_agent_server import app

async def main():
    print("Starting client...")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        print("Sending request to /health...")
        r = await c.get("/health")
        print("Response:", r.status_code, r.text)

if __name__ == "__main__":
    asyncio.run(main())
