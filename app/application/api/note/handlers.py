from fastapi import APIRouter, status, Depends, HTTPException
from punq import Container

from application.api.note.schemas import (
    NoteDetailSchema,
    Filters,
    GetNotesQueryResponseSchema,
    CreateNoteSchema,
)
from domain.entities.note import Note
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from logic.di import get_container
from logic.exceptions.auth import AuthException
from logic.exceptions.base import NotFoundException
from logic.services.auth.utils import get_current_user

from logic.services.note.note import NoteService

router = APIRouter()


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    description="Создать заметку.",
    response_model=NoteDetailSchema,
)
async def create_new_note_handler(
    schema: CreateNoteSchema,
    container: Container = Depends(get_container),
    user: User = Depends(get_current_user),
) -> NoteDetailSchema:
    service: NoteService = container.resolve(NoteService)

    try:
        note = await service.create_note(text=schema.text, user_id=user.oid)

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return NoteDetailSchema.from_entity(note=note)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    description="Получить все заметки текущего авторизованного пользователя.",
    response_model=GetNotesQueryResponseSchema,
)
async def get_all_current_user_notes(
    filters: Filters = Depends(),
    container: Container = Depends(get_container),
    user: User = Depends(get_current_user),
) -> GetNotesQueryResponseSchema:
    service: NoteService = container.resolve(NoteService)

    try:
        notes = await service.get_all_user_notes(
            user_id=user.oid,
            limit=filters.limit,
            offset=filters.offset,
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return GetNotesQueryResponseSchema(
        limit=filters.limit,
        offset=filters.offset,
        items=[NoteDetailSchema.from_entity(note=note) for note in notes],
    )
