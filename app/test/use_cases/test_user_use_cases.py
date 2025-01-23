import pytest
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from app.schemas.user import User
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases


crypt_context = CryptContext(schemes=['sha256_crypt'])


def test_register_user_uc(db_session):
    user = User(
        username="UsuarioTeste",
        password="pass#"
    )

    uc = UserUseCases(db_session=db_session)
    uc.register_user(user=user)

    user_on_db = db_session.query(UserModel).first()
    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)

    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_uc_username_already_exists(db_session, user_on_db):
    user = User(
        username=user_on_db.username,
        password=crypt_context.hash("pass#")
    )

    uc = UserUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.register_user(user=user)


def test_user_login_uc(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    user = User(
        username=user_on_db.username,
        password="pass#"
    )

    token_data = uc.user_login(user=user, expires_in=30)

    assert token_data.expires_at < datetime.utcnow() + timedelta(minutes=31)


def test_user_login_uc_invalid_username(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    user = User(
        username="Invalid",
        password="pass#"
    )

    with pytest.raises(HTTPException):
        token_data = uc.user_login(user=user, expires_in=30)


def test_user_login_uc_invalid_password(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    user = User(
        username=user_on_db.username,
        password="invalid"
    )

    with pytest.raises(HTTPException):
        token_data = uc.user_login(user=user, expires_in=30)
