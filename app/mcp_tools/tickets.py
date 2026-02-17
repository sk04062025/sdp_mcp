
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

@mcp.tool()
def get_request(request_id: str):
    """Get full details of a specific request/ticket."""
    logger.info(f"Tool Call: get_request | ID: {request_id}")
    
    url = f"{settings.SDP_URL}/api/v3/requests/{request_id}"
    
    try:
        logger.info(f"Sending GET request to {url}")
        response = requests.get(url, headers=get_headers(), verify=settings.VERIFY_SSL)
        logger.info(f"SDP Response Status: {response.status_code}")
        
        if response.status_code == 404:
            return {"error": "Request not found"}
            
        return response.json()
    except Exception as e:
        logger.error(f"Error in get_request: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def update_request(request_id: str, subject: str = None, description: str = None, status: str = None, priority: str = None):
    """Update an existing request/ticket."""
    logger.info(f"Tool Call: update_request | ID: {request_id}")
    
    url = f"{settings.SDP_URL}/api/v3/requests/{request_id}"
    
    # Construct update data dynamically based on provided fields
    update_fields = {}
    if subject: update_fields["subject"] = subject
    if description: update_fields["description"] = description
    if status: update_fields["status"] = {"name": status}
    if priority: update_fields["priority"] = {"name": priority}
    
    if not update_fields:
        return {"error": "No fields provided for update"}

    input_data = {
        "request": update_fields
    }
    
    payload = {"input_data": json.dumps(input_data)}
    
    try:
        logger.info(f"Sending PUT request to {url}")
        logger.debug(f"Payload: {payload}")
        
        response = requests.put(url, headers=get_headers(), data=payload, verify=settings.VERIFY_SSL)
        logger.info(f"SDP Response Status: {response.status_code}")
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw": response.text[:200]}
            
    except Exception as e:
        logger.error(f"Error in update_request: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def close_request(request_id: str, closure_comments: str):
    """Close a request/ticket directly."""
    logger.info(f"Tool Call: close_request | ID: {request_id}")
    
    # Re-use the update logic but specifically for closing
    # Note: 'Closed' is the standard status name, but it might vary by SDP configuration.
    # We are also appending closure comments to the resolution or description if needed, 
    # but for now, we'll try adding it as a resolution if simpler, or just updating status.
    
    # Strategy: params specific to closure often require a separate resolution add 
    # or just updating the status. Let's try updating status to 'Closed' first.
    
    # Ideally, we should also add a resolution.
    
    return update_request(request_id, status="Closed", description=f"Closure Comments: {closure_comments}")
