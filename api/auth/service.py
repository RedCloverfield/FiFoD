from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .repository import AuthRepository
from .validation import AuthValidator
from .schemas import UserCreateDTO
from ..core.security import hash_password


class AuthService:

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

    async def create_user(
        self, user_data: UserCreateDTO
    ) -> User:
        async with self.session_factory() as session:
            validator = AuthValidator(repository=self.auth_repository)
            await validator.validate_user_existance(
                username=user_data.username, session=session
            )
            hashed_password = hash_password(
                user_data.password.get_secret_value()
            )
            user = User(
                username=user_data.username,
                hashed_password=hashed_password
            )
            await self.auth_repository.create(
                session=session,
                obj=user
            )
            await session.commit()
            return user

    async def get_user_by_username(self, username: str) -> User:
        async with self.session_factory() as session:
            user = await self.auth_repository.get_by(
                session=session,
                username=username
            )
            return user
