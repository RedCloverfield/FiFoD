from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import ObjectAlreadyExists
from .repository import AuthRepository


class AuthValidator:

    def __init__(self, repository: AuthRepository):
        self._repository = repository

    @property
    def repository(self):
        return self._repository

    async def validate_user_existance(
        self, username: str, session: AsyncSession
    ) -> None:
        if await self.repository.get_by(
            session=session, username=username
        ):
            raise ObjectAlreadyExists(
                'Пользователь с таким именем уже существует'
            )
