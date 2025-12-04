from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.Email()
    username = fields.String()
    role = fields.String()
    created_at = fields.DateTime()


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(load_default="user")
