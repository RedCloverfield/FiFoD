from typing import Any

from pydantic import BaseModel

from ..auth.enums import TokenType


class BaseResponse(BaseModel):
    message: str | None = None


class SuccessResponse(BaseResponse):
    pass


class ErrorDetail(BaseResponse):
    code: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class Token(BaseModel):
    access_token: str
    token_type: TokenType
