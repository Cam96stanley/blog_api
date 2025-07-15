from marshmallow import fields
from marshmallow.validate import Length
from app.extenstions import ma
from app.models import Blog, Comment, Like
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
  
  is_archived = fields.Boolean(dump_only=True)
  author = fields.Nested(UserSchema(only=("id", "username", "name")), dump_only=True)


class CreateCommentSchema(ma.Schema):
  content = fields.String(required=True, validate=Length(min=1, max=250))
  user_id = fields.Integer(load_only=True)
  post_id = fields.Integer(load_only=True)

class CommentSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Comment
    load_instance = True
    include_fk = True
  
  updated_at = fields.DateTime(dump_only=True)


class ReturnCommentSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Comment
    load_instance = True
    include_fk = True
    exclude=("user_id",)
  
  user = fields.Nested(UserSchema(only=("id", "username", "name")), dump_only=True)
  likes_count = fields.Method("get_likes_count", dump_only=True)
  
  def get_likes_count(self, obj):
    return len(obj.likes)


class LikeSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Like
    load_instance = True
    include_fk = True


create_blog_schema = CreateBlogSchema()
blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
return_blog_schema = ReturnBlogSchema()
return_blogs_schema = ReturnBlogSchema(many=True)

create_comment_schema = CreateCommentSchema()
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
return_comment_schema = ReturnCommentSchema()
return_comments_schema = ReturnCommentSchema(many=True)

like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)