from datetime import datetime
import pytest
from app.schemas.user import User, TokenData


def test_user_schema():
    user = User(username="Usuario-Teste", password="pass#")

    assert user.dict() == {
        "username": "Usuario-Teste",
        "password": "pass#"
    }


def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(username="Usuário#", password="pass#")


def test_token_data_schema():
    expires_at = datetime.now()
    
    token_data = TokenData(
        access_token="token qualquer",
        expires_at=expires_at
    )

    assert token_data.dict() == {
        "access_token": "token qualquer",
        "expires_at": expires_at
    }
