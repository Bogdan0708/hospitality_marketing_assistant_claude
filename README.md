# Hospitality Marketing Assistant (MCP Architecture)

A modular, AI-powered social media marketing system built with **Model Context Protocol (MCP)** servers for the hospitality industry. Talk to your marketing stack using natural language through Claude.

## 🎯 What Makes This Special

Instead of a traditional API architecture, this uses **MCP servers** - meaning you can literally have conversations with your marketing system:

```
You: "What's trending on TikTok for street food this week?"
System: [Searches TikTok trends, analyzes data, returns insights]

You: "Create a post about our new burger and schedule it for 6pm tomorrow"
System: [Generates caption with brand voice, suggests hashtags, schedules post]
```

## 🏗️ Architecture

### MCP Servers (Microservices)

Each server is a specialized AI agent that exposes tools via the Model Context Protocol:

#### **Data Collection Layer**
- `mcp-instagram-analytics` - Instagram Business Account insights & post analytics
- `mcp-facebook-insights` - Facebook Page analytics & engagement data
- `mcp-tiktok-scraper` - TikTok trend detection & viral content analysis

#### **Processing Layer**
- `mcp-sentiment-analyzer` - Sentiment analysis using transformers
- `mcp-trend-detector` - Cross-platform trend aggregation

#### **Content Automation Layer**
- `mcp-content-generator` - AI-powered caption & post generation (with brand voice)
- `mcp-post-scheduler` - Multi-platform post scheduling
- `mcp-media-processor` - Image/video enhancement

#### **Data Storage**
- `postgres` - PostgreSQL 16 for all analytics data
- `redis` - Caching layer for API responses

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Meta Developer Account (for Instagram/Facebook API)
- Anthropic API key (for content generation)
- Instagram Business Account
- Facebook Page

### 1. Clone and Setup

```bash
cd C:\Users\godja\Desktop\hospitality_marketing_assistant_claude
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your credentials:

```env
# Meta API (Required)
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_ig_business_id
FACEBOOK_PAGE_ID=your_page_id

# Anthropic API (Required for content generation)
ANTHROPIC_API_KEY=your_anthropic_key

# Brand Configuration
BRAND_VOICE_PROFILE=dracula  # or professional, casual
BUSINESS_NAME=Your Restaurant Name
```

### 3. Start the System

```bash
docker-compose up -d
```

This will start:
- ✅ PostgreSQL database (port 5432)
- ✅ Redis cache (port 6379)
- ✅ All MCP servers

### 4. Verify Everything is Running

```bash
docker-compose ps
```

All services should show `Up` status.

## 📚 Getting Your API Credentials

### Instagram & Facebook (Meta Graph API)

1. **Create Meta App**
   - Go to https://developers.facebook.com/apps/
   - Create new app → Business type
   - Add Instagram Basic Display & Instagram Graph API

2. **Get Access Token**
   - Use Graph API Explorer: https://developers.facebook.com/tools/explorer/
   - Select your app
   - Add permissions: `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`, `pages_show_list`
   - Generate User Access Token
   - **Convert to Long-Lived Token** (60 days):
     ```bash
     curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
     ```

3. **Get Instagram Business Account ID**
   - In Graph API Explorer, query: `me?fields=accounts{instagram_business_account}`
   - Copy the `instagram_business_account.id`

4. **Get Facebook Page ID**
   - Go to your Facebook Page
   - About section → Page ID

### Anthropic API

1. Go to https://console.anthropic.com/
2. Create account / Sign in
3. API Keys → Create Key
4. Copy the key (starts with `sk-ant-`)

## 🔧 Using the MCP Servers

### Option 1: Through Claude Desktop (Recommended)

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "instagram-analytics": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-instagram-analytics", "python", "server.py"]
    },
    "content-generator": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-content-generator", "python", "server.py"]
    }
  }
}
```

Then in Claude Desktop, you can ask:
- "What were my top 5 Instagram posts this week?"
- "Analyze my hashtag performance for #burger and #streetfood"
- "Generate a caption for our new menu launch"

### Option 2: Direct API Calls

Each MCP server exposes a standard MCP interface. You can interact with them programmatically.

## 🛠️ Available Tools

### Instagram Analytics Server

```python
# Get account insights
get_account_insights(date_range="last_7_days")

# Analyze top posts
analyze_post_performance(limit=10, sort_by="engagement_rate")

# Find best posting times
get_optimal_posting_times()

# Track hashtag performance
track_hashtag_performance(hashtags=["#burger", "#foodie"])

# Get audience demographics
get_audience_demographics()
```

### Content Generator Server

