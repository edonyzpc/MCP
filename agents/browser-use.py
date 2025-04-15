import os
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

# from langchain_community.chat_models import ChatTongyi
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY", "")


async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=api_key,
            model="qwen-max",
        ),
    )
    await agent.run()


asyncio.run(main())
