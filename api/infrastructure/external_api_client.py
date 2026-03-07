from typing import Any

from fastapi import HTTPException, status
import httpx

from ..core.config import settings


class ExternalAPIClient:

    @staticmethod
    async def get_request(
        url: str,
        params: dict[str, Any] | None = None,
        timeout: float = 10.0
    ) -> httpx.Response:
        async with httpx.AsyncClient(timeout=timeout, verify=False) as (
            async_client
        ):
            response = await async_client.get(
                url=url,
                params=params,
                headers={
                    'Authorization': f'Bearer {settings.external_api_token}'
                }
            )
            response.raise_for_status()
            return response

    async def get_devices(self) -> list[dict]:
        response = await self.get_request(
            url=settings.external_api_url
        )
        json_response = response.json()
        if json_response.get('success') is True:
            devices = json_response.get('devices')
            available_devices = [
                device for device in devices
                if (
                    device.get('ready') is True
                    and device.get('using') is False
                )
            ]
            return available_devices
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                'В настоящий момент невозможно осуществить запрос. '
                'Попробуйте позже.'
            )
        )
