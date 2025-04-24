from typing import Dict
import os
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

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


class EPUB2AudioClient:
    def __init__(self):
        # Initialize session and client objects
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()

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
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def load_mcp_tools():
    client = EPUB2AudioClient()
    try:
        await client.connect_to_mcp_server("markitdown-mcp")
    finally:
        await client.cleanup()


def main():
    """Main function to run the MCP Client"""
    print("MCP Client Started!")
    asyncio.run(load_mcp_tools())
    print("MCP Client Finished!")
