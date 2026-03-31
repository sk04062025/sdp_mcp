from fastapi import APIRouter, Request
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# --- NEW: Health Check Endpoint ---
@router.get("/health")
async def health_check():
    """GET API to check application health."""
    return {"status": "ok", "message": "SDP Webhook Receiver is healthy and running"}

# --- NEW: Root Endpoint (Optional) ---
@router.get("/")
async def root():
    """Simple greeting for base URL."""
    return {"message": "Welcome to the SDP Webhook Receiver API"}

# --- EXISTING: Webhook Receiver ---
@router.post("/webhook")
async def receive_webhook(request: Request):
    """POST API to receive webhooks from ManageEngine ServiceDesk Plus."""
    try:
        # Parse the JSON payload sent by ServiceDesk Plus
        payload = await request.json()
        
        # Log the raw payload
        logger.info(f"Received Webhook Payload: {payload}")
        
        # Extract specific data (based on the JSON configured in SDP)
        request_id = payload.get("request_id", "N/A")
        status = payload.get("status", "N/A")
        subject = payload.get("subject", "N/A")
        
        logger.info(f"Ticket Processed -> ID: {request_id} | Status: {status} | Subject: {subject}")
        
        # Add your custom business logic here (e.g., database updates, alerting, etc.)
        
        return {"message": "Webhook received successfully", "status": "success"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"message": "Error processing webhook", "status": "error"}
