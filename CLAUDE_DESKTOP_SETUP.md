# Claude Desktop Integration Guide

Connect your MCP servers to Claude Desktop for natural language control of your marketing system.

## Prerequisites

- ✅ Docker containers running (`docker-compose ps` shows all services "Up")
- ✅ Claude Desktop installed ([Download here](https://claude.ai/download))

## Setup (5 minutes)

### Step 1: Locate Claude Desktop Config

The config file location depends on your OS:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Edit Configuration

Open `claude_desktop_config.json` in a text editor and add:

```json
{
  "mcpServers": {
    "instagram-analytics": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-instagram-analytics",
        "python",
        "server.py"
      ],
      "env": {}
    },
    "content-generator": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-content-generator",
        "python",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

**If you already have other MCP servers configured**, just add these entries to the existing `mcpServers` object.

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop completely.

### Step 4: Verify Connection

In Claude Desktop, you should see the MCP servers listed in the settings/tools area (usually indicated by a small icon or menu).

## 🎯 What You Can Now Do

Once connected, you can have natural conversations with your marketing system:

### Content Generation Examples

```
You: "Generate a caption for our new Transylvanian burger"
Claude: [Uses content-generator MCP] Here's a caption with your Dracula brand voice...

You: "Create 3 variations of this caption for A/B testing"
Claude: [Generates variations] Here are 3 different versions...

You: "Suggest hashtags for a post about street food"
Claude: [Returns 10 relevant hashtags with analysis]

You: "Generate a complete Instagram post about our weekend special"
Claude: [Returns caption, hashtags, image suggestions, optimal posting time]
```

### Instagram Analytics Examples

(Requires Instagram API credentials in `.env`)

```
You: "What were my top 5 Instagram posts this week?"
Claude: [Uses instagram-analytics MCP] Here are your best performers...

You: "When should I post to get maximum engagement?"
Claude: [Analyzes historical data] Based on your audience, the best times are...

You: "How are my #burger and #streetfood hashtags performing?"
Claude: [Returns performance metrics for each hashtag]

You: "Show me my Instagram insights for the last 30 days"
Claude: [Returns impressions, reach, engagement, follower growth, etc.]

You: "What are the demographics of my Instagram audience?"
Claude: [Returns age, gender, location breakdown]
```

### Combined Workflows

```
You: "Look at my top posts from last week, identify patterns, and generate 3 new posts that follow those patterns"
Claude: [Analyzes your content, identifies what works, generates new content]

You: "Create a post based on current TikTok trends for street food"
Claude: [Once TikTok scraper is added] Here's a trend-based post idea...
```

## 🔧 Troubleshooting

### "MCP server not found" error

**Cause:** Docker containers aren't running

**Fix:**
```bash
cd C:\Users\godja\Desktop\hospitality_marketing_assistant_claude
docker-compose up -d
docker-compose ps  # Verify all services are "Up"
```

### "Permission denied" when accessing Docker

**Windows Fix:**
1. Ensure Docker Desktop is running
2. Run Claude Desktop as Administrator
3. Or add your user to `docker-users` group

**Mac/Linux Fix:**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### Claude can't see the tools

**Fix:**
1. Verify config file syntax (must be valid JSON)
2. Restart Claude Desktop completely
3. Check Docker containers are running: `docker-compose ps`

### "Tool execution failed"

**Fix:**
1. Check container logs: `docker-compose logs mcp-content-generator`
2. Verify environment variables in `.env`
3. Ensure ANTHROPIC_API_KEY is valid (for content generation)

## 📝 Configuration Tips

### Add More Servers Later

As you enable more MCP servers (TikTok scraper, trend detector, etc.), add them to the config:

```json
{
  "mcpServers": {
    "instagram-analytics": { ... },
    "content-generator": { ... },
    "tiktok-scraper": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-tiktok-scraper", "node", "dist/index.js"],
      "env": {}
    }
  }
}
```

### Testing Individual Servers

You can test if a server is working without Claude Desktop:

```bash
# Test content generator
docker exec -it mcp-content-generator python -c "
from server import generate_caption
print(generate_caption('test topic'))
"
```

## 🎉 You're Ready!

Your Claude Desktop is now connected to your marketing automation system. Start by asking Claude to:

1. Generate some test captions with different brand voices
2. Analyze your Instagram performance (if API connected)
3. Create hashtag suggestions for your content

The beauty of MCP is that Claude understands the context and can chain operations together intelligently!

---

**Next:** Check out [QUICKSTART.md](QUICKSTART.md) for more examples and workflows.
