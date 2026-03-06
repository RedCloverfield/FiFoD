from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repository import BaseRepository
from .enums import TaskStatus


class CeleryTasksRepository(BaseRepository):

    async def update_task_status(
        self, session: AsyncSession, task_id: int, new_status: TaskStatus
    ):
        stmt = (
            update(self.model)
            .where(self.model.id == task_id)
            .values(status=new_status)
        )
        await session.execute(stmt)
        await session.commit()
