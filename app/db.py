import enum
import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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
    applications = relationship("Application", back_populates="user")


class ApplicationStatus(str, enum.Enum):
    PROSPECT = "prospect"
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ApplicationStageStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    REJECTED = "rejected"
    PENDING = "pending"


class ApplicationStage(BaseTable):
    __tablename__ = "application_stages"
    application_uuid = Column(UUID(as_uuid=True), ForeignKey(
        'applications.uuid'), nullable=False)
    name = Column(String)
    status = Column(Enum(ApplicationStageStatus),
                    default=ApplicationStageStatus.PENDING)
    date_scheduled = Column(DateTime, nullable=True)
    date_occurred = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)


class Application(BaseTable):
    __tablename__ = "applications"
    company = Column(String, unique=True)
    position = Column(String)
    description = Column(String, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PROSPECT)
    date_applied = Column(DateTime, nullable=True)
    date_first_response = Column(DateTime, nullable=True)
    date_rejected = Column(DateTime, nullable=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    stages = relationship("ApplicationStage", backref="application",
                          cascade="all, delete-orphan")

    user = relationship("User", back_populates="applications")


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
