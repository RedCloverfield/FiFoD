from typing import Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.declarative_base import Base

T = TypeVar('T', bound=Base)


class BaseRepository:
    '''
    Базовый репозиторий для наследования. Содержит типичные операции 
    с сущностями в базе данных.
    '''

    def __init__(self, model: type[T]):
        self.model: type[T] = model

    async def create(self, session: AsyncSession, obj: T) -> None:
        '''
        Создает объект в базе данных. Производит `flush` для дальнейшей
        работы с объектом.

        Args:
            session (AsyncSession): Асинхронная сессия для обращения к базе
             данных.
        '''
        session.add(obj)
        await session.flush()

    async def get_by(self, session: AsyncSession, **kwargs) -> T | None:
        '''
        Получает и возвращает сущность модели из базы данных по переданным
        атрибутам.

        Args:
            session (AsyncSession): Асинхронная сессия для обращения к базе
             данных.

        Returns:
            T | None: Объект модели или None.
        '''
        query = select(self.model).filter_by(**kwargs)
        return (await session.execute(query)).scalar_one_or_none()

    async def get_all(
        self, session: AsyncSession
    ) -> Sequence[T]:
        '''
        Получает список всех объектов модели из базы данных.

        Args:
            session (AsyncSession): Асинхронная сессия для обращения к базе
             данных.

        Returns:
            Sequence[T]: Список объектов модели.
        '''
        query = select(self.model)
        return (await session.execute(query)).scalars().all()
