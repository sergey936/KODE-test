import pytest

from domain.entities.user import User
from domain.exceptions.base import EmptyValueObjectException
from domain.exceptions.user import InvalidEmailException, UnhashedPasswordException
from domain.values.user import Email, Password


def test_user_create_success():
    email = "testemail@mail.ru"
    password = "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05"

    user = User.create_user(email=email, password=password)

    assert user.email == Email(email)
    assert user.password == Password(password)


def test_user_create_empty_email():
    with pytest.raises(EmptyValueObjectException):
        Email("")


def test_user_create_invalid_email():
    with pytest.raises(InvalidEmailException):
        Email("asd")


def test_user_create_empty_password():
    with pytest.raises(EmptyValueObjectException):
        Password("")


def test_user_create_unhashed_password():
    with pytest.raises(UnhashedPasswordException):
        Password("unhashed_password")
