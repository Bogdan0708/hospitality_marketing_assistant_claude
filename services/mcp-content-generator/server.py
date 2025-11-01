"""
MCP Server for Content Generation
Uses Claude AI to generate social media captions, hashtags, and posts with brand voice
"""

import os
import json
import yaml
from datetime import datetime
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Content Generator")

# Environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
BRAND_VOICE_PROFILE = os.getenv("BRAND_VOICE_PROFILE", "professional")

# Initialize clients
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
redis_client = redis.from_url(REDIS_URL) if REDIS_URL else None


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(DATABASE_URL)


def load_brand_voice(profile: str = None) -> Dict[str, Any]:
    """Load brand voice configuration"""
    if not profile:
        profile = BRAND_VOICE_PROFILE

    brand_voice_path = f"/app/brand-voice/{profile}.yaml"

    # Default brand voice if file doesn't exist
    default_voice = {
        "name": "Professional",
        "tone": "professional, friendly, approachable",
        "style": "Clear, concise, informative",
        "keywords": ["quality", "fresh", "delicious", "local"],
        "emoji_usage": "minimal",
        "hashtag_count": "5-10",
        "call_to_action": "Visit us today!"
    }

    try:
        if os.path.exists(brand_voice_path):
            with open(brand_voice_path, 'r') as f:
                return yaml.safe_load(f)
        return default_voice
    except Exception as e:
        print(f"Error loading brand voice: {e}")
        return default_voice


@mcp.tool()
def generate_caption(
    topic: str,
    platform: str = "instagram",
    include_hashtags: bool = True,
    include_call_to_action: bool = True,
    max_length: int = 2200
) -> Dict[str, Any]:
    """
    Generate an engaging social media caption using AI.

    Args:
        topic: What the post is about (e.g., "new burger menu", "weekend special")
        platform: Target platform - 'instagram', 'facebook', 'tiktok'
        include_hashtags: Whether to include hashtags in the caption
        include_call_to_action: Whether to include a CTA
        max_length: Maximum caption length (Instagram: 2200, Twitter: 280)

    Returns:
        Generated caption with metadata
    """
    try:
        # Load brand voice
        brand_voice = load_brand_voice()

        # Build prompt
        prompt = f"""You are a social media content creator for a hospitality business.

Brand Voice Profile:
- Name: {brand_voice['name']}
- Tone: {brand_voice['tone']}
- Style: {brand_voice['style']}
- Key Keywords: {', '.join(brand_voice['keywords'])}
- Emoji Usage: {brand_voice['emoji_usage']}

Task: Create a {platform} caption about: {topic}

Requirements:
- Maximum length: {max_length} characters
- Match the brand voice and tone perfectly
- {"Include relevant hashtags" if include_hashtags else "Do not include hashtags"}
- {"Include a clear call-to-action" if include_call_to_action else "No call-to-action needed"}
- Make it engaging and shareable
- Use emojis based on the emoji_usage setting

Return ONLY the caption text, nothing else."""

        # Generate with Claude
        message = anthropic_client.messages.create(
            model="claude-3.5-sonnet",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        caption_text = message.content[0].text.strip()

        # Extract hashtags if present
        hashtags = [word for word in caption_text.split() if word.startswith("#")]

        # Store in database
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO generated_content (
                        content_type, platform, generated_text, hashtags,
                        brand_voice, ai_model
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    "caption",
                    platform,
                    caption_text,
                    hashtags,
                    brand_voice['name'],
                    "claude-3.5-sonnet"
                ))
                content_id = cur.fetchone()[0]
                conn.commit()

        return {
            "content_id": str(content_id),
            "caption": caption_text,
            "character_count": len(caption_text),
            "hashtags": hashtags,
            "platform": platform,
            "brand_voice": brand_voice['name'],
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {"error": f"Failed to generate caption: {str(e)}"}

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
