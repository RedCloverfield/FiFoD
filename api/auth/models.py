from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from ..db.declarative_base import Base


class User(Base):
    '''
    Модель пользователей.
    '''
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
        )
    hashed_password: Mapped[str] = mapped_column(
        String, nullable=False
    )
