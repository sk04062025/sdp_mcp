
from fastmcp import FastMCP
from app.config import settings, logger

logger.info(f"Initializing SDP MCP Server with URL: {settings.SDP_URL}")

mcp = FastMCP("ServiceDeskPlus")
