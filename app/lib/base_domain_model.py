from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainModel(BaseModel):
    """A base class for domain models.

    Domain models are used to represent the data of the application.
    Non mutable, should be updated via update() method in a repository.
    """

    uuid: UUID = Field(default_factory=uuid4)
    create_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_mutation = False
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }
