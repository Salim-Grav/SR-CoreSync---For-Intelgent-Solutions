class LocalAgentConfig:
    def __init__(self, model=None, api_key=None, system_instructions=None, tools=None, workspaces=None, timeout=None):
        self.model = model; self.api_key = api_key; self.system_instructions = system_instructions
        self.tools = tools; self.workspaces = workspaces; self.timeout = timeout

class ChatResponse:
    def __init__(self, text=""): self._text = text
    async def text(self): return self._text

class Agent:
    def __init__(self, config=None): self.config = config
    async def __aenter__(self):
        raise RuntimeError("smoke-test stub: LLM intentionally unavailable -> RAG fallback expected")
    async def __aexit__(self, *a): return False
    async def chat(self, message): return ChatResponse("stub")
