# Freshdesk Connector

An MCP connector that enables Agent Studio agents to read support tickets from Freshdesk via `list`, `get`, and `search` primitives.

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/faizahmad87/freshdesk-connector.git
cd freshdesk-connector
poetry install
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
# Required
FRESHDESK_DOMAIN=your-subdomain     # e.g. "acme" for acme.freshdesk.com
FRESHDESK_API_KEY=your_api_key      # Profile Settings → API Key in Freshdesk

# Optional (defaults shown)
REQUEST_TIMEOUT=30                  # HTTP request timeout in seconds
MAX_RETRIES=3                       # Number of retries on rate limit (429)
```

---

## Running the server

### Option 1 — MCP Inspector (test locally)

Start the inspector:

```bash
poetry run fastmcp dev main.py
```

This opens the inspector in your browser. Once open:

1. Set **Transport Type** to `STDIO`
2. Set **Command** to `poetry`
3. Set **Arguments** to `run python main.py`
4. Expand **Environment Variables** and add:
   - `FRESHDESK_DOMAIN` = `your-subdomain`
   - `FRESHDESK_API_KEY` = `your_api_key`
5. Click **Connect**

You can now call `list_tickets`, `get_ticket`, and `search_tickets` directly from the UI.

---

### Option 2 — HTTP server (connect remotely via ngrok or Claude Desktop)

Start as an SSE HTTP server:

```bash
poetry run python main.py --transport sse
```

The server starts on `http://0.0.0.0:8000`. To expose it publicly:

```bash
ngrok http 8000
```

Then connect any MCP-compatible client (Claude, Agent Studio, etc.) to `https://your-ngrok-url/sse`.

To connect Claude Code specifically, add this to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "freshdesk": {
      "type": "sse",
      "url": "https://your-ngrok-url/sse"
    }
  }
}
```

> **Note:** The `"type": "sse"` field is required — without it Claude Code won't recognise the URL as an SSE transport.

To use a different port:

```bash
poetry run python main.py --transport sse --port 9000
```

---

### Option 3 — Claude Desktop (local stdio)

Add this to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "freshdesk": {
      "command": "poetry",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/freshdesk-connector"
    }
  }
}
```

Restart Claude Desktop and ask: *"List my open Freshdesk tickets"*

---

## Tools exposed

| Tool | Description |
|---|---|
| `list_tickets` | Paginated ticket list with optional filter, requester, company, date, sort, and include params |
| `get_ticket` | Fetch a single ticket by ID; optionally include conversations, requester, company, stats |
| `search_tickets` | Full query-syntax search (AND, OR, field comparisons) with pagination |

See [docs/AGENT_CAPABILITIES.md](docs/AGENT_CAPABILITIES.md) for full details on what the agent can and cannot do.

---

## Running tests

```bash
poetry run pytest
```

Tests are fully offline — no Freshdesk account or network access required.

---

## Assumptions & Limitations

- **Read-only** — no write operations are implemented
- `list_tickets` returns only the **last 30 days** of tickets by default (Freshdesk platform limit)
- `search_tickets` returns a **maximum of 30 results per page**, max 10 pages (Freshdesk search API limit)
- `get_ticket` with `include=["conversations"]` costs **2 API calls** against your plan's rate limit
- Authentication is **API key only** — OAuth is not required by Freshdesk for server-to-server access
