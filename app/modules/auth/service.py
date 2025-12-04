from app.modules.users.service import authenticate_user
from app.core.security.jwt_tools import generate_tokens
from app.core.extensions import db
from flask_jwt_extended import get_jwt
from .models import RevokedToken


def login_user(email: str, password: str):
    """
    Авторизовываем пользователя и возвращаем ему JWT токены.
    """
    user = authenticate_user(email, password)
    if not user:
        return None

    tokens = generate_tokens(identity=str(user.id))
    return tokens, user


def revoke_current_token():
    """
    Отзываем токен который пришёл в хедере.
    """
    jti = get_jwt()["jti"]
    revoked = RevokedToken(jti=jti)
    db.session.add(revoked)
    db.session.commit()


def is_token_revoked(decoded_token):
    jti = decoded_token["jti"]
    return db.session.query(RevokedToken.id).filter_by(jti=jti).first() is not None
