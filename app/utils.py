
from app.config import settings

def get_headers():
    return {
        "authtoken": settings.API_KEY,
        "Accept": "application/vnd.manageengine.sdp.v3+json"
    }
