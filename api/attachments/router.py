from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from .dependencies import get_attachment_service
from .schemas import CreateAttachmentDTO, AttachmentDTO
from .service import AttachmentService

router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=AttachmentDTO,
    summary='Ресурс для создания привязки файлов к устройству'
)
async def post_attachment(
    new_attachment: CreateAttachmentDTO,
    service: Annotated[AttachmentService, Depends(get_attachment_service)]
):
    return await service.create_attachment(new_attachment=new_attachment)


@router.get(
    '',
    response_model=list[AttachmentDTO],
    summary='Ресурс для получения всех привязок'
)
async def get_attachments(
    service: Annotated[AttachmentService, Depends(get_attachment_service)],
    tag: list[str] | None = Query(None)
):
    return await service.get_attachments(
        filter_by_tags=tag
    )
