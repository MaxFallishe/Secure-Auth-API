from flask_smorest import Blueprint
from flask import jsonify
from .service import create_user

from .schemas import RegisterSchema, UserSchema

blp = Blueprint(
    "Users",
    __name__,
    url_prefix="/users",
    description="User registration & management",
)


@blp.post("/register")
@blp.arguments(RegisterSchema)
@blp.response(201, UserSchema)
@blp.doc(security=[])
def register_user(data):
    """
    Публичный эндпоинт для регистрации пользователя. Создает только пользователей с ролью "user",
    чтобы создать администратора (роль "admin") - поменяйте значение вручную в базе данных.
    """
    email = data["email"]
    username = data["username"]
    password = data["password"]
    role = "user"

    try:
        user = create_user(email, username, password, role)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return user
