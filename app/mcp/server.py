from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from app.resources.ticket_entities import Ticket, TicketSearchResult
from app.resources.tickets import TicketService
from app.utils.http import FreshdeskHTTPClient

mcp = FastMCP(
    name="Freshdesk Connector",
    instructions=(
        "You are connected to a Freshdesk helpdesk. "
        "You can list, retrieve, and search support tickets. "
        "Status values: 2=Open, 3=Pending, 4=Resolved, 5=Closed. "
        "Priority values: 1=Low, 2=Medium, 3=High, 4=Urgent. "
        "To filter by status or priority use search_tickets, not list_tickets."
    ),
)

_http_client = FreshdeskHTTPClient()
_ticket_service = TicketService(_http_client)


@mcp.tool()
async def list_tickets(
    page: int = 1,
    per_page: int = 30,
    filter: Optional[str] = None,
    requester_id: Optional[int] = None,
    email: Optional[str] = None,
    unique_external_id: Optional[str] = None,
    company_id: Optional[int] = None,
    updated_since: Optional[str] = None,
    order_by: Optional[str] = None,
    order_type: Optional[str] = None,
    include: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    List Freshdesk tickets with optional filters.

    - page              : page number (default 1, max 300)
    - per_page          : tickets per page, max 100 (default 30)
    - filter            : new_and_my_open | watching | spam | deleted
    - requester_id      : filter by requester ID
    - email             : filter by requester email
    - unique_external_id: filter by requester's external ID
    - company_id        : filter by company ID
    - updated_since     : ISO 8601 string e.g. 2024-01-01T00:00:00Z
    - order_by          : created_at | due_by | updated_at | status
    - order_type        : asc | desc
    - include           : list of stats | requester | description
    """
    tickets = await _ticket_service.list_tickets(
        page=page,
        per_page=per_page,
        filter=filter,
        requester_id=requester_id,
        email=email,
        unique_external_id=unique_external_id,
        company_id=company_id,
        updated_since=updated_since,
        order_by=order_by,
        order_type=order_type,
        include=include,
    )
    return [t.model_dump() for t in tickets]


@mcp.tool()
async def get_ticket(
    ticket_id: int,
    include: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Retrieve a single Freshdesk ticket by ID.

    - include: list of conversations | requester | company | stats
      Note: including conversations costs 2 API calls.
    """
    ticket = await _ticket_service.get_ticket(
        ticket_id=ticket_id,
        include=include,
    )
    return ticket.model_dump()


@mcp.tool()
async def search_tickets(query: str) -> Dict[str, Any]:
    """
    Search Freshdesk tickets using query syntax. Returns up to 30 results.

    Field operators : AND, OR, :> (greater/equal), :< (less/equal)
    Supported fields: status, priority, agent_id, group_id, tag, type,
                      due_by, created_at, updated_at, closed_at, custom fields

    Examples:
      "status:2 AND priority:4"       → Open + Urgent
      "priority:3 OR priority:4"      → High or Urgent
      "status:2 AND group_id:11"      → Open tickets in group 11
      "created_at:>2024-01-01"        → tickets created after Jan 1 2024
    """
    result = await _ticket_service.search_tickets(query=query)
    return result.model_dump()
