from typing import Callable

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import AuthenticationError
from ..core.security import verify_password
from ..config import settings
from .enums import TokenType
from .schemas import TokensDTO
from ..users.models import User
from ..users.schemas import UserDTO
from .repository import AuthRepository
from .jwt import decode_token, create_token


class AuthService:
    '''
    Сервисный слой, для осуществления операций с аутентификацей и токенами.
    '''

    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        repository: AuthRepository
    ):
        self._session_factory = session_factory
        self._repository = repository

    @property
    def auth_repository(self):
        return self._repository

    @property
    def session_factory(self):
        return self._session_factory

    async def get_user_by_username(self, username: str) -> User:
        '''
        Получает и возвращает пользователя по никнейму.

        Args:
            username (str): Никнейм пользователя.

        Returns:
            User: Пользователь.
        '''
        async with self.session_factory() as session:
            user = await self.auth_repository.get_by(
                session=session,
                username=username
            )
            return user

    async def authenticate_user(
        self, auth_data: OAuth2PasswordRequestForm
    ) -> TokensDTO:
        user = await self.get_user_by_username(username=auth_data.username)
        if not user or not verify_password(
            password=auth_data.password,
            hashed_password=user.hashed_password
        ):
            raise AuthenticationError('Неверный логин или пароль')
        access_token = create_token(
            {
                'sub': user.username,
                'type': TokenType.ACCESS_TOKEN
            },
            expire_delta=settings.access_token_expire_minutes
        )
        refresh_token = create_token(
            {
                'sub': user.username,
                'type': TokenType.REFRESH_TOKEN
            },
            expire_delta=settings.refresh_token_expire_minutes
        )
        return TokensDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def get_user_from_token(
        self, token: str, expected_token_type: TokenType
    ):
        payload = decode_token(token=token)
        token_type = payload.get("type")
        if token_type != expected_token_type:
            raise AuthenticationError(message="Неверный тип токена")
        username: str = payload.get('sub', None)
        if username is None:
            raise AuthenticationError('Неверный токен')
        user = await self.get_user_by_username(username=username)
        if user is None:
            raise AuthenticationError('Неверные учетные данные')
        return user

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> str:
        user = await self.get_user_from_token(
            token=refresh_token,
            expected_token_type=TokenType.REFRESH_TOKEN,
        )
        access_token = create_token(
            data={
                'sub': user.username,
                'type': TokenType.ACCESS_TOKEN
            },
            expire_delta=settings.access_token_expire_minutes
        )
        return access_token
