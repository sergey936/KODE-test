from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from punq import Container

from application.api.auth.schemas import TokenSchema
from domain.exceptions.base import ApplicationException
from logic.di import get_container
from logic.exceptions.auth import AuthException
from logic.exceptions.base import NotFoundException
from logic.services.auth.auth import AuthService

router = APIRouter()


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    description="Аутентификация для получения токена",
    response_model=TokenSchema,
)
async def login_for_access_token_handler(
    form_data: OAuth2PasswordRequestForm = Depends(),
    container: Container = Depends(get_container),
) -> TokenSchema:
    service: AuthService = container.resolve(AuthService)

    try:
        await service.authenticate_user(
            email=form_data.username,
            password=form_data.password,
        )

        access_token = await service.create_access_token(email=form_data.username)

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})
    
    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
    )
