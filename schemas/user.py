from marshmallow import Schema, fields, validate, post_load
from flask_bcrypt import generate_password_hash


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True,
                             validate=[
                                 validate.Length(max=20),
                                 validate.ContainsNoneOf(' ')
                             ])
    password = fields.String(required=True, validate=validate.Length(min=6))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def secure_user(self, data, **kwargs):
        data['password'] = generate_password_hash(data['password'])
        return data