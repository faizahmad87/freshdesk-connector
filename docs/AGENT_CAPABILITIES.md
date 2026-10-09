# Agent Capabilities

## What the agent CAN do

| Capability | Tool | Notes |
|---|---|---|
| List recent tickets | `list_tickets` | Paginated; filters by status, priority, created date |
| Fetch a single ticket | `get_ticket` | Returns full ticket detail |
| Attach reply thread to a ticket | `get_ticket` | Set `include=["conversations"]` |
| Attach requester info to a ticket | `get_ticket` | Set `include=["requester"]` |
| Search tickets by field values | `search_tickets` | Supports AND / OR / comparison operators |

### Supported filter values

**Status** — `status:2` (Open), `status:3` (Pending), `status:4` (Resolved), `status:5` (Closed)

**Priority** — `priority:1` (Low), `priority:2` (Medium), `priority:3` (High), `priority:4` (Urgent)

### Example queries for `search_tickets`

```
status:2 AND priority:4          → Open + Urgent
priority:3 OR priority:4         → High or Urgent
status:2 AND group_id:11         → Open tickets in group 11
```

---

## What the agent CANNOT do

- **Create, update, or delete tickets** — this connector is read-only
- **Access tickets older than 30 days** via `list_tickets` — use `search_tickets` for older records
- **Search beyond 10 pages** — `search_tickets` supports pages 1–10, 30 results per page (300 total max); this is a Freshdesk API hard limit
- **List all contacts or agents** — only ticket data is exposed
- **Access private notes or attachments** — conversations returned by `include_conversations` do not include file attachments
- **Perform bulk operations** — each ticket must be fetched individually via `get_ticket`

---

## Rate limit behaviour

The connector automatically retries on 429 (rate limited) up to `MAX_RETRIES` times, honouring the `Retry-After` header. If retries are exhausted, a `RateLimitException` is raised with the `retry_after` value so the caller can back off.

Note: `get_ticket` with `include=["conversations"]` costs **2 API calls** per request against your plan's per-minute limit.
