from datetime import datetime

from pydantic import BaseModel


class FileInfoDTO(BaseModel):
    name: str
    size: int
    extention: str
    updated_at: datetime
