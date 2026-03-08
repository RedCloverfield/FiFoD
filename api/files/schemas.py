from datetime import datetime

from pydantic import BaseModel


class FileInfoDTO(BaseModel):
    '''
    Модель для отображения метаданных файлов.
    '''
    name: str
    size: int
    extention: str
    updated_at: datetime
