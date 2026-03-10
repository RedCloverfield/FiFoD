from pydantic import BaseModel, ConfigDict, SecretStr


class UserCreateDTO(BaseModel):
    '''
    Модель для создания пользователя.
    '''
    username: str
    password: SecretStr
    is_admin: bool = False


class UserDTO(BaseModel):
    '''
    Модель для отображения пользователя.
    '''
    id: int
    username: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
