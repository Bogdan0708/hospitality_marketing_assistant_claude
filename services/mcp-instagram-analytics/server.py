"""
MCP Server for Instagram Analytics
Exposes tools for retrieving Instagram Business Account insights and performance data
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Instagram Analytics")

# Environment variables
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

# Graph API base URL
GRAPH_API_URL = "https://graph.facebook.com/v18.0"

# Initialize Redis connection
redis_client = redis.from_url(REDIS_URL) if REDIS_URL else None


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(DATABASE_URL)


def cache_get(key: str) -> Optional[str]:
    """Get cached value from Redis"""
    if redis_client:
        try:
            return redis_client.get(key)
        except Exception as e:
            print(f"Redis get error: {e}")
    return None


def cache_set(key: str, value: str, expiry: int = 3600):
    """Set cached value in Redis with expiry in seconds"""
    if redis_client:
        try:
            redis_client.setex(key, expiry, value)
        except Exception as e:
            print(f"Redis set error: {e}")


def make_graph_api_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make request to Facebook Graph API"""
    params["access_token"] = META_ACCESS_TOKEN
    url = f"{GRAPH_API_URL}/{endpoint}"

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_account_insights(date_range: str = "last_7_days") -> Dict[str, Any]:
    """
    Get Instagram Business Account insights for a specified date range.

    Args:
        date_range: One of 'today', 'yesterday', 'last_7_days', 'last_30_days'

    Returns:
        Dictionary containing account metrics (impressions, reach, profile views, etc.)
    """
    # Calculate date range
    today = datetime.now().date()

    if date_range == "today":
        start_date = today
        end_date = today
    elif date_range == "yesterday":
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
    elif date_range == "last_7_days":
        start_date = today - timedelta(days=7)
        end_date = today - timedelta(days=1)
    elif date_range == "last_30_days":
        start_date = today - timedelta(days=30)
        end_date = today - timedelta(days=1)
    else:
        return {"error": "Invalid date_range. Use: today, yesterday, last_7_days, last_30_days"}

    # Check cache
    cache_key = f"instagram_insights:{INSTAGRAM_BUSINESS_ACCOUNT_ID}:{date_range}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    try:
        # Fetch insights from Graph API
        metrics = [
            "impressions",
            "reach",
            "profile_views",
            "website_clicks",
            "email_contacts",
            "phone_call_clicks",
            "get_directions_clicks",
            "follower_count"
        ]

        params = {
            "metric": ",".join(metrics),
            "period": "day",
            "since": int(start_date.strftime("%s")),
            "until": int(end_date.strftime("%s"))
        }

        data = make_graph_api_request(
            f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}/insights",
            params
        )

        # Process and aggregate results
        result = {
            "account_id": INSTAGRAM_BUSINESS_ACCOUNT_ID,
            "date_range": date_range,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "metrics": {}
        }

        for metric_data in data.get("data", []):
            metric_name = metric_data["name"]
            values = metric_data.get("values", [])

            # Sum up values for the period
            total = sum(v.get("value", 0) for v in values)
            result["metrics"][metric_name] = total

        # Cache for 1 hour
        cache_set(cache_key, json.dumps(result), 3600)

        # Store in database
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get or create social account
                cur.execute("""
                    INSERT INTO social_accounts (platform, account_id, is_active)
                    VALUES ('instagram', %s, true)
                    ON CONFLICT (platform, account_id) DO NOTHING
                    RETURNING id
                """, (INSTAGRAM_BUSINESS_ACCOUNT_ID,))

                # Store daily insights
                for single_date in [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]:
                    cur.execute("""
                        INSERT INTO instagram_insights (
                            account_id,
                            date,
                            followers_count,
                            impressions,
                            reach,
                            profile_views,
                            website_clicks,
                            email_contacts,
                            phone_calls,
                            get_directions_clicks
                        ) VALUES (
                            (SELECT id FROM social_accounts WHERE platform='instagram' AND account_id=%s),
                            %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (account_id, date) DO UPDATE SET
                            followers_count = EXCLUDED.followers_count,
                            impressions = EXCLUDED.impressions,
                            reach = EXCLUDED.reach,
                            profile_views = EXCLUDED.profile_views,
                            website_clicks = EXCLUDED.website_clicks,
                            email_contacts = EXCLUDED.email_contacts,
                            phone_calls = EXCLUDED.phone_calls,
                            get_directions_clicks = EXCLUDED.get_directions_clicks,
                            updated_at = CURRENT_TIMESTAMP
                    """, (
                        INSTAGRAM_BUSINESS_ACCOUNT_ID,
                        single_date,
                        result["metrics"].get("follower_count", 0),
                        result["metrics"].get("impressions", 0),
                        result["metrics"].get("reach", 0),
                        result["metrics"].get("profile_views", 0),
                        result["metrics"].get("website_clicks", 0),
                        result["metrics"].get("email_contacts", 0),
                        result["metrics"].get("phone_call_clicks", 0),
                        result["metrics"].get("get_directions_clicks", 0)
                    ))
                conn.commit()

        return result

    except Exception as e:
        return {"error": f"Failed to fetch insights: {str(e)}"}


