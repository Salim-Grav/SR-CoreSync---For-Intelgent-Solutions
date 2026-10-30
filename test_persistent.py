import asyncio
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

from sr_agent_core import create_sovereign_agent_config
from google.antigravity import Agent

async def test_persistent_agent():
    cfg = create_sovereign_agent_config()
    agent_cm = Agent(cfg)
    agent = await agent_cm.__aenter__()
    print("Agent started! is_started:", getattr(agent, "is_started", None))
    try:
        resp = await agent.chat("مرحبا باختصار")
        txt = await resp.text()
        print("Reply received:", txt[:60])
    finally:
        await agent_cm.__aexit__(None, None, None)
        print("Agent closed successfully!")

asyncio.run(test_persistent_agent())
