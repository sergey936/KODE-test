import pytest

from httpx import Response

from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_note_non_validation_success(
    app: FastAPI,
    client: TestClient,
):
    email: str = "appuser1@mail.ru"
    password: str = "testpassword"
    text: str = "Заметка без ошибок"

    url_create_user = app.url_path_for("create_new_user_handler")
    response_create_user: Response = client.post(
        url=url_create_user,
        json={
            "email": email,
            "password": password,
        },
    )

    url_login = app.url_path_for("login_for_access_token_handler")
    response_login: Response = client.post(
        url=url_login,
        data={
            "username": email,
            "password": password,
        },
    )

    token: str = response_login.json()["access_token"]

    url_create_note = app.url_path_for("create_new_note_handler")
    response_create_note: Response = client.post(
        url=url_create_note,
        json={
            "text": text,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response_create_note.is_success
    note_json_data = response_create_note.json()
    user_json_data = response_create_user.json()

    assert note_json_data["text"] == text
    assert note_json_data["owner_id"] == user_json_data["id"]


@pytest.mark.asyncio
async def test_create_note_validation_success(
    app: FastAPI,
    client: TestClient,
):
    email: str = "appuser2@mail.ru"
    password: str = "testpassword"

    text: str = "В зометке есть gfhf ашибак"
    valid_text: str = "В заметке есть пара ошибок"

    url_create_user = app.url_path_for("create_new_user_handler")
    response_create_user: Response = client.post(
        url=url_create_user,
        json={
            "email": email,
            "password": password,
        },
    )

    url_login = app.url_path_for("login_for_access_token_handler")
    response_login: Response = client.post(
        url=url_login,
        data={
            "username": email,
            "password": password,
        },
    )

    token: str = response_login.json()["access_token"]

    url_create_note = app.url_path_for("create_new_note_handler")
    response_create_note: Response = client.post(
        url=url_create_note,
        json={
            "text": text,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response_create_note.is_success
    note_json_data = response_create_note.json()
    user_json_data = response_create_user.json()

    assert note_json_data["text"] == valid_text
    assert note_json_data["owner_id"] == user_json_data["id"]


@pytest.mark.asyncio
async def test_get_all_user_notes_success(
    app: FastAPI,
    client: TestClient,
):
    email: str = "appuser3@mail.ru"
    password: str = "testpassword"

    url_create_user = app.url_path_for("create_new_user_handler")
    response_create_user: Response = client.post(
        url=url_create_user,
        json={
            "email": email,
            "password": password,
        },
    )

    url_login = app.url_path_for("login_for_access_token_handler")
    response_login: Response = client.post(
        url=url_login,
        data={
            "username": email,
            "password": password,
        },
    )

    token: str = response_login.json()["access_token"]

    url_get_notes = app.url_path_for("get_all_current_user_notes")
    response_get_notes: Response = client.get(
        url=url_get_notes,
        params={
            "limit": 10,
            "offset": 0,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response_get_notes.is_success
