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
FRESHDESK_DOMAIN=your-subdomain     # e.g. "acme" for acme.freshdesk.com
FRESHDESK_API_KEY=your_api_key      # Profile Settings → API Key in Freshdesk
```

### 3. Run the MCP server

```bash
poetry run python main.py
```

The server runs over `stdio` and is ready to be wired into any MCP-compatible agent.

---

## Tools exposed

| Tool | Description |
|---|---|
| `list_tickets` | Paginated ticket list with optional status / priority / date filters |
| `get_ticket` | Fetch a single ticket by ID; optionally include conversations and requester |
| `search_tickets` | Full query-syntax search (AND, OR, field comparisons) |

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
- `search_tickets` returns a **maximum of 30 results** with no pagination (Freshdesk search API limit)
- `include_conversations=true` on `get_ticket` costs **2 API calls** against your plan's rate limit
- Authentication is **API key only** — OAuth is not required by Freshdesk for server-to-server access
