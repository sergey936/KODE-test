from dataclasses import dataclass


class ApplicationException(BaseException):

    @property
    def message(self) -> str:
        return 'Ошибка приложения.'


@dataclass
class EmptyValueObjectException(ApplicationException):
    object_title: str

    @property
    def message(self) -> str:
        return f'{self.object_title} не может быть пустым.'
