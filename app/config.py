
import os
import logging
import sys

class Settings:
    def __init__(self):
        self.SDP_URL = os.getenv("SDP_URL", "http://localhost:8080").strip("/")
        self.API_KEY = os.getenv("SDP_API_KEY")
        self.VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

# Configure Logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger("sdp-mcp")

if not settings.API_KEY:
    logger.error("SDP_API_KEY is not set in environment variables!")
