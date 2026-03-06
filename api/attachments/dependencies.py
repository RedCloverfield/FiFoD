from fastapi import Depends
from typing import Annotated, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session_factory
from .models import Attachment
from .service import AttachmentService
from .repository import AttachmentRepository


def get_attachment_repository() -> AttachmentRepository:
    return AttachmentRepository(model=Attachment)


def get_attachment_service(
    session_factory: Annotated[
        Callable[[], AsyncSession], Depends(get_session_factory)
        ],
    repository: Annotated[
        AttachmentRepository, Depends(get_attachment_repository)
    ]
) -> AttachmentService:
    return AttachmentService(
        session_factory=session_factory,
        repository=repository
    )
