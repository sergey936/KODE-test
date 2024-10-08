from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.models.base import Base


class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(primary_key=True)

    text: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
