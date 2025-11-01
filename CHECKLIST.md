# Pre-Launch Checklist

Use this checklist to ensure everything is properly configured before launching your MCP marketing system.

## 📋 Phase 1: Content Generation (Available Now)

### Prerequisites ✅

- [ ] Docker Desktop installed and running
- [ ] Anthropic API account created
- [ ] API key generated (starts with `sk-ant-`)
- [ ] API key has credits ($5-10 recommended for testing)

### Configuration ✅

- [ ] `.env` file created from `.env.example`
- [ ] `ANTHROPIC_API_KEY` added to `.env`
- [ ] `BRAND_VOICE_PROFILE` selected (dracula/professional/casual)
- [ ] Business name configured (optional)

### Docker Services ✅

- [ ] Run `docker-compose up -d --build`
- [ ] All containers show "Up" status in `docker-compose ps`
- [ ] PostgreSQL accessible: `docker-compose exec postgres psql -U postgres -c "SELECT 1;"`
- [ ] Redis accessible: `docker-compose exec redis redis-cli ping` returns "PONG"
- [ ] No error logs: `docker-compose logs | grep -i error`

### Content Generator Testing ✅

- [ ] Test script runs successfully: `python scripts/test-content-generator.py`
- [ ] Caption generation works
- [ ] Hashtag suggestions work
- [ ] Full post generation works
- [ ] Content variations work

### Claude Desktop Integration ✅

- [ ] Claude Desktop installed
- [ ] `claude_desktop_config.json` file located
- [ ] MCP servers added to config
- [ ] Claude Desktop restarted
- [ ] Can see MCP servers in Claude interface
- [ ] Test query works: "Generate a caption for a new menu item"

## 📊 Phase 2: Instagram Analytics (Optional)

### Meta Developer Setup ✅

- [ ] Facebook Developer account created
- [ ] App created in Meta Developer Console
- [ ] Instagram Basic Display product added
- [ ] Instagram Graph API product added
- [ ] Permissions configured: `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`

### Access Token ✅

- [ ] Short-lived token generated in Graph API Explorer
- [ ] Converted to long-lived token (60 days)
- [ ] Token tested and working
- [ ] Token added to `.env` as `META_ACCESS_TOKEN`

### Account IDs ✅

- [ ] Instagram Business Account connected to Facebook Page
- [ ] Instagram Business Account ID obtained
- [ ] Facebook Page ID obtained
- [ ] Both IDs added to `.env`

### Instagram Analytics Testing ✅

- [ ] Services restarted: `docker-compose restart`
- [ ] Test account insights: Query Claude "What are my Instagram insights for last 7 days?"
- [ ] Test post analysis: "What were my top posts this week?"
- [ ] Test hashtag tracking: "How is #burger performing?"
- [ ] Data appears in database: `SELECT COUNT(*) FROM instagram_posts;`

## 🎨 Customization

### Brand Voice ✅

- [ ] Reviewed all brand voice profiles in `brand-voice/`
- [ ] Selected appropriate voice OR created custom profile
- [ ] Tested content generation with selected voice
- [ ] Voice matches brand personality

### Database ✅

- [ ] Database schema reviewed (`database/init.sql`)
- [ ] All tables created successfully: `docker-compose exec postgres psql -U postgres -d hospitality_marketing -c "\dt"`
- [ ] No errors in PostgreSQL logs

## 🔒 Security

### Environment Variables ✅

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys committed to git
- [ ] `.env.example` has placeholder values only
- [ ] Sensitive data not in any committed files

### Access Control ✅

- [ ] Database credentials are strong (change from defaults for production)
- [ ] Redis doesn't expose to internet (Docker network only)
- [ ] API keys have minimal required permissions
- [ ] Long-lived tokens set to expire (60 days)

## 📈 Monitoring

### Logs ✅

- [ ] Know how to view logs: `docker-compose logs -f [service]`
- [ ] No critical errors in logs
- [ ] Can access container shells: `docker exec -it [container] bash`

