from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.core.security.rbac import require_role
from .schemas import QuestSchema, QuestCreateSchema
from .service import (
    create_quest,
    get_all_quests,
    get_quest_by_id,
    delete_quest
)

blp = Blueprint(
    "Quests",
    __name__,
    url_prefix="/quests",
    description="Quest management operations",
)


@blp.get("/ping")
@blp.doc(security=[])
def ping_quests():
    return {"quests": "ok"}


@blp.post("/")
@require_role("admin")
@blp.arguments(QuestCreateSchema)
@blp.response(201, QuestSchema)
@blp.doc(security=[{"BearerAuth": []}])
def create(data):
    quest = create_quest(
        title=data["title"],
        description=data.get("description"),
    )
    return quest


@blp.get("/")
@jwt_required()
@blp.response(200, QuestSchema(many=True))
@blp.doc(security=[{"BearerAuth": []}])
def list_quests():
    return get_all_quests()


@blp.get("/<int:quest_id>")
@jwt_required()
@blp.response(200, QuestSchema)
@blp.doc(security=[{"BearerAuth": []}])
def get_one(quest_id):
    quest = get_quest_by_id(quest_id)
    if not quest:
        return jsonify({"error": "Quest not found"}), 404
    return quest


@blp.delete("/<int:quest_id>")
@require_role("admin")
@blp.response(200, description="Quest deleted")
@blp.doc(security=[{"BearerAuth": []}])
def delete(quest_id):
    if not delete_quest(quest_id):
        return jsonify({"error": "Quest not found"}), 404
    return {"status": "deleted"}
