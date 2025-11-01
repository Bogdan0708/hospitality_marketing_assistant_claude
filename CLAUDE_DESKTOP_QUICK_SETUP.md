# Claude Desktop Setup - Quick Guide for MitchfromTransylvania

## Step 1: Locate Your Claude Desktop Config File

The config file is located at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**To open it:**
1. Press `Windows + R`
2. Type: `%APPDATA%\Claude`
3. Press Enter
4. Look for `claude_desktop_config.json`
5. Open it with Notepad or VS Code

## Step 2: Add MCP Server Configuration

**If the file is empty or doesn't exist**, create it with this content:

```json
{
  "mcpServers": {
    "mitch-content-generator": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-content-generator",
        "python",
        "-c",
        "import sys; sys.path.insert(0, '/app'); exec(sys.stdin.read())"
      ]
    }
  }
}
```

**If the file already has content**, add the `mitch-content-generator` entry inside the existing `mcpServers` object.

## Step 3: Restart Claude Desktop

1. Close Claude Desktop completely (check system tray)
2. Reopen Claude Desktop

## Step 4: Test It!

In Claude Desktop, you can now say:

### Generate Content:
```
"Generate an Instagram caption for our new Transylvanian burger special"
```

```
"Create 5 different captions for our weekend brunch menu"
```

```
"Generate a spooky Halloween post for MitchfromTransylvania"
```

### More Examples:
```
"Create a caption about our midnight dining experience with Gothic vibes"
```

```
"Generate hashtags for a post about garlic fries"
```

```
"Write a full Instagram post about our new vampire-themed cocktail menu"
```

## What You Can Ask For:

✅ **Generate captions** - "Create a caption for [topic]"
✅ **Suggest hashtags** - "Give me hashtags for [topic]"
✅ **Full posts** - "Create a complete Instagram post about [topic]"
✅ **Multiple variations** - "Generate 3 different versions of a caption about [topic]"
✅ **Specific tone** - "Make it more playful/mysterious/urgent"

## Your Brand Voice is Already Set!

All content will automatically use your **Dracula brand voice**:
- Playfully dark & mysterious
- Gothic charm with vampire humor
- Keywords: "wickedly delicious", "bite into", "hauntingly flavorful"
- Perfect for MitchfromTransylvania! 🧛‍♂️

## Troubleshooting

### "MCP server not found"
- Make sure Docker containers are running: `docker-compose ps`
- Restart containers: `cd "C:\Users\godja\Desktop\hospitality_marketing_assistant_claude" && docker-compose restart`

### "Server connection failed"
- Check containers are Up: `docker-compose ps`
- View logs: `docker-compose logs mcp-content-generator`

### "Tool not responding"
- Restart Claude Desktop
- Check Docker Desktop is running

## Direct Testing (Without Claude Desktop)

You can also generate content directly via command line:

```powershell
cd C:\Users\godja\Desktop\hospitality_marketing_assistant_claude

docker exec mcp-content-generator python -c "
from anthropic import Anthropic
import yaml

with open('/app/brand-voice/dracula.yaml', 'r') as f:
    voice = yaml.safe_load(f)

client = Anthropic()
message = client.messages.create(
    model='claude-3-haiku-20240307',
    max_tokens=300,
    messages=[{'role': 'user', 'content': 'Create an Instagram caption for [YOUR TOPIC]. Gothic tone. 5 hashtags.'}]
)
print(message.content[0].text)
"
```

## Next Steps

Once Claude Desktop is configured:
1. Try generating 5-10 different posts
2. Save your favorites
3. Build a content calendar
4. Experiment with different topics and tones!

---

**Need help?** Check the full documentation in [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)
