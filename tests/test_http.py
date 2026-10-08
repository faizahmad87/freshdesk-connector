import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

os.environ.setdefault("FRESHDESK_DOMAIN", "testdomain")
os.environ.setdefault("FRESHDESK_API_KEY", "test_api_key_123")

from app.utils.http import FreshdeskHTTPClient
from app.exceptions.handlers import (
    AuthenticationException,
    FreshdeskAPIException,
    RateLimitException,
    ResourceNotFoundException,
)
from tests.conftest import make_response


@pytest.fixture
def http_client():
    with patch("app.utils.http.httpx.AsyncClient"):
        client = FreshdeskHTTPClient()
        client._client = MagicMock()
        client._client.request = AsyncMock()
        return client


async def test_raises_auth_exception_on_401(http_client):
    http_client._client.request.return_value = make_response(401)
    with pytest.raises(AuthenticationException):
        await http_client.get("/tickets")


async def test_raises_not_found_on_404(http_client):
    http_client._client.request.return_value = make_response(404)
    with pytest.raises(ResourceNotFoundException):
        await http_client.get("/tickets/9999")


async def test_raises_api_exception_on_500(http_client):
    http_client._client.request.return_value = make_response(500, json_body={"error": "server error"})
    with pytest.raises(FreshdeskAPIException) as exc_info:
        await http_client.get("/tickets")
    assert exc_info.value.status_code == 500


async def test_raises_rate_limit_after_max_retries(http_client):
    http_client._client.request.return_value = make_response(
        429, headers={"Retry-After": "1", "X-RateLimit-Remaining": "0"}
    )
    with patch("app.utils.http.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(RateLimitException) as exc_info:
            await http_client.get("/tickets")
        assert exc_info.value.retry_after == 1


async def test_returns_json_on_success(http_client):
    payload = [{"id": 1, "subject": "Test ticket"}]
    http_client._client.request.return_value = make_response(200, json_body=payload)
    result = await http_client.get("/tickets")
    assert result == payload
