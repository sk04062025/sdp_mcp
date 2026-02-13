# ServiceDesk Plus MCP Server

This is a Model Context Protocol (MCP) server for ManageEngine ServiceDesk Plus (SDP), built with [FastMCP](https://github.com/fastmcp/fastmcp). It enables AI agents to interact with SDP to fetch requests and create tickets.

## Features

- **Modular Architecture**: Organized into `app/` with separate modules for config, tools, models, and routes.
- **FastMCP**: Uses the FastMCP framework for easy MCP tool definition and SSE transport.
- **Dockerized**: specific `Dockerfile` and `docker-compose.yml` for easy deployment.

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional but recommended)
- ServiceDesk Plus API Key

## Configuration

The application uses environment variables for configuration. You can set these in a `.env` file or directly in your environment.

| Variable | Description | Default |
|----------|-------------|---------|
| `SDP_URL` | URL of your ServiceDesk Plus instance | `http://localhost:8080` |
| `SDP_API_KEY` | Your SDP Technician API Key | **Required** |
| `VERIFY_SSL` | Verify SSL certificates | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Installation & Running

### Using Docker Compose (Recommended)

1. Create a `.env` file with your credentials:
   ```env
   SDP_URL=https://your-sdp-instance.com
   SDP_API_KEY=your-api-key-here
   VERIFY_SSL=true
   ```

2. Build and start the container:
   ```bash
   docker-compose up --build
   ```

The server will start on port `8000` (SSE transport).

### Local Python Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   # Set env vars first or use a .env file loader
   python run.py
   ```

## Available Tools

The following tools are currently implemented in `app/mcp_tools/tickets.py`:

- **`list_requests(row_count=10)`**: Fetch the latest helpdesk tickets.
- **`create_ticket(subject, description, requester_name)`**: Create a new support ticket.

## Project Structure

```text
sdp_mcp/
├── app/
│   ├── config.py           # Configuration loading
│   ├── server.py           # MCP instance creation
│   ├── utils.py            # Helper functions
│   ├── mcp_tools/          # MCP Tools definition
│   ├── models/             # Pydantic models
│   └── routes/             # HTTP routes (if needed)
├── run.py                  # Entry point
├── Dockerfile
└── docker-compose.yml
```
