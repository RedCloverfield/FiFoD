from pydantic import BaseModel, ConfigDict, SecretStr


class UserCreateDTO(BaseModel):
    '''
    Модель для создания пользователя.
    '''
    username: str
    password: SecretStr


class UserDTO(BaseModel):
    '''
    Модель для отображения пользователя.
    '''
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
