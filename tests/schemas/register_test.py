import pytest
from pydantic import ValidationError

from backend_v2.database.schemas.register_auth import UserCreate


def test_valid_registration():
    user = UserCreate(
        email="test@gmail.com",
        password="Hello12345",
        confirm_password="Hello12345"
    )

    assert user.email == "test@gmail.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="not-an-email",
            password="Hello12345",
            confirm_password="Hello12345"
        )


def test_password_too_short():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@gmail.com",
            password="1234567",
            confirm_password="1234567"
        )


def test_password_mismatch():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@gmail.com",
            password="Hello12345",
            confirm_password="Different123"
        )


def test_password_at_minimum_length():
    user = UserCreate(
        email="test@gmail.com",
        password="12345678",
        confirm_password="12345678"
    )

    assert user.password == "12345678"


def test_password_at_maximum_length():
    password = "a" * 128

    user = UserCreate(
        email="test@gmail.com",
        password=password,
        confirm_password=password
    )

    assert user.password == password


def test_password_exceeds_maximum_length():
    password = "a" * 129

    with pytest.raises(ValidationError):
        UserCreate(
            email="test@gmail.com",
            password=password,
            confirm_password=password
        )


def test_empty_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@gmail.com",
            password="",
            confirm_password=""
        )