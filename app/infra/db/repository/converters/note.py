from domain.entities.note import Note
from domain.values.note import Text
from infra.db.models.note import NoteModel


def convert_entity_to_note_db_model(note: Note) -> NoteModel:
    return NoteModel(
        id=note.oid,
        text=note.text.as_generic_type(),
        user_id=note.user_id,
        created_at=note.created_at,
    )


def convert_note_db_model_to_entity(note: NoteModel) -> Note:
    return Note(
        oid=note.id,
        text=Text(note.text),
        user_id=note.user_id,
        created_at=note.created_at,
    )
