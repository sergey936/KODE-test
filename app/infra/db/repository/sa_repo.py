from abc import ABC
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker


@dataclass
class SQLAlchemyRepository(ABC):
    _session: async_sessionmaker
