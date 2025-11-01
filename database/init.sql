-- ============================================
-- HOSPITALITY MARKETING ASSISTANT DATABASE
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- SOCIAL MEDIA ACCOUNTS
-- ============================================

CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL, -- instagram, facebook, tiktok, twitter
    account_id VARCHAR(255) NOT NULL,
    account_name VARCHAR(255),
    access_token TEXT,
    token_expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(platform, account_id)
);

-- ============================================
-- INSTAGRAM ANALYTICS
-- ============================================

CREATE TABLE instagram_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id VARCHAR(255) UNIQUE NOT NULL,
    account_id UUID REFERENCES social_accounts(id),
    caption TEXT,
    media_type VARCHAR(50), -- IMAGE, VIDEO, CAROUSEL
    media_url TEXT,
    permalink TEXT,
    timestamp TIMESTAMP,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2),
    saved_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    hashtags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE instagram_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id),
    date DATE NOT NULL,
    followers_count INTEGER,
    impressions INTEGER,
    reach INTEGER,
    profile_views INTEGER,
    website_clicks INTEGER,
    email_contacts INTEGER,
    phone_calls INTEGER,
    get_directions_clicks INTEGER,
    audience_demographics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(account_id, date)
);

CREATE TABLE instagram_stories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id VARCHAR(255) UNIQUE NOT NULL,
    account_id UUID REFERENCES social_accounts(id),
    media_type VARCHAR(50),
    media_url TEXT,
    timestamp TIMESTAMP,
    impressions INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    exits INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    taps_forward INTEGER DEFAULT 0,
    taps_back INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- FACEBOOK ANALYTICS
-- ============================================

CREATE TABLE facebook_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id VARCHAR(255) UNIQUE NOT NULL,
    account_id UUID REFERENCES social_accounts(id),
    message TEXT,
    post_type VARCHAR(50), -- photo, video, link, status
    created_time TIMESTAMP,
    reactions_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2),
    permalink_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE facebook_page_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id),
    date DATE NOT NULL,
    page_views INTEGER,
    page_likes INTEGER,
    page_engaged_users INTEGER,
    page_impressions INTEGER,
    page_reach INTEGER,
    post_engagements INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(account_id, date)
);

-- ============================================
-- TIKTOK TRENDS & DATA
-- ============================================

CREATE TABLE tiktok_trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hashtag VARCHAR(255),
    sound_id VARCHAR(255),
    sound_name VARCHAR(500),
    description TEXT,
    category VARCHAR(100), -- food, entertainment, lifestyle, etc
    view_count BIGINT,
    post_count INTEGER,
    trending_score DECIMAL(10,2),
    region VARCHAR(50),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE tiktok_viral_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id VARCHAR(255) UNIQUE,
    author_username VARCHAR(255),
    description TEXT,
    hashtags TEXT[],
    sound_id VARCHAR(255),
    view_count BIGINT,
    like_count BIGINT,
    comment_count INTEGER,
    share_count INTEGER,
    is_food_related BOOLEAN DEFAULT false,
    relevance_score DECIMAL(5,2),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- ============================================
-- SENTIMENT ANALYSIS
-- ============================================

CREATE TABLE sentiment_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_platform VARCHAR(50), -- instagram, facebook, tiktok
    source_id VARCHAR(255), -- post_id, comment_id, etc
    text_content TEXT,
    sentiment VARCHAR(20), -- positive, negative, neutral
    sentiment_score DECIMAL(5,4), -- -1 to 1
    confidence DECIMAL(5,4),
    emotions JSONB, -- {joy: 0.8, anger: 0.1, etc}
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TREND DETECTION & AGGREGATION
-- ============================================

CREATE TABLE detected_trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_type VARCHAR(50), -- hashtag, topic, sound, food_item
    trend_value VARCHAR(500),
    platforms TEXT[], -- [instagram, tiktok, facebook]
    occurrence_count INTEGER,
    growth_rate DECIMAL(10,2), -- percentage
    trend_score DECIMAL(10,2),
    time_period VARCHAR(20), -- daily, weekly, monthly
    start_date DATE,
    end_date DATE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- CONTENT GENERATION & SCHEDULING
-- ============================================

