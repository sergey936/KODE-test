from dataclasses import dataclass

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.sql.functions import count

from domain.entities.note import Note
from infra.db.models.note import NoteModel
from infra.db.repository.converters.note import (
    convert_entity_to_note_db_model,
    convert_note_db_model_to_entity,
)
from infra.db.repository.note.base import BaseNoteRepository
from infra.db.repository.sa_repo import SQLAlchemyRepository


@dataclass
class SQLAlchemyNoteRepository(SQLAlchemyRepository, BaseNoteRepository):
    async def create_note(self, note: Note) -> Note:
        async with self._session() as session:
            db_note = convert_entity_to_note_db_model(note=note)
            session.add(db_note)
            await session.commit()

            return note

    async def get_all_user_notes(
        self,
        user_id: str,
        limit: int,
        offset: int,
    ) -> Iterable[Note] | None:
        async with self._session() as session:
            query = (
                select(NoteModel)
                .where(NoteModel.user_id == user_id)
                .limit(limit)
                .offset(offset)
            )
            notes = await session.scalars(query)

            if notes:
                return [convert_note_db_model_to_entity(note=note) for note in notes]
