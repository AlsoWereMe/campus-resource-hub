"""服务间 HTTP 调用：自动附带服务令牌与 traceparent（IAM-AUTH-03、NFR-13）。"""

from datetime import UTC, datetime, timedelta
from typing import Any

import httpx

from campus_common.config import ServiceName, ServiceSettings
from campus_common.errors import UpstreamError
from campus_common.tracing import outgoing_headers


class ServiceTokenProvider:
    """用服务凭证向 IAM 换取服务令牌，并在过期前复用。"""

    def __init__(self, settings: ServiceSettings, http: httpx.AsyncClient) -> None:
        self._settings = settings
        self._http = http
        self._token: str | None = None
        self._expires_at = datetime.min.replace(tzinfo=UTC)

    async def token(self) -> str:
        if self._token and datetime.now(UTC) < self._expires_at - timedelta(seconds=60):
            return self._token
        try:
            response = await self._http.post(
                self._settings.service_token_url,
                json={
                    "clientId": self._settings.service_client_id,
                    "clientSecret": self._settings.service_client_secret,
                },
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise UpstreamError("无法获取服务令牌", details={"service": "platform"}) from exc
        data = response.json()
        self._token = str(data["accessToken"])
        self._expires_at = datetime.now(UTC) + timedelta(seconds=int(data["expiresIn"]))
        return self._token


class InternalClient:
    """调用其他服务的内部或公开接口。返回 httpx.Response，由调用方处理 4xx。"""

    def __init__(
        self,
        settings: ServiceSettings,
        http: httpx.AsyncClient | None = None,
        token_provider: ServiceTokenProvider | None = None,
    ) -> None:
        self._settings = settings
        self._http = http or httpx.AsyncClient(timeout=10)
        self._tokens = token_provider or ServiceTokenProvider(settings, self._http)

    async def request(
        self,
        service: ServiceName,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> httpx.Response:
        headers = {
            "Authorization": f"Bearer {await self._tokens.token()}",
            **outgoing_headers(),
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        url = self._settings.service_url(service) + path
        try:
            response = await self._http.request(
                method, url, json=json, params=params, headers=headers
            )
        except httpx.HTTPError as exc:
            raise UpstreamError(f"调用 {service} 失败", details={"service": service}) from exc
        if response.status_code >= 500:
            raise UpstreamError(
                f"{service} 返回 {response.status_code}",
                details={"service": service, "status": response.status_code},
            )
        return response

    async def aclose(self) -> None:
        await self._http.aclose()
