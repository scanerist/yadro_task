from app.exceptions import UserAlreadyExistsException, IncorrectPasswordException
from fastapi import HTTPException
import pytest

def test_user_already_exists_exception():
    with pytest.raises(HTTPException) as excinfo:
        raise UserAlreadyExistsException
    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == "Пользователь уже существует"

def test_incorrect_password_exception():
    with pytest.raises(HTTPException) as excinfo:
        raise IncorrectPasswordException
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Неверный пароль"