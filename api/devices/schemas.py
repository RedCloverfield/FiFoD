from pydantic import BaseModel


class DeviceDTO(BaseModel):
    '''
    Модель для отображения устройств.
    '''
    serial: str
    model: str
    version: str
    notes: str
