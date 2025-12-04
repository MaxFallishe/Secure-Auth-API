from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.core.security.password import hash_password, verify_password
from .models import User


def create_user(email: str, username: str, password: str, role: str):
    """Создаеь пользователя с переданными данными."""
    user = User(
        email=email,
        username=username,
        password_hash=hash_password(password),
        role=role,
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Email already in use")
    return user


def authenticate_user(email: str, password: str):
    """Авторизует пользователя по имейлу и паролю указанных пр регистрации."""

    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
