from flask import Flask
from flask_migrate import Migrate
from .config import Config, TestingConfig
from app.application import application_bp
from app.extensions import db


migrate = Migrate()


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main

    app.register_blueprint(main)
    app.register_blueprint(application_bp, url_prefix="/application")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app


app = create_app()
