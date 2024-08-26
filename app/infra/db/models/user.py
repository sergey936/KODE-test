from sqlalchemy.orm import Mapped

from infra.db.models.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    email: Mapped[str]
    password: Mapped[str]
