from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class AuthException(LogicException):

    @property
    def message(self) -> str:
        return "Ошибка аутентификации."


@dataclass
class CredentialsException(AuthException):

    @property
    def message(self) -> str:
        return "Не удалось подтвердить учетные данные."


@dataclass
class IncorrectCredentialsException(AuthException):

    @property
    def message(self) -> str:
        return "Неверный email или пароль."
