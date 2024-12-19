from typing import Optional

from app.lib.data_access.domain_model import DomainModel


class User(DomainModel):
    """User domain model."""
    google_user_id: str
    name: str
    email: str
    image_url: Optional[str] = None

    class Meta:
        primary_key = 'email'


class MutableUserFields:
    """Fields that can be updated on a user."""
    name: str
    email: str
    image_url: str
