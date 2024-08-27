from fastapi import APIRouter, status, Depends, HTTPException, Body
from punq import Container

from application.api.note.schemas import (
    NoteDetailSchema,
    Filters,
    GetNotesQueryResponseSchema,
    CreateNoteSchema,
)
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from logic.di import get_container
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

    except ApplicationException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": error.message}
        )

    return NoteDetailSchema.from_entity(note=note)


@router.get(
    path="",
    status_code=status.HTTP_201_CREATED,
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

    except ApplicationException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": error.message}
        )

    return GetNotesQueryResponseSchema(
        limit=filters.limit,
        offset=filters.offset,
        items=[NoteDetailSchema.from_entity(note=note) for note in notes],
    )
