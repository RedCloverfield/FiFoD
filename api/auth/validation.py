from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import ObjectAlreadyExists
from .repository import UserRepository


class UserValidator:
    '''
    Валидатор операций с пользователями.
    '''

    def __init__(self, repository: UserRepository):
        self._repository = repository

    @property
    def repository(self):
        return self._repository

    async def validate_user_existance(
        self, username: str, session: AsyncSession
    ) -> None:
        '''
        Проверяет, что пользователь с указанным никнеймом не существует.

        Args:
            username (str): Никнейм пользователя.
            session (AsyncSession): Асинхронная сессия для работы с базой
             данных.

        Raises:
            ObjectAlreadyExists: Ошибка, если пользователь с указанным
             никнеймом уже существует.
        '''
        if await self.repository.get_by(
            session=session, username=username
        ):
            raise ObjectAlreadyExists(
                'Пользователь с таким именем уже существует'
            )
