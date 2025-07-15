from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from app.models import db
from app.extenstions import ma
from app.blueprints.user import user_bp
from app.blueprints.blog import blog_bp

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swagger_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL, 
  API_URL,
  config = {
    "app_name": "Blog API"
  }
)

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f"config.{config_name}")
  
  db.init_app(app)
  ma.init_app(app)
  
  app.register_blueprint(user_bp, url_prefix="/users")
  app.register_blueprint(blog_bp, url_prefix="/blogs")
  app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
  
  return app