CREATE TABLE generated_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_type VARCHAR(50), -- caption, hashtags, full_post
    platform VARCHAR(50),
    generated_text TEXT,
    hashtags TEXT[],
    brand_voice VARCHAR(50),
    inspiration_source VARCHAR(255), -- trend_id, manual, etc
    ai_model VARCHAR(100), -- claude-3-5-sonnet, gpt-4, etc
    quality_score DECIMAL(5,2),
    used BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scheduled_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50),
    account_id UUID REFERENCES social_accounts(id),
    content_id UUID REFERENCES generated_content(id),
    caption TEXT,
    media_urls TEXT[],
    hashtags TEXT[],
    scheduled_time TIMESTAMP,
    status VARCHAR(50), -- pending, published, failed, cancelled
    published_at TIMESTAMP,
    post_id VARCHAR(255), -- ID from the platform after publishing
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- MEDIA ASSETS
-- ============================================

CREATE TABLE media_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(500),
    file_path TEXT,
    media_type VARCHAR(50), -- image, video
    mime_type VARCHAR(100),
    file_size_bytes BIGINT,
    width INTEGER,
    height INTEGER,
    duration_seconds INTEGER, -- for videos
    processed BOOLEAN DEFAULT false,
    watermarked BOOLEAN DEFAULT false,
    optimized BOOLEAN DEFAULT false,
    tags TEXT[],
    metadata JSONB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- PERFORMANCE TRACKING
-- ============================================

CREATE TABLE campaign_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_name VARCHAR(255),
    platforms TEXT[],
    post_ids TEXT[],
    start_date DATE,
    end_date DATE,
    total_impressions BIGINT,
    total_reach BIGINT,
    total_engagement INTEGER,
    total_clicks INTEGER,
    engagement_rate DECIMAL(5,2),
    roi_score DECIMAL(10,2),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES for Performance
-- ============================================

CREATE INDEX idx_instagram_posts_timestamp ON instagram_posts(timestamp DESC);
CREATE INDEX idx_instagram_posts_engagement ON instagram_posts(engagement_rate DESC);
CREATE INDEX idx_instagram_insights_date ON instagram_insights(date DESC);

CREATE INDEX idx_facebook_posts_created_time ON facebook_posts(created_time DESC);
CREATE INDEX idx_facebook_posts_engagement ON facebook_posts(engagement_rate DESC);

CREATE INDEX idx_tiktok_trends_detected_at ON tiktok_trends(detected_at DESC);
CREATE INDEX idx_tiktok_trends_score ON tiktok_trends(trending_score DESC);
CREATE INDEX idx_tiktok_trends_category ON tiktok_trends(category);

CREATE INDEX idx_sentiment_platform ON sentiment_analysis(source_platform, analyzed_at DESC);
CREATE INDEX idx_sentiment_score ON sentiment_analysis(sentiment_score DESC);

CREATE INDEX idx_detected_trends_score ON detected_trends(trend_score DESC);
CREATE INDEX idx_detected_trends_period ON detected_trends(time_period, start_date DESC);

CREATE INDEX idx_scheduled_posts_time ON scheduled_posts(scheduled_time);
CREATE INDEX idx_scheduled_posts_status ON scheduled_posts(status);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_instagram_posts_updated_at BEFORE UPDATE ON instagram_posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_facebook_posts_updated_at BEFORE UPDATE ON facebook_posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scheduled_posts_updated_at BEFORE UPDATE ON scheduled_posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Calculate engagement rate automatically
CREATE OR REPLACE FUNCTION calculate_engagement_rate()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.impressions > 0 THEN
        NEW.engagement_rate = ((NEW.like_count + NEW.comment_count + COALESCE(NEW.saved_count, 0)) * 100.0 / NEW.impressions)::DECIMAL(5,2);
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_instagram_engagement BEFORE INSERT OR UPDATE ON instagram_posts
    FOR EACH ROW EXECUTE FUNCTION calculate_engagement_rate();

-- ============================================
-- SEED DATA (Optional)
-- ============================================

-- Insert a sample social account (you'll update this with real data)
-- INSERT INTO social_accounts (platform, account_id, account_name, is_active)
-- VALUES ('instagram', 'sample_id', 'Your Restaurant Name', true);
