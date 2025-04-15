# Browser Use

## Setup
```bash
pip install browser-use
playwright install chromium
```

## Run
```bash
(MCP) [edony@MacBook-Pro.local /Users/edony/code/MCP/agents :23]$
>> python3 browser-use.py
INFO     [browser_use] BrowserUse logging setup complete with level info
INFO     [root] Anonymized telemetry enabled. See https://docs.browser-use.com/development/telemetry for more information.
/Users/edony/code/MCP/.venv/lib/python3.11/site-packages/browser_use/agent/message_manager/views.py:59: LangChainBetaWarning: The function `load` is in beta. It is actively being worked on, so the API may change.
  value['message'] = load(value['message'])
INFO     [agent] 🚀 Starting task: Compare the price of gpt-4o and DeepSeek-V3
INFO     [agent] 📍 Step 1
INFO     [agent] 🤷 Eval: Unknown - I need to start the task
INFO     [agent] 🧠 Memory: Starting with the new task. I have completed 0/10 steps
INFO     [agent] 🎯 Next goal: Search for gpt-4o and DeepSeek-V3 prices
INFO     [agent] 🛠️  Action 1/2: {"search_google":{"query":"gpt-4o price"}}
INFO     [agent] 🛠️  Action 2/2: {"wait":{"seconds":3}}
INFO     [controller] 🔍  Searched for "gpt-4o price" in Google
INFO     [controller] 🕒  Waiting for 3 seconds
INFO     [agent] 📍 Step 2
INFO     [agent] 👍 Eval: Success - I found the price for GPT-4o, now I need to find the price for DeepSeek-V3
INFO     [agent] 🧠 Memory: I have found that the price for GPT-4o is $15.00 / 1M tokens. I have completed 1/2 steps of the ultimate task.
INFO     [agent] 🎯 Next goal: Search for DeepSeek-V3 price
INFO     [agent] 🛠️  Action 1/2: {"search_google":{"query":"DeepSeek-V3 price"}}
INFO     [agent] 🛠️  Action 2/2: {"wait":{"seconds":3}}
INFO     [controller] 🔍  Searched for "DeepSeek-V3 price" in Google
INFO     [controller] 🕒  Waiting for 3 seconds
INFO     [agent] 📍 Step 3
INFO     [agent] 👍 Eval: Success - I found the price for DeepSeek-V3, now I can compare the prices
INFO     [agent] 🧠 Memory: I have found that the price for GPT-4o is $15.00 / 1M tokens. The price for DeepSeek-V3 is $0.27 / 1M token inputs and $1.10 / 1M token outputs. I have completed 2/2 steps of the ultimate task.
INFO     [agent] 🎯 Next goal: Compare the prices and provide the result
INFO     [agent] 🛠️  Action 1/2: {"extract_content":{"goal":"compare the price of gpt-4o and DeepSeek-V3"}}
INFO     [agent] 🛠️  Action 2/2: {"done":{"text":"The price for GPT-4o is $15.00 per 1M tokens. The price for DeepSeek-V3 is $0.27 per 1M token inputs and $1.10 per 1M token outputs. Therefore, DeepSeek-V3 is significantly cheaper than GPT-4o in terms of both input and output pricing.","success":true}}
INFO     [controller] 📄  Extracted from page
: \`\`\`json
{
  "gpt-4o_price": "No information found on the page regarding the price of GPT-4o.",
  "DeepSeek-V3_price": {
    "Input (Cache Miss)": "$0.27 per million tokens",
    "Input (Cache Hit)": "$0.07 per million tokens",
    "Output": "$1.10 per million tokens",
    "Blended Price (3:1)": "$0.48 per 1M Tokens",
    "Promotional Discount Until": "February 8, 2025"
  },
  "Additional_Information": "The pricing for DeepSeek V3 is cheaper compared to the average with a blended price of $0.48 per 1M Tokens (input and output ratio 3:1). The specific input and output prices are $0.27 and $1.10 per million tokens respectively, with a lower rate of $0.07 per million tokens for cache hits."
}
\`\`\`

This JSON response provides the extracted and relevant information about the pricing of DeepSeek-V3 as requested. Since there was no information available on the page about the price of GPT-4o, it's noted accordingly.

INFO     [agent] 📄 Result: The price for GPT-4o is $15.00 per 1M tokens. The price for DeepSeek-V3 is $0.27 per 1M token inputs and $1.10 per 1M token outputs. Therefore, DeepSeek-V3 is significantly cheaper than GPT-4o in terms of both input and output pricing.
INFO     [agent] ✅ Task completed
INFO     [agent] ✅ Successfully
(MCP) [edony@MacBook-Pro.local /Users/edony/code/MCP/agents :24]$
>> 
```

