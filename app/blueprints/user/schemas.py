from marshmallow import fields
from marshmallow.validate import Length
from app.models import User
from app.extenstions import ma

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
    
  email = fields.Email()
  username = fields.Str(validate=Length(min=3))


create_user_schema = CreateUserSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)