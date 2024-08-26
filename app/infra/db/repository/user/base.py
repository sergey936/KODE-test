from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def add_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...
