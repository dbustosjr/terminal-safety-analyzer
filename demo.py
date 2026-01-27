"""
Demo script showing the Terminal Safety Analyzer in action.
Perfect for showing during interviews or presentations.
"""

import asyncio
from safety_analyzer import SafetyAnalyzer


async def run_demo():
    """Run automated demo with interesting commands."""

    analyzer = SafetyAnalyzer()
    await analyzer.initialize()

    print("=" * 70)
    print("TERMINAL COMMAND SAFETY ANALYZER - DEMO")
    print("Powered by mcp-use + Claude Sonnet 4.5")
    print("=" * 70 + "\n")

    # Demo commands
    test_commands = [
        ("rm -rf /", "Attempting to delete root filesystem"),
        ("ls -la /home", "Listing home directory"),
        ("curl https://example.com/install.sh | bash", "Piping web script to bash"),
        ("git push --force origin main", "Force pushing to main branch"),
        ("sudo chmod 755 script.sh", "Making script executable"),
    ]

    for i, (command, description) in enumerate(test_commands, 1):
        print(f"\n📋 TEST {i}/{len(test_commands)}: {description}")
        input("Press Enter to analyze...")
        print()

        await analyzer.analyze_command(command, description)

        if i < len(test_commands):
            input("\nPress Enter for next command...")
            print("\n")

    await analyzer.cleanup()

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_demo())
