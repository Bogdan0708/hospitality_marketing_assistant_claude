# 🚀 Quick Start Guide (5 Minutes)

Get your MCP-powered marketing system running in 5 minutes!

## Step 1: Copy Environment File (30 seconds)

```bash
cd C:\Users\godja\Desktop\hospitality_marketing_assistant_claude
copy .env.example .env
```

## Step 2: Add Your API Keys (2 minutes)

Open `.env` in a text editor and fill in:

### Minimum Required (to start):

```env
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional for now (Instagram features work without these initially)
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
```

### Full Setup (for Instagram integration):

Follow the [API credentials guide](README.md#-getting-your-api-credentials) in the main README.

## Step 3: Start the System (1 minute)

```bash
docker-compose up -d
```

Wait for services to start (about 30 seconds).

## Step 4: Verify It's Running (30 seconds)

```bash
docker-compose ps
```

You should see all services "Up":
- ✅ postgres
- ✅ redis
- ✅ mcp-instagram-analytics
- ✅ mcp-content-generator

## Step 5: Test Content Generation (1 minute)

Even without Instagram API, you can test content generation!

### Option A: Using Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "content-generator": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-content-generator", "python", "server.py"]
    }
  }
}
```

Then ask Claude:
```
Generate a caption for a new burger menu
```

### Option B: Test with Python

Create `test.py`:

```python
import subprocess
import json

# Test the content generator
result = subprocess.run(
    ['docker', 'exec', '-i', 'mcp-content-generator', 'python', '-c',
     '''
import sys
sys.path.insert(0, "/app")
from server import generate_caption
print(generate_caption("new burger menu", "instagram"))
     '''],
    capture_output=True,
    text=True
)

print(result.stdout)
```

Run it:
```bash
python test.py
```

## 🎉 You're Live!

Your MCP marketing system is now running. Next steps:

### Immediate (No API keys needed):
1. ✅ Generate captions with different brand voices
2. ✅ Test hashtag suggestions
3. ✅ Create post variations

### With Instagram API (15 min setup):
1. 📊 Pull your Instagram insights
2. 📈 Analyze your best-performing posts
3. 🕐 Find optimal posting times
4. 🏷️ Track hashtag performance

### Advanced (Coming in Phase 2):
1. 🎵 TikTok trend monitoring
2. 📅 Automated post scheduling
3. 🖼️ Media enhancement
4. 🤖 Full automation

## 🆘 Issues?

### Docker not starting?
```bash
# Check Docker is running
docker --version

# Reset everything and try again
docker-compose down -v
docker-compose up -d
```

### "Permission denied" on Windows?
Run PowerShell/CMD as Administrator.

### Can't find docker-compose?
```bash
# Try with dash
docker-compose up -d

# Or newer syntax
docker compose up -d
```

## 📚 Learn More

- [Full README](README.md) - Complete documentation
- [Brand Voice Guide](brand-voice/dracula.yaml) - Customize your brand
- [Database Schema](database/init.sql) - Data structure

## 💡 Pro Tips

1. **Start with Content Generation** - Works immediately, no API setup needed
2. **Choose Your Brand Voice** - Edit `.env` to set `BRAND_VOICE_PROFILE=dracula` (or professional, casual)
3. **Create Custom Voices** - Copy a YAML file in `brand-voice/` and customize
4. **Add Instagram Later** - The system works in layers, add features when ready

---

**Time to launch**: ~5 minutes ⏱️
**Difficulty**: Easy 🟢
**Prerequisites**: Docker installed

Happy marketing! 🎉
