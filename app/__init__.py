from flask import Flask
from app.models import db
from app.extenstions import ma
from app.blueprints.user import user_bp
from app.blueprints.blog import blog_bp

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f"config.{config_name}")
  
  db.init_app(app)
  ma.init_app(app)
  
  app.register_blueprint(user_bp, url_prefix="/users")
  app.register_blueprint(blog_bp, url_prefix="/blogs")
  
  return app