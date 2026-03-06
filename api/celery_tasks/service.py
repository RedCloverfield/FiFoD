from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import CeleryTasksRepository
from ..core.exceptions import ObjectNotFound


class CeleryTasksService:

    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        repository: CeleryTasksRepository
    ):
        self._session_factory = session_factory
        self._repository = repository

    @property
    def celery_tasks_repository(self):
        return self._repository

    @property
    def session_factory(self):
        return self._session_factory

    async def get_all_tasks(self):
        async with self.session_factory() as session:
            tasks = await self.celery_tasks_repository.get_all(
                session=session
            )
            return tasks

    async def get_task_by_id(self, task_id: int):
        async with self.session_factory() as session:
            task = await self.celery_tasks_repository.get_by(
                session=session, id=task_id
            )
            if not task:
                raise ObjectNotFound(
                    'Задача с таким идентификатором не найдена'
                )
            return task
