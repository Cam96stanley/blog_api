import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  SECRET_KEY = os.environ.get("SECRET_KEY") or "super secret key"
  CACHE_TYPE = "SimpleCache"
  DEBUG = True