from flask import request, jsonify, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from app.blueprints.user.schemas import user_schema, create_user_schema
from app.blueprints.user import user_bp
from utils.auth import hash_password

@user_bp.route("/", methods=["POST"])
def create_user():
  try:
    user_data = create_user_schema.load(request.json)
    user_data["password"] = hash_password(user_data["password"])
    
    user = User(**user_data)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 201
  
  except ValidationError as err:
    return jsonify({"errors": err.messages}), 400
  
  except IntegrityError as e:
    db.session.rollback()
    
    if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
      return jsonify({"error": "Email already registered"}), 409
    return jsonify({"error": "Database integrity error"}), 400
    
  except Exception as e:
    current_app.logger.error(f"Error creating user: {e}")
    return jsonify({"error": "Internal server error"}), 500