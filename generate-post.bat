@echo off
REM Quick content generation for MitchfromTransylvania
REM Usage: generate-post.bat "your topic here"

if "%~1"=="" (
    echo Usage: generate-post.bat "your topic"
    echo Example: generate-post.bat "weekend burger special"
    exit /b 1
)

echo.
echo ========================================
echo  MitchfromTransylvania Content Generator
echo ========================================
echo.
echo Generating content for: %~1
echo.

docker exec mcp-content-generator python -c "from anthropic import Anthropic; import yaml; voice = yaml.safe_load(open('/app/brand-voice/dracula.yaml')); client = Anthropic(); msg = client.messages.create(model='claude-3-haiku-20240307', max_tokens=350, messages=[{'role': 'user', 'content': f'Create an Instagram caption for MitchfromTransylvania about: %~1. Use Gothic/vampire tone: {voice[\"tone\"]}. Include 5 hashtags.'}]); print('\n=== GENERATED POST ===\n'); print(msg.content[0].text); print('\n======================')"

echo.
echo Done! Use this caption on Instagram.
echo.
