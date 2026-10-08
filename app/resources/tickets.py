from typing import Any, Dict, List, Optional

from app.utils.http import FreshdeskHTTPClient


class TicketService:
    def __init__(self, client: FreshdeskHTTPClient):
        self.client = client

    async def list_tickets(
        self,
        page: int = 1,
        per_page: int = 30,
        status: Optional[int] = None,
        priority: Optional[int] = None,
        created_since: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}

        if status is not None:
            params["status"] = status
        if priority is not None:
            params["priority"] = priority
        if created_since is not None:
            params["created_since"] = created_since

        return await self.client.get("/tickets", params=params)

    async def get_ticket(
        self,
        ticket_id: int,
        include: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}

        if include:
            params["include"] = ",".join(include)

        return await self.client.get(f"/tickets/{ticket_id}", params=params)

    async def search_tickets(self, query: str) -> Dict[str, Any]:
        # Freshdesk search API requires the query wrapped in double quotes
        return await self.client.get("/search/tickets", params={"query": f'"{query}"'})
