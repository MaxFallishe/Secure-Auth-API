from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(Schema):
    user_id = fields.Integer()
    email = fields.Email()
    access_token = fields.String()
    refresh_token = fields.String()
