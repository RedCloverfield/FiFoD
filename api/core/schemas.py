from typing import Any

from pydantic import BaseModel

from ..auth.enums import TokenType


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


class AccessToken(BaseModel):
    '''
    Модель ответа, содержащего JWT Access токен, а также информацию о нем.
    '''
    access_token: str
    token_type: TokenType
