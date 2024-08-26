from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.user import Email, Password


@dataclass
class User(BaseEntity):
    email: Email
    password: Password

    @classmethod
    def create_user(
            cls,
            email: str,
            password: str,
    ) -> 'User':
        return cls(
            email=Email(email),
            password=Password(password)
        )
