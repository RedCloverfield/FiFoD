from typing import Annotated

from fastapi import APIRouter, Depends, status

from .dependencies import get_user_service
from .schemas import UserCreateDTO, UserDTO
from .service import UserService

router = APIRouter()


@router.post(
    '/register-user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserDTO,
    summary='Ресурс для создания пользователя'
)
async def register_user(
    user_data: UserCreateDTO,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.create_user(user_data=user_data)
