from typing import Annotated, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import AuthenticationError
from ..db.session import get_session_factory
from .models import User
from .repository import UserRepository
from .service import UserService
from .jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_auth_repository() -> UserRepository:
    '''
    Создает экземпляр репозитория :class:`UserRepository`.

    Returns:
        AuthRepository: Экземпляр репозитория :class:`UserRepository`
         для работы с моделью :class:`User`.
    '''
    return UserRepository(model=User)


def get_auth_service(
    session_factory: Annotated[
        Callable[[], AsyncSession], Depends(get_session_factory)
        ],
    repository: Annotated[
        UserRepository, Depends(get_auth_repository)
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


async def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends(get_auth_service)]
) -> User:
    '''
    Получает пользователя из никнейма, переданного в JWT Access токене
    и возвращает его.

    Args:
        token (Annotated[str, Depends): JWT Access токен.
        service (Annotated[AuthService, Depends): Экземпляр сервиса
         :class:`UserService`.

    Raises:
        AuthenticationError: Ошибка, если токен истек или токен содержит
         некорректные учетные данные.

    Returns:
        User: Пользователь.
    '''
    payload = decode_token(access_token)
    username: str = payload.get('sub', None)
    if username is None:
        raise AuthenticationError('Неверный токен')
    user = await service.get_user_by_username(username=username)
    if user is None:
        raise AuthenticationError('Неверные учетные данные')
    return user
