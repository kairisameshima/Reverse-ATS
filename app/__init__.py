from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Set up the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@db:5432/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import and register the blueprint
from app.routes import main

app.register_blueprint(main)
