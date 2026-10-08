from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from app.resources.tickets import TicketService
from app.utils.http import FreshdeskHTTPClient

mcp = FastMCP(
    name="Freshdesk Connector",
    instructions=(
        "You are connected to a Freshdesk helpdesk. "
        "You can list, retrieve, and search support tickets. "
        "Status values: 2=Open, 3=Pending, 4=Resolved, 5=Closed. "
        "Priority values: 1=Low, 2=Medium, 3=High, 4=Urgent."
    ),
)

_http_client = FreshdeskHTTPClient()
_ticket_service = TicketService(_http_client)


@mcp.tool()
async def list_tickets(
    page: int = 1,
    per_page: int = 30,
    status: Optional[int] = None,
    priority: Optional[int] = None,
    created_since: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List Freshdesk tickets with optional filters.

    - page: page number (default 1)
    - per_page: tickets per page, max 100 (default 30)
    - status: 2=Open, 3=Pending, 4=Resolved, 5=Closed
    - priority: 1=Low, 2=Medium, 3=High, 4=Urgent
    - created_since: ISO 8601 string e.g. 2024-01-01T00:00:00Z
    """
    return await _ticket_service.list_tickets(
        page=page,
        per_page=per_page,
        status=status,
        priority=priority,
        created_since=created_since,
    )


@mcp.tool()
async def get_ticket(
    ticket_id: int,
    include_conversations: bool = False,
    include_requester: bool = False,
) -> Dict[str, Any]:
    """
    Retrieve a single Freshdesk ticket by ID.

    - include_conversations: attach reply thread (costs 2 API calls)
    - include_requester: attach requester name, email, phone
    """
    include: List[str] = []

    if include_conversations:
        include.append("conversations")
    if include_requester:
        include.append("requester")

    return await _ticket_service.get_ticket(
        ticket_id=ticket_id,
        include=include or None,
    )


@mcp.tool()
async def search_tickets(query: str) -> Dict[str, Any]:
    """
    Search Freshdesk tickets using query syntax.

    Examples:
      "status:2 AND priority:3"       → Open + High priority
      "priority:4 OR priority:3"      → Urgent or High
      "status:2 AND group_id:11"      → Open tickets in a group

    Returns up to 30 results (Freshdesk search API limit).
    """
    return await _ticket_service.search_tickets(query=query)
