from fastapi import FastAPI, Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError
from jose import JWTError, ExpiredSignatureError

from .exceptions import BaseAPIException
from .schemas import ErrorResponse, ErrorDetail


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPStatusError)
    async def httpx_exception_handler(
        request: Request,
        exc: HTTPStatusError
    ) -> JSONResponse:
        error = ErrorResponse(
            error=ErrorDetail(
                message=exc.response.json().get('message'),
                code='httpx_error',
                details=exc.response.json()
            )
        )
        return JSONResponse(
            status_code=exc.response.status_code,
            content=error.model_dump()
        )

    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(
        request: Request,
        exc: BaseAPIException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict()
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_handler(
        request: Request,
        exc: ResponseValidationError
    ):
        error = ErrorResponse(
            error=ErrorDetail(
                message='Ошибка валидации',
                code='response_validation_error',
                details=exc.errors()
            )
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=error.model_dump()
        )

    @app.exception_handler(Exception)
    async def base_exception_handler(
        request: Request,
        exc: Exception
    ):
        error = ErrorResponse(
            error=ErrorDetail(
                message=(
                    'При обработке запроса возникла '
                    'ошибка на уровне сервера. Попробуйте позже'
                ),
                code='internal_error',
            )
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error.model_dump(exclude_none=True)
        )

    @app.exception_handler(ExpiredSignatureError)
    async def expired_token_handler(
        request: Request,
        exc: ExpiredSignatureError
    ):
        error = ErrorResponse(
            error=ErrorDetail(
                message='Токен истек',
                code='token_expired',
            )
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error.model_dump(exclude_none=True)
        )

    @app.exception_handler(JWTError)
    async def invalid_token_handler(
        request: Request,
        exc: JWTError
    ):
        error = ErrorResponse(
            error=ErrorDetail(
                message='Предоставлены неверные учетные данные',
                code='invalid_token',
            )
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error.model_dump(exclude_none=True)
        )
