#!/usr/bin/env python3
"""
Test script for the Content Generator MCP server
Run this to verify content generation is working
"""

import subprocess
import json
import sys

def run_mcp_tool(tool_name, **kwargs):
    """Execute an MCP tool in the content-generator container"""
    # Build Python code to call the tool
    args_str = json.dumps(kwargs)

    python_code = f'''
import sys
sys.path.insert(0, "/app")
from server import mcp
import json
mcp.run(default_tool=tool_name, default_params=json.loads('{args_str}'))
'''

    result = subprocess.run(
        ['docker', 'exec', '-i', 'mcp-content-generator', 'python', '-c', python_code],
        capture_output=True,
        text=True
    )

    return result.stdout, result.stderr, result.returncode


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def main():
    print_section("🤖 Content Generator Test Suite")

    # Check if container is running
    print("Checking if mcp-content-generator is running...")
    check = subprocess.run(
        ['docker', 'ps', '--filter', 'name=mcp-content-generator', '--format', '{{.Names}}'],
        capture_output=True,
        text=True
    )

    if 'mcp-content-generator' not in check.stdout:
        print("❌ mcp-content-generator container is not running!")
        print("Run: docker-compose up -d")
        sys.exit(1)

    print("✅ Container is running\n")

    # Test 1: Generate Caption
    print_section("Test 1: Generate Caption")
    print("Generating caption for 'new burger menu'...")

    stdout, stderr, code = run_mcp_tool(
        'generate_caption',
        topic='new burger menu',
        platform='instagram',
        include_hashtags=True
    )

    if code == 0:
        print("✅ Caption generated successfully!\n")
        print(stdout)
    else:
        print(f"❌ Failed to generate caption")
        print(f"Error: {stderr}")
        return

    # Test 2: Suggest Hashtags
    print_section("Test 2: Suggest Hashtags")
    print("Generating hashtags for 'street food'...")

    stdout, stderr, code = run_mcp_tool(
        'suggest_hashtags',
        topic='street food',
        count=10,
        platform='instagram'
    )

    if code == 0:
        print("✅ Hashtags generated successfully!\n")
        print(stdout)
    else:
        print(f"❌ Failed to generate hashtags")
        print(f"Error: {stderr}")
        return

    # Test 3: Generate Full Post
    print_section("Test 3: Generate Full Post")
    print("Generating complete post for 'weekend special'...")

    stdout, stderr, code = run_mcp_tool(
        'generate_full_post',
        topic='weekend special',
        platform='instagram',
        post_goal='engagement'
    )

    if code == 0:
        print("✅ Full post generated successfully!\n")
        print(stdout)
    else:
        print(f"❌ Failed to generate full post")
        print(f"Error: {stderr}")
        return

    # Test 4: Create Variations
    print_section("Test 4: Create Content Variations")
    print("Creating variations of a sample caption...")

    stdout, stderr, code = run_mcp_tool(
        'create_content_variations',
        base_caption='Join us this weekend for amazing food!',
        num_variations=3,
        platform='instagram'
    )

    if code == 0:
        print("✅ Variations created successfully!\n")
        print(stdout)
    else:
        print(f"❌ Failed to create variations")
        print(f"Error: {stderr}")
        return

    # Summary
    print_section("✨ Test Summary")
    print("✅ All tests passed!")
    print("\nYour content generator is working correctly.")
    print("\nNext steps:")
    print("  1. Configure Claude Desktop to use this MCP server")
    print("  2. Try different brand voices (edit BRAND_VOICE_PROFILE in .env)")
    print("  3. Customize brand voice files in brand-voice/ directory")
    print("\nHappy content creating! 🎉")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)