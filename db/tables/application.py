from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import BaseTable


class Application(BaseTable):
    __tablename__ = "applications"

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    note = Column(String(500))
