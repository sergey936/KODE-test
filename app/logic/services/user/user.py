from dataclasses import dataclass

from domain.entities.user import User
from infra.db.repository.user.base import BaseUserRepository
from logic.exceptions.base import UserAlreadyExistsException
from logic.services.password.password import PasswordService


@dataclass
class UserService:
    user_repository: BaseUserRepository
    password_service: PasswordService

    async def create_user(self, email: str, password: str) -> None:
        user = await self.user_repository.get_user_by_email(email=email)

        if user:
            raise UserAlreadyExistsException()

        hash_password = self.password_service.hash_password(password)

        user = User.create_user(
            email=email,
            password=hash_password
        )

        await self.user_repository.add_user(user=user)

    async def get_user(self, email: str) -> User:
        ...