### Database Access ✅

- [ ] Can connect to PostgreSQL: `docker-compose exec postgres psql -U postgres -d hospitality_marketing`
- [ ] Understand schema structure
- [ ] Know how to query generated content

### Performance ✅

- [ ] Redis caching is working (check TTL on cached keys)
- [ ] API rate limits understood (Instagram: 200 calls/hour)
- [ ] Database queries are reasonably fast

## 🚀 Production Readiness (If Deploying)

### Infrastructure ✅

- [ ] Hosting platform selected (AWS, DigitalOcean, Railway, etc.)
- [ ] Docker Compose configured for production
- [ ] Persistent volumes configured
- [ ] Backup strategy for PostgreSQL data
- [ ] Environment variables secured (not in docker-compose.yml)

### Scaling ✅

- [ ] Resource limits set in docker-compose.yml
- [ ] Health checks configured
- [ ] Restart policies appropriate
- [ ] Monitoring solution chosen (Prometheus/Grafana optional)

### Domains & SSL ✅

- [ ] Domain name configured (if exposing services)
- [ ] SSL certificates configured
- [ ] Reverse proxy setup (nginx/Traefik)

## 📝 Documentation

### Team Onboarding ✅

- [ ] README.md reviewed
- [ ] GETTING_STARTED.md is clear
- [ ] Team knows how to access documentation
- [ ] Claude Desktop setup guide shared

### Maintenance ✅

- [ ] Know how to update services: `docker-compose pull && docker-compose up -d`
- [ ] Know how to backup database: `docker-compose exec postgres pg_dump ...`
- [ ] Know how to restore database
- [ ] Know how to rotate API keys

## 🎯 Usage Goals

### Content Creation ✅

- [ ] Can generate captions in < 30 seconds
- [ ] Can create full posts with hashtags
- [ ] Can create A/B test variations
- [ ] Content matches brand voice

### Analytics (If Instagram configured) ✅

- [ ] Can pull weekly insights
- [ ] Can analyze top-performing posts
- [ ] Can track hashtag performance
- [ ] Can identify optimal posting times

## ✨ Nice to Have

### Advanced Features ✅

- [ ] Custom brand voice created
- [ ] Multiple brand voices for different campaigns
- [ ] Automated testing scripts
- [ ] CI/CD pipeline (for updates)

### Phase 2 Planning ✅

- [ ] TikTok trend scraping scope defined
- [ ] Sentiment analysis use cases identified
- [ ] Post scheduling requirements documented

---

## 🎉 Launch Checklist

Ready to go live? Final verification:

- [ ] ✅ All Phase 1 items checked
- [ ] ✅ Instagram analytics working (if needed)
- [ ] ✅ Brand voice customized
- [ ] ✅ Security reviewed
- [ ] ✅ Team trained
- [ ] ✅ Backup strategy in place
- [ ] ✅ Monitoring configured

**Status:** 🟢 Ready | 🟡 Almost | 🔴 Not Ready

---

## 📊 Success Metrics

Track these after launch:

| Metric | Target | Actual |
|--------|--------|--------|
| Content generation time | < 1 min | ___ |
| Instagram data refresh | Daily | ___ |
| System uptime | > 99% | ___ |
| Content pieces per week | 10+ | ___ |
| Brand voice consistency | High | ___ |

---

## 🆘 Emergency Contacts

- **Docker Issues:** Check [Docker Documentation](https://docs.docker.com/)
- **Meta API Issues:** [Meta Developer Support](https://developers.facebook.com/support/)
- **Anthropic API Issues:** [Anthropic Documentation](https://docs.anthropic.com/)
- **MCP Protocol:** [MCP Specification](https://modelcontextprotocol.io/)

---

**Last Updated:** [Date of launch]
**System Version:** Phase 1 - Content Generation
**Next Review:** [30 days after launch]
