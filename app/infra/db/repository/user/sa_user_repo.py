from dataclasses import dataclass

from sqlalchemy import select

from domain.entities.user import User
from infra.db.models.user import UserModel
from infra.db.repository.converters.user import (
    convert_user_db_model_to_entity,
    convert_entity_to_user_db_model,
)
from infra.db.repository.sa_repo import SQLAlchemyRepository
from infra.db.repository.user.base import BaseUserRepository


@dataclass
class SQLAlchemyUserRepository(SQLAlchemyRepository, BaseUserRepository):

    async def add_user(self, user: User) -> User:
        async with self._session() as session:
            db_user = convert_entity_to_user_db_model(user=user)

            session.add(db_user)
            await session.commit()

            return user

    async def get_user_by_email(self, email: str) -> User | None:
        async with self._session() as session:
            query = select(UserModel).where(UserModel.email == email)
            user = await session.scalar(query)

            if user:
                return convert_user_db_model_to_entity(user=user)
