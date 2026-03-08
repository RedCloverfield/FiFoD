from .service import DeviceService


def get_device_service() -> DeviceService:
    '''
    Создает экземпляр класса :class:`DeviceService`.
    '''
    return DeviceService()
