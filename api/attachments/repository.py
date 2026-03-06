from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repository import BaseRepository
from .models import Attachment


class AttachmentRepository(BaseRepository):

    async def get_attachments(
        self, session: AsyncSession, filter_by
    ) -> Sequence[Attachment]:
        query = select(self.model)
        if filter_by:
            query = query.where(self.model.tags.overlap(filter_by))
        return (await session.execute(query)).scalars().all()
