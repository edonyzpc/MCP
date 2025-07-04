import os
from browser_use import BrowserSession
import asyncio
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
from browser_use import Agent
from agents.browser.chat import ChatLangchain

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY", "")


# If no executable_path provided, uses Playwright/Patchright's built-in Chromium
browser_session = BrowserSession(
    # Path to a specific Chromium-based executable (optional)
    executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
    # For Windows: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # For Linux: '/usr/bin/google-chrome'
    # Use a specific data directory on disk (optional, set to None for incognito)
    # user_data_dir="~/.config/browseruse/profiles/default",  # this is the default
    # ... any other BrowserProfile or playwright launch_persistnet_context config...
    # headless=False,
)


async def main():
    # Create a LangChain model (OpenAI)
    langchain_model = ChatOpenAI(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=api_key,
        model="qwen-max",
    )
    langchain_model.bind(response_format={"type": "json_object"})

    tongyi_model = ChatTongyi(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=api_key,
        model="qwen-max",
    )
    tongyi_model.bind(response_format={"type": "json_object"})

    # Wrap it with ChatLangchain to make it compatible with browser-use
    llm = ChatLangchain(chat=langchain_model)

    agent = Agent(
        task="Open https://www.edony.ink/ and click the menu named '🕰️ 时光穿梭'，注意所有输出不要包括```json和```",
        llm=llm,
        browser=browser_session,
        use_thinking=False,
    )

    history = await agent.run()


asyncio.run(main())
