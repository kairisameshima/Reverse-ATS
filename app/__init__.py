from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config, TestingConfig


db = SQLAlchemy()
migrate = Migrate(db)


# Import and register the blueprint
from app.routes import main
from db.tables import *


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(main)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    migrate.init_app(app, db)
    return app


app = create_app()
