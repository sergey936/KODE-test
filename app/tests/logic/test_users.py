import pytest

from infra.db.repository.user.base import BaseUserRepository
from logic.exceptions.auth import IncorrectCredentialsException
from logic.exceptions.user import UserAlreadyExistsException
from logic.services.auth.auth import AuthService
from logic.services.user.user import UserService


@pytest.mark.asyncio
async def test_user_service_create_user_success(
    user_service: UserService,
    user_repo: BaseUserRepository,
):
    email = "user1@mail.ru"
    password = "testpassword"

    user = await user_service.create_user(
        email=email,
        password=password,
    )
    db_user = await user_repo.get_user_by_email(email=email)

    assert db_user
    assert user.oid == db_user.oid
    assert user.email == db_user.email
    assert user.password == db_user.password


@pytest.mark.asyncio
async def test_user_service_create_user_already_exists(
    user_service: UserService,
    user_repo: BaseUserRepository,
):
    with pytest.raises(UserAlreadyExistsException):
        email = "user2@mail.ru"
        password = "testpassword"

        await user_service.create_user(
            email=email,
            password=password,
        )

        await user_service.create_user(
            email=email,
            password=password,
        )


@pytest.mark.asyncio
async def test_user_service_login_user_success(
    user_service: UserService,
    user_repo: BaseUserRepository,
    auth_service: AuthService,
):
    email = "user3@mail.ru"
    password = "testpassword"

    user = await user_service.create_user(
        email=email,
        password=password,
    )

    await auth_service.authenticate_user(email=email, password=password)

    access_token = await auth_service.create_access_token(email=email)

    authenticated_user = await user_service.get_current_user_by_token(
        token=access_token
    )

    assert user.oid == authenticated_user.oid
    assert user.email == authenticated_user.email
    assert user.password == authenticated_user.password


@pytest.mark.asyncio
async def test_user_service_login_user_incorrect_email(
    user_service: UserService,
    user_repo: BaseUserRepository,
    auth_service: AuthService,
):
    with pytest.raises(IncorrectCredentialsException):
        email = "user4@mail.ru"
        password = "testpassword"

        await user_service.create_user(
            email=email,
            password=password,
        )

        await auth_service.authenticate_user(
            email="incorrect@mail.ru", password=password
        )


@pytest.mark.asyncio
async def test_user_service_login_user_incorrect_password(
    user_service: UserService,
    user_repo: BaseUserRepository,
    auth_service: AuthService,
):
    with pytest.raises(IncorrectCredentialsException):
        email = "user5@mail.ru"
        password = "testpassword"

        await user_service.create_user(
            email=email,
            password=password,
        )

        await auth_service.authenticate_user(
            email=email, password="non_hashed_password"
        )
