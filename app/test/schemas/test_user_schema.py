import pytest
from app.schemas.user import User


def test_user_schema():
    user = User(username="Usuario-Teste", password="pass#")

    assert user.dict() == {
        "username": "Usuario-Teste",
        "password": "pass#"
    }


def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(username="Usuário#", password="pass#")
