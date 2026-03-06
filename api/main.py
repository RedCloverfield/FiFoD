from fastapi import Depends, FastAPI

from .core.exception_handlers import add_exception_handlers
from .config import settings
from .auth.dependencies import get_current_user
from .auth.router import router as auth_router
from .attachments.router import router as attachment_router
from .devices.router import router as device_router
from .files.router import router as file_router
from .core.router import router as base_router
from .celery_tasks.attachments.router import router as attachment_tasks_router

app = FastAPI(
    title=settings.project_title,
    root_path="/api/v1",
)
app.include_router(
    router=auth_router,
    tags=['auth'],
    prefix='/auth'
)
app.include_router(
    router=base_router,
    tags=['core'],
    prefix='/core',
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

add_exception_handlers(app=app)
