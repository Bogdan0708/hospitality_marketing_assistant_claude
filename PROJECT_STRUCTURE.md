# Project Structure

```
hospitality_marketing_assistant_claude/
│
├── docker-compose.yml              # Main orchestration file for all services
├── .env.example                    # Template for environment variables
├── .env                           # Your actual credentials (git-ignored)
├── .gitignore                     # Git ignore rules
│
├── README.md                      # Main documentation
├── QUICKSTART.md                  # 5-minute setup guide
├── CLAUDE_DESKTOP_SETUP.md       # Claude Desktop integration guide
├── PROJECT_STRUCTURE.md          # This file
│
├── database/
│   └── init.sql                   # PostgreSQL schema & initial setup
│
├── brand-voice/                   # Brand voice configuration files
│   ├── dracula.yaml              # Gothic/vampire-themed voice
│   ├── professional.yaml         # Polished, sophisticated voice
│   └── casual.yaml               # Friendly, conversational voice
│
├── scripts/                       # Utility scripts
│   ├── setup.ps1                 # Windows setup automation
│   └── test-content-generator.py # Test content generation
│
└── services/                      # MCP server implementations
    │
    ├── mcp-instagram-analytics/   # Instagram Business API integration
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── server.py              # MCP server with tools:
    │                              #   - get_account_insights()
    │                              #   - analyze_post_performance()
    │                              #   - get_optimal_posting_times()
    │                              #   - track_hashtag_performance()
    │                              #   - get_audience_demographics()
    │
    ├── mcp-content-generator/     # AI-powered content creation
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── server.py              # MCP server with tools:
    │                              #   - generate_caption()
    │                              #   - suggest_hashtags()
    │                              #   - generate_full_post()
    │                              #   - create_content_variations()
    │                              #   - generate_trend_based_content()
    │
    ├── mcp-facebook-insights/     # [Placeholder] Facebook Page analytics
    │   └── (to be implemented)
    │
    ├── mcp-tiktok-scraper/        # [Phase 2] TikTok trend detection
    │   └── (to be implemented)
    │
    ├── mcp-sentiment-analyzer/    # [Phase 2] Sentiment analysis
    │   └── (to be implemented)
    │
    ├── mcp-trend-detector/        # [Phase 2] Cross-platform trend aggregation
    │   └── (to be implemented)
    │
    ├── mcp-post-scheduler/        # [Phase 3] Multi-platform scheduling
    │   └── (to be implemented)
    │
    └── mcp-media-processor/       # [Phase 3] Image/video enhancement
        └── (to be implemented)
```

## Service Status

### ✅ Implemented (Phase 1)

| Service | Status | Description |
|---------|--------|-------------|
| **PostgreSQL** | ✅ Ready | Database with complete schema for all platforms |
| **Redis** | ✅ Ready | Caching layer for API responses |
| **mcp-instagram-analytics** | ✅ Ready | Full Instagram Business API integration |
| **mcp-content-generator** | ✅ Ready | AI content generation with brand voices |

### 🚧 Coming Soon (Phase 2)

| Service | Status | Description |
|---------|--------|-------------|
| **mcp-facebook-insights** | 📋 Planned | Facebook Page analytics |
| **mcp-tiktok-scraper** | 📋 Planned | TikTok trend scraping with Playwright |
| **mcp-sentiment-analyzer** | 📋 Planned | Sentiment analysis using transformers |
| **mcp-trend-detector** | 📋 Planned | Cross-platform trend aggregation |

### 🔮 Future (Phase 3)

| Service | Status | Description |
|---------|--------|-------------|
| **mcp-post-scheduler** | 💡 Roadmap | Automated post scheduling & publishing |
| **mcp-media-processor** | 💡 Roadmap | Image enhancement, watermarks, resizing |

## Key Files Explained

### Configuration Files

- **`docker-compose.yml`**: Defines all services, networks, volumes. This is the heart of the system.
- **`.env`**: Environment variables for API keys and configuration. NEVER commit this file.
- **`.env.example`**: Template showing what variables are needed. Safe to commit.

### Database Files

- **`database/init.sql`**: Complete PostgreSQL schema with 15+ tables for:
  - Social media posts and analytics
  - Trend detection
  - Content generation
  - Sentiment analysis
  - Media assets
  - Campaign tracking

### Brand Voice Files

- **`brand-voice/*.yaml`**: YAML configuration files defining:
  - Tone and style
  - Keywords to use
  - Emoji usage
  - Hashtag strategy
  - Sample captions
  - Platform-specific guidelines

### MCP Servers

Each service in `services/` is a standalone MCP server that:
- Exposes tools via Model Context Protocol
- Can be called by Claude or other AI systems
- Operates independently but shares database/cache
- Is containerized for easy deployment

## Data Flow

```
┌─────────────────┐
│  Claude/User    │
│   (Questions)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     MCP Servers (Docker)            │
│  ┌──────────────────────────────┐   │
│  │ Instagram Analytics          │   │
│  │ Content Generator            │   │
│  │ TikTok Scraper (Phase 2)    │   │
│  └──────────────────────────────┘   │
└─────────┬───────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│   Data Layer                         │
│  ┌────────────┐    ┌──────────────┐  │
│  │ PostgreSQL │    │    Redis     │  │
│  │ (Storage)  │    │   (Cache)    │  │
│  └────────────┘    └──────────────┘  │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│   External APIs                      │
│  • Meta Graph API (Instagram/FB)    │
│  • TikTok (scraping)                │
│  • Anthropic Claude                 │
└──────────────────────────────────────┘
```

## Adding New Features

### To add a new MCP server:

1. **Create service directory**: `services/mcp-your-server/`
2. **Add Dockerfile**: Define container image
3. **Implement server**: Using FastMCP (Python) or @modelcontextprotocol/sdk (TypeScript)
4. **Add to docker-compose.yml**: Define service, environment variables, dependencies
5. **Update documentation**: Add to README.md and this file
6. **Test**: Use test scripts or Claude Desktop

### To add a new brand voice:

1. **Copy template**: `cp brand-voice/professional.yaml brand-voice/your-voice.yaml`
2. **Customize**: Edit YAML with your tone, keywords, examples
3. **Set in .env**: `BRAND_VOICE_PROFILE=your-voice`
4. **Test**: Generate content and verify it matches your voice

## Environment Variables Reference

See `.env.example` for complete list. Key variables:

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `ANTHROPIC_API_KEY` | ✅ Yes | Content generation |
| `META_ACCESS_TOKEN` | For Instagram | Instagram/Facebook data |
| `META_APP_ID` | For Instagram | Instagram/Facebook data |
| `META_APP_SECRET` | For Instagram | Instagram/Facebook data |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | For Instagram | Your IG account |
| `BRAND_VOICE_PROFILE` | Optional | Which voice to use (default: professional) |

## Ports Used

| Port | Service | Purpose |
|------|---------|---------|
| 5432 | PostgreSQL | Database access |
| 6379 | Redis | Cache access |

MCP servers don't expose ports - they're accessed via stdio through Docker exec.

## Storage Volumes

| Volume | Purpose | Persistence |
|--------|---------|-------------|
| `postgres-data` | Database storage | Persistent |
| `redis-data` | Cache storage | Persistent |
| `model-cache` | ML model cache | Persistent |
| `media-storage` | Uploaded media | Persistent |

All volumes persist across container restarts unless you run `docker-compose down -v`.

---

**Questions about the structure?** Check the main [README.md](README.md) or open an issue!
