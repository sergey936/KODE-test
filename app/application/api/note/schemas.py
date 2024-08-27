from datetime import datetime

from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.note import Note


class Filters(BaseModel):
    limit: int = 10
    offset: int = 0


class CreateNoteSchema(BaseModel):
    text: str


class NoteDetailSchema(BaseModel):
    id: str
    text: str
    owner_id: str
    created_at: datetime

    @classmethod
    def from_entity(cls, note: Note) -> "NoteDetailSchema":
        return cls(
            id=note.oid,
            text=note.text.as_generic_type(),
            owner_id=note.user_id,
            created_at=note.created_at,
        )


class GetNotesQueryResponseSchema(BaseQueryResponseSchema[list[NoteDetailSchema]]): ...
