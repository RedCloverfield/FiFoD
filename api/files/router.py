from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from .dependencies import get_file_service
from .service import FileService
from .schemas import FileInfoDTO

router = APIRouter()


@router.get(
    '',
    summary='Ресурс для получения файлов, хранимых на сервере'
)
async def get_files(
    service: Annotated[FileService, Depends(get_file_service)]
) -> list[FileInfoDTO]:
    return await service.get_image_files()


@router.post(
    '',
    summary='Ресурс для загрузки файла на сервер'
)
async def post_file(
    service: Annotated[FileService, Depends(get_file_service)],
    uploaded_file: UploadFile
):
    return await service.upload_file(uploaded_file)
