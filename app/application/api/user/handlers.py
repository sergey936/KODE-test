from fastapi import APIRouter, Depends, HTTPException
from punq import Container
from starlette import status

from application.api.user.schemas import UserDetailSchema, UserCreateSchema
from domain.exceptions.base import ApplicationException
from logic.di import get_container
from logic.exceptions.auth import AuthException
from logic.exceptions.base import NotFoundException
from logic.services.user.user import UserService

router = APIRouter()


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    description="Создание нового пользователя.",
    response_model=UserDetailSchema,
)
async def create_new_user_handler(
    schema: UserCreateSchema,
    container: Container = Depends(get_container),
) -> UserDetailSchema:
    service: UserService = container.resolve(UserService)

    try:
        user = await service.create_user(
            email=schema.email,
            password=schema.password,
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return UserDetailSchema.from_entity(user=user)
