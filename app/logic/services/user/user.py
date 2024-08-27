from dataclasses import dataclass

import jwt
from jwt import InvalidTokenError

from domain.entities.user import User
from infra.db.repository.user.base import BaseUserRepository
from logic.exceptions.auth import CredentialsException
from logic.exceptions.user import UserAlreadyExistsException

from logic.services.password.password import PasswordService
from settings.config import Config


@dataclass
class UserService:
    user_repository: BaseUserRepository
    password_service: PasswordService
    config: Config

    async def create_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_user_by_email(email=email)

        if user:
            raise UserAlreadyExistsException()

        hash_password = self.password_service.hash_password(password)

        user = User.create_user(email=email, password=hash_password)

        return await self.user_repository.add_user(user=user)

    async def get_current_user_by_token(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, self.config.secret_key, algorithms=[self.config.algorithm]
            )
            email: str = payload.get("email")

            if not email:
                raise CredentialsException()

        except InvalidTokenError:
            raise CredentialsException()

        user = await self.user_repository.get_user_by_email(email=email)

        if not user:
            raise CredentialsException()

        return user
