from fastapi import Depends, FastAPI

from ..auth.dependencies import get_current_admin_user, get_current_user
from ..auth.router import router as auth_router
from ..attachments.router import router as attachment_router
from ..celery_tasks.attachments.router import router as attachment_tasks_router
from ..devices.router import router as device_router
from ..files.router import router as file_router
from .router import router as base_router
from ..users.router import router as user_router


def register_routers(app: FastAPI):
    '''
    Регистрирует роутеры в FastAPI приложении.

    Args:
        app (FastAPI): Объект FastAPI приложения.
    '''
    app.include_router(
        router=auth_router,
        tags=['auth'],
        prefix='/auth'
    )
    app.include_router(
        router=base_router,
        tags=['core'],
    )
    app.include_router(
        router=attachment_router,
        tags=['attachments'],
        prefix='/attachments',
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        router=attachment_tasks_router,
        tags=['attachments_tasks'],
        prefix='/attachments_tasks',
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        router=device_router,
        tags=['devices'],
        prefix='/devices',
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        router=file_router,
        tags=['files'],
        prefix='/files',
        dependencies=[Depends(get_current_user)]
    )
    app.include_router(
        router=user_router,
        tags=['users'],
        prefix='/users',
        dependencies=[Depends(get_current_admin_user)]
    )
