from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.modules.users.models import User


def require_role(*allowed_roles):
    """
    Декоратор используемый для обозначения того что доступ к эндпоинту требует определенной роли.

    Используется по примеру ниже:
    @require_role("admin")
    @require_role("user")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404

            if user.role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden",
                    "required_roles": allowed_roles,
                    "user_role": user.role
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
