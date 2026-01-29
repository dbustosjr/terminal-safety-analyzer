# Terminal Command Safety Analyzer

AI-powered tool that analyzes terminal commands for safety issues using **mcp-use** and **Claude Sonnet 4.5**.

## 🎯 Purpose

Built to demonstrate proficiency with mcp-use library for the **MCP Use Software Engineer** role. This project showcases:
- Integration of mcp-use's MCPAgent and MCPClient
- Real-world application of MCP for developer tools
- Production-ready Python code
- Claude API integration via LangChain

## ✨ Features

- **Pattern Matching**: Detects 30+ dangerous command patterns
- **AI Analysis**: Claude provides context-aware safety assessment
- **Severity Levels**: CRITICAL, HIGH, MEDIUM, LOW classifications
- **Safe Alternatives**: Suggests safer ways to accomplish tasks
- **MCP Integration**: Uses filesystem MCP server for context

## 🚀 Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## 💻 Usage

### Interactive Mode
```bash
python safety_analyzer.py
```

### Demo Mode (for presentations)
```bash
python demo.py
```

## 🏗️ Architecture
```
User Command → Safety Analyzer → Pattern Check → Claude Analysis → Result
                      ↓
                 MCP Client → Filesystem MCP Server
```

## 🔧 Tech Stack

- **mcp-use**: MCP framework for agent and client
- **Claude Sonnet 4.5**: AI analysis via Anthropic API
- **LangChain**: LLM integration layer
- **Python 3.10+**: Core language

## 📊 Example Output
```
==================================================================
COMMAND: rm -rf /
==================================================================

⚠️  SAFETY WARNING: This command is potentially DANGEROUS

[CRITICAL] file_system_destruction
  Pattern: rm -rf /
  ✓ Safe alternative: Specify exact directory to remove

Claude's Analysis:
------------------------------------------------------------------
This command is EXTREMELY DANGEROUS and should NEVER be run.

What it does: Attempts to recursively delete all files starting
from the root filesystem.

Risks: Complete system destruction, data loss, unrecoverable system

Safer alternative: Always specify the exact directory path and
verify before deletion: rm -rf /path/to/specific/directory
==================================================================
```

## 🎓 What I Learned

Building this project taught me:
1. How mcp-use simplifies MCP integration
2. The power of combining pattern matching + AI analysis
3. Importance of user-friendly error messages
4. Production-ready Python project structure

## 🔗 Links

- [mcp-use GitHub](https://github.com/mcp-use/mcp-use)


## 📝 License

MIT

## 📚 Citation

@software{mcp_use2025,
  author = {Zullo, Pietro and Contributors},
  title = {MCP-Use: Complete MCP Ecosystem for Python and TypeScript},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/mcp-use/mcp-use}
  
}


