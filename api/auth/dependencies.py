from typing import Annotated, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import AuthenticationError
from ..db.session import get_session_factory
from .models import User
from .repository import AuthRepository
from .service import AuthService
from .jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_auth_repository() -> AuthRepository:
    return AuthRepository(model=User)


def get_auth_service(
    session_factory: Annotated[
        Callable[[], AsyncSession], Depends(get_session_factory)
        ],
    repository: Annotated[
        AuthRepository, Depends(get_auth_repository)
    ]
) -> AuthService:
    return AuthService(
        session_factory=session_factory,
        repository=repository
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> User:
    payload = decode_token(token)
    username: str = payload.get('sub', None)
    if username is None:
        raise AuthenticationError('Неверный токен')
    user = await service.get_user_by_username(username=username)
    if user is None:
        raise AuthenticationError('Неверные учетные данные')
    return user
