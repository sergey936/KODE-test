from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.note import Note


@dataclass
class BaseNoteRepository(ABC):
    @abstractmethod
    async def create_note(self, note: Note) -> Note: ...

    @abstractmethod
    async def get_all_user_notes(
        self,
        user_id: str,
        limit: int,
        offset: int,
    ) -> tuple[int, Iterable[Note]] | None: ...
