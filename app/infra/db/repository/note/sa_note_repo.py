from dataclasses import dataclass
from typing import Iterable

from domain.entities.note import Note
from infra.db.models.note import NoteModel
from infra.db.repository.note.base import BaseNoteRepository
from infra.db.repository.sa_repo import SQLAlchemyRepository


@dataclass
class SQLAlchemyNoteRepository(SQLAlchemyRepository, BaseNoteRepository):
    async def create_note(self, user_id: str, note: NoteModel) -> Note:
        ...

    async def get_all_user_notes(self, user_id: str) -> Iterable[Note]:
        ...
