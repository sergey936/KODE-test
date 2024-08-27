import pytest

from httpx import Response

from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_user_success(
    app: FastAPI,
    client: TestClient,
):
    email = "appuser@mail.ru"
    password = "testpassword"

    url = app.url_path_for("create_new_user_handler")
    response: Response = client.post(
        url=url,
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.is_success
    json_data = response.json()

    assert json_data["email"] == email


@pytest.mark.asyncio
async def test_create_user_already_exists(
    app: FastAPI,
    client: TestClient,
):
    email = "appuser@mail.ru"
    password = "testpassword"

    url = app.url_path_for("create_new_user_handler")
    response: Response = client.post(
        url=url,
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.is_error

    error_text = response.json()["detail"]["error"]
    assert error_text == "Пользователь с таким email уже существует."


@pytest.mark.asyncio
async def test_login_for_token_success(
    app: FastAPI,
    client: TestClient,
):
    email = "appuser@mail.ru"
    password = "testpassword"

    url = app.url_path_for("login_for_access_token_handler")
    response: Response = client.post(
        url=url,
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.is_success


@pytest.mark.asyncio
async def test_login_for_token_incorrect_email(
    app: FastAPI,
    client: TestClient,
):
    password = "testpassword"

    url = app.url_path_for("login_for_access_token_handler")
    response: Response = client.post(
        url=url,
        data={
            "username": "invalid@mail.ru",
            "password": password,
        },
    )

    assert response.is_error


@pytest.mark.asyncio
async def test_login_for_token_incorrect_password(
    app: FastAPI,
    client: TestClient,
):
    email = "appuser@mail.ru"

    url = app.url_path_for("login_for_access_token_handler")
    response: Response = client.post(
        url=url,
        data={
            "username": email,
            "password": "nonhashed_password",
        },
    )

    assert response.is_error
