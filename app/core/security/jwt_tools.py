from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)


def generate_tokens(identity: str):
    """
    Генерация access и refresh токена на основе строки ключа (строки identity)
    выступающей уникальным идентификатором пользователя для последующей аутентификации
    """
    return {
        "access_token": create_access_token(identity=identity),
        "refresh_token": create_refresh_token(identity=identity),
    }
