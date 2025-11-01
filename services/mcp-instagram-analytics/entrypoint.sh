#!/bin/bash
# Entrypoint for MCP server - keep container alive
echo "MCP Instagram Analytics starting..."
echo "Waiting for connections via stdio..."

# Keep container running - MCP servers are called via exec, not direct run
tail -f /dev/null
