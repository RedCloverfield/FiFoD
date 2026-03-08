from typing import Callable, Sequence, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import ObjectNotFound
from .repository import CeleryTasksRepository
from .models import TaskBaseModel

T = TypeVar('T', bound=TaskBaseModel)


class CeleryTasksService:
    '''
    Сервисный слой, для осуществления операций с задачами Celery.
    '''

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

    async def get_all_tasks(self) -> Sequence[T]:
        '''
        Возвращает все Celery задачи.

        Returns:
            Sequence[T]: Список моделей конкретной Celery задачи,
             наследованной от класса :class:`TaskBaseModel`.
        '''
        async with self.session_factory() as session:
            tasks = await self.celery_tasks_repository.get_all(
                session=session
            )
            return tasks

    async def get_task_by_id(self, task_id: int) -> T:
        '''
        Возвращает Celery задачу по ее идентификатору.

        Args:
            task_id (int): Идентификатор Celery задачи.

        Raises:
            ObjectNotFound: Ошибка, если задачи с переданным
             идентификатором не существует.

        Returns:
            T: Экземпляр Celery задачи, унаследованной от класса
             :class:`TaskBaseModel`.
        '''
        async with self.session_factory() as session:
            task = await self.celery_tasks_repository.get_by(
                session=session, id=task_id
            )
            if not task:
                raise ObjectNotFound(
                    'Задача с таким идентификатором не найдена'
                )
            return task
