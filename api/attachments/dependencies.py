from fastapi import Depends
from typing import Annotated, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session_factory
from .models import Attachment
from .service import AttachmentService
from .repository import AttachmentRepository


def get_attachment_repository() -> AttachmentRepository:
    '''
    Создает экземпляр репозитория `AttachmentRepository`.

    Returns:
        AttachmentRepository: Экземпляр репозитория `AttachmentRepository`
        для работы с моделью `Attachment`.
    '''
    return AttachmentRepository(model=Attachment)


def get_attachment_service(
    session_factory: Annotated[
        Callable[[], AsyncSession], Depends(get_session_factory)
        ],
    repository: Annotated[
        AttachmentRepository, Depends(get_attachment_repository)
    ]
) -> AttachmentService:
    '''
    Создает экземпляр сервиса `AttachmentService`.

    Args:
        session_factory (Annotated[ Callable[[], AsyncSession], Depends): Фабрика сессий.
        repository (Annotated[ AttachmentRepository, Depends): Класс `AttachmentRepository`.

    Returns:
        AttachmentService: Экземпляр сервиса `AttachmentService` для управления привязками.
    '''
    return AttachmentService(
        session_factory=session_factory,
        repository=repository
    )
