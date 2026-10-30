import asyncio, os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
from google.antigravity import LocalAgentConfig, Agent
config = LocalAgentConfig(model='gemini-3.5-flash', api_key=api_key, timeout=60)

async def main():
    async with Agent(config) as agent:
        resp = await agent.chat('ما هو أحدث نموذج Gemini؟')
        print('type resp:', type(resp))
        print('has attr text?', hasattr(resp, 'text'))
        txt = getattr(resp, 'text', None)
        print('txt attr:', txt)
        print('callable?', callable(txt))
        if callable(txt):
            maybe = txt()
            print('maybe:', maybe, type(maybe))
            if hasattr(maybe, '__await__'):
                result = await maybe
                print('awaited result:', result)
            else:
                print('result directly:', maybe)
        else:
            print('txt not callable')

asyncio.run(main())

