from marshmallow import Schema, fields


class QuestSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime()


class QuestCreateSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(load_default=None)
