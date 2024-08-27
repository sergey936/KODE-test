from dataclasses import dataclass
from typing import Iterable

from domain.entities.note import Note
from infra.db.repository.note.base import BaseNoteRepository
from logic.services.yandex.validator import YandexService


@dataclass
class NoteService:
    note_repository: BaseNoteRepository

    async def create_note(self, user_id: str, text: str) -> Note: ...

    async def get_all_user_notes(
        self, user_id: str, limit: int, offset: int
    ) -> tuple[int, Iterable[Note]]: ...


@dataclass
class CompositeNoteService(NoteService):
    yandex_service: YandexService

    async def create_note(self, user_id: str, text: str) -> Note:
        correct_text: str = text
        invalid_words: list[dict] = await self.yandex_service.validate_text(text=text)
        shift: int = 0

        for correction in invalid_words:
            start_index = correction["pos"] + shift
            end_index = start_index + correction["len"]
            replacement_word = correction["s"][0]

            correct_text = (
                correct_text[:start_index] + replacement_word + correct_text[end_index:]
            )
            shift += len(replacement_word) - correction["len"]

        new_note = Note.create_note(user_id=user_id, text=correct_text)
        await self.note_repository.create_note(
            note=new_note,
        )

        return new_note

    async def get_all_user_notes(
        self, user_id: str, limit: int, offset: int
    ) -> tuple[int, Iterable[Note]]:

        notes = await self.note_repository.get_all_user_notes(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
        if not notes:
            return []

        return notes
