from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from ..db.declarative_base import Base


class User(Base):
    '''
    Модель пользователей.
    '''
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
        )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String, nullable=False
    )
