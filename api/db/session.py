from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from ..config import settings

engine = create_async_engine(settings.postgres_url)

session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def get_session_factory() -> Callable[[], AsyncSession]:
    return session_factory
