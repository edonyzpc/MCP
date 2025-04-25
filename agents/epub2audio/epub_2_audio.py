from typing import Dict
import os
import math
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from datetime import datetime

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import (
    load_mcp_tools,
    convert_mcp_tool_to_langchain_tool,
)
from langchain_text_splitters import MarkdownTextSplitter
from langgraph.prebuilt import create_react_agent
from langchain_community.chat_models import ChatTongyi

from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback

from . import utils
from tracing.logging import logger

MCP_SERVER_CONFIGs = {
    "markitdown-mcp": {
        "command": "/opt/homebrew/bin/markitdown-mcp",
        "args": [],
        "env": None,
    },
    "filesystem-mcp": {
        "command": "/Users/edony/.nvm/versions/node/v20.18.3/bin/npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/Users/edony/Downloads/",
        ],
        "env": None,
    },
}


class ThreadSafeAsyncioEvent(asyncio.Event):
    def set(self):
        self._loop.call_soon_threadsafe(super().set)


class EPUB2AudioClient:
    def __init__(self):
        # Initialize session and client objects
        self.sessions: Dict[str, ClientSession] = {}
        self.qwen = ChatTongyi(
            temperature=0.85, model="qwen-max-latest", verbose=False, streaming=True
        )
        self.exit_stack = AsyncExitStack()
        self.__md_str = ""

    def split_text(self, text: str, max_length: int = 2000) -> list:
        splitter = MarkdownTextSplitter(chunk_size=max_length, chunk_overlap=0)
        return splitter.split_text(text)

    async def connect_to_mcp_server(self, mcp_server_name: str):
        """Connect to an MCP server

        Args:
            mcp_server_name: Name of the MCP server to connect to
        """
        if mcp_server_name not in MCP_SERVER_CONFIGs:
            raise ValueError(f"Server {mcp_server_name} not found in configuration")

        command = MCP_SERVER_CONFIGs[mcp_server_name]["command"]
        args = MCP_SERVER_CONFIGs[mcp_server_name]["args"]
        env = MCP_SERVER_CONFIGs[mcp_server_name]["env"]

        server_params = StdioServerParameters(command=command, args=args, env=env)

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.sessions[mcp_server_name] = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.sessions[mcp_server_name].initialize()

        # List available tools
        response = await self.sessions[mcp_server_name].list_tools()
        tools = response.tools
        logger.debug(
            "Connected to server with tools: %s", [tool.name for tool in tools]
        )

    async def convert_epub_to_markdown(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        available_tools = []

        # Load tools from all sessions
        for session in self.sessions:
            tools = await load_mcp_tools(self.sessions[session])
            available_tools.extend(tools)
            if session == "markitdown-mcp":
                # enforce a tool output from an agent avoiding any additional text the the agent adds after the tool call
                for tool in tools:
                    tool.return_direct = True

        # logger.debug("Available tools:", available_tools[0])

        # Initial Qwen API call
        agent = create_react_agent(self.qwen, available_tools)
        response = await agent.ainvoke({"messages": query})

        # Detailed processing of tool calls if you use other LLM, e.g. Claude
        self.__md_str = response["messages"][-1].content
        return response["messages"][-1].content

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

    async def synthesis_text_to_speech_using_asyncio(self, text_array, id):
        """
        Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
        for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
        """

        # Define a callback to handle the result
        class Callback(ResultCallback):
            def __init__(self, complete_event):
                self.file = open(f"result-{id}.mp3", "wb")
                self.complete_event = complete_event

            def on_open(self):
                logger.debug(f"websocket is open.")

            def on_complete(self):
                logger.debug(f"speech synthesis task complete successfully.")
                self.complete_event.set()

            def on_error(self, message: str):
                logger.debug(f"speech synthesis task failed, {message}")

            def on_close(self):
                logger.debug(f"websocket is closed.")
                # self.complete_event.clear()
                # self.file.close()

            def on_event(self, message):
                # logger.debug(f'recv speech synthsis message {message}')
                pass

            def on_data(self, data: bytes) -> None:
                # save audio to file
                self.file.write(data)

        # Call the speech synthesizer callback
        complete_event = ThreadSafeAsyncioEvent()
        synthesizer_callback = Callback(complete_event)

        # Initialize the speech synthesizer
        # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
        speech_synthesizer = SpeechSynthesizer(
            model="cosyvoice-v1", voice="loongstella", callback=synthesizer_callback
        )

        for text in text_array:
            speech_synthesizer.streaming_call(text)
            logger.debug(f"send text: {text[:30]}...")
            await asyncio.sleep(0.1)
        speech_synthesizer.async_streaming_complete()

        logger.debug("waiting for the synthesis to complete...")
        await complete_event.wait()

        logger.debug(
            "[Metric] data chunk id: {}, requestId: {}, first package delay ms: {}".format(
                id,
                speech_synthesizer.get_last_request_id(),
                speech_synthesizer.get_first_package_delay(),
            )
        )


async def exec():
    load_dotenv()  # load environment variables from .env
    client = EPUB2AudioClient()
    try:
        await client.connect_to_mcp_server("markitdown-mcp")
        # await client.connect_to_mcp_server("filesystem-mcp")
        response = await client.convert_epub_to_markdown(
            "把文件`/Users/edony/Downloads/hemingway-old-man-and-the-sea.epub`转换为markdown格式，大模型不要处理任何markdown，直接输出全部原文"
        )

        # split_text method
        chunks = client.split_text(response, max_length=2000)
        batch_size = 10
        batch = math.ceil(len(chunks) / batch_size)
        for i in range(batch):
            sub_chunks = chunks[i * batch_size : (i + 1) * batch_size]
            await client.synthesis_text_to_speech_using_asyncio(sub_chunks, i)
        logger.info(len(chunks))
        """
        total_length = sum(utils.calculate_actual_length(chunk) for chunk in chunks)
        if total_length > 200000:
            logger.debug(
                f"Total length of text exceeds 200000 characters. Total length: {total_length}"
            )
            # Handle the situation, e.g., truncate or raise an error
            truncated_chunks = []
            current_length = 0
            for chunk in chunks:
                if current_length + utils.calculate_actual_length(chunk) > 200000:
                    break
                truncated_chunks.append(chunk)
                current_length += utils.calculate_actual_length(chunk)
            chunks = truncated_chunks
        await client.synthesis_text_to_speech_using_asyncio(chunks)
        """

    finally:
        await client.cleanup()


def main():
    """Main function to run the MCP Client"""
    logger.debug("MCP Client Started!")
    # Load MCP tools
    asyncio.run(exec())
    logger.debug("MCP Client Finished!")
