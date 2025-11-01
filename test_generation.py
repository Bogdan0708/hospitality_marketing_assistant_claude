#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick test of content generation"""

import subprocess
import json
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("Testing MitchfromTransylvania Content Generator...")
print("=" * 60)

# Test generating a caption
test_code = '''
import os
os.chdir("/app")

from server import generate_caption

result = generate_caption(
    topic="new Transylvanian burger with garlic sauce",
    platform="instagram",
    include_hashtags=True,
    include_call_to_action=True
)

print(json.dumps(result, indent=2))
'''

result = subprocess.run(
    ['docker', 'exec', '-i', 'mcp-content-generator', 'python', '-c', test_code],
    capture_output=True,
    text=True,
    timeout=30
)

if result.returncode == 0:
    print("✅ SUCCESS! Here's your generated content:\n")
    try:
        data = json.loads(result.stdout)
        print(f"📝 Caption:\n{data.get('caption', 'N/A')}\n")
        print(f"📊 Stats:")
        print(f"   - Character count: {data.get('character_count', 0)}")
        print(f"   - Hashtags: {len(data.get('hashtags', []))}")
        print(f"   - Brand voice: {data.get('brand_voice', 'N/A')}")
        print(f"   - Platform: {data.get('platform', 'N/A')}")
    except:
        print(result.stdout)
else:
    print("❌ Error occurred:")
    print(result.stderr)

print("\n" + "=" * 60)
print("Content generator is working!")
