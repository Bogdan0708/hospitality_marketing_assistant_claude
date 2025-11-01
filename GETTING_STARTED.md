# Getting Started - Your First 30 Minutes

Welcome! This guide will get you from zero to generating AI-powered social media content in 30 minutes.

## 🎯 What You'll Achieve

By the end of this guide, you'll be able to:
- ✅ Generate social media captions with custom brand voices
- ✅ Get hashtag suggestions based on trends
- ✅ Create complete post packages (caption + hashtags + image ideas)
- ✅ (Optional) Analyze your Instagram performance data

## 📋 Prerequisites

Before starting, make sure you have:

1. **Docker Desktop installed** ([Download](https://www.docker.com/products/docker-desktop/))
   - Windows: Docker Desktop for Windows
   - Mac: Docker Desktop for Mac
   - Linux: Docker Engine + Docker Compose

2. **Anthropic API Key** ([Get here](https://console.anthropic.com/))
   - Sign up for Anthropic account
   - Create an API key
   - You'll need credits ($5-10 should last months for testing)

3. **(Optional) Instagram Business Account**
   - Only needed if you want Instagram analytics
   - Can skip this for now and add later

## ⏱️ 30-Minute Setup Timeline

| Time | Task | Details |
|------|------|---------|
| **0-5 min** | Initial setup | Clone/download, copy .env |
| **5-10 min** | Add API keys | Edit .env file |
| **10-20 min** | Start services | Docker build + startup |
| **20-25 min** | Test content generation | Run test script |
| **25-30 min** | Connect to Claude Desktop | MCP configuration |

Let's go! 🚀

---

## Step 1: Initial Setup (5 minutes)

### 1.1 Navigate to Project Directory

Open your terminal/PowerShell:

```bash
cd C:\Users\godja\Desktop\hospitality_marketing_assistant_claude
```

### 1.2 Copy Environment File

```bash
# Windows PowerShell
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

### 1.3 Verify Docker is Running

```bash
docker --version
```

You should see something like: `Docker version 24.x.x`

If not, start Docker Desktop and wait for it to fully start (whale icon in system tray).

---

## Step 2: Add API Keys (5 minutes)

### 2.1 Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Click "API Keys" in sidebar
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)

### 2.2 Edit .env File

Open `.env` in your favorite text editor:

**Minimum required to start:**

```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx

# Optional - customize your brand
BRAND_VOICE_PROFILE=dracula
BUSINESS_NAME=Your Restaurant Name
```

**Available brand voices:**
- `dracula` - Gothic, playful, vampire-themed
- `professional` - Polished, sophisticated
- `casual` - Friendly, conversational, emoji-rich

### 2.3 (Optional) Add Instagram Credentials

If you want Instagram analytics, add these too:

```env
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_ACCESS_TOKEN=your_long_lived_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_ig_id
```

**Don't have these yet?** Skip for now. See [README.md](README.md#-getting-your-api-credentials) for setup guide.

---

## Step 3: Start Services (10 minutes)

### 3.1 Build and Start

```bash
docker-compose up -d --build
```

This will:
- Download base images (Python, PostgreSQL, Redis)
- Build your custom containers
- Start all services
- Initialize the database

**First run takes 5-10 minutes.** Subsequent starts are faster (30 seconds).

### 3.2 Check Status

```bash
docker-compose ps
```

You should see:
```
NAME                          STATUS
postgres                      Up
redis                         Up
mcp-content-generator         Up
mcp-instagram-analytics       Up
```

If any show "Exit" status:
```bash
# View logs to see what went wrong
docker-compose logs [service-name]

# Common fix: restart all services
docker-compose restart
```

### 3.3 Verify Database

```bash
docker-compose exec postgres psql -U postgres -d hospitality_marketing -c "\dt"
```

You should see a list of tables (instagram_posts, generated_content, etc.).

---

## Step 4: Test Content Generation (5 minutes)

### 4.1 Run Test Script

```bash
python scripts/test-content-generator.py
```

This will test:
- ✅ Caption generation
- ✅ Hashtag suggestions
- ✅ Full post creation
- ✅ Content variations

**Expected output:** You'll see AI-generated captions, hashtags, and post ideas.

### 4.2 Test Manually (Alternative)

Try generating a caption directly:

```bash
docker exec -it mcp-content-generator python -c "
from server import generate_caption
result = generate_caption('new burger menu', 'instagram')
print(result)
"
```

---

## Step 5: Connect to Claude Desktop (5 minutes)

### 5.1 Find Config File

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 5.2 Add MCP Servers

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "content-generator": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-content-generator", "python", "server.py"]
    },
    "instagram-analytics": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-instagram-analytics", "python", "server.py"]
    }
  }
}
```

### 5.3 Restart Claude Desktop

Close completely and reopen.

### 5.4 Test in Claude

Try asking:

```
Generate a caption for our new Transylvanian burger using the Dracula brand voice
```

Claude should use the `content-generator` MCP server and return a Gothic-themed caption!

---

## 🎉 You're Done!

### What You Can Do Now

#### Content Generation (Works immediately)

```
"Generate a caption for [topic]"
"Suggest hashtags for [topic]"
"Create a complete Instagram post about [topic]"
"Make 3 variations of this caption for A/B testing"
```

#### Instagram Analytics (Requires Instagram API setup)

```
"What were my top 5 posts this week?"
"When should I post for maximum engagement?"
"How are my hashtags performing?"
"Show me my audience demographics"
```

### Next Steps

1. **Customize Your Brand Voice**
   - Edit `brand-voice/dracula.yaml` (or create your own)
   - Restart content generator: `docker-compose restart mcp-content-generator`

2. **Add Instagram Integration**
   - Follow [Instagram API Setup Guide](README.md#instagram--facebook-meta-graph-api)
   - Add credentials to `.env`
   - Restart services: `docker-compose restart`

3. **Explore Database**
   ```bash
   docker-compose exec postgres psql -U postgres -d hospitality_marketing
   \dt  # List tables
   SELECT * FROM generated_content LIMIT 5;
   ```

4. **Phase 2: Add TikTok Scraper**
   - Coming soon in next update
   - Will enable trend-based content generation

---

## 🆘 Troubleshooting

### "Docker daemon not running"
- Start Docker Desktop
- Wait for whale icon to show it's ready

### "Error: pull access denied"
- Restart Docker Desktop
- Try: `docker-compose pull`

### "Container keeps restarting"
```bash
# View logs
docker-compose logs [service-name]

# Common issues:
# - Missing API key in .env
# - Syntax error in .env
# - Port conflict (another service using 5432 or 6379)
```

### "MCP server not found in Claude"
1. Check containers are running: `docker-compose ps`
2. Verify config file syntax (valid JSON)
3. Restart Claude Desktop completely
4. Check Docker Desktop is running

### "Content generation fails"
- Verify `ANTHROPIC_API_KEY` in `.env`
- Check API key has credits: https://console.anthropic.com/
- View logs: `docker-compose logs mcp-content-generator`

---

## 📚 Further Reading

- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - Alternative quick start
- [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md) - Detailed MCP setup
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Understanding the codebase

---

## 💬 Example Conversation

Once everything is set up, here's a real conversation you can have:

```
You: Generate a caption for our new menu item - a spicy chicken burger with jalapeños

Claude: [Uses content-generator]
Here's a caption with your Dracula brand voice:

"Dare to face the heat? 🔥🧛‍♂️ Our new Inferno Chicken Burger rises from the flames with fire-roasted jalapeños, ghost pepper aioli, and a wickedly crispy chicken that'll haunt your taste buds (in the best way). Not for the faint of heart. Come get burned. 🌶️

#SpicyFood #ChickenBurger #LondonEats #Foodie #HotChicken #SpiceLovers #StreetFood #FoodPorn #Jalapeño #LondonFoodie"

---

You: Make that more casual and friendly

Claude: [Regenerates with different tone]
"OMG this new spicy chicken burger is 🔥🔥🔥 Jalapeños, crispy chicken, and our special sauce... it's INSANE! Who's brave enough to try it? Tag a friend who loves spicy food! 🌶️😍"

---

You: What were my top 3 Instagram posts last week?

Claude: [Uses instagram-analytics if configured]
Based on your Instagram data, here are your top 3 posts:

1. Burger photo (Oct 14) - 8.5% engagement, 2,450 reach
2. Weekend special (Oct 12) - 7.2% engagement, 1,890 reach
3. Kitchen behind-scenes (Oct 15) - 6.8% engagement, 1,650 reach

The burger photo performed best - consider posting more product close-ups!
```

---

**Ready to revolutionize your social media marketing?** Start generating content! 🚀
