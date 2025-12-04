from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from app.modules.auth.schemas import LoginSchema, LoginResponseSchema
from app.modules.auth.service import login_user
from app.modules.users.models import User
from app.core.security.rbac import require_role
from app.core.security.jwt_tools import generate_tokens
from app.modules.auth.service import revoke_current_token

blp = Blueprint(
    "Auth",
    __name__,
    url_prefix="/auth",
    description="Authentication & Authorization operations",
)


@blp.post("/login")
@blp.arguments(LoginSchema)
@blp.response(200, LoginResponseSchema)
@blp.doc(security=[])
def login(data):
    """Эндпоинт для авторизации пользователя."""
    email = data["email"]
    password = data["password"]

    result = login_user(email, password)
    if not result:
        return jsonify({"error": "Invalid credentials"}), 401

    tokens, user = result
    return {
        "user_id": user.id,
        "email": user.email,
        **tokens,
    }


@blp.get("/me")
@jwt_required()
@blp.doc(security=[{"BearerAuth": []}])
def me():
    """Эндпоинт для проверки текущего активного аккаунта пользователя."""
    identity = get_jwt_identity()
    user = User.query.get(int(identity))
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role,
    }


@blp.get("/admin-only")
@require_role("admin")
@blp.doc(security=[{"BearerAuth": []}])
def admin_only():
    """
    Эндпоинт для проверки что текущий пользователь имеет роль `admin`.
    Только администратор может получить доступ к этому эндпоинты
    """
    return {"message": "Welcome, admin!"}


@blp.get("/user-area")
@require_role("user", "admin")
@blp.doc(security=[{"BearerAuth": []}])
def user_area():
    """Эндпоинт для проверки что текущий пользователь имеет роль `admin` или `user`"""
    return {"message": "Hello, user or admin!"}


@blp.post("/logout")
@jwt_required()
@blp.doc(security=[{"BearerAuth": []}])
def logout():
    """Эндпоинт для корректного логаута аккаунта."""
    revoke_current_token()
    return {"message": "Token revoked"}, 200


@blp.post("/logout-refresh")
@jwt_required(refresh=True)
@blp.doc(security=[{"BearerAuth": []}])
def logout_refresh():
    """Эндпоинт отзыва текущего токена."""
    revoke_current_token()
    return {"message": "Refresh token revoked"}, 200


@blp.post("/refresh")
@jwt_required(refresh=True)
@blp.doc(security=[{"BearerAuth": []}])
def refresh():
    """Эндпоинт для рефреша токена."""
    revoke_current_token()
    identity = get_jwt_identity()
    tokens = generate_tokens(identity=str(identity))
    return jsonify(tokens), 200
