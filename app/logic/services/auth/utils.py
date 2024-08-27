from punq import Container

from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from logic.di import get_container
from logic.services.user.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    container: Container = Depends(get_container),
) -> User:
    service: UserService = container.resolve(UserService)

    try:
        user = await service.get_current_user_by_token(token=token)
    except ApplicationException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": error.message}
        )

    return user