@mcp.tool()
def analyze_post_performance(limit: int = 10, sort_by: str = "engagement_rate") -> Dict[str, Any]:
    """
    Analyze top-performing Instagram posts.

    Args:
        limit: Number of posts to return (default: 10)
        sort_by: Sort metric - 'engagement_rate', 'reach', 'impressions', 'like_count'

    Returns:
        List of top-performing posts with metrics
    """
    try:
        # Fetch recent media from Graph API
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,insights.metric(impressions,reach,engagement,saved)",
            "limit": 50  # Fetch more to have data to sort
        }

        data = make_graph_api_request(
            f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
            params
        )

        posts = []

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                for media in data.get("data", []):
                    # Extract insights
                    insights = {}
                    for insight in media.get("insights", {}).get("data", []):
                        insights[insight["name"]] = insight["values"][0]["value"]

                    # Calculate engagement rate
                    impressions = insights.get("impressions", 0)
                    engagement = insights.get("engagement", 0)
                    engagement_rate = (engagement / impressions * 100) if impressions > 0 else 0

                    # Extract hashtags from caption
                    caption = media.get("caption", "")
                    hashtags = [word for word in caption.split() if word.startswith("#")]

                    post_data = {
                        "post_id": media["id"],
                        "caption": caption,
                        "media_type": media.get("media_type"),
                        "media_url": media.get("media_url"),
                        "permalink": media.get("permalink"),
                        "timestamp": media.get("timestamp"),
                        "like_count": media.get("like_count", 0),
                        "comment_count": media.get("comments_count", 0),
                        "impressions": impressions,
                        "reach": insights.get("reach", 0),
                        "engagement_rate": round(engagement_rate, 2),
                        "saved_count": insights.get("saved", 0),
                        "hashtags": hashtags
                    }

                    posts.append(post_data)

                    # Store in database
                    cur.execute("""
                        INSERT INTO instagram_posts (
                            post_id, account_id, caption, media_type, media_url,
                            permalink, timestamp, like_count, comment_count,
                            reach, impressions, engagement_rate, saved_count, hashtags
                        ) VALUES (
                            %s,
                            (SELECT id FROM social_accounts WHERE platform='instagram' AND account_id=%s),
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (post_id) DO UPDATE SET
                            like_count = EXCLUDED.like_count,
                            comment_count = EXCLUDED.comment_count,
                            reach = EXCLUDED.reach,
                            impressions = EXCLUDED.impressions,
                            saved_count = EXCLUDED.saved_count,
                            updated_at = CURRENT_TIMESTAMP
                    """, (
                        post_data["post_id"],
                        INSTAGRAM_BUSINESS_ACCOUNT_ID,
                        post_data["caption"],
                        post_data["media_type"],
                        post_data["media_url"],
                        post_data["permalink"],
                        post_data["timestamp"],
                        post_data["like_count"],
                        post_data["comment_count"],
                        post_data["reach"],
                        post_data["impressions"],
                        post_data["engagement_rate"],
                        post_data["saved_count"],
                        post_data["hashtags"]
                    ))

                conn.commit()

        # Sort posts
        valid_sort_keys = ["engagement_rate", "reach", "impressions", "like_count"]
        if sort_by not in valid_sort_keys:
            sort_by = "engagement_rate"

        posts.sort(key=lambda x: x.get(sort_by, 0), reverse=True)

        return {
            "total_posts": len(posts),
            "top_posts": posts[:limit],
            "sorted_by": sort_by
        }

    except Exception as e:
        return {"error": f"Failed to analyze posts: {str(e)}"}


