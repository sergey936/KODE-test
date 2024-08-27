import pytest

from domain.entities.note import Note
from domain.exceptions.base import EmptyValueObjectException
from domain.values.note import Text


def test_create_note_success():
    text = "Тестовая заметка"

    note = Note.create_note(
        text=text,
        user_id="a48b997f-9f25-4c14-9b45-21f709e43894",
    )

    assert note.text == Text(text)


def test_create_note_empty_text():
    with pytest.raises(EmptyValueObjectException):
        Text("")
