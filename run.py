import uvicorn
from fastapi import FastAPI
from app.server import mcp, logger

# Import tools to ensure they are registered with the MCP instance
import app.mcp_tools.tickets 

# Import the new webhook router
from app.routes.webhook import router as webhook_router

# Create the parent FastAPI application
app = FastAPI(title="SDP Webhook Receiver & FastMCP Server")

# Include the custom FastAPI routes (such as /webhook, /health, /)
app.include_router(webhook_router)

# Extract and mount the inner Starlette app from FastMCP
# This preserves the /sse and /messages endpoints without breaking previous functionality
mcp_app = mcp.http_app()
app.mount("/", mcp_app)

if __name__ == "__main__":
    logger.info("Starting Combined Webhook and FastMCP Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