@mcp.tool()
def get_optimal_posting_times() -> Dict[str, Any]:
    """
    Analyze historical data to determine optimal posting times.

    Returns:
        Recommended posting times based on when your audience is most active
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get posts with their engagement metrics
                cur.execute("""
                    SELECT
                        EXTRACT(DOW FROM timestamp) as day_of_week,
                        EXTRACT(HOUR FROM timestamp) as hour_of_day,
                        AVG(engagement_rate) as avg_engagement,
                        AVG(reach) as avg_reach,
                        COUNT(*) as post_count
                    FROM instagram_posts
                    WHERE account_id = (
                        SELECT id FROM social_accounts
                        WHERE platform='instagram' AND account_id=%s
                    )
                    AND timestamp > NOW() - INTERVAL '90 days'
                    GROUP BY day_of_week, hour_of_day
                    HAVING COUNT(*) >= 3
                    ORDER BY avg_engagement DESC
                    LIMIT 10
                """, (INSTAGRAM_BUSINESS_ACCOUNT_ID,))

                optimal_times = cur.fetchall()

                if not optimal_times:
                    return {
                        "message": "Not enough data yet. Post regularly for 2-3 weeks to get recommendations.",
                        "optimal_times": []
                    }

                # Format results
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

                formatted_times = []
                for time in optimal_times:
                    formatted_times.append({
                        "day": day_names[int(time["day_of_week"])],
                        "hour": f"{int(time['hour_of_day']):02d}:00",
                        "avg_engagement_rate": float(time["avg_engagement"]),
                        "avg_reach": int(time["avg_reach"]),
                        "sample_size": int(time["post_count"])
                    })

                return {
                    "optimal_times": formatted_times,
                    "recommendation": f"Best time to post: {formatted_times[0]['day']} at {formatted_times[0]['hour']}"
                }

    except Exception as e:
        return {"error": f"Failed to calculate optimal times: {str(e)}"}


@mcp.tool()
def track_hashtag_performance(hashtags: List[str]) -> Dict[str, Any]:
    """
    Analyze performance of specific hashtags across your posts.

    Args:
        hashtags: List of hashtags to analyze (e.g., ["#foodie", "#burger"])

    Returns:
        Performance metrics for each hashtag
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                results = {}

                for hashtag in hashtags:
                    # Ensure hashtag starts with #
                    if not hashtag.startswith("#"):
                        hashtag = f"#{hashtag}"

                    cur.execute("""
                        SELECT
                            COUNT(*) as usage_count,
                            AVG(engagement_rate) as avg_engagement,
                            AVG(reach) as avg_reach,
                            AVG(impressions) as avg_impressions,
                            SUM(like_count) as total_likes,
                            SUM(comment_count) as total_comments
                        FROM instagram_posts
                        WHERE account_id = (
                            SELECT id FROM social_accounts
                            WHERE platform='instagram' AND account_id=%s
                        )
                        AND %s = ANY(hashtags)
                    """, (INSTAGRAM_BUSINESS_ACCOUNT_ID, hashtag))

                    data = cur.fetchone()

                    results[hashtag] = {
                        "usage_count": int(data["usage_count"]) if data["usage_count"] else 0,
                        "avg_engagement_rate": float(data["avg_engagement"]) if data["avg_engagement"] else 0,
                        "avg_reach": int(data["avg_reach"]) if data["avg_reach"] else 0,
                        "avg_impressions": int(data["avg_impressions"]) if data["avg_impressions"] else 0,
                        "total_likes": int(data["total_likes"]) if data["total_likes"] else 0,
                        "total_comments": int(data["total_comments"]) if data["total_comments"] else 0
                    }

                # Sort by engagement rate
                sorted_hashtags = sorted(
                    results.items(),
                    key=lambda x: x[1]["avg_engagement_rate"],
                    reverse=True
                )

                return {
                    "hashtags_analyzed": len(hashtags),
                    "performance": dict(sorted_hashtags),
                    "best_performing": sorted_hashtags[0][0] if sorted_hashtags else None
                }

    except Exception as e:
        return {"error": f"Failed to track hashtags: {str(e)}"}


@mcp.tool()
def get_audience_demographics() -> Dict[str, Any]:
    """
    Get demographic information about your Instagram audience.

    Returns:
        Audience demographics including age, gender, location
    """
    cache_key = f"instagram_demographics:{INSTAGRAM_BUSINESS_ACCOUNT_ID}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    try:
        # Fetch audience demographics from Graph API
        params = {
            "metric": "audience_city,audience_country,audience_gender_age",
            "period": "lifetime"
        }

        data = make_graph_api_request(
            f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}/insights",
            params
        )

        demographics = {
            "cities": {},
            "countries": {},
            "gender_age": {}
        }

        for metric_data in data.get("data", []):
            metric_name = metric_data["name"]
            if metric_data.get("values"):
                value = metric_data["values"][0].get("value", {})

                if metric_name == "audience_city":
                    demographics["cities"] = value
                elif metric_name == "audience_country":
                    demographics["countries"] = value
                elif metric_name == "audience_gender_age":
                    demographics["gender_age"] = value

        result = {
            "account_id": INSTAGRAM_BUSINESS_ACCOUNT_ID,
            "demographics": demographics,
            "top_city": max(demographics["cities"].items(), key=lambda x: x[1])[0] if demographics["cities"] else None,
            "top_country": max(demographics["countries"].items(), key=lambda x: x[1])[0] if demographics["countries"] else None
        }

        # Cache for 24 hours (demographics don't change frequently)
        cache_set(cache_key, json.dumps(result), 86400)

        return result

    except Exception as e:
        return {"error": f"Failed to fetch demographics: {str(e)}"}


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
