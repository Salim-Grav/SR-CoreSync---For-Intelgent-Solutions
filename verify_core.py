import asyncio
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

from sr_agent_core import create_sovereign_agent_config, SOVEREIGN_SYSTEM_INSTRUCTIONS, WORKSPACE_TOOLS

cfg = create_sovereign_agent_config()
print("Model:", cfg.model)
print("System Instructions Length:", len(cfg.system_instructions))
print("Tools Count:", len(cfg.tools))
print("Workspaces:", cfg.workspaces)
print("SUCCESS: Sovereign agent core configuration verified!")
