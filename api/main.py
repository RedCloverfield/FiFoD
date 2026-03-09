from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .core.constants import API_ROOT_URL
from .core.exception_handlers import add_exception_handlers
from .core.register_routers import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_routers(app=app)
    yield


app = FastAPI(
    title=settings.project_title,
    root_path=API_ROOT_URL,
    lifespan=lifespan
)

add_exception_handlers(app=app)
