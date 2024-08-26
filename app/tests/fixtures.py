from punq import Container, Scope

from logic.di import _init_container
from logic.services.user.user import UserService


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(UserService, MemoryChatsRepository, scope=Scope.singleton)

    return container
