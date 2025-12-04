from app.core.extensions import db
from .models import Quest


def create_quest(title: str, description: str | None = None):
    """Создать квест."""
    quest = Quest(title=title, description=description)
    db.session.add(quest)
    db.session.commit()
    return quest


def get_all_quests():
    """Получить все квесты."""
    return Quest.query.order_by(Quest.created_at.desc()).all()


def get_quest_by_id(quest_id: int):
    """Получить квест по идентификатору."""
    return Quest.query.get(quest_id)


def delete_quest(quest_id: int):
    """Удалить квест по идентификатору."""
    quest = Quest.query.get(quest_id)
    if not quest:
        return False

    db.session.delete(quest)
    db.session.commit()
    return True
