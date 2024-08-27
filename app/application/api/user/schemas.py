from datetime import datetime

from pydantic import BaseModel

from domain.entities.user import User


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserDetailSchema(BaseModel):
    id: str

    email: str
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserDetailSchema":
        return cls(
            id=user.oid,
            email=user.email.as_generic_type(),
            created_at=user.created_at,
        )
