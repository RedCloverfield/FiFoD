from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repository import BaseRepository
from .models import Attachment


class AttachmentRepository(BaseRepository):
    '''
    Репозиторий для осуществления операций с привязками в базе данных.
    '''

    async def get_attachments(
        self, session: AsyncSession, filter_by_tags: str | list[str]
    ) -> Sequence[Attachment]:
        '''
        Возвращает перечень привязок из базы данных.

        Args:
            session (AsyncSession): Асинхронная сессия для
             обращения к базе данных.
            filter_by (str | list[str]): Один или несколько
             тегов для фильтрации ответа базы данных.

        Returns:
            Sequence[Attachment]: Перечень привязок.
        '''
        query = select(self.model)
        if filter_by_tags:
            query = query.where(self.model.tags.overlap(filter_by_tags))
        return (await session.execute(query)).scalars().all()
