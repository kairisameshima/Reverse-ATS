import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    DEBUG = os.getenv("DEBUG")
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
