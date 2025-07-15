from marshmallow import fields
from app.models import User
from app.extenstions import ma
from app.models import db

class CreateUserSchema(ma.Schema):
  name = fields.String(required=True)
  username = fields.String(required=True)
  email = fields.String(required=True)
  password = fields.String(required=True, load_only=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True
    exclude = ("password",)


create_user_schema = CreateUserSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)