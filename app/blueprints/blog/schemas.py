from marshmallow import fields
from marshmallow.validate import Length
from app.extenstions import ma
from app.models import Blog
from app.blueprints.user.schemas import UserSchema


class CreateBlogSchema(ma.Schema):
  title = fields.String(required=True, validate=Length(min=3, max=100))
  body = fields.String(required=True, validate=Length(min=10, max=5000))


class BlogSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Blog
    load_instance = True
    include_fk = True


class ReturnBlogSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Blog
    load_instance = True
    include_fk = True
    exclude = ("author_id",)
    
  author = fields.Nested(UserSchema(only=("id", "username", "name")), dump_only=True)


create_blog_schema = CreateBlogSchema()
blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
return_blog_schema = ReturnBlogSchema()
return_blogs_schema = ReturnBlogSchema(many=True)