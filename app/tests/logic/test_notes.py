import pytest

from logic.services.note.note import NoteService
from logic.services.user.user import UserService


@pytest.mark.asyncio
async def test_create_note_non_validation_success(
    user_service: UserService,
    note_service: NoteService,
):
    email = "noteuser1@mail.ru"
    password = "testpassword"
    text = "Заметка без ошибок"

    user = await user_service.create_user(
        email=email,
        password=password,
    )

    note = await note_service.create_note(user_id=user.oid, text=text)

    assert note.text.as_generic_type() == text


@pytest.mark.asyncio
async def test_create_note_validation_success(
    user_service: UserService,
    note_service: NoteService,
):
    email = "noteuser2@mail.ru"
    password = "testpassword"
    text = "Pfvtnrf с ашибками"
    valid_text = "Заметка с ошибками"

    user = await user_service.create_user(
        email=email,
        password=password,
    )

    note = await note_service.create_note(user_id=user.oid, text=text)

    assert note.text.as_generic_type() == valid_text
