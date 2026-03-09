from typing import Annotated, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session_factory
from .models import User
from .repository import UserRepository
from .service import UserService


def get_user_repository() -> UserRepository:
    '''
    Создает экземпляр репозитория :class:`UserRepository`.

    Returns:
        AuthRepository: Экземпляр репозитория :class:`UserRepository`
         для работы с моделью :class:`User`.
    '''
    return UserRepository(model=User)


def get_user_service(
    session_factory: Annotated[
        Callable[[], AsyncSession], Depends(get_session_factory)
        ],
    repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ]
) -> UserService:
    '''
    Создает экземпляр сервиса :class:`UserService`.

    Args:
        session_factory (Annotated[ Callable[[], AsyncSession], Depends):
         Фабрика сессий.
        repository (Annotated[ AttachmentRepository, Depends): Класс
         :class:`UserRepository`.

    Returns:
        UserService: Экземпляр сервиса :class:`UserService` для управления
         аутентифкацией и авторизацией.
    '''
    return UserService(
        session_factory=session_factory,
        repository=repository
    )
