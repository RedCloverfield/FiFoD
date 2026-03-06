from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..core.exceptions import AuthenticationError
from ..core.schemas import Token
from .dependencies import get_auth_service
from .enums import TokenType
from .schemas import UserCreateDTO, UserDTO
from ..core.security import verify_password
from .service import AuthService
from .jwt import create_access_token

router = APIRouter()


@router.post(
    '/register-user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserDTO
)
async def register_user(
    user_data: UserCreateDTO,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    return await service.create_user(user_data=user_data)


@router.post(
    '/token'
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> Token:
    user = await service.get_user_by_username(username=form_data.username)
    if not user or not verify_password(
        password=form_data.password,
        hashed_password=user.hashed_password
    ):
        raise AuthenticationError('Неверный логин или пароль')
    access_token = create_access_token({'sub': user.username})
    return Token(
        access_token=access_token,
        token_type=TokenType.BEARER
    )
