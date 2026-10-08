import os

import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock

os.environ.setdefault("FRESHDESK_DOMAIN", "testdomain")
os.environ.setdefault("FRESHDESK_API_KEY", "test_api_key_123")

from app.utils.http import FreshdeskHTTPClient
from app.resources.tickets import TicketService


@pytest.fixture
def mock_http_client():
    client = MagicMock(spec=FreshdeskHTTPClient)
    client.get = AsyncMock()
    return client


@pytest.fixture
def ticket_service(mock_http_client):
    return TicketService(client=mock_http_client)


def make_response(status_code: int, json_body=None, headers=None):
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.is_success = 200 <= status_code < 300
    response.json.return_value = json_body or {}
    response.text = str(json_body)
    response.headers = headers or {"X-RateLimit-Remaining": "100"}
    return response
