from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.note import Text


@dataclass
class Note(BaseEntity):
    user_id: str

    text: Text

    @classmethod
    def create_note(
            cls,
            user_id: str,
            text: str,
    ) -> 'Note':
        return cls(
            user_id=user_id,
            text=Text(text),
        )
