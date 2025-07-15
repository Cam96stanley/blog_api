from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.blueprints.blog import blog_bp
from utils.auth import token_required
from app.models import db, User, Blog
from app.blueprints.blog.schemas import create_blog_schema, blog_schema


@blog_bp.route("/", methods=["POST"])
@token_required
def create_blog(user_id):
  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"message": "No user found"}), 404
  
  try:
    json_data = request.get_json()
    blog_data = create_blog_schema.load(json_data)
    
    blog = Blog(**blog_data)
    blog.author_id = user.id
    
    db.session.add(blog)
    db.session.commit()
    
    return jsonify(blog_schema.dump(blog)), 201
  except ValidationError as err:
    return jsonify({"errors": err.messages}), 400
  
  except IntegrityError as e:
    db.session.rollback()
    
    return jsonify({"error": str(e)}), 400
  except Exception as e:
    return jsonify({
      "error": "Internal server error",
      "details": str(e)
    }), 500