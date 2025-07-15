from flask import jsonify, request, g
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.blueprints.blog import blog_bp
from utils.auth import token_required
from app.models import db, User, Blog
from app.blueprints.blog.schemas import create_blog_schema, blog_schema, blogs_schema, return_blog_schema, return_blogs_schema


@blog_bp.route("/", methods=["POST"])
@token_required
def create_blog():
  user = db.session.get(User, g.user_id)
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


@blog_bp.route("/", methods=["GET"])
def get_all_blogs():
  try:
    blogs = db.scalars(select(Blog)).all()
    if not blogs:
      return jsonify({"message": "No blogs found"}), 404
    return jsonify(return_blogs_schema.dump(blogs)), 200
  except Exception as e:
    return jsonify({
      "error": "Internal server error",
      "details": str(e)
    }), 500


@blog_bp.route("/<int:blog_id>", methods=["GET"])
def get_blog(blog_id):
  try:
    blog = db.session.get(Blog, blog_id)
    if not blog:
      return jsonify({"message": "No blog found"}), 404
    
    return jsonify(return_blog_schema.dump(blog)), 200
  except Exception as e:
    return jsonify({
      "error": "Internal server error",
      "details": str(e)
    }), 500


@blog_bp.route("/<int:blog_id>", methods=["PATCH"])
@token_required
def update_blog(blog_id):
  user_id = g.user_id
  
  blog = db.session.get(Blog, blog_id)
  if not blog:
    return jsonify({"message": "blog not found"}), 404
  
  if blog.author_id != user_id:
    return jsonify({"error": "Forbidden: You cannot edit this blog"}), 403
  
  try:
    data = request.get_json()
    
    for field in ("id", "author_id", "created_at"):
      data.pop(field, None)
    
    blog = blog_schema.load(data, instance=blog, partial=True)
    
    db.session.commit()
    
    return jsonify(return_blog_schema.dump(blog)), 200
  
  except ValidationError as err:
    return jsonify({"errors": err.messages}), 400
  
  except IntegrityError as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 400
  
  except Exception as e:
    return jsonify({"error": "Internal server error", "details": str(e)}), 500