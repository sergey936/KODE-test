from punq import Container

from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from logic.di import get_container
from logic.exceptions.auth import AuthException
from logic.exceptions.base import NotFoundException
from logic.services.user.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(get_container),
) -> User:
    service: UserService = container.resolve(UserService)

    try:
        user = await service.get_current_user_by_token(token=token)

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return user
