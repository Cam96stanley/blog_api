import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  CACHE_TYPE = "SimpleCache"
  DEBUG = True