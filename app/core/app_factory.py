import os
from flask import Flask, jsonify

from .config import config_by_env
from .extensions import db, migrate, cors, jwt
from app.modules.auth.service import is_token_revoked
from app.core.docs.api import create_api

from app.modules.auth.routes import blp as auth_blueprint
from app.modules.users.routes import blp as user_blueprint
from app.modules.quests.routes import blp as quest_blueprint


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    # Настройка конфигурации из config.py
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")
    ConfigClass = config_by_env.get(config_name, config_by_env["default"])
    app.config.from_object(ConfigClass)

    # Регистрируем extensions в приложении
    register_extensions(app)

    # Подключаем документацию к приложению
    api = create_api(app)
    api.spec.components.security_scheme(
        "BearerAuth",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    )
    # Регистрируем blueprints (шаблоны которые можно переиспользовать)
    register_blueprints(api)

    # Подключаем обработчик ошибок
    register_error_handlers(app)

    # Объявляем вспомогательный эндпоинт для проверки работоспособности прилодежения в любой момент
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_data):
        return is_token_revoked(jwt_data)


def register_blueprints(api):
    api.register_blueprint(auth_blueprint)
    api.register_blueprint(user_blueprint)
    api.register_blueprint(quest_blueprint)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal(e):
        return jsonify({"error": "Internal server error"}), 500
