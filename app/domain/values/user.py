import re
from dataclasses import dataclass

from domain.exceptions.base import EmptyValueObjectException
from domain.exceptions.user import InvalidEmailException, UnhashedPasswordException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Email(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyValueObjectException(object_title='Email')

        if not self._is_valid_email():
            raise InvalidEmailException()

    def _is_valid_email(self) -> bool:
        email_regex = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        )
        return re.match(email_regex, str(self.value)) is not None

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyValueObjectException(object_title='Пароль')

        if not self.is_hashed():
            raise UnhashedPasswordException()

    def is_hashed(self) -> bool:
        pattern = re.compile(r'^[a-f0-9]{64}$', re.IGNORECASE)
        return bool(pattern.match(str(self.value)))

    def as_generic_type(self) -> str:
        return str(self.value)
