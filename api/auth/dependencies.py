from typing import Annotated, Callable

from fastapi import Cookie, Depends  # noqa
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import AuthorizationError
from ..db.session import get_session_factory
from .enums import TokenType
from .repository import AuthRepository
from ..users.models import User
from .service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_auth_repository() -> AuthRepository:
    '''
    Создает экземпляр репозитория :class:`AuthRepository`.

    Returns:
        AuthRepository: Экземпляр репозитория :class:`AuthRepository`
         для работы с моделью :class:`User`.
    '''
    return AuthRepository(model=User)


def get_auth_service(
    session_factory: Annotated[
        Callable[[], AsyncSession], Depends(get_session_factory)
        ],
    repository: Annotated[
        AuthRepository, Depends(get_auth_repository)
    ]
) -> AuthService:
    '''
    Создает экземпляр сервиса :class:`AuthService`.

    Args:
        session_factory (Annotated[ Callable[[], AsyncSession], Depends):
         Фабрика сессий.
        repository (Annotated[ AttachmentRepository, Depends): Класс
         :class:`AuthRepository`.

    Returns:
        AuthService: Экземпляр сервиса :class:`AuthService` для управления
         аутентифкацией и авторизацией.
    '''
    return AuthService(
        session_factory=session_factory,
        repository=repository
    )


async def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    # пример получения access токена из cookie
    # access_token: str | None = Cookie(default=None),
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> User:
    '''
    Получает пользователя из базы данных по никнейму, переданному в JWT Access
    токене и возвращает пользователя, если он существует.

    Args:
        token (Annotated[str, Depends): JWT Access токен.
        service (Annotated[AuthService, Depends): Экземпляр сервиса
         :class:`AuthService`.

    Raises:
        AuthenticationError: Ошибка, если токен невалиден.

    Returns:
        User: Пользователь.
    '''
    return await service.get_user_from_token(
        token=access_token,
        expected_token_type=TokenType.ACCESS_TOKEN
    )


async def get_current_admin_user(
    user: Annotated[User, Depends(get_current_user)]
) -> User:
    if user.is_admin:
        return user
    raise AuthorizationError(
        message='У вас недостаточно прав для осуществления данного действия'
    )
