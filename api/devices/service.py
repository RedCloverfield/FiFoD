from .schemas import DeviceDTO
from ..infrastructure.external_api_client import ExternalAPIClient


class DeviceService:
    '''
    Сервисный слой, для осуществления операций с устройствами.
    '''

    def __init__(
        self,
    ):
        self.external_api_client = ExternalAPIClient()

    async def get_devices(
        self
    ) -> list[DeviceDTO]:
        return await self.external_api_client.get_devices()
