from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class YandexServiceIntegrationException(LogicException):

    @property
    def message(self) -> str:
        return "Ошибка при обращении к яндекс спеллеру."
