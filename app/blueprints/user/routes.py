from flask import request, jsonify, current_app, g
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from app.blueprints.user.schemas import user_schema, create_user_schema
from app.blueprints.user import user_bp
from utils.auth import hash_password, check_password, generate_token, token_required


@user_bp.route("/login", methods=["POST"])
def login():
  try:
    data = request.get_json()
    
    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    if not email or not password:
      return jsonify({"error": "Email and password are required"}), 400
    
    user = db.session.query(User).filter_by(email=email).first()
    
    if not user or not check_password(password, user.password):
      return jsonify({"error": "Invalid email or password"}), 401
    
    token = generate_token(user.id)
    
    return jsonify({
      "status": "success",
      "message": "Login successfull",
      "token": token,
      "user": {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
      }
    }), 200
    
  except Exception as e:
    return jsonify({
      "error": "Internal server error",
      "details": str(e)
    }), 500


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


@user_bp.route("/me", methods=["PATCH"])
@token_required
def update_user():
    user = db.session.get(User, g.user_id)
    if not user:
      return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    
    if "password" in data:
      return jsonify({
        "message": "Do not use this route to update password. Use /users/changePassword"
      }), 400

    try:
      for field in ("id", "created_at", "password"):
        data.pop(field, None)
        
      updated_user = user_schema.load(data, instance=user, partial=True)
      
      db.session.commit()
      
      return jsonify(user_schema.dump(updated_user)), 200
    
    except ValidationError as err:
      return jsonify({"errors": err.messages}), 400
    
    except Exception as e:
      db.session.rollback()
      return jsonify({
        "error": "Internal server error",
        "details": str(e)
      }),500