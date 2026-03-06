from .service import DeviceService


def get_device_service() -> DeviceService:
    return DeviceService()
