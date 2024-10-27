from sqlalchemy.orm import declarative_base
import sqlalchemy as sa
from datetime import datetime
from app.extensions import db


class Base(db.Model):
    __abstract__ = True

    create_date = sa.Column(sa.DateTime, default=datetime.now)
    update_date = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
