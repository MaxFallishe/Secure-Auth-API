# Secure-Auth-API

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![UV](https://img.shields.io/badge/Package_Manager-UV-orange?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=for-the-badge)

Пример backend-приложения на **Flask + SQLAlchemy + SQLite**. 
Реализованный функционал:
- регистрации и аутентификации пользователей (JWT)
- RBAC-система доступа (admin / user)
- создания и управления квестами
- документированный API через **Swagger / Redoc** (flask-smorest)

---

# Быстрый старт (dev mode)

## Шаг 1 - установить зависимости через UV 
_(если uv не установлен - установите)_
```bash
uv sync
```

Создаст `.venv` и установит все зависимости, указанные в `pyproject.toml`.


## Шаг 2 - настройка интерпретатора в PyCharm  
_(пример для PyCharm 2025.02)_

1. Открыть **File → Settings → Python → Interpreter**
2. Нажать **Add Interpreter → Add Local Interpreter**
3. Выбрать **Use existing environment**
4. В поле **Type** указать: **uv**
5. В **Path to uv** прописать путь к uv (обычно:  
   `/home/<user>/.local/bin/uv`)
6. В поле **Uv env use** указать Python из папки проекта:  
   `./.venv/bin/python`
7. Подтвердить настройки

После этого PyCharm будет использовать то же окружение, что и UV.


## Шаг 3 - настройка pre-commit 

1. Установить pre-commit с поддержкой uv:

```bash
uv tool install pre-commit --with pre-commit-uv
```

2. Проверить установку:

```bash
pre-commit --version
```

3. Установить хуки:

```bash
pre-commit install --hook-type commit-msg
```

4. Проверить: выполнить некорректный commit:

```bash
git commit -m "fix workflow error"
```

Если вы видите ошибку вроде:

```
Conventional Commit..............................Failed
```

- значит pre-commit настроен правильно.


## Шаг 4 - проверить Ruff

```bash
uv run ruff check .
```

Если ошибок нет - Ruff работает.


##  Шаг 5 - запустить миграции и dev-сервер

```bash
uv run alembic upgrade head
uv run python run.py
```

Документация API:

- Swagger UI - http://127.0.0.1:5000/swagger-ui  
- Redoc - http://127.0.0.1:5000/redoc  
- OpenAPI JSON - http://127.0.0.1:5000/openapi.json  

---

# Продакшен запуск

Продакшен можно собрать через готовый docker-compose.  
Например:

```bash
docker compose up -d --build
```

---

# Структура проекта

```text
backend/
├── app/
│   ├── __init__.py                 # Вспомогательный файл для работы с импортами
│   ├── core/                       # Базовые элементы приложения
│   │   ├── app_factory.py          # Создание Flask-приложения (настройка и инициализация базовых сущностей)
│   │   ├── config.py               # Конфигурация Flask-приложения 
│   │   ├── extensions.py           # Централизовано
│   │   ├── __init__.py             # Вспомогательный файл для работы с импортами 
│   │   ├── docs/                   # Настройки для документации приложения 
│   │   │   └── api.py              # Инициализация API документации 
│   │   └── security/               # Механизмы безопасности
│   │       ├── password.py         # Проверка, хэширование и другая работа с паролями
│   │       ├── jwt_tools.py        # Генерация JWT токенов
│   │       └── rbac.py             # Механизм и логика проверки ролей
│   │
│   ├── modules/                    # Функциональные модули приложения
│   │   ├── auth/                   # Логика работы связанная с авторизацией
│   │   │   ├── routes.py           # Эндпоинты для операций с авторизацией 
│   │   │   ├── service.py          # Операции связанные с процессом авторизацией (так называемая бизнес-логика)
│   │   │   ├── schemas.py          # Схемы данных связанные с авторизацией
│   │   │   └── models.py           # SQLAlchemy-модели связанные с авторизацией
│   │   │
│   │   ├── users/                  # Логика работы с сущностями типа "пользователь"
│   │   │   ├── routes.py           # Эндпоинты для операций с пользователями
│   │   │   ├── service.py          # Операции над пользователями (так называемая бизнес-логика)
│   │   │   ├── schemas.py          # Схемы данных связанные с пользователями для валидации
│   │   │   └── models.py           # SQLAlchemy-модели связанные с пользователями
│   │   │
│   │   └── quests/                 # Логика работы с сущностями типа "квест"
│   │       ├── routes.py           # Эндпоинты для операций с квестами
│   │       ├── service.py          # Операции над квестами (так называемая бизнес-логика)
│   │       ├── schemas.py          # Схемы данных связанные с квестами для валидации
│   │       └── models.py           # SQLAlchemy-модели связанные с квестами
│   │
│   │
│   └── __init__.py                 # Вспомогательный файл для работы с импортами
│
├── .github/                         # CI/CD-конфигурации проекта
│   └── workflows/
│       └── lint-and-commit.yml      # GitHub Actions: автоматический линтинг и проверка коммитов
│
├── migrations/                     # Alembic-миграции (скрипты для воспроизведения эволюции бд)
│   ├── versions/                   # Миграции
|   └── env.py                      # Настройки окружения Alembic
|
├── .gitignore                      # Список файлов и директорий, которые не должны попадать в Git
├── .python-version                 # Версия Python для pyenv/uv и других менеджеров окружений
├── alembic.ini                     # Основной конфигурационный файл Alembic
├── pyproject.toml                  # Файл с зависимостями проекта
├── uv.lock                         # Файл в котором автоматически "собираются" точные версии всех зависимостей
├── run.py                          # Entry-point Flask приложения
└── README.md                       # Документация к проекту
```

---

# При необходимости добавить новый фунцкционал

Не забывайте проверить что:

- `uv ruff check .` проходит без ошибок  
- вы используете conventional commits (прим. `git commit m "fix: add quest entity"`)
- механизм `pre-commit` работает корректно   
- все новые эндпоинты описаны в интерактивной Swagger-документации  
