from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.note import Note
from infra.db.models.note import NoteModel


@dataclass
class BaseNoteRepository(ABC):
    @abstractmethod
    async def create_note(self, user_id: str, note: NoteModel) -> Note:
        ...

    @abstractmethod
    async def get_all_user_notes(self, user_id: str) -> Iterable[Note]:
        ...
