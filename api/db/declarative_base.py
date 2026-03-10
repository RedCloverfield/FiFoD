from sqlalchemy import Column, Integer
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    '''
    Базовый класс для декларативного объявления моделей.
    '''

    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    id = Column(Integer, primary_key=True)
