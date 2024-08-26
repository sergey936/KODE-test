from dataclasses import dataclass

from domain.exceptions.base import EmptyValueObjectException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyValueObjectException('Текст заметки')

    def as_generic_type(self) -> str:
        return str(self.value)
