# MCP Wrapper Script for Claude Desktop on Windows
# This script allows Claude Desktop to call the MCP servers running in Docker

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerName,

    [Parameter(Mandatory=$true)]
    [string]$ToolName,

    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ProjectPath = "C:\Users\godja\Desktop\hospitality_marketing_assistant_claude"

# Map server names to container names
$containerMap = @{
    "content-generator" = "mcp-content-generator"
    "instagram-analytics" = "mcp-instagram-analytics"
}

$containerName = $containerMap[$ServerName]

if (-not $containerName) {
    Write-Error "Unknown server: $ServerName"
    exit 1
}

# Check if container is running
$running = docker ps --filter "name=$containerName" --format "{{.Names}}" 2>$null

if ($running -ne $containerName) {
    Write-Error "Container $containerName is not running. Run: docker-compose up -d"
    exit 1
}

# Execute the tool via docker exec
docker exec -i $containerName python -c @"
import sys
sys.path.insert(0, '/app')
from server import $ToolName
import json

# Parse arguments if provided
args = '$Arguments'
if args:
    result = $ToolName($args)
else:
    result = $ToolName()

print(json.dumps(result, indent=2))
"@
