import os
import pytest

os.environ.setdefault("FRESHDESK_DOMAIN", "testdomain")
os.environ.setdefault("FRESHDESK_API_KEY", "test_api_key_123")


TICKET_STUB = {"id": 42, "subject": "Login broken", "status": 2, "priority": 3}
SEARCH_STUB = {"total": 1, "results": [TICKET_STUB]}


async def test_list_tickets_calls_correct_path(ticket_service, mock_http_client):
    mock_http_client.get.return_value = [TICKET_STUB]
    result = await ticket_service.list_tickets()
    mock_http_client.get.assert_called_once_with(
        "/tickets", params={"page": 1, "per_page": 30}
    )
    assert result == [TICKET_STUB]


async def test_list_tickets_passes_filters(ticket_service, mock_http_client):
    mock_http_client.get.return_value = [TICKET_STUB]
    await ticket_service.list_tickets(status=2, priority=3, created_since="2024-01-01T00:00:00Z")
    call_params = mock_http_client.get.call_args[1]["params"]
    assert call_params["status"] == 2
    assert call_params["priority"] == 3
    assert call_params["created_since"] == "2024-01-01T00:00:00Z"


async def test_get_ticket_by_id(ticket_service, mock_http_client):
    mock_http_client.get.return_value = TICKET_STUB
    result = await ticket_service.get_ticket(ticket_id=42)
    mock_http_client.get.assert_called_once_with("/tickets/42", params={})
    assert result["id"] == 42


async def test_get_ticket_with_includes(ticket_service, mock_http_client):
    mock_http_client.get.return_value = TICKET_STUB
    await ticket_service.get_ticket(ticket_id=42, include=["conversations", "requester"])
    call_params = mock_http_client.get.call_args[1]["params"]
    assert call_params["include"] == "conversations,requester"


async def test_search_tickets_wraps_query_in_quotes(ticket_service, mock_http_client):
    mock_http_client.get.return_value = SEARCH_STUB
    await ticket_service.search_tickets(query="status:2 AND priority:3")
    call_params = mock_http_client.get.call_args[1]["params"]
    assert call_params["query"] == '"status:2 AND priority:3"'
