import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  SECRET_KEY = os.environ.get("SECRET_KEY") or "super secret key"
  CACHE_TYPE = "SimpleCache"
  DEBUG = True


class TestingConfig:
  SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
  DEBUG = True
  CACHE_TYPE = "SimpleCache"
  SECRET_KEY = "lsknvaownvowbwngawahbwrs"