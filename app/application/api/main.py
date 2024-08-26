from fastapi import FastAPI
from punq import Container

from application.api.auth.handlers import router as auth_router
from application.api.user.handlers import router as user_router
from logic.di import get_container


def create_app() -> FastAPI:
    app = FastAPI(
        title='Note service',
        description='Приложение для создания заметок',
    )
    app.dependency_overrides[Container] = get_container

    app.include_router(router=auth_router, prefix='/auth', tags=['Auth'])
    app.include_router(router=user_router, prefix='/user', tags=['User'])

    return app
