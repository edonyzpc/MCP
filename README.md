# MCP
Personal MCP Servers and Clients for LLM

## Setup
1. init the project with `uv`
```bash
uv init --python=3.10 .
touch .gitignore .env
cat << EOF >> .gitignore
.env
.venv/
__pycache__/
EOF
```
2. init python virtual environment
```bash
uv venv
source .venv/bin/activate
```
3. install dependencies
```bash
uv add httpx mcp python-dotenv langchain langchain-core langchain-mcp-adapters langchain-community langgraph
```

## MCP Server


## MCP Client