from typing import Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository:

    def __init__(self, model: type[T]):
        self.model: type[T] = model

    async def create(self, session: AsyncSession, obj: T) -> None:
        session.add(obj)
        await session.flush()

    async def get_by(self, session: AsyncSession, **kwargs) -> T | None:
        query = select(self.model).filter_by(**kwargs)
        return (await session.execute(query)).scalar_one_or_none()

    async def get_all(
        self, session: AsyncSession
    ) -> Sequence[T]:
        query = select(self.model)
        return (await session.execute(query)).scalars().all()
