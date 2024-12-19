from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_serializer, ConfigDict


class DomainModel(BaseModel):
    """Base class for domain models.

    Represents a business entity, not necessarily mapped to a database table.
    Not an ORM model. Service layer interacts with domain models only.

    The uuid field is a unique identifier, not necessarily the primary key.
    Automatically generated if not provided.

    Domain models are immutable. Use repository's update() method to persist changes.
    """

    uuid: UUID = Field(default_factory=uuid4)
    create_date: datetime = Field(default_factory=datetime.now)
    update_date: datetime = Field(default_factory=datetime.now)

    @field_serializer('uuid')
    def serialize_uuid(self, value: UUID) -> str:
        return str(value)

    @field_serializer('create_date')
    def serialize_create_date(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer('update_date')
    def serialize_update_date(self, value: datetime) -> str:
        return value.isoformat()

    model_config = ConfigDict(frozen=True)
