from dataclasses import dataclass

from logic.exceptions.base import LogicException, NotFoundException


@dataclass
class UserAlreadyExistsException(LogicException):

    @property
    def message(self) -> str:
        return "Пользователь с таким email уже существует."


@dataclass
class UserNotFoundException(NotFoundException):

    @property
    def message(self) -> str:
        return "Пользоваиель с таким email не найден."
