from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class InvalidEmailException(ApplicationException):

    @property
    def message(self) -> str:
        return 'Неправильная почта.'


@dataclass
class UnhashedPasswordException(ApplicationException):

    @property
    def message(self) -> str:
        return 'Пароль должен быть захеширован.'
