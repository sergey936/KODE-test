from dataclasses import dataclass
from datetime import timedelta, timezone

import jwt
from sqlalchemy.sql.functions import now

from infra.db.repository.user.base import BaseUserRepository
from logic.services.password.password import PasswordService
from settings.config import Config


@dataclass
class AuthService:
    user_repository: BaseUserRepository
    password_service: PasswordService
    config: Config

    async def create_access_token(self, email: str) -> str:
        data = {
            'email': email,
        }

        expires_delta = timedelta(minutes=self.config.token_expire_min)
        to_encode = data.copy()

        if expires_delta:
            expire = now(timezone.utc) + expires_delta
        else:
            expire = now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)

        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> None:
        user = await self.user_repository.get_user_by_email(email=email)

        if not user:
            raise IncorrectCredentialsException()

        if not self.password_service.check_password(
                plain_password=password,
                password=user.password,
        ):
            raise IncorrectCredentialsException()
