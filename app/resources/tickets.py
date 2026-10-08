from typing import List, Optional

from app.resources.ticket_entities import Ticket, TicketSearchResult
from app.utils.http import FreshdeskHTTPClient


class TicketService:
    def __init__(self, client: FreshdeskHTTPClient):
        self.client = client

    async def list_tickets(
        self,
        page: int = 1,
        per_page: int = 30,
        filter: Optional[str] = None,
        requester_id: Optional[int] = None,
        email: Optional[str] = None,
        company_id: Optional[int] = None,
        updated_since: Optional[str] = None,
        order_by: Optional[str] = None,
        order_type: Optional[str] = None,
        include: Optional[List[str]] = None,
    ) -> List[Ticket]:
        """
        Valid filter values   : new_and_my_open | watching | spam | deleted
        Valid include values  : stats | requester | description
        Valid order_by values : created_at | due_by | updated_at | status
        To filter by status/priority use search_tickets instead.
        """
        params = {"page": page, "per_page": per_page}

        if filter is not None:
            params["filter"] = filter
        if requester_id is not None:
            params["requester_id"] = requester_id
        if email is not None:
            params["email"] = email
        if company_id is not None:
            params["company_id"] = company_id
        if updated_since is not None:
            params["updated_since"] = updated_since
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include:
            params["include"] = ",".join(include)

        raw = await self.client.get("/tickets", params=params)
        return [Ticket.model_validate(t) for t in raw]

    async def get_ticket(
        self,
        ticket_id: int,
        include: Optional[List[str]] = None,
    ) -> Ticket:
        """
        Valid include values: conversations | requester | company | stats
        Note: include=conversations costs 2 API calls.
        """
        params = {}

        if include:
            params["include"] = ",".join(include)

        raw = await self.client.get(f"/tickets/{ticket_id}", params=params)
        return Ticket.model_validate(raw)

    async def search_tickets(self, query: str) -> TicketSearchResult:
        # Freshdesk search API requires the query value wrapped in double quotes
        raw = await self.client.get("/search/tickets", params={"query": f'"{query}"'})
        return TicketSearchResult.model_validate(raw)
