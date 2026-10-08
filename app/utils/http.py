import asyncio
from typing import Any, Dict, Optional

import httpx

from app.config import Config
from app.exceptions.handlers import (
    AuthenticationException,
    FreshdeskAPIException,
    RateLimitException,
    ResourceNotFoundException,
)
from app.utils.auth import FreshdeskAuth


class FreshdeskHTTPClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=Config.BASE_URL,
            headers={
                **FreshdeskAuth.get_auth_header(),
                "Content-Type": "application/json",
            },
            timeout=Config.REQUEST_TIMEOUT,
        )

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", path, params=params)

    async def _request(
        self, method: str, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        for attempt in range(Config.MAX_RETRIES):
            response = await self._client.request(method, path, params=params)

            remaining = response.headers.get("X-RateLimit-Remaining")

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                if attempt < Config.MAX_RETRIES - 1:
                    await asyncio.sleep(retry_after)
                    continue
                raise RateLimitException(
                    message=f"Rate limit exceeded. Retry after {retry_after}s",
                    retry_after=retry_after,
                )

            if response.status_code == 401:
                raise AuthenticationException("Invalid API key or unauthorized access")

            if response.status_code == 404:
                raise ResourceNotFoundException(f"Resource not found: {path}")

            if not response.is_success:
                raise FreshdeskAPIException(
                    message=f"Freshdesk API error: {response.text}",
                    status_code=response.status_code,
                )

            # warn when nearing rate limit (under 10% remaining)
            if remaining is not None and int(remaining) < 5:
                print(f"[warn] Freshdesk rate limit low: {remaining} requests remaining")

            return response.json()

    async def close(self):
        await self._client.aclose()
