from pydantic import BaseModel


class DeviceDTO(BaseModel):
    serial: str
    model: str
    version: str
    notes: str
