from sqlalchemy.orm import Mapped, mapped_column

from infra.db.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)

    email: Mapped[str]
    password: Mapped[str]
