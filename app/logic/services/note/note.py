from dataclasses import dataclass

from domain.entities.note import Note
from infra.db.repository.note.base import BaseNoteRepository
from logic.services.yandex.validator import YandexService


@dataclass
class NoteService:
    note_repository: BaseNoteRepository

    async def create_note(self, user_id: str, text: str) -> None:
        ...

    async def get_all_user_notes(self, user_id: str) -> Note:
        ...


@dataclass
class CompositeNoteService(NoteService):
    yandex_service: YandexService

    async def create_note(self, user_id: str, text: str) -> None:
        ...

    async def get_all_user_notes(self, user_id: str) -> Note:
        ...

