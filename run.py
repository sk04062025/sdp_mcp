
from app.server import mcp, logger
# Import tools to ensure they are registered with the MCP instance
import app.mcp_tools.tickets 

if __name__ == "__main__":
    logger.info("Starting FastMCP SSE Server...")
    # In SSE mode, fastmcp uses uvicorn internally
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
