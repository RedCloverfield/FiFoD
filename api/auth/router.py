from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from ..core.schemas import SuccessResponse
from .schemas import AccessTokenDTO
from .dependencies import get_auth_service
from .enums import TokenType
from .service import AuthService

router = APIRouter()


@router.post(
    '/login',
    summary=(
        'Ресурс для получения JWT Access токена и аутентификации '
        '(для фронтенда)'
    )
)
async def login(
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response
) -> AccessTokenDTO:
    tokens = await service.authenticate_user(auth_data=auth_data)
    response.set_cookie(
        key=TokenType.ACCESS_TOKEN,
        value=tokens.access_token,
        httponly=True
    )
    response.set_cookie(
        key=TokenType.REFRESH_TOKEN,
        value=tokens.refresh_token,
        httponly=True
    )
    return AccessTokenDTO(
        access_token=tokens.access_token,
    )


@router.post(
    '/logout',
    summary='Ресурс для выхода системы (для фронтенда)'
)
async def logout(response: Response):
    response.delete_cookie(key=TokenType.ACCESS_TOKEN)
    response.delete_cookie(key=TokenType.REFRESH_TOKEN)
    return SuccessResponse(message='Вы успешно вышли из системы')


@router.post(
    '/refresh',
    summary='Ресурс для обновлления JWT Access токена (для фронтенда)'
)
async def refresh_access_token(
    response: Response,
    request: Request,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    refresh_token = request.cookies.get(TokenType.REFRESH_TOKEN)
    access_token = await service.refresh_access_token(
        refresh_token=str(refresh_token)
    )
    response.delete_cookie(TokenType.ACCESS_TOKEN)
    response.set_cookie(
        key=TokenType.ACCESS_TOKEN,
        value=access_token,
        secure=True
    )
    return AccessTokenDTO(access_token=access_token)
