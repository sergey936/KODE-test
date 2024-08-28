from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from logic.di import _init_container
from settings.config import Config


def build_sa_test_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        config.test_database_url,
    )
    return engine


def init_dummy_container() -> Container:
    container: Container = _init_container()

    config: Config = container.resolve(Config)
    container.register(
        AsyncEngine, factory=build_sa_test_engine, config=config, scope=Scope.singleton
    )

    return container