```python
# Generate caption
generate_caption(
    topic="new burger menu",
    platform="instagram",
    include_hashtags=True
)

# Suggest hashtags
suggest_hashtags(
    topic="street food",
    count=10,
    include_trending=True
)

# Generate full post
generate_full_post(
    topic="weekend special",
    platform="instagram",
    post_goal="engagement"
)

# Create A/B test variations
create_content_variations(
    base_caption="Your original caption",
    num_variations=3
)

# Generate trend-based content
generate_trend_based_content(limit=5)
```

## 🎨 Brand Voice Profiles

The system includes 3 pre-configured brand voices (in `brand-voice/` directory):

### 1. **Dracula** (`dracula.yaml`)
Playfully dark, mysterious, Gothic-themed with vampire humor.

Example:
> "Our Transylvanian Burger has been haunting dreams for centuries 🦇 Topped with caramelized garlic (vampire-approved), aged cheddar, and our secret 'midnight sauce' - it's wickedly delicious. Come for a bite... if you dare 🧛‍♂️"

### 2. **Professional** (`professional.yaml`)
Polished, sophisticated, quality-focused.

Example:
> "Our signature burger starts with premium, locally sourced beef, expertly seasoned and grilled to perfection. Quality you can taste in every bite ✨"

### 3. **Casual** (`casual.yaml`)
Friendly, energetic, emoji-rich, conversational.

Example:
> "OMG you guys! 😍 This burger is literally INSANE 🔥 Tag your burger buddy! 👇"

**To switch brand voices**, set in `.env`:
```env
BRAND_VOICE_PROFILE=dracula  # or professional, casual
```

**To create your own**, copy one of the YAML files and customize!

## 📊 Database Schema

The PostgreSQL database includes tables for:

- `social_accounts` - Connected social media accounts
- `instagram_posts` - Post data with engagement metrics
- `instagram_insights` - Daily account insights
- `facebook_posts` - Facebook post analytics
- `tiktok_trends` - Trending hashtags and sounds
- `sentiment_analysis` - Sentiment scores for content
- `detected_trends` - Cross-platform trend aggregation
- `generated_content` - AI-generated captions and posts
- `scheduled_posts` - Post scheduling queue
- `media_assets` - Media file management

## 🔍 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mcp-instagram-analytics
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d hospitality_marketing

# View recent Instagram posts
SELECT post_id, caption, engagement_rate FROM instagram_posts ORDER BY timestamp DESC LIMIT 5;
```

### Redis Cache

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# View cached keys
KEYS *

# Get cached value
GET instagram_insights:your_account_id:last_7_days
```

## 📈 Roadmap

### Phase 1: Foundation ✅ (Current)
- [x] Docker Compose setup
- [x] Instagram Analytics MCP server
- [x] Content Generator with brand voices
- [x] PostgreSQL schema
- [x] Basic documentation

### Phase 2: TikTok Intelligence (Next 2-3 weeks)
- [ ] TikTok scraper (TypeScript + Playwright)
- [ ] Trend detection aggregation
- [ ] Sentiment analysis integration

### Phase 3: Automation (Following 2-3 weeks)
- [ ] Post scheduler with Meta API publishing
- [ ] Media processor (image enhancement, watermarks)
- [ ] Automated trend reports

### Phase 4: Advanced Features
- [ ] Competitor analysis
- [ ] A/B testing framework
- [ ] Grafana dashboards
- [ ] Webhook integrations

## 🐛 Troubleshooting

### "Meta API error: Invalid access token"
- Your access token expired (short-lived tokens last 1 hour)
- Convert to long-lived token (60 days) using the curl command above
- Or regenerate in Graph API Explorer

### "Database connection refused"
- Wait 30 seconds for PostgreSQL to fully initialize
- Check: `docker-compose logs postgres`

### "MCP server not responding"
- Check server logs: `docker-compose logs [service-name]`
- Verify environment variables are set correctly
- Restart: `docker-compose restart [service-name]`

### "No trends detected"
- TikTok scraper needs 3-5 days of data collection
- Instagram needs at least 10 posts for meaningful analysis

## 🤝 Contributing

This is a template system - customize it for your needs!

Areas to extend:
- Add more social platforms (Twitter/X, LinkedIn)
- Create custom brand voice profiles
- Build a web dashboard
- Add email/SMS marketing integration

## 📝 License

MIT License - use freely for your hospitality business!

## 🙏 Credits

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Anthropic Claude](https://anthropic.com) - AI content generation
- [Meta Graph API](https://developers.facebook.com/docs/graph-api/) - Instagram/Facebook data
- [PostgreSQL](https://www.postgresql.org/) - Data storage
- [Redis](https://redis.io/) - Caching

---

**Questions?** Open an issue or check the docs in each service's directory.

**Ready to launch your AI-powered marketing?** Start with Phase 1 and gradually enable more features! 🚀
