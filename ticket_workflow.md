# ManageEngine Service Desk Plus - Ticket Creation & Resolution Workflow

## Objective
This document outlines the conversational workflow and system state machine for an AI Agent to:
1. Receive a user request to create a support ticket.
2. Gather required ticket details interactively.
3. Call an MCP tool to create the ticket in ManageEngine Service Desk Plus.
4. Suspend execution/wait for an asynchronous webhook callback.
5. Resume and conclude when the webhook indicates the ticket status is "Resolved" or "Closed".

This workflow is explicitly structured to facilitate the generation of a **Petri Net** (Places and Transitions).

---

## 1. Required Variables / State Data
- `user_request`: Initial intent provided by the user.
- `ticket_subject`: Short summary of the issue.
- `ticket_description`: Detailed explanation of the issue.
- `requester_name`: Name or email of the person requesting help.
- `ticket_id`: Unique identifier returned by ManageEngine after creation.
- `ticket_status`: Current status of the ticket (Open, Resolved, Closed).

---

## 2. Petri Net Mapping Definition

### **Places (States/Conditions)**
- **P0: Idle** - System is waiting for a user request.
- **P1: Gathering_Details** - System needs more information (Subject, Description, Requester).
- **P2: Ready_To_Create** - System has all required information and is ready to execute the MCP tool.
- **P3: Waiting_For_Callback** - Ticket is created. System is paused, listening for an external webhook.
- **P4: Workflow_Complete** - Ticket has been resolved or closed. Workflow terminates.

### **Transitions (Events/Actions)**
- **T1: Trigger_Ticket_Creation** - User asks to create a ticket. (Moves token from P0 -> P1)
- **T2: Provide_Details** - User provides missing required information. (Moves token from P1 -> P2)
- **T3: Execute_MCP_Tool** - System calls `manageengine_create_ticket` MCP tool. Returns `ticket_id`. (Moves token from P2 -> P3)
- **T4: Receive_Webhook** - System receives an HTTP callback indicating `status` == `Resolved` OR `status` == `Closed`. (Moves token from P3 -> P4)

---

## 3. Step-by-Step Agent Workflow Instructions

### Step 1: Initialization (P0 -> P1)
- **Trigger**: User says "I need to create a ticket" or describes an issue.
- **Action**: Acknowledge the request. Check if `ticket_subject`, `ticket_description`, and `requester_name` are present in the user's prompt.
- **Output to User**: If any details are missing, ask the user for them. 
  > *"I can help you create a ticket in ManageEngine. Could you please provide the Subject, a brief Description of the issue, and your Name/Email?"*

### Step 2: Information Gathering (P1 -> P2)
- **Trigger**: User replies with the requested details.
- **Action**: Validate that all three required fields (`subject`, `description`, `requester`) are populated.
- **Output to User**: 
  > *"Thank you. I am creating the ticket now..."*

### Step 3: MCP Tool Execution (P2 -> P3)
- **Trigger**: All details are validated.
- **Action**: Call the MCP Tool.
  ```json
  // MCP Tool Call Request
  {
    "tool_name": "mcp_manageengine_create_ticket",
    "parameters": {
      "subject": "{{ticket_subject}}",
      "description": "{{ticket_description}}",
      "requester": "{{requester_name}}"
    }
  }
