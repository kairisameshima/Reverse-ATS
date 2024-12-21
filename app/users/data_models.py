from typing import Optional

from pydantic import BaseModel


class UserFromEndPoint(BaseModel):
    """Used to store user data from Google."""
    google_user_id: str
    name: str
    email: str
    image_url: Optional[str] = None
