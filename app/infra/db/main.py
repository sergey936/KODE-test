from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from settings.config import Config


def build_sa_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        config.database_url,
        echo=True,
    )
    return engine


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False
    )
    return session_factory
