import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseConfig:
    # Базовые конфигурации Flask приложения
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'secure_auth_api.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JSON_SORT_KEYS = False

    # Переменные для настройки документации к приложению
    OPENAPI_VERSION = "3.0.3"
    API_TITLE = "City Quest API"
    API_VERSION = "1.0.0"

    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"

    OPENAPI_SECURITY_SCHEMES = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    OPENAPI_SPEC_OPTIONS = {
        "security": [{"BearerAuth": []}]
    }


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


config_by_env = {
    "development": DevConfig,
    "production": ProdConfig,
    "default": DevConfig,
}
