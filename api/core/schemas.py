from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    '''
    Модель базового ответа приложения.
    '''
    message: str | None = None


class SuccessResponse(BaseResponse):
    '''
    Модель удачного ответа приложения.
    '''
    pass


class ErrorDetail(BaseResponse):
    '''
    Модель с данными о возникшей ошибке.
    '''
    code: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    '''
    Модель ответа, содержащего ошибку.
    '''
    error: ErrorDetail
