from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repository import BaseRepository
from .enums import TaskStatus


class CeleryTasksRepository(BaseRepository):
    '''
    Репозиторий для осуществления операций с задачами Celery в базе данных.
    '''

    async def update_task_status(
        self, session: AsyncSession, task_id: int, new_status: TaskStatus
    ) -> None:
        '''
        Обновляет статус выполнения Celery задачи по ее идентификатору.

        Args:
            session (AsyncSession): Асинхронная сессия для
             обращения к базе данных.
            task_id (int): Идентификатор задачи.
            new_status (TaskStatus): Новый статус задачи.
        '''
        stmt = (
            update(self.model)
            .where(self.model.id == task_id)
            .values(status=new_status)
        )
        await session.execute(stmt)
        await session.commit()
