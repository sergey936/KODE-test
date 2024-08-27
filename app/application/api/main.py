from fastapi import FastAPI

from application.api.auth.handlers import router as auth_router
from application.api.note.handlers import router as note_handler
from application.api.user.handlers import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Note service",
        description="Приложение для создания заметок",
    )

    app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(router=user_router, prefix="/user", tags=["User"])
    app.include_router(router=note_handler, prefix="/note", tags=["Note"])

    return app
