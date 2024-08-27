from functools import lru_cache

from httpx import AsyncClient
from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncEngine

from infra.db.main import build_sa_session_factory, build_sa_engine
from infra.db.repository.note.base import BaseNoteRepository
from infra.db.repository.note.sa_note_repo import SQLAlchemyNoteRepository
from infra.db.repository.user.base import BaseUserRepository
from infra.db.repository.user.sa_user_repo import SQLAlchemyUserRepository
from logic.services.auth.auth import AuthService
from logic.services.note.note import NoteService, CompositeNoteService
from logic.services.password.password import PasswordService
from logic.services.user.user import UserService
from logic.services.yandex.validator import YandexService
from settings.config import Config


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    container.register(
        AsyncEngine, factory=build_sa_engine, config=config, scope=Scope.singleton
    )

    def init_password_service() -> PasswordService:
        return PasswordService()

    container.register(
        PasswordService, factory=init_password_service, scope=Scope.singleton
    )

    def init_user_repo() -> BaseUserRepository:
        return SQLAlchemyUserRepository(
            _session=build_sa_session_factory(
                engine=container.resolve(AsyncEngine),
            ),
        )

    container.register(
        BaseUserRepository, factory=init_user_repo, scope=Scope.singleton
    )

    def init_user_service() -> UserService:
        return UserService(
            user_repository=container.resolve(BaseUserRepository),
            password_service=container.resolve(PasswordService),
            config=config,
        )

    container.register(UserService, factory=init_user_service, scope=Scope.singleton)

    def init_yandex_validator_service() -> YandexService:
        return YandexService(
            config=config,
            http_client=AsyncClient(),
        )

    container.register(
        YandexService, factory=init_yandex_validator_service, scope=Scope.singleton
    )

    def init_note_service() -> NoteService:
        def init_note_repo() -> BaseNoteRepository:
            return SQLAlchemyNoteRepository(
                _session=build_sa_session_factory(
                    engine=container.resolve(AsyncEngine),
                ),
            )

        return CompositeNoteService(
            note_repository=init_note_repo(),
            yandex_service=container.resolve(YandexService),
        )

    container.register(NoteService, factory=init_note_service, scope=Scope.singleton)

    def init_auth_service() -> AuthService:
        return AuthService(
            user_repository=container.resolve(BaseUserRepository),
            password_service=container.resolve(PasswordService),
            config=config,
        )

    container.register(AuthService, factory=init_auth_service, scope=Scope.singleton)

    return container
