from typing import Annotated

from fastapi import APIRouter, Depends

from .dependencies import get_attachments_tasks_service
from ..service import CeleryTasksService

router = APIRouter()


@router.get('/')
async def get_attachments_tasks(
    service: Annotated[
        CeleryTasksService, Depends(get_attachments_tasks_service)
    ]
):
    return await service.get_all_tasks()


@router.get('/{task_id}')
async def get_attachment_task(
    task_id: int,
    service: Annotated[
        CeleryTasksService, Depends(get_attachments_tasks_service)
    ]
):
    return await service.get_task_by_id(task_id=task_id)
