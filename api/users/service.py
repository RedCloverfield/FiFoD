from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .repository import UserRepository
from .validation import UserValidator
from .schemas import UserCreateDTO
from ..core.security import hash_password


class UserService:
    '''
    Сервисный слой, для осуществления операций с пользователями.
    '''

    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        repository: UserRepository
    ):
        self._session_factory = session_factory
        self._repository = repository

    @property
    def user_repository(self):
        return self._repository

    @property
    def session_factory(self):
        return self._session_factory

    async def create_user(
        self, user_data: UserCreateDTO
    ) -> User:
        '''
        Создает и возвращает пользователя.

        Args:
            user_data (UserCreateDTO): Данные нового пользователя.

        Returns:
            User: Новый пользователь.
        '''
        async with self.session_factory() as session:
            validator = UserValidator(repository=self.user_repository)
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
            await self.user_repository.create(
                session=session,
                obj=user
            )
            await session.commit()
            return user
