from typing import Annotated

from fastapi import APIRouter, Depends

from .dependencies import get_device_service
from .schemas import DeviceDTO
from .service import DeviceService

router = APIRouter()


@router.get(
    '',
    response_model=list[DeviceDTO],
    summary='Ресурс для получения списка устройств'
)
async def get_devices(
    service: Annotated[DeviceService, Depends(get_device_service)]
):
    return await service.get_devices()
