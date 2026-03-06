from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import DeviceDTO
from ..infrastructure.external_api_client import ExternalAPIClient


class DeviceService:

    def __init__(
        self,
    ):
        self.external_api_client = ExternalAPIClient()

    async def get_devices(
        self
    ) -> list[DeviceDTO]:
        return await self.external_api_client.get_devices()
