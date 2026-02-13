
import json
import requests
from app.server import mcp, logger
from app.config import settings
from app.utils import get_headers

@mcp.tool()
def list_requests(row_count: int = 10):
    """Fetch the latest helpdesk tickets from ServiceDesk Plus."""
    logger.info(f"Tool Call: list_requests | count: {row_count}")
    
    url = f"{settings.SDP_URL}/api/v3/requests"
    input_data = {
        "list_info": {
            "row_count": row_count,
            "sort_field": "created_time",
            "sort_order": "desc"
        }
    }
    params = {"input_data": json.dumps(input_data)}
    
    try:
        logger.info(f"Sending GET request to {url}")
        response = requests.get(url, headers=get_headers(), params=params, verify=settings.VERIFY_SSL)
        logger.info(f"SDP Response Status: {response.status_code}")
        
        data = response.json()
        logger.info(f"Successfully retrieved {len(data.get('requests', []))} requests")
        return data
    except Exception as e:
        logger.error(f"Error in list_requests: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def create_ticket(subject: str, description: str, requester_name: str):
    """Create a new support request/ticket."""
    logger.info(f"Tool Call: create_ticket | Subject: {subject} | Requester: {requester_name}")
    
    url = f"{settings.SDP_URL}/api/v3/requests"
    input_data = {
        "request": {
            "subject": subject,
            "description": description,
            "requester": {"name": requester_name}
        }
    }
    
    payload = {"input_data": json.dumps(input_data)}
    
    try:
        logger.info(f"Sending POST request to {url}")
        # Log the payload for debugging (be careful not to log sensitive data in production)
        logger.debug(f"Payload: {payload}")
        
        response = requests.post(url, headers=get_headers(), data=payload, verify=settings.VERIFY_SSL)
        
        logger.info(f"SDP Response Status: {response.status_code}")
        
        # Check if response is empty or not JSON
        if not response.text:
            logger.error("SDP returned an empty response body.")
            return {"error": "Empty response from SDP"}

        try:
            result = response.json()
            if response.status_code in [200, 201]:
                logger.info("Ticket created successfully")
            else:
                logger.warning(f"Ticket creation failed with details: {response.text}")
            return result
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON. Raw response: {response.text}")
            return {"error": "Invalid JSON response from server", "raw": response.text[:200]}

    except Exception as e:
        logger.error(f"Critical error in create_ticket: {str(e)}")
        return {"error": str(e)}
