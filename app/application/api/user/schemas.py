from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserCreatedResponseSchema(BaseModel):
    response: str = 'Пользователь создан.'