from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from application.api.user.schemas import UserCreatedResponseSchema, UserCreateSchema
from domain.exceptions.base import ApplicationException
from logic.services.user.user import UserService

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    description='Создание нового пользователя.',
    response_model=UserCreatedResponseSchema,
)
async def create_new_user_handler(
        schema: UserCreateSchema,
        container: Container = Depends(),
) -> UserCreatedResponseSchema:
    service: UserService = container.resolve(UserService)

    try:
        await service.create_user(
            email=schema.email,
            password=schema.password,
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return UserCreatedResponseSchema()
