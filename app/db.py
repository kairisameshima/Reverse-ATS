from datetime import datetime
import os

from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Load database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost/local_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True
    uuid = Column(UUID(as_uuid=True), primary_key=True,
                  default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class User(BaseTable):
    __tablename__ = "users"
    google_user_id = Column(String, unique=True)
    name = Column(String)
    email = Column(String, primary_key=True, unique=True)
    image_url = Column(String, nullable=True)


# Create the database tables


def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper functions to interact with the database


# def get_user_by_id(db_session, user_id):
#     return db_session.query(User).filter(User.id == user_id).first()


# def get_users(db_session):
#     return db_session.query(User).all()


# def add_user(db_session, user_data):
#     user = User(**user_data)
#     db_session.add(user)
#     db_session.commit()


# def update_user(db_session, user_id, updated_data):
#     user = get_user_by_id(db_session, user_id)
#     if user:
#         for key, value in updated_data.items():
#             setattr(user, key, value)
#         db_session.commit()
