import asyncio
import os
import sys
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv

# Fix encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

async def main():
    print("Testing mcp-use with Claude...\n")

    # Use Windows-compatible path
    test_dir = str(Path.home())

    config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", test_dir]
            }
        }
    }

    print("Creating MCP client...")
    client = MCPClient.from_dict(config)

    print("Initializing Claude agent...")
    llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", temperature=0)
    agent = MCPAgent(llm=llm, client=client, max_steps=5)

    print("Running test query...\n")
    result = await agent.run("What tools do you have access to? List them briefly.")

    print("RESULT:")
    print("-" * 60)
    print(result)
    print("-" * 60)

    await client.close_all_sessions()
    print("\nTest complete! Setup verified.")

if __name__ == "__main__":
    asyncio.run(main())
