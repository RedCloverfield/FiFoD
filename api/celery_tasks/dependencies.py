from typing import Annotated, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repository import BaseRepository
from ..db.session import get_session_factory
from .repository import CeleryTasksRepository
from .service import CeleryTasksService


def get_celery_tasks_service(
    repository_construct: Callable[[], BaseRepository]
):
    def construct_celery_tasks_service(
        session_factory: Annotated[
            Callable[[], AsyncSession], Depends(get_session_factory)
            ],
        repository: Annotated[
            CeleryTasksRepository, Depends(repository_construct)
        ]
    ) -> CeleryTasksService:
        return CeleryTasksService(
            session_factory=session_factory,
            repository=repository
        )
    return construct_celery_tasks_service
