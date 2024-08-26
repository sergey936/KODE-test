from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any


VT = TypeVar('VT', bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    value: VT

    @abstractmethod
    def as_generic_type(self):
        ...

    @abstractmethod
    def validate(self) -> None:
        ...

    def __post_init__(self):
        self.validate()
