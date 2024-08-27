from punq import Container
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from infra.db.models.base import Base
from infra.db.repository.user.base import BaseUserRepository
from logic.services.auth.auth import AuthService
from logic.services.note.note import NoteService
from logic.services.user.user import UserService
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture(scope="function")
def user_repo(container: Container) -> UserService:
    return container.resolve(BaseUserRepository)


@fixture(scope="function")
def user_service(container: Container) -> UserService:
    return container.resolve(UserService)


@fixture(scope="function")
def note_service(container: Container) -> NoteService:
    return container.resolve(NoteService)


@fixture(scope="function")
def auth_service(container: Container) -> AuthService:
    return container.resolve(AuthService)


@fixture(scope="session", autouse=True)
async def prepare_database():

    container: Container = init_dummy_container()
    test_engine: AsyncEngine = container.resolve(AsyncEngine)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
